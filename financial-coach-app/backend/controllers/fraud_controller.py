from flask import request, jsonify
from services.fraud_service import FraudService
from utils.validators import validate_fraud_input

class FraudController:
    def __init__(self):
        self.fraud_service = FraudService()
    
    def detect_fraud(self):
        """Detect potential fraud using AI/ML models"""
        try:
            data = request.get_json()
            
            # Validate input
            validation_result = validate_fraud_input(data)
            if not validation_result['valid']:
                return jsonify({
                    'error': 'Invalid input',
                    'details': validation_result['errors']
                }), 400
            
            # Run fraud detection
            fraud_result = self.fraud_service.detect_fraud(data)
            
            return jsonify({
                'success': True,
                'fraud_detection': fraud_result,
                'message': 'Fraud detection completed'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def analyze_transaction_patterns(self):
        """Analyze transaction patterns for anomalies"""
        try:
            data = request.get_json()
            analysis = self.fraud_service.analyze_patterns(data)
            
            return jsonify({
                'success': True,
                'analysis': analysis
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def get_security_recommendations(self):
        """Get AI-powered security recommendations"""
        try:
            data = request.get_json()
            recommendations = self.fraud_service.get_security_recommendations(data)
            
            return jsonify({
                'success': True,
                'recommendations': recommendations
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500