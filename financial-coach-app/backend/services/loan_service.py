import numpy as np
from utils.calculator import LoanCalculator

class LoanService:
    def __init__(self):
        self.calculator = LoanCalculator()
    
    def check_affordability(self, loan_data):
        """Check loan affordability using AI-enhanced analysis"""
        try:
            # Extract loan parameters
            income = loan_data.get('monthly_income', 0)
            existing_debt = loan_data.get('monthly_debt_payments', 0)
            loan_amount = loan_data.get('loan_amount', 0)
            interest_rate = loan_data.get('interest_rate', 5.0)
            loan_term = loan_data.get('loan_term_months', 360)
            
            # Calculate loan payment
            monthly_payment = self.calculator.calculate_payment(
                principal=loan_amount,
                rate=interest_rate / 100 / 12,
                term=loan_term
            )['monthly_payment']
            
            # Calculate debt-to-income ratios
            total_monthly_debt = existing_debt + monthly_payment
            dti_ratio = (total_monthly_debt / income) if income > 0 else float('inf')
            
            # AI-enhanced affordability analysis
            affordability_analysis = self._analyze_affordability(
                income, existing_debt, monthly_payment, dti_ratio, loan_data
            )
            
            return {
                'loan_amount': loan_amount,
                'monthly_payment': monthly_payment,
                'debt_to_income_ratio': dti_ratio,
                'debt_to_income_percentage': f"{dti_ratio * 100:.1f}%",
                'affordability_score': affordability_analysis['score'],
                'approval_likelihood': affordability_analysis['approval_likelihood'],
                'recommendations': affordability_analysis['recommendations'],
                'risk_factors': affordability_analysis['risk_factors']
            }
            
        except Exception as e:
            raise Exception(f"Error checking loan affordability: {str(e)}")
    
    def _analyze_affordability(self, income, existing_debt, monthly_payment, dti_ratio, loan_data):
        """AI-enhanced affordability analysis"""
        score = 100
        recommendations = []
        risk_factors = []
        
        # DTI ratio analysis
        if dti_ratio > 0.43:  # 43% is typical max DTI for mortgages
            score -= 40
            risk_factors.append("High debt-to-income ratio")
            recommendations.append({
                'type': 'debt_reduction',
                'message': 'Reduce existing debt before applying',
                'priority': 'high'
            })
        elif dti_ratio > 0.36:
            score -= 20
            risk_factors.append("Elevated debt-to-income ratio")
            recommendations.append({
                'type': 'budget_review',
                'message': 'Review budget to ensure comfortable payment',
                'priority': 'medium'
            })
        
        # Income stability
        employment_years = loan_data.get('employment_years', 0)
        if employment_years < 2:
            score -= 15
            risk_factors.append("Limited employment history")
        
        # Credit score impact
        credit_score = loan_data.get('credit_score', 700)
        if credit_score < 620:
            score -= 30
            risk_factors.append("Low credit score")
            recommendations.append({
                'type': 'credit_improvement',
                'message': 'Improve credit score before applying',
                'priority': 'high'
            })
        elif credit_score < 700:
            score -= 15
            recommendations.append({
                'type': 'credit_improvement',
                'message': 'Consider improving credit score for better rates',
                'priority': 'medium'
            })
        
        # Down payment analysis (for home loans)
        loan_type = loan_data.get('loan_type', 'personal')
        if loan_type.lower() in ['mortgage', 'home']:
            down_payment = loan_data.get('down_payment', 0)
            home_price = loan_data.get('home_price', loan_data.get('loan_amount', 0))
            if home_price > 0:
                down_payment_ratio = down_payment / home_price
                if down_payment_ratio < 0.20:
                    score -= 10
                    recommendations.append({
                        'type': 'down_payment',
                        'message': 'Consider larger down payment to avoid PMI',
                        'priority': 'medium'
                    })
        
        # Emergency fund check
        emergency_fund = loan_data.get('emergency_fund', 0)
        monthly_expenses = loan_data.get('monthly_expenses', income * 0.7)
        if emergency_fund < monthly_expenses * 3:
            score -= 10
            recommendations.append({
                'type': 'emergency_fund',
                'message': 'Build emergency fund before taking on debt',
                'priority': 'medium'
            })
        
        # Determine approval likelihood
        if score >= 80:
            approval_likelihood = "Very High"
        elif score >= 70:
            approval_likelihood = "High"
        elif score >= 60:
            approval_likelihood = "Moderate"
        elif score >= 50:
            approval_likelihood = "Low"
        else:
            approval_likelihood = "Very Low"
        
        return {
            'score': max(score, 0),
            'approval_likelihood': approval_likelihood,
            'recommendations': recommendations,
            'risk_factors': risk_factors
        }
    
    def get_recommendations(self, user_data):
        """Get personalized loan recommendations"""
        try:
            income = user_data.get('monthly_income', 0)
            credit_score = user_data.get('credit_score', 700)
            loan_purpose = user_data.get('loan_purpose', 'personal')
            
            recommendations = []
            
            # Home loan recommendations
            if loan_purpose.lower() in ['home', 'mortgage', 'house']:
                recommendations.extend(self._get_mortgage_recommendations(user_data))
            
            # Auto loan recommendations
            elif loan_purpose.lower() in ['auto', 'car', 'vehicle']:
                recommendations.extend(self._get_auto_loan_recommendations(user_data))
            
            # Personal loan recommendations
            elif loan_purpose.lower() in ['personal', 'debt_consolidation']:
                recommendations.extend(self._get_personal_loan_recommendations(user_data))
            
            # General recommendations
            recommendations.extend(self._get_general_loan_recommendations(user_data))
            
            return {
                'recommendations': recommendations,
                'best_loan_types': self._identify_best_loan_types(user_data),
                'rate_optimization_tips': self._get_rate_optimization_tips(user_data)
            }
            
        except Exception as e:
            raise Exception(f"Error generating loan recommendations: {str(e)}")
    
    def _get_mortgage_recommendations(self, user_data):
        """Get mortgage-specific recommendations"""
        recommendations = []
        income = user_data.get('monthly_income', 0)
        
        # Calculate affordable home price
        max_monthly_payment = income * 0.28  # 28% rule
        affordable_loan = self.calculator.calculate_affordable_loan(
            monthly_payment=max_monthly_payment,
            rate=0.065,  # 6.5% assumed rate
            term=360
        )
        
        recommendations.append({
            'type': 'mortgage',
            'loan_type': '30-Year Fixed Rate Mortgage',
            'max_loan_amount': affordable_loan,
            'estimated_rate': '6.5% - 7.0%',
            'pros': ['Predictable payments', 'Lower monthly payment'],
            'cons': ['Higher total interest paid'],
            'best_for': 'Long-term homeownership'
        })
        
        recommendations.append({
            'type': 'mortgage',
            'loan_type': '15-Year Fixed Rate Mortgage',
            'max_loan_amount': affordable_loan * 0.7,  # Higher payment, lower amount
            'estimated_rate': '6.0% - 6.5%',
            'pros': ['Lower total interest', 'Faster equity building'],
            'cons': ['Higher monthly payments'],
            'best_for': 'Higher income borrowers'
        })
        
        return recommendations
    
    def _get_auto_loan_recommendations(self, user_data):
        """Get auto loan recommendations"""
        recommendations = []
        credit_score = user_data.get('credit_score', 700)
        
        if credit_score >= 750:
            rate_range = '3.0% - 4.5%'
        elif credit_score >= 700:
            rate_range = '4.5% - 6.0%'
        elif credit_score >= 650:
            rate_range = '6.0% - 8.0%'
        else:
            rate_range = '8.0% - 12.0%'
        
        recommendations.append({
            'type': 'auto',
            'loan_type': 'New Car Loan',
            'estimated_rate': rate_range,
            'term_options': ['36 months', '48 months', '60 months'],
            'pros': ['Lower rates than used cars', 'Warranty coverage'],
            'cons': ['Higher depreciation'],
            'best_for': 'Buyers wanting latest features'
        })
        
        recommendations.append({
            'type': 'auto',
            'loan_type': 'Used Car Loan',
            'estimated_rate': f"{float(rate_range.split(' - ')[0][:-1]) + 0.5}% - {float(rate_range.split(' - ')[1][:-1]) + 1.0}%",
            'term_options': ['36 months', '48 months'],
            'pros': ['Lower purchase price', 'Slower depreciation'],
            'cons': ['Slightly higher rates', 'Potential maintenance issues'],
            'best_for': 'Budget-conscious buyers'
        })
        
        return recommendations
    
    def _get_personal_loan_recommendations(self, user_data):
        """Get personal loan recommendations"""
        recommendations = []
        credit_score = user_data.get('credit_score', 700)
        
        if credit_score >= 750:
            rate_range = '6.0% - 10.0%'
        elif credit_score >= 700:
            rate_range = '10.0% - 15.0%'
        elif credit_score >= 650:
            rate_range = '15.0% - 20.0%'
        else:
            rate_range = '20.0% - 25.0%'
        
        recommendations.append({
            'type': 'personal',
            'loan_type': 'Unsecured Personal Loan',
            'estimated_rate': rate_range,
            'term_options': ['24 months', '36 months', '48 months'],
            'pros': ['No collateral required', 'Fixed rates', 'Quick approval'],
            'cons': ['Higher rates than secured loans'],
            'best_for': 'Debt consolidation, home improvements'
        })
        
        return recommendations
    
    def _get_general_loan_recommendations(self, user_data):
        """Get general loan recommendations"""
        recommendations = []
        
        # Rate shopping recommendation
        recommendations.append({
            'type': 'general',
            'recommendation': 'Shop around with multiple lenders',
            'description': 'Compare rates from at least 3-5 lenders',
            'potential_savings': 'Up to 0.5% rate reduction'
        })
        
        # Timing recommendation
        recommendations.append({
            'type': 'general',
            'recommendation': 'Time your application strategically',
            'description': 'Apply when your credit score and income are at their best',
            'potential_savings': 'Better approval odds and rates'
        })
        
        return recommendations
    
    def _identify_best_loan_types(self, user_data):
        """Identify best loan types for user"""
        credit_score = user_data.get('credit_score', 700)
        income = user_data.get('monthly_income', 0)
        
        best_types = []
        
        if credit_score >= 750 and income >= 5000:
            best_types.extend(['Conventional Mortgage', 'Premium Auto Loans'])
        elif credit_score >= 700:
            best_types.extend(['FHA Mortgage', 'Standard Auto Loans'])
        elif credit_score >= 650:
            best_types.extend(['FHA Mortgage', 'Subprime Auto Loans'])
        else:
            best_types.extend(['VA Loan (if eligible)', 'Secured Personal Loans'])
        
        return best_types
    
    def _get_rate_optimization_tips(self, user_data):
        """Get tips to optimize loan rates"""
        tips = []
        credit_score = user_data.get('credit_score', 700)
        
        if credit_score < 750:
            tips.append({
                'tip': 'Improve credit score',
                'description': 'Pay down credit card balances and ensure on-time payments',
                'potential_impact': f'Could reduce rate by 0.5-1.0%'
            })
        
        tips.append({
            'tip': 'Increase down payment',
            'description': 'Larger down payment reduces lender risk',
            'potential_impact': 'Lower rate and eliminate PMI'
        })
        
        tips.append({
            'tip': 'Consider shorter loan terms',
            'description': 'Shorter terms typically offer lower rates',
            'potential_impact': 'Save thousands in total interest'
        })
        
        tips.append({
            'tip': 'Get pre-approved',
            'description': 'Pre-approval shows sellers you are serious',
            'potential_impact': 'Better negotiating position'
        })
        
        return tips