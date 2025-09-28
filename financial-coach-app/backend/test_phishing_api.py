#!/usr/bin/env python3

import requests
import sys

def test_phishing_api():
    """Test the phishing detection API endpoint"""
    url = "http://localhost:5000/api/fraud/phishing/detect"
    
    # Test data
    test_cases = [
        {
            "name": "Suspicious phishing text",
            "text": "URGENT! Your account will be suspended. Click here immediately to verify your account details!"
        },
        {
            "name": "Normal text",
            "text": "Hello, this is a normal business email about our meeting tomorrow."
        },
        {
            "name": "Suspicious URL",
            "text": "https://bit.ly/fake-bank-login"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"Input: {test_case['text'][:100]}...")
        
        # Prepare form data
        data = {'text': test_case['text']}
        
        try:
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"   Risk Score: {result.get('risk_score', 0):.2f}")
                print(f"   Is Phishing: {result.get('is_phishing', False)}")
                print(f"   ML Probability: {result.get('ml_probability', 0):.2f}")
                print(f"   Text Probability: {result.get('text_probability', 0):.2f}")
                if result.get('keywords_detected'):
                    print(f"   Keywords: {result.get('keywords_detected')}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Backend is not running on localhost:5000")
        except requests.exceptions.Timeout:
            print("❌ Timeout Error: Request took too long")
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")

if __name__ == "__main__":
    print("🔍 Testing Phishing Detection API")
    print("=" * 50)
    test_phishing_api()
    print("\n" + "=" * 50)
    print("✨ Test completed!")