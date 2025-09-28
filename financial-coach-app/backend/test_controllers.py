#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Simple test for fraud controller
try:
    from controllers.fraud_controller import FraudController
    print("✓ FraudController imported successfully")
    
    controller = FraudController()
    print("✓ FraudController initialized successfully")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error initializing controller: {e}")

# Test phishing controller
try:
    from controllers.phishing_controller import PhishingController
    print("✓ PhishingController imported successfully")
    
    phishing_controller = PhishingController("hybrid_phishing_components.pkl")
    print("✓ PhishingController initialized successfully")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error initializing phishing controller: {e}")

print("\nTest completed!")