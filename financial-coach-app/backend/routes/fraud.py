from flask import Blueprint
from controllers.fraud_controller import FraudController

fraud_bp = Blueprint('fraud', __name__)
fraud_controller = FraudController()

@fraud_bp.route('/detect', methods=['POST'])
def detect_fraud():
    """Detect potential fraud"""
    return fraud_controller.detect_fraud()

@fraud_bp.route('/analyze-patterns', methods=['POST'])
def analyze_patterns():
    """Analyze transaction patterns"""
    return fraud_controller.analyze_transaction_patterns()

@fraud_bp.route('/security-recommendations', methods=['POST'])
def get_security_recommendations():
    """Get security recommendations"""
    return fraud_controller.get_security_recommendations()