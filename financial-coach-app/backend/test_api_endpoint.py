#!/usr/bin/env python3
"""
Test script for the updated phishing API with separate URL and text parameters
"""

import requests
import json

def test_phishing_api_endpoint():
    """Test the phishing API endpoint with separate URL and text"""
    url = "http://localhost:5000/api/fraud/phishing/detect"
    
    test_cases = [
        {
            "name": "Suspicious email with phishing URL",
            "url": "https://bit.ly/fake-bank-login", 
            "text": "URGENT! Your account will be suspended. Click here to verify your account details!"
        },
        {
            "name": "URL only - suspicious",
            "url": "https://paypal-verification.phishing-site.com/login",
            "text": ""
        },
        {
            "name": "Text only - phishing content",
            "url": "",
            "text": "Congratulations! You've won $10,000! Click here immediately to claim your prize!"
        },
        {
            "name": "Normal business email",
            "url": "",
            "text": "Hello, this is a reminder about our meeting tomorrow at 2 PM in conference room A."
        },
        {
            "name": "Legitimate website",
            "url": "https://www.google.com",
            "text": "Google search homepage"
        }
    ]
    
    print("🔍 Testing Phishing Detection API Endpoint")
    print("=" * 60)
    
    for i, case in enumerate(test_cases):
        print(f"\n🧪 Test {i+1}: {case['name']}")
        print(f"   URL: {case['url'] if case['url'] else 'None'}")
        print(f"   Text: {case['text'][:50] if case['text'] else 'None'}{'...' if len(case['text']) > 50 else ''}")
        
        # Prepare form data
        data = {
            'url': case['url'],
            'text': case['text']
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📊 Risk Score: {result.get('risk_score', 0):.3f} ({result.get('risk_score', 0)*100:.1f}%)")
                print(f"   🎯 Is Phishing: {result.get('is_phishing', False)}")
                print(f"   🔗 URL Score: {result.get('ml_probability', 0):.3f}")
                print(f"   📝 Text Score: {result.get('text_probability', 0):.3f}")
                
                if result.get('keywords_detected'):
                    keywords = [kw.get('keyword', '') for kw in result.get('keywords_detected', [])]
                    print(f"   🚩 Keywords: {len(keywords)} found - {', '.join(keywords[:3])}")
                
            else:
                print(f"   ❌ Error {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"   Error: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error: Backend server not running on localhost:5000")
            break
        except requests.exceptions.Timeout:
            print("   ❌ Timeout Error: Request took too long")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✨ API Test completed!")

if __name__ == "__main__":
    test_phishing_api_endpoint()