import pandas as pd
import numpy as np
import joblib
import re
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from PyPDF2 import PdfReader
from flask import request, jsonify

class FraudController:
    def __init__(self):
        # === Layer definitions ===
        self.layers = {
            "Transaction": ["amount", "interest_rate_scaled", "promised_return_scaled"],
            "Document": ["doc_score", "doc_length", "word_count", "unique_word_ratio", "special_char_ratio"],
            "Behavior": [
                "behavior_score", "suspicious_words_count", "urgency_terms_count",
                "all_caps_count", "exclamation_count", "link_count", "email_count", "contact_missing"
            ],
            "Unrealistic": ["unrealistic_amount", "unrealistic_rate"]
        }

        # Load models & scalers
        self.models = {layer: joblib.load(f"models/{layer}_model.pkl") for layer in self.layers}
        self.scalers = {layer: joblib.load(f"models/{layer}_scaler.pkl") for layer in self.layers}

        # Load dataset & compute anomaly indicators
        self.data = pd.read_csv("data/synthetic_fraud_dataset_large.csv")
        self._build_anomaly_indicators()

        # Build Bayesian network
        self._build_bayesian_network()

    # --------------------------------------------------------------
    def _extract_amounts_from_text(self, text: str):
        """Extract amount, interest rate, and promised return from text."""
        text = text.replace(",", "").lower()

        # Amount
        amount_match = re.search(r"r\s*(\d+\.?\d*)|amount[:\s]+(\d+\.?\d*)", text)
        amount = float(amount_match.group(1) or amount_match.group(2)) if amount_match else 0.0

        # Interest rate (%)
        interest_match = re.search(r"(\d+\.?\d*)\s*%.*interest", text)
        interest_rate = float(interest_match.group(1)) / 100 if interest_match else 0.0

        # Promised return (%)
        return_match = re.search(r"(\d+\.?\d*)\s*%.*return", text)
        promised_return = float(return_match.group(1)) / 100 if return_match else 0.0

        return round(amount, 2), round(interest_rate, 2), round(promised_return, 2)

    # --------------------------------------------------------------
    def extract_features_from_pdf(self, text_content: str, amount: float,
                                  interest_rate: float = 0, promised_return: float = 0):
        """Extract all NLP-based and numeric features from PDF text."""
        text = text_content.lower()
        words = text.split()

        try:
            with open("data/suspecious_keywords.txt") as f:
                suspicious_words = [w.strip().lower() for w in f]
        except FileNotFoundError:
            suspicious_words = []

        susp_count = sum(word in suspicious_words for word in words)

        features = {
            "amount": round(amount, 2),
            "interest_rate_scaled": round(interest_rate, 2),
            "promised_return_scaled": round(promised_return, 2),
            "doc_score": round(min(susp_count, 1.0), 2),
            "behavior_score": 0.0,  # placeholder
            "suspicious_words_count": susp_count,
            "urgency_terms_count": sum(term in text for term in ["act now", "limited time", "expires today"]),
            "all_caps_count": sum(1 for w in words if w.isupper()),
            "exclamation_count": text.count("!"),
            "link_count": len(re.findall(r'https?://\S+', text)),
            "email_count": len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)),
            "contact_missing": int(len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)) == 0),
            "doc_length": len(text),
            "word_count": len(words),
            "unique_word_ratio": round(len(set(words)) / len(words), 2) if words else 0.0,
            "special_char_ratio": round(sum(not c.isalnum() and not c.isspace() for c in text) / max(1, len(text)), 2),
            "unrealistic_amount": int(amount > 1_000_000 or amount < 100),
            "unrealistic_rate": int(interest_rate > 0.35 or promised_return > 0.30),
        }
        return features

    # --------------------------------------------------------------
    def _build_anomaly_indicators(self):
        for layer, feats in self.layers.items():
            X_scaled = self.scalers[layer].transform(self.data[feats])
            self.data[f"{layer}_Anomaly"] = (self.models[layer].predict(X_scaled) == -1).astype(int)

    # --------------------------------------------------------------
    def _build_bayesian_network(self):
        self.bn_model = DiscreteBayesianNetwork([
            ("Transaction_Anomaly", "Fraud"),
            ("Document_Anomaly", "Fraud"),
            ("Behavior_Anomaly", "Fraud"),
            ("Unrealistic_Anomaly", "Fraud")
        ])

        for layer in self.layers:
            p0 = (self.data[f"{layer}_Anomaly"] == 0).mean()
            cpd = TabularCPD(f"{layer}_Anomaly", 2, [[p0], [1 - p0]])
            self.bn_model.add_cpds(cpd)

        fraud_values = []
        for t in [0, 1]:
            for d in [0, 1]:
                for b in [0, 1]:
                    for u in [0, 1]:
                        count = t + d + b + u
                        p_fraud = min(0.1 + 0.25 * count, 0.99)
                        fraud_values.append([1 - p_fraud, p_fraud])

        fraud_cpd = TabularCPD(
            "Fraud", 2,
            np.array(fraud_values).T,
            evidence=[f"{l}_Anomaly" for l in self.layers],
            evidence_card=[2, 2, 2, 2]
        )
        self.bn_model.add_cpds(fraud_cpd)
        assert self.bn_model.check_model()
        self.infer = VariableElimination(self.bn_model)

    # --------------------------------------------------------------
    def infer_fraud(self, evidence: dict):
        result = self.infer.query(variables=["Fraud"], evidence=evidence)
        prob = float(result.values[1])
        return {"fraud_probability": round(prob, 2), "is_fraud": prob > 0.5}

    # --------------------------------------------------------------
    def analyze_pdf(self, pdf_path, amount=0, interest_rate=0, promised_return=0):
        reader = PdfReader(pdf_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)

        # --- Extract numeric values from form data ---
        try:
            if amount == 0 and interest_rate == 0 and promised_return == 0:
                amount, interest_rate, promised_return = self._extract_amounts_from_text(text)
            interest_rate = float(interest_rate/100)
            promised_return = float(promised_return/100)
        except ValueError:
            amount, interest_rate, promised_return = 0.0, 0.0, 0.0

        # --- Extract features ---
        features = self.extract_features_from_pdf(text, amount, interest_rate, promised_return)

        # --- Compute anomalies for each layer ---
        evidence = {}
        red_flags = []

        for layer, feats in self.layers.items():
            X_layer = pd.DataFrame([[features[f] for f in feats]], columns=feats)
            X_scaled = self.scalers[layer].transform(X_layer)
            anomaly = int(self.models[layer].predict(X_scaled)[0] == -1)
            evidence[f"{layer}_Anomaly"] = anomaly

            # --- Build red flags ---
            if anomaly:
                if layer == "Transaction":
                    red_flags.append(
                        f"Transaction anomalies detected: Amount={amount}, Interest={interest_rate}%, Promised Return={promised_return*100}%"
                    )
                elif layer == "Document":
                    red_flags.append(
                        f"Document anomalies detected: {features['suspicious_words_count']} suspicious keywords, {features['all_caps_count']} all-caps words, {features['link_count']} links"
                    )
                elif layer == "Behavior":
                    red_flags.append(
                        f"Behavior anomalies detected: {features['urgency_terms_count']} urgency terms, {features['exclamation_count']} exclamation marks"
                    )
                elif layer == "Unrealistic":
                    red_flags.append(
                        f"Unrealistic values detected: Amount or Rate outside normal range"
                    )

        # --- Compute fraud probability ---
        # Weighted sum to make scores more granular
        fraud_prob = (
            0.3 * evidence["Transaction_Anomaly"] +
            0.3 * evidence["Document_Anomaly"] +
            0.3 * evidence["Behavior_Anomaly"] +
            0.1 * evidence["Unrealistic_Anomaly"]
        )
        fraud_prob = min(max(fraud_prob, 0.0), 1.0)  # ensure 0-1 range

        result = {
            "fraud_probability": round(fraud_prob, 2),
            "is_fraud": fraud_prob > 0.5,
            "red_flags": red_flags
        }

        # Return both fraud result and extracted features
        return {**result, **features}



    # --------------------------------------------------------------
    def detect_fraud_route(self):
        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF uploaded"}), 400

        pdf_file = request.files['pdf']

        # Get numeric inputs from form
        try:
            amount = float(request.form.get('amount', 0))
            interest_rate = float(request.form.get('interest_rate', 0))
            promised_return = float(request.form.get('promised_return', 0))
        except ValueError:
            return jsonify({"error": "Invalid numeric input"}), 400

        result = self.analyze_pdf(pdf_file, amount, interest_rate, promised_return)
        return jsonify(result)
