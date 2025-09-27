from flask import Blueprint
from controllers.investment_controller import InvestmentController

investment_bp = Blueprint('investment', __name__)
investment_controller = InvestmentController()

@investment_bp.route('/suggestions', methods=['POST'])
def get_suggestions():
    """Get investment suggestions"""
    return investment_controller.get_investment_suggestions()

@investment_bp.route('/analyze', methods=['POST'])
def analyze_portfolio():
    """Analyze investment portfolio"""
    return investment_controller.analyze_portfolio()

@investment_bp.route('/insights', methods=['GET'])
def get_market_insights():
    """Get market insights"""
    return investment_controller.get_market_insights()