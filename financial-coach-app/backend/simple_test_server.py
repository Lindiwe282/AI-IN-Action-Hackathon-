#!/usr/bin/env python3
"""
Simple test server for hedge endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from services.simple_options_service import SimpleOptionsService
from controllers.simple_hedge_controller import get_market_contracts

app = Flask(__name__)
CORS(app)

# Initialize service
options_service = SimpleOptionsService()

@app.route('/api/hedge/contracts', methods=['GET'])
def contracts():
    result = get_market_contracts()
    return jsonify(result)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test server running", "status": "ok"})

if __name__ == '__main__':
    print("Starting simple hedge test server on port 5001...")
    print("Test endpoints:")
    print("  GET http://localhost:5001/test")
    print("  GET http://localhost:5001/api/hedge/contracts")
    app.run(debug=True, port=5001)