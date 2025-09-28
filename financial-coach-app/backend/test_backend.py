#!/usr/bin/env python3
"""
Test script to verify the phishing API endpoint is working correctly
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_controllers():
    """Test if controllers can be initialized"""
    try:
        print("🧪 Testing controller initialization...")
        
        # Test fraud controller
        from controllers.fraud_controller import FraudController
        print("✅ FraudController imported successfully")
        
        controller = FraudController()
        print("✅ FraudController initialized")
        
        # Check if phishing controller is available
        if controller.phishing_controller:
            print("✅ PhishingController is available in FraudController")
        else:
            print("❌ PhishingController is NOT available in FraudController")
            
        return controller
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_phishing_prediction(controller):
    """Test phishing prediction with sample data"""
    if not controller or not controller.phishing_controller:
        print("❌ Cannot test phishing - controller not available")
        return
        
    try:
        print("\n🧪 Testing phishing prediction...")
        
        # Test cases with separate URL and text
        test_cases = [
            {
                "name": "Suspicious email with phishing URL",
                "url": "https://bit.ly/fake-bank-login",
                "text": "URGENT! Your account will be suspended. Click here to verify your account details!"
            },
            {
                "name": "Normal business email",
                "url": "",
                "text": "Hello, this is a regular business email about our meeting tomorrow at 2 PM."
            },
            {
                "name": "Suspicious URL only",
                "url": "https://paypal-verification.phishing-site.com/login",
                "text": ""
            },
            {
                "name": "Phishing text without URL",
                "url": "",
                "text": "Congratulations! You've won $10,000! Click here immediately to claim your prize before it expires!"
            },
            {
                "name": "Legitimate website",
                "url": "https://www.google.com",
                "text": "Welcome to Google Search"
            }
        ]
        
        for i, case in enumerate(test_cases):
            print(f"\n📝 Test case {i+1}: {case['name']}")
            print(f"   URL: {case['url'] if case['url'] else 'None'}")
            print(f"   Text: {case['text'][:50]}{'...' if len(case['text']) > 50 else ''}")
            
            result = controller.phishing_controller.predict(case['url'], case['text'])
            print(f"   Result: {result}")
            print(f"   Prediction: {result.get('prediction', 'unknown')}")
            print(f"   Hybrid Probability: {result.get('hybrid_prob', 0):.4f}")
            if result.get('keywords_detected'):
                print(f"   Keywords: {len(result.get('keywords_detected', []))} suspicious keywords found")
            
    except Exception as e:
        print(f"❌ Error in phishing prediction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Testing Phishing Detection Backend")
    print("=" * 50)
    
    controller = test_controllers()
    test_phishing_prediction(controller)
    
    print("\n" + "=" * 50)
    print("✨ Test completed!")