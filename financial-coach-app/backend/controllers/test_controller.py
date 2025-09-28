import os
from fraud_controller import FraudController  # Ensure this matches the filename of your main class

def main():
    # === Initialize the fraud detection controller ===
    controller = FraudController()
    print("[INFO] FraudController initialized successfully.\n")

    # === Provide a test PDF file ===
    # Replace this path with an actual PDF file path on your system
    test_pdf_path = "data/fraudulent_document.pdf"

    if not os.path.exists(test_pdf_path):
        print(f"[ERROR] Test PDF not found at: {test_pdf_path}")
        print("Please place a PDF at the above path before running the test.")
        return

    # === Example numeric values ===
    # You can modify these to simulate different scenarios
    amount = 11000           # R50,000 investment amount
    interest_rate = 0       # 12% annual interest rate
    promised_return = 100     # 20% promised return

    print(f"[INFO] Running fraud analysis on: {test_pdf_path}")
    print(f"[INFO] Input Amount: {amount}, Interest Rate: {interest_rate}%, Promised Return: {promised_return}%\n")

    # === Run analysis ===
    try:
        result = controller.analyze_pdf(
            pdf_path=test_pdf_path,
            amount=amount,
            interest_rate=interest_rate,
            promised_return=promised_return
        )
    except Exception as e:
        print("[ERROR] Failed to analyze PDF:", e)
        return

    # === Print results ===
    print("========== FRAUD ANALYSIS RESULT ==========")
    print(f"Fraud Probability : {result['fraud_probability'] * 100:.1f}%")
    print(f"Fraud Detected    : {'YES' if result['is_fraud'] else 'NO'}")
    print("\n---- RED FLAGS ----")
    if result.get("red_flags"):
        for i, flag in enumerate(result["red_flags"], 1):
            print(f"{i}. {flag}")
    else:
        print("No significant anomalies detected.")

    # Optional: Display extracted key features for debugging
    print("\n---- EXTRACTED FEATURES (sample) ----")
    feature_keys = ["amount", "interest_rate_scaled", "promised_return_scaled",
                    "doc_score", "suspicious_words_count", "unrealistic_amount", "unrealistic_rate"]
    for key in feature_keys:
        print(f"{key}: {result.get(key, 'N/A')}")

if __name__ == "__main__":
    main()
