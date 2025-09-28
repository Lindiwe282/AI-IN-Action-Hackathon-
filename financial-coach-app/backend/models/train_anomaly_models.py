# models/train_layered_anomaly_models.py
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load large synthetic dataset
df = pd.read_csv("../data/synthetic_fraud_dataset_large.csv")

# Define feature groups for layers
layers = {
    "Transaction": ["amount", "interest_rate_scaled", "promised_return_scaled"],
    "Document": ["doc_score", "doc_length", "word_count", "unique_word_ratio", "special_char_ratio"],
    "Behavior": ["behavior_score", "suspicious_words_count", "urgency_terms_count", 
                 "all_caps_count", "exclamation_count", "link_count", "email_count", "contact_missing"],
    "Unrealistic": ["unrealistic_amount", "unrealistic_rate"]
}

scalers = {}
models = {}

for layer_name, features in layers.items():
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    scalers[layer_name] = scaler

    # Train IsolationForest
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_scaled)
    models[layer_name] = model

    # Save each layer model & scaler
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, f"models/{layer_name}_model.pkl")
    joblib.dump(scaler, f"models/{layer_name}_scaler.pkl")
    print(f"✅ {layer_name} anomaly model trained and saved.")
