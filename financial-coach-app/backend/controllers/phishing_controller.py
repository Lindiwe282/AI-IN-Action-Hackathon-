# controller.py
import pandas as pd
import pickle
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from exploration.phishing_models import HybridPhishingModel


class PhishingController:
    def __init__(self, model_path="exploration/hybrid_phishing_components.pkl"):
        """
        Initialize controller and load trained model components.
        """
        self.model = None
        self.load_model(model_path)

    def load_model(self, model_path):
        try:
            print(f"🔄 Loading phishing model from: {model_path}")
            self.model = HybridPhishingModel()
            self.model.load_components(model_path)   # this method rehydrates the class
            print(f"✅ Phishing model components loaded successfully from {model_path}")
        except FileNotFoundError:
            print(f"❌ Model file not found: {model_path}")
            raise
        except Exception as e:
            print(f"❌ Error loading phishing model: {e}")
            raise


    def extract_url_features(self, url):
        """
        Extract URL features required by the model.
        """
        features = {}
        features['length_url'] = len(url)
        features['length_hostname'] = len(url.split('//')[-1].split('/')[0])
        features['nb_dots'] = url.count('.')
        features['nb_hyphens'] = url.count('-')
        features['nb_at'] = url.count('@')
        features['nb_qm'] = url.count('?')
        features['nb_slash'] = url.count('/')
        features['shortening_service'] = 1 if any(s in url for s in ['bit.ly','tinyurl','goo.gl']) else 0
        features['domain_in_brand'] = 0
        features['brand_in_subdomain'] = 0
        features['brand_in_path'] = 0
        features['tld_in_path'] = 0
        features['tld_in_subdomain'] = 0
        features['suspecious_tld'] = 0
        features['abnormal_subdomain'] = 0
        features['prefix_suffix'] = 0
        features['random_domain'] = 1 if any(c.isdigit() for c in url.split('//')[-1].split('.')[0]) else 0
        features['ratio_digits_url'] = sum(c.isdigit() for c in url) / max(len(url),1)
        features['ratio_digits_host'] = sum(c.isdigit() for c in url.split('//')[-1].split('/')[0]) / max(len(url.split('//')[-1].split('/')[0]),1)
        features['nb_subdomains'] = len(url.split('//')[-1].split('.')[0].split('-'))

        # Fill missing features with 0
        for f in self.model.selected_url_features:
            if f not in features:
                features[f] = 0

        return pd.DataFrame([features])

    def predict(self, url, text, ml_weight=0.8, nlp_weight=0.2):
        """
        Predict whether the input is phishing or legitimate.
        Weighted hybrid probability between ML (URL) and NLP (text) models.
        """
        # Extract URL features
        url_features_df = self.extract_url_features(url)

        # ML probability
        X_scaled = self.model.scaler.transform(url_features_df[self.model.selected_url_features])
        ml_prob = self.model.ml_models[self.model.best_ml_model].predict_proba(X_scaled)[0,1]

        # NLP probability
        X_text = self.model.vectorizer.transform([text])
        text_prob = self.model.nlp_model.predict_proba(X_text)[0,1]

        # Weighted hybrid probability
        hybrid_prob = ml_prob*ml_weight + text_prob*nlp_weight

        # Prediction
        prediction = 'phishing' if hybrid_prob >= 0.5 else 'legitimate'

        # Detected keywords - return full information (keyword, category, advice)
        text_lower = text.lower()
        keywords_detected = [kw for kw in self.model.suspicious_keywords if kw in text_lower]
        masked_keywords = HybridPhishingModel.map_key_words_to_meaning_safe(keywords_detected, show_masked=True)
        
        return {
            'prediction': prediction,
            'ml_prob': ml_prob,
            'text_prob': text_prob,
            'hybrid_prob': hybrid_prob,
            'keywords_detected': masked_keywords  # Return full objects with keyword, category, advice
        }

