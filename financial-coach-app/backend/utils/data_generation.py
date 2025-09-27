import pandas as pd
import numpy as np
import os

def generate_synthetic_large_dataset(num_samples=50000,
                                     save_path="data/synthetic_fraud_dataset_large.csv"):
    np.random.seed(42)
    data = []

    for _ in range(num_samples):

        # Amount (money)
        if np.random.rand() < 0.05:
            # Extreme but plausible large transfers
            amount = round(np.random.uniform(50_000, 5_000_000), 2)
        else:
            # Everyday transactions
            amount = round(np.random.uniform(10, 50_000), 2)

        # Interest & promised return (as ratios)
        interest_rate   = round(np.random.uniform(0, 0.40), 2)
        promised_return = round(np.random.uniform(0, 0.35), 2)

        # Document score (0–1)
        doc_score = round(np.clip(np.random.normal(0.7, 0.2), 0, 1), 2)

        # Behavior score
        if np.random.rand() < 0.05:
            behavior_score = round(np.random.uniform(0.3, 1.0), 2)
        else:
            behavior_score = round(np.random.uniform(0.0, 0.3), 2)

        # Text-based features (simulate)
        suspicious_words_count = round(behavior_score * 10, 2)
        urgency_terms_count    = round(float(np.random.poisson(0.2)), 2)
        all_caps_count         = round(float(np.random.poisson(0.5)), 2)
        exclamation_count      = round(float(np.random.poisson(0.2)), 2)
        link_count             = round(float(np.random.poisson(0.05)), 2)
        email_count            = round(float(np.random.poisson(0.05)), 2)
        contact_missing        = int(email_count == 0)
        doc_length             = round(float(np.random.randint(100, 2000)), 2)
        word_count             = round(float(np.random.randint(50, 500)), 2)
        unique_word_ratio      = round(np.random.uniform(0.3, 0.9), 2)
        special_char_ratio     = round(np.random.uniform(0, 0.2), 2)

        unrealistic_amount = int(amount > 1_000_000 or amount < 100)
        unrealistic_rate   = int(interest_rate > 0.35 or promised_return > 0.30)

        data.append([
            amount, interest_rate, promised_return, doc_score, behavior_score,
            suspicious_words_count, urgency_terms_count,
            all_caps_count, exclamation_count, link_count, email_count, contact_missing,
            doc_length, word_count, unique_word_ratio, special_char_ratio,
            unrealistic_amount, unrealistic_rate
        ])

    columns = [
        "amount", "interest_rate_scaled", "promised_return_scaled", "doc_score", "behavior_score",
        "suspicious_words_count", "urgency_terms_count",
        "all_caps_count", "exclamation_count", "link_count", "email_count", "contact_missing",
        "doc_length", "word_count", "unique_word_ratio", "special_char_ratio",
        "unrealistic_amount", "unrealistic_rate"
    ]

    df = pd.DataFrame(data, columns=columns)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False, float_format="%.2f")  # force 2-decimal output
    print(f"✅ Large synthetic dataset saved to {save_path} with {len(df)} rows.")

if __name__ == "__main__":
    generate_synthetic_large_dataset(num_samples=50000)
