from flask import Blueprint
from controllers.planner_controller import PlannerController

planner_bp = Blueprint('planner', __name__)
planner_controller = PlannerController()

@planner_bp.route('/create', methods=['POST'])
def create_plan():
    """Create a new financial plan"""
    return planner_controller.create_financial_plan()

@planner_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get recommendations for a user"""
    return planner_controller.get_plan_recommendations(user_id)

@planner_bp.route('/update/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id):
    """Update an existing plan"""
    return planner_controller.update_plan(plan_id)