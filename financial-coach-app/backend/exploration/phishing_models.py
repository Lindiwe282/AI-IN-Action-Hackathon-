import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import joblib

# NLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Factor Graph
from pgmpy.models import MarkovNetwork
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import BeliefPropagation
from sklearn.preprocessing import LabelEncoder

import pickle



class HybridPhishingModel:
    def __init__(self, suspicious_keywords=None, top_tfidf_features=5):
    
        self.ml_models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "gradient_boost": GradientBoostingClassifier(random_state=42),
            "logistic_regression": LogisticRegression(max_iter=500)
        }
        self.best_ml_model = None
        self.scaler = StandardScaler()
        self.selected_url_features = [
            'length_url', 'length_hostname', 'nb_dots', 'nb_hyphens', 'nb_at',
            'nb_qm', 'nb_slash', 'shortening_service', 'domain_in_brand',
            'brand_in_subdomain', 'brand_in_path', 'tld_in_path',
            'tld_in_subdomain', 'suspecious_tld', 'abnormal_subdomain',
            'prefix_suffix', 'random_domain', 'ratio_digits_url', 'ratio_digits_host',
            'nb_subdomains'
        ]
        # NLP
        self.use_nlp = True
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.nlp_model = MultinomialNB()
        self.top_tfidf_features = top_tfidf_features
        # Factor graph
        self.factor_graph = None
        # Keywords
        if suspicious_keywords is None:
            self.suspicious_keywords = ['urgent', 'verify', 'password', 'suspended', 'click', 'bank', 'account']
        else:
            self.suspicious_keywords = suspicious_keywords
    # --------------------------
    # Prepare URL features
    # --------------------------
    def prepare_url_features(self, df):
        for f in self.selected_url_features:
            if f not in df.columns:
                df[f] = 0
        return df[self.selected_url_features]

    # --------------------------
    # Train ML
    # --------------------------
    def train_ml(self, df_url, target='status'):
        X_url = self.prepare_url_features(df_url)
        y_url = df_url[target]

        X_scaled = self.scaler.fit_transform(X_url)
        best_auc = 0
        for name, model in self.ml_models.items():
            auc = cross_val_score(model, X_scaled, y_url, cv=3, scoring='roc_auc').mean()
            print(f"{name}: CV AUC={auc:.4f}")
            if auc > best_auc:
                best_auc = auc
                self.best_ml_model = name
        self.ml_models[self.best_ml_model].fit(X_scaled, y_url)
        print(f"Selected ML model: {self.best_ml_model}")

    # --------------------------
    # Train NLP
    # --------------------------
    def train_nlp(self, df_text, text_col='TEXT', target='LABEL'):
        texts = df_text[text_col].astype(str)
        y_text = df_text[target]
        self.vectorizer.fit(texts)
        X_text = self.vectorizer.transform(texts)
        self.nlp_model.fit(X_text, y_text)

    # --------------------------
    # Build factor graph
    # --------------------------
    def build_factor_graph(self):
        self.factor_graph = MarkovNetwork()
        nodes = ['Hybrid']
        # ML feature nodes
        for f in self.selected_url_features:
            nodes.append(f"ML_{f}")
        # NLP node
        nodes.append('NLP_prob')
        # ML probability node
        nodes.append('ML_prob')
        # Top TF-IDF term nodes
        nodes += [f"TFIDF_{i}" for i in range(self.top_tfidf_features)]
        # Keyword nodes
        nodes += [f"KW_{kw}" for kw in self.suspicious_keywords]
        self.factor_graph.add_nodes_from(nodes)
        # Connect all factor nodes to Hybrid
        edges = [(f, 'Hybrid') for f in nodes if f != 'Hybrid']
        self.factor_graph.add_edges_from(edges)

    # --------------------------
    # Binning numerical URL features
    # --------------------------
    def bin_url_feature(self, feature):
        if feature == 0:
            return 0
        elif feature <= 2:
            return 1
        else:
            return 2

    # --------------------------
    # Fit hybrid model
    # --------------------------
    def fit(self, df_url=None, df_text=None):
        if df_url is not None:
            self.train_ml(df_url)
        if self.use_nlp and df_text is not None:
            self.train_nlp(df_text)
        elif self.use_nlp:
            print("No text dataset provided; NLP used only at prediction time.")
        self.build_factor_graph()
    
    def map_key_words_to_meaning_safe(keywords, show_masked=False):
        """
        Map suspicious keywords to safe, non-actionable labels.
        - keywords: list of detected keyword strings (lowercased)
        - show_masked: if True, returns a lightly masked version of the keyword (e.g. p*****d)
        
        Returns list of dicts: [{'keyword': <masked_or_none>, 'category': <label>, 'advice': <generic>}]
        """
        # High-level, non-actionable categories only
        mapping = {
            'urgent': 'Urgency cue',
            'verify': 'Authentication request cue',
            'password': 'Credential-related cue',
            'suspended': 'Account status scare cue',
            'click': 'Click/redirect cue',
            'bank': 'Financial entity mention',
            'account': 'Account-related mention'
        }

        def mask_word(w):
            if len(w) <= 2:
                return w[0] + '*'*(len(w)-1)
            return w[0] + '*'*(len(w)-2) + w[-1]

        results = []
        for kw in keywords:
            cat = mapping.get(kw.lower(), 'Suspicious language')
            entry = {
                # only include the exact keyword if show_masked is True (masked), else None
                'keyword': mask_word(kw) if show_masked else None,
                'category': cat,
                # Generic advice only. No actionable or exploit details.
                'advice': 'Exercise caution; verify sender with independent channels.'  
            }
            results.append(entry)
        return results

    # --------------------------
    # Predict per user input
    # --------------------------
    def predict_from_user_input(self, url_features_df, text_input, ml_weight=0.7, nlp_weight=0.3):
        # --- Step 1: ML probability ---
        X_scaled = self.scaler.transform(url_features_df[self.selected_url_features])
        ml_prob = self.ml_models[self.best_ml_model].predict_proba(X_scaled)[0, 1]

        # ML feature-level factors (binned)
        ml_factor_nodes = {}
        for f in self.selected_url_features:
            val = url_features_df[f].values[0]
            ml_factor_nodes[f"ML_{f}"] = min(int(val), 2)

        # --- Step 2: NLP probability ---
        if self.use_nlp:
            X_text = self.vectorizer.transform([text_input])
            text_prob = self.nlp_model.predict_proba(X_text)[0, 1]
            nlp_factor_node = 1 if text_prob >= 0.5 else 0
        else:
            text_prob = 0.0
            nlp_factor_node = 0

        # --- Step 3: Keyword factors ---
        keyword_factors = {}
        text_lower = text_input.lower()
        for kw in self.suspicious_keywords:
            keyword_factors[f"KW_{kw}"] = 1 if kw in text_lower else 0

        # --- Step 4: TF-IDF top terms factors ---
        tfidf_vector = self.vectorizer.transform([text_input]).toarray()[0]
        top_indices = np.argsort(tfidf_vector)[-self.top_tfidf_features:]
        tfidf_factors = {f"TFIDF_{i}": int(tfidf_vector[idx] > 0) for i, idx in enumerate(top_indices)}

        # --- Step 5: Create fresh factor graph ---
        fg = MarkovNetwork()
        fg.add_node('Hybrid')
        fg.add_node('ML_prob')
        fg.add_node('NLP_prob')
        for f in ml_factor_nodes.keys():
            fg.add_node(f)
        for kw in keyword_factors.keys():
            fg.add_node(kw)
        for tf in tfidf_factors.keys():
            fg.add_node(tf)

        # --- Step 6: Add factors ---
        factors = []

        # ML feature factors
        for f_node, val in ml_factor_nodes.items():
            p_legit = max(0.05, 0.9 - 0.3*val)  # higher val => more suspicious
            p_phish = 1 - p_legit
            values = [p_legit, p_phish, 1-p_legit, 1-p_phish]
            values = np.array(values) * ml_weight  # weighted by ML weight
            values = values / values.sum()
            factors.append(DiscreteFactor([f_node, 'Hybrid'], [2, 2], values=values))

        # ML probability factor (weighted)
        values_ml = [1-ml_prob, ml_prob, 1-ml_prob, ml_prob]
        values_ml = np.array(values_ml) * ml_weight
        values_ml = values_ml / values_ml.sum()
        factors.append(DiscreteFactor(['ML_prob', 'Hybrid'], [2, 2], values=values_ml))

        # NLP probability factor (weighted)
        values_nlp = [0.9 if nlp_factor_node==0 else 0.2,
                    0.1 if nlp_factor_node==0 else 0.8,
                    0.2 if nlp_factor_node==0 else 0.1,
                    0.8 if nlp_factor_node==0 else 0.9]
        values_nlp = np.array(values_nlp) * nlp_weight
        values_nlp = values_nlp / values_nlp.sum()
        factors.append(DiscreteFactor(['NLP_prob', 'Hybrid'], [2, 2], values=values_nlp))

        # Keyword factors
        for kw_node, val in keyword_factors.items():
            factors.append(DiscreteFactor([kw_node, 'Hybrid'], [2, 2],
                                        values=[0.9 if val==0 else 0.2,
                                                0.1 if val==0 else 0.8,
                                                0.2 if val==0 else 0.1,
                                                0.8 if val==0 else 0.9]))

        # TF-IDF factors
        for tf_node, val in tfidf_factors.items():
            factors.append(DiscreteFactor([tf_node, 'Hybrid'], [2, 2],
                                        values=[0.9 if val==0 else 0.2,
                                                0.1 if val==0 else 0.8,
                                                0.2 if val==0 else 0.1,
                                                0.8 if val==0 else 0.9]))

        # Add all factors
        fg.add_factors(*factors)

        # --- Step 7: Belief Propagation ---
        bp = BeliefPropagation(fg)
        hybrid_marginals = bp.query(variables=['Hybrid'], show_progress=False)
        hybrid_prob = hybrid_marginals.values[1]  # phishing probability

        # --- Step 8: Prediction ---
        prediction = 'phishing' if hybrid_prob >= 0.5 else 'legitimate'

        raw_keywords = [kw for kw in self.suspicious_keywords if kw in text_lower]
        # Map to safe descriptions
        mapped_keywords = self.map_keywords_safe(raw_keywords, show_masked=True)

        return {
            'prediction': prediction,
            'hybrid_prob': hybrid_prob,
            'keywords_detected': mapped_keywords
        }
            
    # --------------------------
    # Save & load
    # --------------------------
    def save_components(self, filepath):
            components = {
                "ml_models": self.ml_models,
                "best_ml_model": self.best_ml_model,
                "scaler": self.scaler,
                "vectorizer": self.vectorizer,
                "nlp_model": self.nlp_model,
                "selected_url_features": self.selected_url_features
            }
            with open(filepath, "wb") as f:
                pickle.dump(components, f)
            print(f"Components saved to {filepath}")

    # --------------------------
    # Load components into a new class instance
    # --------------------------
    def load_components(self, filepath):
        with open(filepath, "rb") as f:
            components = pickle.load(f)
        self.ml_models = components["ml_models"]
        self.best_ml_model = components["best_ml_model"]
        self.scaler = components["scaler"]
        self.vectorizer = components["vectorizer"]
        self.nlp_model = components["nlp_model"]
        self.selected_url_features = components["selected_url_features"]
        print(f"Components loaded from {filepath}")


        

