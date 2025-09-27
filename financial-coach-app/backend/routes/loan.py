from flask import Blueprint, request, jsonify
from services.loan_service import LoanService
from utils.calculator import LoanCalculator

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/affordability', methods=['POST'])
def check_affordability():
    """Check loan affordability"""
    try:
        data = request.get_json()
        loan_service = LoanService()
        result = loan_service.check_affordability(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_bp.route('/calculate', methods=['POST'])
def calculate_loan():
    """Calculate loan payments"""
    try:
        data = request.get_json()
        calculator = LoanCalculator()
        result = calculator.calculate_payment(
            principal=data.get('principal'),
            rate=data.get('rate'),
            term=data.get('term')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loan_bp.route('/recommendations', methods=['POST'])
def get_loan_recommendations():
    """Get loan recommendations"""
    try:
        data = request.get_json()
        loan_service = LoanService()
        recommendations = loan_service.get_recommendations(data)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500