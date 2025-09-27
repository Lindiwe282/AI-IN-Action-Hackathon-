from flask import request, jsonify
from services.planner_service import PlannerService
from utils.validators import validate_planner_input

class PlannerController:
    def __init__(self):
        self.planner_service = PlannerService()
    
    def create_financial_plan(self):
        """Create a personalized financial plan based on user data"""
        try:
            data = request.get_json()
            
            # Validate input
            validation_result = validate_planner_input(data)
            if not validation_result['valid']:
                return jsonify({
                    'error': 'Invalid input',
                    'details': validation_result['errors']
                }), 400
            
            # Generate financial plan using AI/ML
            plan = self.planner_service.generate_plan(data)
            
            return jsonify({
                'success': True,
                'plan': plan,
                'message': 'Financial plan generated successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def get_plan_recommendations(self, user_id):
        """Get AI-powered recommendations for an existing plan"""
        try:
            recommendations = self.planner_service.get_recommendations(user_id)
            
            return jsonify({
                'success': True,
                'recommendations': recommendations
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    
    def update_plan(self, plan_id):
        """Update an existing financial plan"""
        try:
            data = request.get_json()
            updated_plan = self.planner_service.update_plan(plan_id, data)
            
            return jsonify({
                'success': True,
                'plan': updated_plan,
                'message': 'Plan updated successfully'
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500