# def main():
#     data = pd.read_csv("data/dataset_phishing.csv")

#     text_data=pd.read_csv("data/Dataset_5971.csv")


#    #preprocessing the data
#     data['domain_age'] = data['domain_age'].apply(lambda x: data['domain_age'].median() if x < 0 else x)
#     data['domain_registration_length'] = data['domain_registration_length'].apply(lambda x: data['domain_registration_length'].median() if x < 0 else x)

#     label_encoder = LabelEncoder()
#     data['status'] = label_encoder.fit_transform(data['status'])

#     data['status'].value_counts()

#     model = HybridPhishingModel()
#     model.fit(df_url=data, df_text=text_data)

#     model.save_components("hybrid_phishing_components.pkl")

#     model = HybridPhishingModel()

#     # Load components (safe in Jupyter)
#     model.load_components("hybrid_phishing_components.pkl")

#     # Example URL and text input
#     user_url = "http://bit.ly/suspicious-link.html"
#     user_text = "Your account has been suspended! Click here to verify your password urgently."

#     # Function to extract URL features
#     def extract_url_features(url, model):
#         features = {}
#         features['length_url'] = len(url)
#         features['length_hostname'] = len(url.split('//')[-1].split('/')[0])
#         features['nb_dots'] = url.count('.')
#         features['nb_hyphens'] = url.count('-')
#         features['nb_at'] = url.count('@')
#         features['nb_qm'] = url.count('?')
#         features['nb_slash'] = url.count('/')
#         features['shortening_service'] = 1 if any(s in url for s in ['bit.ly','tinyurl','goo.gl']) else 0
#         features['domain_in_brand'] = 0
#         features['brand_in_subdomain'] = 0
#         features['brand_in_path'] = 0
#         features['tld_in_path'] = 0
#         features['tld_in_subdomain'] = 0
#         features['suspecious_tld'] = 0
#         features['abnormal_subdomain'] = 0
#         features['prefix_suffix'] = 0
#         features['random_domain'] = 1 if any(c.isdigit() for c in url.split('//')[-1].split('.')[0]) else 0
#         features['ratio_digits_url'] = sum(c.isdigit() for c in url) / max(len(url),1)
#         features['ratio_digits_host'] = sum(c.isdigit() for c in url.split('//')[-1].split('/')[0]) / max(len(url.split('//')[-1].split('/')[0]),1)
#         features['nb_subdomains'] = len(url.split('//')[-1].split('.')[0].split('-'))

