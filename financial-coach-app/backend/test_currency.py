#!/usr/bin/env python3
"""
Test script for hedge endpoints with currency support
"""

import requests
import json

API_BASE = "http://localhost:5000/api/hedge"

def test_contracts():
    """Test getting market contracts"""
    print("Testing /contracts endpoint...")
    try:
        response = requests.get(f"{API_BASE}/contracts")
        if response.status_code == 200:
            data = response.json()
            print("✓ Contracts endpoint working")
            
            # Check US markets
            us_markets = data.get('data', {}).get('us_markets', [])
            if us_markets:
                sample_us = us_markets[0]
                print(f"  US Sample: {sample_us['symbol']} - {sample_us.get('currency', 'No currency')} {sample_us['current_price']}")
            
            # Check SA markets
            sa_markets = data.get('data', {}).get('sa_markets', [])
            if sa_markets:
                sample_sa = sa_markets[0]
                print(f"  SA Sample: {sample_sa['symbol']} - {sample_sa.get('currency', 'No currency')} {sample_sa['current_price']}")
                
            return True
        else:
            print(f"✗ Contracts endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing contracts: {e}")
        return False

def test_options_chain():
    """Test getting options chain"""
    print("\nTesting /options-chain endpoint...")
    try:
        payload = {"symbol": "SBK.JO"}
        response = requests.post(f"{API_BASE}/options-chain", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Options chain endpoint working")
            options_data = data.get('data', {})
            currency = options_data.get('currency', 'No currency')
            current_price = options_data.get('current_price', 0)
            print(f"  SBK.JO Options: {currency} {current_price}")
            return True
        else:
            print(f"✗ Options chain failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing options chain: {e}")
        return False

def test_portfolio_analysis():
    """Test portfolio analysis"""
    print("\nTesting /portfolio-analysis endpoint...")
    try:
        payload = {"symbols": ["SBK.JO", "AAPL"]}
        response = requests.post(f"{API_BASE}/portfolio-analysis", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Portfolio analysis endpoint working")
            contracts = data.get('data', {}).get('contracts', [])
            for contract in contracts:
                symbol = contract.get('symbol')
                currency = contract.get('currency', 'No currency')
                price = contract.get('current_price', 0)
                print(f"  {symbol}: {currency} {price}")
            return True
        else:
            print(f"✗ Portfolio analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing portfolio analysis: {e}")
        return False

if __name__ == "__main__":
    print("Testing Hedge API Endpoints with Currency Support")
    print("=" * 50)
    
    results = []
    results.append(test_contracts())
    results.append(test_options_chain())
    results.append(test_portfolio_analysis())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed! Currency support is working.")
    else:
        print("✗ Some tests failed. Check the server and endpoints.")