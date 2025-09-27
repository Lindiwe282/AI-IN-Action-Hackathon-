from flask import Blueprint, request, jsonify
from services.literacy_service import LiteracyService

literacy_bp = Blueprint('literacy', __name__)

@literacy_bp.route('/tips', methods=['GET'])
def get_tips():
    """Get financial literacy tips"""
    try:
        literacy_service = LiteracyService()
        tips = literacy_service.get_personalized_tips(request.args.to_dict())
        return jsonify(tips), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@literacy_bp.route('/quiz', methods=['POST'])
def financial_quiz():
    """Financial literacy quiz"""
    try:
        data = request.get_json()
        literacy_service = LiteracyService()
        result = literacy_service.evaluate_quiz(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@literacy_bp.route('/resources', methods=['GET'])
def get_resources():
    """Get educational resources"""
    try:
        literacy_service = LiteracyService()
        resources = literacy_service.get_resources(request.args.to_dict())
        return jsonify(resources), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500