#         # Fill missing features
#         for f in model.selected_url_features:
#             if f not in features:
#                 features[f] = 0
#         return pd.DataFrame([features])

#     # Prepare features
#     url_features_df = extract_url_features(user_url, model)


#     # --- ML probability ---
#     X_scaled = model.scaler.transform(url_features_df[model.selected_url_features])
#     ml_prob = model.ml_models[model.best_ml_model].predict_proba(X_scaled)[0,1]

#     # --- NLP probability ---
#     X_text = model.vectorizer.transform([user_text])
#     text_prob = model.nlp_model.predict_proba(X_text)[0,1]

#     # --- Weighted hybrid probability ---
#     ml_weight = 0.8  # give more importance to ML (URL features)
#     nlp_weight = 0.2  # less weight to NLP (text)
#     hybrid_prob = ml_prob*ml_weight + text_prob*nlp_weight

#     # --- Prediction ---
#     prediction = 'phishing' if hybrid_prob >= 0.5 else 'legitimate'

#     # --- Show results ---
#     detected_keywords = [kw for kw in model.suspicious_keywords if kw in user_text.lower()]
#     masked_keywords = HybridPhishingModel.map_keywords_safe(detected_keywords, show_masked=True)

#     # --- Show results ---
#     print("\nPrediction result:")
#     print(f"Prediction: {prediction}")
#     print(f"ML probability: {ml_prob:.4f}")
#     print(f"Text probability: {text_prob:.4f}")
#     print(f"Weighted Hybrid probability: {hybrid_prob:.4f}")
#     print(f"Detected suspicious keywords (masked): {[kw['keyword'] for kw in masked_keywords]}")


# if __name__ == "__main__":
#     main()