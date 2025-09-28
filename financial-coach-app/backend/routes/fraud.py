# financial-coach-app/backend/routes/fraud.py
from flask import Blueprint, jsonify
from controllers.fraud_controller import FraudController

fraud_bp = Blueprint('fraud', __name__)
fraud_controller = FraudController()

@fraud_bp.route('/detect', methods=['POST'])
def detect_fraud():
    """Detect potential fraud"""
    return fraud_controller.detect_fraud_route()

@fraud_bp.route('/phishing/detect', methods=['POST'])
def detect_phishing():
    """Detect potential phishing"""
    return fraud_controller.detect_phishing_route()

@fraud_bp.route('/phishing/test', methods=['GET'])
def test_phishing():
    """Test phishing endpoint"""
    try:
        if fraud_controller.phishing_controller:
            return jsonify({
                "status": "available",
                "message": "Phishing detection is working",
                "test_result": fraud_controller.phishing_controller.predict("", "test message")
            })
        else:
            return jsonify({
                "status": "unavailable", 
                "message": "Phishing controller not initialized"
            }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@fraud_bp.route('/analyze-patterns', methods=['POST'])
def analyze_patterns():
    """Analyze transaction patterns"""
    return fraud_controller.analyze_transaction_patterns()

@fraud_bp.route('/security-recommendations', methods=['POST'])
def get_security_recommendations():
    """Get security recommendations"""
    return fraud_controller.get_security_recommendations()