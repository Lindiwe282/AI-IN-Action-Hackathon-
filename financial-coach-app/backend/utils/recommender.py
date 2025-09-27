import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import random

class FinancialRecommender:
    """AI-powered recommendation engine for financial products and advice"""
    
    def __init__(self):
        self.user_profiles = {}
        self.financial_products = self._initialize_products()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
    def _initialize_products(self):
        """Initialize database of financial products"""
        return {
            'savings_accounts': [
                {
                    'name': 'High-Yield Savings Account',
                    'type': 'savings',
                    'apy': 4.5,
                    'minimum_balance': 0,
                    'features': ['high_yield', 'fdic_insured', 'online_banking'],
                    'risk_level': 'low',
                    'target_audience': ['conservative', 'emergency_fund']
                },
                {
                    'name': 'Money Market Account',
                    'type': 'savings',
                    'apy': 3.8,
                    'minimum_balance': 1000,
                    'features': ['check_writing', 'fdic_insured', 'tiered_rates'],
                    'risk_level': 'low',
                    'target_audience': ['conservative', 'short_term']
                }
            ],
            'investment_products': [
                {
                    'name': 'Total Stock Market Index Fund',
                    'type': 'etf',
                    'expense_ratio': 0.03,
                    'expected_return': 8.0,
                    'risk_level': 'medium',
                    'features': ['broad_diversification', 'low_cost', 'passive'],
                    'target_audience': ['moderate', 'long_term', 'beginner']
                },
                {
                    'name': 'Bond Index Fund',
                    'type': 'mutual_fund',
                    'expense_ratio': 0.05,
                    'expected_return': 4.0,
                    'risk_level': 'low',
                    'features': ['income_focused', 'low_volatility', 'diversified'],
                    'target_audience': ['conservative', 'income', 'near_retirement']
                },
                {
                    'name': 'Target Date Fund 2050',
                    'type': 'mutual_fund',
                    'expense_ratio': 0.15,
                    'expected_return': 7.5,
                    'risk_level': 'medium',
                    'features': ['automatic_rebalancing', 'age_appropriate', 'one_fund_solution'],
                    'target_audience': ['beginner', 'retirement', 'hands_off']
                }
            ],
            'credit_cards': [
                {
                    'name': 'Cash Back Credit Card',
                    'type': 'credit_card',
                    'annual_fee': 0,
                    'cash_back_rate': 1.5,
                    'features': ['no_annual_fee', 'cash_back', 'fraud_protection'],
                    'credit_score_required': 650,
                    'target_audience': ['cash_back', 'no_fee', 'everyday_spending']
                },
                {
                    'name': 'Travel Rewards Card',
                    'type': 'credit_card',
                    'annual_fee': 95,
                    'rewards_rate': 2.0,
                    'features': ['travel_rewards', 'no_foreign_fees', 'travel_insurance'],
                    'credit_score_required': 700,
                    'target_audience': ['travel', 'premium', 'frequent_traveler']
                }
            ]
        }
    
    def create_user_profile(self, user_data):
        """Create and store user profile for recommendations"""
        user_id = user_data.get('user_id')
        
        profile = {
            'age': user_data.get('age', 30),
            'income': user_data.get('monthly_income', 0) * 12,
            'risk_tolerance': user_data.get('risk_tolerance', 'medium').lower(),
            'investment_experience': user_data.get('investment_experience', 'beginner').lower(),
            'financial_goals': user_data.get('financial_goals', ['retirement', 'emergency_fund']),
            'current_savings': user_data.get('current_savings', 0),
            'debt_amount': user_data.get('total_debt', 0),
            'investment_timeline': user_data.get('investment_timeline', 10),
            'preferences': user_data.get('preferences', [])
        }
        
        # Calculate derived attributes
        profile['life_stage'] = self._determine_life_stage(profile['age'])
        profile['investment_capacity'] = self._calculate_investment_capacity(profile)
        profile['risk_score'] = self._calculate_risk_score(profile)
        
        self.user_profiles[user_id] = profile
        return profile
    
    def _determine_life_stage(self, age):
        """Determine user's life stage based on age"""
        if age < 25:
            return 'young_professional'
        elif age < 35:
            return 'early_career'
        elif age < 45:
            return 'mid_career'
        elif age < 55:
            return 'peak_earning'
        elif age < 65:
            return 'pre_retirement'
        else:
            return 'retirement'
    
    def _calculate_investment_capacity(self, profile):
        """Calculate user's investment capacity"""
        monthly_income = profile['income'] / 12
        debt_to_income = profile['debt_amount'] / profile['income'] if profile['income'] > 0 else 0
        
        if monthly_income < 3000 or debt_to_income > 0.4:
            return 'low'
        elif monthly_income < 8000 or debt_to_income > 0.2:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_risk_score(self, profile):
        """Calculate numerical risk score (0-10)"""
        score = 5  # Base score
        
        # Age factor
        if profile['age'] < 30:
            score += 2
        elif profile['age'] < 40:
            score += 1
        elif profile['age'] > 55:
            score -= 2
        
        # Risk tolerance
        risk_adjustments = {'low': -2, 'medium': 0, 'high': 2}
        score += risk_adjustments.get(profile['risk_tolerance'], 0)
        
        # Experience
        exp_adjustments = {'beginner': -1, 'intermediate': 0, 'expert': 1}
        score += exp_adjustments.get(profile['investment_experience'], 0)
        
        # Timeline
        if profile['investment_timeline'] > 15:
            score += 1
        elif profile['investment_timeline'] < 5:
            score -= 1
        
        return max(0, min(10, score))
    
    def get_personalized_recommendations(self, user_id, recommendation_type='all'):
        """Get personalized recommendations for user"""
        if user_id not in self.user_profiles:
            return {'error': 'User profile not found'}
        
        profile = self.user_profiles[user_id]
        recommendations = {}
        
        if recommendation_type in ['all', 'savings']:
            recommendations['savings'] = self._recommend_savings_products(profile)
        
        if recommendation_type in ['all', 'investments']:
            recommendations['investments'] = self._recommend_investment_products(profile)
        
        if recommendation_type in ['all', 'credit']:
            recommendations['credit'] = self._recommend_credit_products(profile)
        
        if recommendation_type in ['all', 'strategies']:
            recommendations['strategies'] = self._recommend_strategies(profile)
        
        return recommendations
    
    def _recommend_savings_products(self, profile):
        """Recommend savings products based on user profile"""
        products = self.financial_products['savings_accounts']
        recommendations = []
        
        for product in products:
            score = self._calculate_product_score(product, profile, 'savings')
            if score > 0.5:  # Threshold for recommendation
                recommendations.append({
                    'product': product,
                    'score': score,
                    'reasons': self._generate_recommendation_reasons(product, profile, 'savings')
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]  # Top 3 recommendations
    
    def _recommend_investment_products(self, profile):
        """Recommend investment products based on user profile"""
        products = self.financial_products['investment_products']
        recommendations = []
        
        for product in products:
            score = self._calculate_product_score(product, profile, 'investment')
            if score > 0.3:  # Lower threshold for investments
                recommendations.append({
                    'product': product,
                    'score': score,
                    'reasons': self._generate_recommendation_reasons(product, profile, 'investment'),
                    'allocation_percentage': self._suggest_allocation(product, profile)
                })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations
    
    def _recommend_credit_products(self, profile):
        """Recommend credit products based on user profile"""
        products = self.financial_products['credit_cards']
        recommendations = []
        
        # Estimate credit score based on profile
        estimated_credit_score = self._estimate_credit_score(profile)
        
        for product in products:
            if estimated_credit_score >= product.get('credit_score_required', 600):
                score = self._calculate_product_score(product, profile, 'credit')
                if score > 0.4:
                    recommendations.append({
                        'product': product,
                        'score': score,
                        'reasons': self._generate_recommendation_reasons(product, profile, 'credit')
                    })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:2]  # Top 2 credit recommendations
    
    def _recommend_strategies(self, profile):
        """Recommend financial strategies based on user profile"""
        strategies = []
        
        # Emergency fund strategy
        emergency_fund_months = profile['current_savings'] / (profile['income'] / 12) if profile['income'] > 0 else 0
        if emergency_fund_months < 6:
            strategies.append({
                'strategy': 'Build Emergency Fund',
                'priority': 'high',
                'description': 'Focus on building 3-6 months of expenses in savings',
                'action_steps': [
                    'Open high-yield savings account',
                    'Set up automatic transfers',
                    f'Save ${(profile["income"] / 12 * 6 - profile["current_savings"]):.0f} to reach 6-month goal'
                ]
            })
        
        # Debt payoff strategy
        if profile['debt_amount'] > 0:
            debt_to_income = profile['debt_amount'] / profile['income']
            if debt_to_income > 0.2:
                strategies.append({
                    'strategy': 'Debt Payoff Plan',
                    'priority': 'high',
                    'description': 'Focus on reducing high-interest debt',
                    'action_steps': [
                        'List all debts with interest rates',
                        'Consider debt avalanche method',
                        'Look into debt consolidation options'
                    ]
                })
        
        # Investment strategy
        if profile['investment_capacity'] in ['medium', 'high'] and emergency_fund_months >= 3:
            strategies.append({
                'strategy': 'Start Investing',
                'priority': 'medium',
                'description': 'Begin building long-term wealth through investing',
                'action_steps': [
                    'Open investment account',
                    'Start with low-cost index funds',
                    f'Consider target allocation: {self._suggest_asset_allocation(profile)}'
                ]
            })
        
        return strategies
    
    def _calculate_product_score(self, product, profile, product_type):
        """Calculate compatibility score between product and user profile"""
        score = 0.5  # Base score
        
        # Risk alignment
        product_risk = product.get('risk_level', 'medium')
        risk_alignment = self._calculate_risk_alignment(product_risk, profile['risk_tolerance'])
        score += risk_alignment * 0.3
        
        # Target audience match
        target_audience = product.get('target_audience', [])
        audience_match = self._calculate_audience_match(target_audience, profile)
        score += audience_match * 0.3
        
        # Life stage appropriateness
        life_stage_match = self._calculate_life_stage_match(product, profile['life_stage'])
        score += life_stage_match * 0.2
        
        # Product-specific scoring
        if product_type == 'investment':
            # Consider expense ratio for investments
            expense_ratio = product.get('expense_ratio', 0.5)
            if expense_ratio < 0.1:
                score += 0.1
            elif expense_ratio > 0.5:
                score -= 0.1
        elif product_type == 'savings':
            # Consider APY for savings
            apy = product.get('apy', 1.0)
            if apy > 4.0:
                score += 0.1
            elif apy < 2.0:
                score -= 0.1
        
        return max(0, min(1, score))
    
    def _calculate_risk_alignment(self, product_risk, user_risk):
        """Calculate how well product risk matches user risk tolerance"""
        risk_scores = {'low': 1, 'medium': 2, 'high': 3}
        product_score = risk_scores.get(product_risk, 2)
        user_score = risk_scores.get(user_risk, 2)
        
        difference = abs(product_score - user_score)
        if difference == 0:
            return 1.0
        elif difference == 1:
            return 0.5
        else:
            return 0.0
    
    def _calculate_audience_match(self, target_audience, profile):
        """Calculate how well user matches target audience"""
        matches = 0
        total_checks = 0
        
        # Check various profile attributes against target audience
        checks = [
            (profile['risk_tolerance'] in target_audience, 1),
            (profile['life_stage'] in target_audience, 1),
            (profile['investment_experience'] in target_audience, 0.5),
            ('beginner' in target_audience and profile['investment_experience'] == 'beginner', 0.5)
        ]
        
        for check, weight in checks:
            total_checks += weight
            if check:
                matches += weight
        
        return matches / total_checks if total_checks > 0 else 0.5
    
    def _calculate_life_stage_match(self, product, life_stage):
        """Calculate life stage appropriateness"""
        # Define product-life stage compatibility
        compatibility = {
            'young_professional': ['high_yield', 'low_cost', 'simple'],
            'early_career': ['growth', 'aggressive', 'long_term'],
            'mid_career': ['balanced', 'diversified', 'moderate'],
            'peak_earning': ['tax_advantaged', 'premium', 'sophisticated'],
            'pre_retirement': ['conservative', 'income', 'low_risk'],
            'retirement': ['income', 'conservative', 'liquid']
        }
        
        life_stage_features = compatibility.get(life_stage, [])
        product_features = product.get('features', [])
        
        matches = len(set(life_stage_features) & set(product_features))
        return matches / max(len(life_stage_features), 1)
    
    def _generate_recommendation_reasons(self, product, profile, product_type):
        """Generate human-readable reasons for recommendation"""
        reasons = []
        
        # Risk alignment reason
        if product.get('risk_level') == profile['risk_tolerance']:
            reasons.append(f"Matches your {profile['risk_tolerance']} risk tolerance")
        
        # Feature-based reasons
        features = product.get('features', [])
        if 'low_cost' in features:
            reasons.append("Low fees help maximize returns")
        if 'fdic_insured' in features:
            reasons.append("FDIC insured for safety")
        if 'high_yield' in features:
            reasons.append("Higher interest rate than average")
        
        # Life stage reason
        life_stage_reasons = {
            'young_professional': "Good for building initial wealth",
            'early_career': "Supports long-term growth goals",
            'mid_career': "Balanced approach for your career stage",
            'peak_earning': "Takes advantage of higher income capacity",
            'pre_retirement': "Conservative approach as you near retirement",
            'retirement': "Provides stable income in retirement"
        }
        
        if profile['life_stage'] in life_stage_reasons:
            reasons.append(life_stage_reasons[profile['life_stage']])
        
        if not reasons:
            reasons.append("Good fit for your financial profile")
        
        return reasons[:3]  # Limit to top 3 reasons
    
    def _suggest_allocation(self, product, profile):
        """Suggest allocation percentage for investment product"""
        base_allocation = {
            'low': {'stocks': 30, 'bonds': 70},
            'medium': {'stocks': 60, 'bonds': 40},
            'high': {'stocks': 80, 'bonds': 20}
        }
        
        risk_level = profile['risk_tolerance']
        product_type = product.get('type', '')
        
        if 'stock' in product['name'].lower() or product_type == 'etf':
            return base_allocation[risk_level]['stocks']
        elif 'bond' in product['name'].lower():
            return base_allocation[risk_level]['bonds']
        else:
            return 20  # Default allocation
    
    def _suggest_asset_allocation(self, profile):
        """Suggest overall asset allocation"""
        age = profile['age']
        risk_tolerance = profile['risk_tolerance']
        
        # Age-based rule: stocks = 100 - age, adjusted for risk tolerance
        base_stock_pct = 100 - age
        
        # Risk tolerance adjustments
        if risk_tolerance == 'high':
            stock_pct = min(90, base_stock_pct + 20)
        elif risk_tolerance == 'low':
            stock_pct = max(20, base_stock_pct - 20)
        else:
            stock_pct = base_stock_pct
        
        bond_pct = 100 - stock_pct
        
        return f"{stock_pct}% stocks, {bond_pct}% bonds"
    
    def _estimate_credit_score(self, profile):
        """Estimate credit score based on profile"""
        base_score = 650
        
        # Income factor
        annual_income = profile['income']
        if annual_income > 100000:
            base_score += 50
        elif annual_income > 60000:
            base_score += 30
        elif annual_income < 30000:
            base_score -= 30
        
        # Debt factor
        debt_to_income = profile['debt_amount'] / profile['income'] if profile['income'] > 0 else 0
        if debt_to_income < 0.1:
            base_score += 40
        elif debt_to_income < 0.3:
            base_score += 20
        elif debt_to_income > 0.5:
            base_score -= 50
        
        return max(300, min(850, base_score))
    
    def get_similar_users_recommendations(self, user_id, num_recommendations=5):
        """Get recommendations based on similar users (collaborative filtering)"""
        if user_id not in self.user_profiles:
            return {'error': 'User profile not found'}
        
        current_user = self.user_profiles[user_id]
        similar_users = self._find_similar_users(current_user, user_id)
        
        if not similar_users:
            return {'message': 'No similar users found, using content-based recommendations'}
        
        # Aggregate recommendations from similar users
        recommendations = self._aggregate_similar_user_recommendations(similar_users)
        
        return {
            'collaborative_recommendations': recommendations,
            'similar_users_count': len(similar_users)
        }
    
    def _find_similar_users(self, target_user, target_user_id):
        """Find users similar to target user"""
        similar_users = []
        
        for user_id, profile in self.user_profiles.items():
            if user_id == target_user_id:
                continue
            
            similarity = self._calculate_user_similarity(target_user, profile)
            if similarity > 0.7:  # Similarity threshold
                similar_users.append({
                    'user_id': user_id,
                    'profile': profile,
                    'similarity': similarity
                })
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_users[:5]  # Top 5 similar users
    
    def _calculate_user_similarity(self, user1, user2):
        """Calculate similarity between two user profiles"""
        # Feature vector for comparison
        features1 = [
            user1['age'] / 100,  # Normalize age
            user1['income'] / 200000,  # Normalize income
            user1['risk_score'] / 10,  # Risk score is already 0-10
            user1['investment_timeline'] / 30,  # Normalize timeline
            user1['current_savings'] / 100000  # Normalize savings
        ]
        
        features2 = [
            user2['age'] / 100,
            user2['income'] / 200000,
            user2['risk_score'] / 10,
            user2['investment_timeline'] / 30,
            user2['current_savings'] / 100000
        ]
        
        # Calculate cosine similarity
        features1 = np.array(features1).reshape(1, -1)
        features2 = np.array(features2).reshape(1, -1)
        
        similarity = cosine_similarity(features1, features2)[0][0]
        return similarity
    
    def _aggregate_similar_user_recommendations(self, similar_users):
        """Aggregate recommendations from similar users"""
        # This would typically pull actual recommendations from database
        # For now, return sample aggregated recommendations
        
        aggregated = {
            'popular_products': [
                'Total Stock Market Index Fund',
                'High-Yield Savings Account',
                'Target Date Fund'
            ],
            'common_strategies': [
                'Emergency fund building',
                'Index fund investing',
                'Automated savings'
            ],
            'average_allocations': {
                'stocks': 65,
                'bonds': 30,
                'cash': 5
            }
        }
        
        return aggregated