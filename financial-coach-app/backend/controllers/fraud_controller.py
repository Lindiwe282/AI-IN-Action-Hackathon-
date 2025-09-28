import pandas as pd
import numpy as np
import joblib
import re
try:
    from pgmpy.models import BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
    PGMPY_AVAILABLE = True
except ImportError:
    try:
        from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
        from pgmpy.factors.discrete import TabularCPD
        from pgmpy.inference import VariableElimination
        PGMPY_AVAILABLE = True
    except ImportError:
        PGMPY_AVAILABLE = False
        print("Warning: pgmpy not available, Bayesian network features will be disabled")

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("Warning: PyPDF2 not available, PDF processing will be disabled")

from flask import request, jsonify
from controllers.phishing_controller import PhishingController

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
        try:
            self.models = {layer: joblib.load(f"models/{layer}_model.pkl") for layer in self.layers}
            self.scalers = {layer: joblib.load(f"models/{layer}_scaler.pkl") for layer in self.layers}
        except FileNotFoundError as e:
            print(f"Model file not found: {e}")
            # Create dummy models if files don't exist
            self.models = {}
            self.scalers = {}
        except Exception as e:
            print(f"Error loading models: {e}")
            self.models = {}
            self.scalers = {}

        # Load dataset & compute anomaly indicators
        try:
            self.data = pd.read_csv("data/synthetic_fraud_dataset_large.csv")
            if self.models and self.scalers:
                self._build_anomaly_indicators()
        except FileNotFoundError as e:
            print(f"Dataset file not found: {e}")
            self.data = None
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.data = None

        # Build Bayesian network
        if PGMPY_AVAILABLE and self.data is not None:
            self._build_bayesian_network()
        else:
            self.bn_model = None
            self.infer = None
        
        # Initialize phishing controller
        try:
            # The model file is in the backend root directory
            self.phishing_controller = PhishingController("hybrid_phishing_components.pkl")
            print("✅ PhishingController initialized successfully")
        except Exception as e:
            print(f"❌ Warning: Could not initialize PhishingController: {e}")
            print("This means phishing detection will not be available")
            self.phishing_controller = None

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
            with open("data/suspicious_keywords.txt") as f:
                suspicious_words = [w.strip().lower() for w in f]
        except FileNotFoundError:
            print("Warning: suspicious_keywords.txt not found, using empty list")
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
        if not PGMPY_AVAILABLE:
            print("Warning: Bayesian network disabled - pgmpy not available")
            return
            
        self.bn_model = BayesianNetwork([
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
    def analyze_pdf(self, pdf_file, amount=0, interest_rate=0, promised_return=0):
        if not PYPDF2_AVAILABLE:
            return {
                "fraud_probability": 0.5,
                "is_fraud": False,
                "red_flags": ["PDF processing not available - PyPDF2 not installed"]
            }
        
        # Handle both file path (string) and file object
        try:
            if isinstance(pdf_file, str):
                # It's a file path
                reader = PdfReader(pdf_file)
            else:
                # It's a file object from request
                reader = PdfReader(pdf_file)
            
            text = "".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return {
                "fraud_probability": 0.5,
                "is_fraud": False,
                "red_flags": [f"Error reading PDF: {str(e)}"]
            }

        # --- Extract numeric values from form data ---
        try:
            if amount == 0 and interest_rate == 0 and promised_return == 0:
                amount, interest_rate, promised_return = self._extract_amounts_from_text(text)
            interest_rate = float(interest_rate/100) if interest_rate > 1 else float(interest_rate)
            promised_return = float(promised_return/100) if promised_return > 1 else float(promised_return)
        except ValueError:
            amount, interest_rate, promised_return = 0.0, 0.0, 0.0

        # --- Extract features ---
        features = self.extract_features_from_pdf(text, amount, interest_rate, promised_return)

        # Check if models are available
        if not self.models or not self.scalers:
            # Simple rule-based approach when ML models are not available
            red_flags = []
            anomaly_count = 0
            
            # Simple rules for fraud detection
            if amount > 1000000 or amount < 100:
                red_flags.append(f"Unusual investment amount: {amount}")
                anomaly_count += 1
                
            if interest_rate > 0.35 or promised_return > 0.30:
                red_flags.append(f"Unrealistic returns promised: Interest={interest_rate*100}%, Return={promised_return*100}%")
                anomaly_count += 1
                
            if features['suspicious_words_count'] > 5:
                red_flags.append(f"High number of suspicious keywords detected: {features['suspicious_words_count']}")
                anomaly_count += 1
                
            if features['urgency_terms_count'] > 2:
                red_flags.append(f"Multiple urgency terms detected: {features['urgency_terms_count']}")
                anomaly_count += 1
            
            fraud_prob = min(anomaly_count * 0.25, 1.0)
            
            result = {
                "fraud_probability": round(fraud_prob, 2),
                "is_fraud": fraud_prob > 0.5,
                "red_flags": red_flags
            }
            
            return {**result, **features}

        # --- Compute anomalies for each layer ---
        evidence = {}
        red_flags = []

        for layer, feats in self.layers.items():
            try:
                X_layer = pd.DataFrame([[features[f] for f in feats]], columns=feats)
                X_scaled = self.scalers[layer].transform(X_layer)
                anomaly = int(self.models[layer].predict(X_scaled)[0] == -1)
                evidence[f"{layer}_Anomaly"] = anomaly
            except Exception as e:
                print(f"Error processing layer {layer}: {e}")
                evidence[f"{layer}_Anomaly"] = 0

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
        try:
            if 'pdf' not in request.files:
                return jsonify({"error": "No PDF uploaded"}), 400

            pdf_file = request.files['pdf']
            
            if pdf_file.filename == '':
                return jsonify({"error": "No file selected"}), 400

            # Get numeric inputs from form
            try:
                amount = float(request.form.get('amount', 0))
                interest_rate = float(request.form.get('interest_rate', 0))
                promised_return = float(request.form.get('promised_return', 0))
            except ValueError:
                return jsonify({"error": "Invalid numeric input"}), 400

            result = self.analyze_pdf(pdf_file, amount, interest_rate, promised_return)
            return jsonify(result)
        
        except Exception as e:
            print(f"Error in detect_fraud_route: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    def detect_phishing_route(self):
        """Route for detecting phishing in text or URLs"""
        try:
            # Check if phishing controller is available
            if not self.phishing_controller:
                return jsonify({
                    "error": "Phishing detection not available", 
                    "risk_score": 0.5,
                    "is_phishing": False,
                    "details": "PhishingController not initialized"
                }), 503
            
            # Get text and URL inputs from form data
            text_input = request.form.get('text', '').strip()
            url_input = request.form.get('url', '').strip()
            
            if not text_input and not url_input:
                return jsonify({
                    "error": "No text or URL provided for analysis",
                    "risk_score": 0.0,
                    "is_phishing": False
                }), 400
            
            print(f"Processing phishing detection...")
            print(f"URL input: {url_input if url_input else 'None'}")
            print(f"Text input: {text_input[:100] if text_input else 'None'}...")
            
            # Use the provided URL and text directly
            url = url_input if url_input else ""
            text = text_input if text_input else ""
            
            # If only URL is provided, use URL as text too for NLP analysis
            if url and not text:
                text = url
                print(f"Using URL as text for NLP analysis")
            
            # If text contains URLs and no separate URL provided, extract URL
            if text and not url:
                import re
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                urls_found = re.findall(url_pattern, text)
                if urls_found:
                    url = urls_found[0]
                    # Keep the original text for NLP analysis
                    print(f"Extracted URL from text: {url}")
            
            print(f"Final URL for analysis: {url if url else 'None'}")
            print(f"Final text for analysis: {text[:100] if text else 'None'}...")
            
            # Use the phishing controller to predict
            result = self.phishing_controller.predict(url, text)
            print(f"Phishing prediction result: {result}")
            
            # Format response to match frontend expectations
            response = {
                "risk_score": float(result.get('hybrid_prob', 0)),
                "is_phishing": result.get('prediction') == 'phishing',
                "ml_probability": float(result.get('ml_prob', 0)),
                "text_probability": float(result.get('text_prob', 0)),
                "keywords_detected": result.get('keywords_detected', []),
                "prediction_details": result.get('prediction', 'unknown')
            }
            
            print(f"Formatted response: {response}")
            return jsonify(response)
            
        except Exception as e:
            print(f"Error in detect_phishing_route: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "error": f"Internal server error: {str(e)}",
                "risk_score": 0.5,
                "is_phishing": False
            }), 500
