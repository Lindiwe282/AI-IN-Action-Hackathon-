from flask import request, jsonify
from services.investment_service import InvestmentService
from utils.validators import validate_investment_input

class InvestmentController:
    def __init__(self):
        self.investment_service = InvestmentService()
    
    def get_investment_suggestions(self):
        """Get AI-powered investment suggestions based on user profile"""
        try:
            data = request.get_json()
            
            # Validate input
            validation_result = validate_investment_input(data)
            if not validation_result['valid']:
                return jsonify({
                    'error': 'Invalid input',
                    'details': validation_result['errors']
                }), 400
            
            # Get AI-powered investment suggestions
            suggestions = self.investment_service.get_suggestions(data)
            
            return jsonify({
                'success': True,
                'suggestions': suggestions,
                'message': 'Investment suggestions generated successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def analyze_portfolio(self):
        """Analyze user's current investment portfolio"""
        try:
            data = request.get_json()
            analysis = self.investment_service.analyze_portfolio(data)
            
            return jsonify({
                'success': True,
                'analysis': analysis
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def get_market_insights(self):
        """Get AI-powered market insights and trends"""
        try:
            insights = self.investment_service.get_market_insights()
            
            return jsonify({
                'success': True,
                'insights': insights
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500