import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class PlannerService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained financial planning model"""
        try:
            model_path = os.path.join('models', 'financial_planner_model.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                # Initialize a basic model if no pre-trained model exists
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def generate_plan(self, user_data):
        """Generate personalized financial plan using AI/ML"""
        try:
            # Extract features from user data
            features = self._extract_features(user_data)
            
            # Generate AI-powered recommendations
            recommendations = self._generate_recommendations(features)
            
            # Calculate budget allocation
            budget_allocation = self._calculate_budget_allocation(user_data)
            
            # Generate savings goals
            savings_goals = self._generate_savings_goals(user_data)
            
            plan = {
                'user_id': user_data.get('user_id'),
                'budget_allocation': budget_allocation,
                'savings_goals': savings_goals,
                'recommendations': recommendations,
                'risk_assessment': self._assess_risk(user_data),
                'timeline': self._create_timeline(user_data),
                'emergency_fund': self._calculate_emergency_fund(user_data)
            }
            
            return plan
            
        except Exception as e:
            raise Exception(f"Error generating financial plan: {str(e)}")
    
    def _extract_features(self, user_data):
        """Extract features for ML model"""
        return {
            'income': user_data.get('monthly_income', 0),
            'expenses': user_data.get('monthly_expenses', 0),
            'age': user_data.get('age', 30),
            'dependents': user_data.get('dependents', 0),
            'debt': user_data.get('total_debt', 0),
            'savings': user_data.get('current_savings', 0),
            'risk_tolerance': user_data.get('risk_tolerance', 'medium')
        }
    
    def _generate_recommendations(self, features):
        """Generate AI-powered financial recommendations"""
        recommendations = []
        
        # Income to expense ratio analysis
        if features['income'] > 0:
            expense_ratio = features['expenses'] / features['income']
            if expense_ratio > 0.8:
                recommendations.append({
                    'type': 'expense_reduction',
                    'priority': 'high',
                    'message': 'Consider reducing expenses as they exceed 80% of income',
                    'suggested_action': 'Review and cut non-essential expenses'
                })
        
        # Emergency fund recommendation
        monthly_expenses = features['expenses']
        emergency_fund_target = monthly_expenses * 6
        if features['savings'] < emergency_fund_target:
            recommendations.append({
                'type': 'emergency_fund',
                'priority': 'high',
                'message': f'Build emergency fund to ${emergency_fund_target:,.2f}',
                'suggested_action': 'Set aside 10-15% of income monthly'
            })
        
        # Debt management
        if features['debt'] > features['income'] * 12:
            recommendations.append({
                'type': 'debt_management',
                'priority': 'critical',
                'message': 'High debt-to-income ratio detected',
                'suggested_action': 'Consider debt consolidation or payment plan'
            })
        
        return recommendations
    
    def _calculate_budget_allocation(self, user_data):
        """Calculate optimal budget allocation using 50/30/20 rule with AI adjustments"""
        income = user_data.get('monthly_income', 0)
        
        # Base allocation (50/30/20 rule)
        base_needs = income * 0.5
        base_wants = income * 0.3
        base_savings = income * 0.2
        
        # AI adjustments based on user profile
        age = user_data.get('age', 30)
        dependents = user_data.get('dependents', 0)
        
        # Adjust for age and dependents
        if age < 30:
            savings_multiplier = 1.1  # Encourage more savings for younger users
        elif age > 50:
            needs_multiplier = 1.1  # More conservative approach
            savings_multiplier = 0.9
        else:
            savings_multiplier = 1.0
            needs_multiplier = 1.0
        
        if dependents > 0:
            needs_multiplier = 1.2  # More for family needs
            wants_multiplier = 0.8
        else:
            needs_multiplier = 1.0
            wants_multiplier = 1.0
        
        return {
            'needs': base_needs * needs_multiplier,
            'wants': base_wants * wants_multiplier,
            'savings': base_savings * savings_multiplier,
            'percentages': {
                'needs': (base_needs * needs_multiplier / income) * 100,
                'wants': (base_wants * wants_multiplier / income) * 100,
                'savings': (base_savings * savings_multiplier / income) * 100
            }
        }
    
    def _generate_savings_goals(self, user_data):
        """Generate personalized savings goals"""
        income = user_data.get('monthly_income', 0)
        age = user_data.get('age', 30)
        
        goals = []
        
        # Emergency fund goal
        emergency_fund = user_data.get('monthly_expenses', income * 0.7) * 6
        goals.append({
            'type': 'emergency_fund',
            'target_amount': emergency_fund,
            'priority': 'high',
            'timeline_months': 12
        })
        
        # Retirement goal based on age
        retirement_years = 65 - age
        retirement_target = income * 12 * 10  # 10x annual income
        goals.append({
            'type': 'retirement',
            'target_amount': retirement_target,
            'priority': 'medium',
            'timeline_months': retirement_years * 12
        })
        
        return goals
    
    def _assess_risk(self, user_data):
        """Assess financial risk profile"""
        risk_factors = []
        risk_score = 0
        
        income = user_data.get('monthly_income', 0)
        expenses = user_data.get('monthly_expenses', 0)
        debt = user_data.get('total_debt', 0)
        savings = user_data.get('current_savings', 0)
        
        # Income stability risk
        if income < 3000:
            risk_factors.append("Low income level")
            risk_score += 2
        
        # Expense ratio risk
        if income > 0 and (expenses / income) > 0.8:
            risk_factors.append("High expense-to-income ratio")
            risk_score += 3
        
        # Debt risk
        if debt > income * 5:
            risk_factors.append("High debt burden")
            risk_score += 4
        
        # Savings risk
        if savings < expenses * 3:
            risk_factors.append("Insufficient emergency savings")
            risk_score += 2
        
        if risk_score <= 3:
            risk_level = "Low"
        elif risk_score <= 6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return {
            'level': risk_level,
            'score': risk_score,
            'factors': risk_factors
        }
    
    def _create_timeline(self, user_data):
        """Create financial milestone timeline"""
        timeline = []
        
        # 3-month milestone
        timeline.append({
            'months': 3,
            'milestone': 'Emergency fund (1 month expenses)',
            'target_amount': user_data.get('monthly_expenses', 0)
        })
        
        # 6-month milestone
        timeline.append({
            'months': 6,
            'milestone': 'Emergency fund (3 months expenses)',
            'target_amount': user_data.get('monthly_expenses', 0) * 3
        })
        
        # 12-month milestone
        timeline.append({
            'months': 12,
            'milestone': 'Full emergency fund (6 months expenses)',
            'target_amount': user_data.get('monthly_expenses', 0) * 6
        })
        
        return timeline
    
    def _calculate_emergency_fund(self, user_data):
        """Calculate emergency fund requirement"""
        monthly_expenses = user_data.get('monthly_expenses', 0)
        dependents = user_data.get('dependents', 0)
        
        # Base: 6 months of expenses
        base_months = 6
        
        # Adjust based on dependents and job stability
        if dependents > 0:
            base_months += 2
        
        target_amount = monthly_expenses * base_months
        current_savings = user_data.get('current_savings', 0)
        
        return {
            'target_amount': target_amount,
            'current_amount': current_savings,
            'shortfall': max(0, target_amount - current_savings),
            'months_to_target': base_months
        }
    
    def get_recommendations(self, user_id):
        """Get updated recommendations for existing user"""
        # This would typically fetch user data from database
        # For now, return sample recommendations
        return {
            'recommendations': [
                {
                    'type': 'investment',
                    'message': 'Consider increasing investment allocation',
                    'priority': 'medium'
                }
            ]
        }
    
    def update_plan(self, plan_id, updated_data):
        """Update existing financial plan"""
        # This would typically update the plan in database
        return {
            'plan_id': plan_id,
            'updated': True,
            'message': 'Plan updated successfully'
        }