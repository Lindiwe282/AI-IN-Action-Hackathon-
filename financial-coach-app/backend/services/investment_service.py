import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class InvestmentService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained investment recommendation model"""
        try:
            model_path = os.path.join('models', 'investment_model.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                # Initialize a basic model if no pre-trained model exists
                self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        except Exception as e:
            print(f"Error loading investment model: {e}")
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def get_suggestions(self, user_data):
        """Get AI-powered investment suggestions"""
        try:
            # Analyze user profile
            risk_profile = self._analyze_risk_profile(user_data)
            
            # Generate portfolio allocation
            allocation = self._generate_portfolio_allocation(user_data, risk_profile)
            
            # Get specific investment recommendations
            recommendations = self._get_specific_recommendations(user_data, risk_profile)
            
            # Calculate expected returns
            expected_returns = self._calculate_expected_returns(allocation)
            
            return {
                'risk_profile': risk_profile,
                'portfolio_allocation': allocation,
                'specific_recommendations': recommendations,
                'expected_returns': expected_returns,
                'investment_timeline': self._create_investment_timeline(user_data)
            }
            
        except Exception as e:
            raise Exception(f"Error generating investment suggestions: {str(e)}")
    
    def _analyze_risk_profile(self, user_data):
        """Analyze user's investment risk profile"""
        age = user_data.get('age', 30)
        income = user_data.get('monthly_income', 0) * 12
        savings = user_data.get('current_savings', 0)
        risk_tolerance = user_data.get('risk_tolerance', 'medium').lower()
        investment_experience = user_data.get('investment_experience', 'beginner').lower()
        time_horizon = user_data.get('investment_timeline', 10)
        
        # Calculate risk score
        risk_score = 0
        
        # Age factor (younger = higher risk tolerance)
        if age < 30:
            risk_score += 3
        elif age < 40:
            risk_score += 2
        elif age < 50:
            risk_score += 1
        else:
            risk_score += 0
        
        # Income factor
        if income > 100000:
            risk_score += 2
        elif income > 50000:
            risk_score += 1
        
        # Risk tolerance factor
        if risk_tolerance == 'high':
            risk_score += 3
        elif risk_tolerance == 'medium':
            risk_score += 2
        else:
            risk_score += 1
        
        # Experience factor
        if investment_experience == 'expert':
            risk_score += 2
        elif investment_experience == 'intermediate':
            risk_score += 1
        
        # Time horizon factor
        if time_horizon > 10:
            risk_score += 2
        elif time_horizon > 5:
            risk_score += 1
        
        # Determine risk category
        if risk_score >= 8:
            risk_category = 'aggressive'
        elif risk_score >= 6:
            risk_category = 'moderate_aggressive'
        elif risk_score >= 4:
            risk_category = 'moderate'
        elif risk_score >= 2:
            risk_category = 'conservative'
        else:
            risk_category = 'very_conservative'
        
        return {
            'category': risk_category,
            'score': risk_score,
            'factors': {
                'age': age,
                'risk_tolerance': risk_tolerance,
                'experience': investment_experience,
                'time_horizon': time_horizon
            }
        }
    
    def _generate_portfolio_allocation(self, user_data, risk_profile):
        """Generate optimal portfolio allocation"""
        risk_category = risk_profile['category']
        
        # Base allocations based on risk profile
        allocations = {
            'very_conservative': {
                'bonds': 70, 'stocks': 20, 'cash': 10, 'alternatives': 0
            },
            'conservative': {
                'bonds': 60, 'stocks': 30, 'cash': 8, 'alternatives': 2
            },
            'moderate': {
                'bonds': 40, 'stocks': 50, 'cash': 5, 'alternatives': 5
            },
            'moderate_aggressive': {
                'bonds': 30, 'stocks': 60, 'cash': 3, 'alternatives': 7
            },
            'aggressive': {
                'bonds': 20, 'stocks': 70, 'cash': 2, 'alternatives': 8
            }
        }
        
        base_allocation = allocations.get(risk_category, allocations['moderate'])
        
        # Adjust based on age (rule of thumb: age in bonds)
        age = user_data.get('age', 30)
        suggested_bond_percentage = min(age, 70)
        
        # Blend base allocation with age-based adjustment
        adjusted_allocation = base_allocation.copy()
        if abs(base_allocation['bonds'] - suggested_bond_percentage) > 10:
            # Adjust gradually towards age-based allocation
            adjustment_factor = 0.3
            adjusted_allocation['bonds'] = int(
                base_allocation['bonds'] * (1 - adjustment_factor) + 
                suggested_bond_percentage * adjustment_factor
            )
            # Rebalance stocks
            difference = adjusted_allocation['bonds'] - base_allocation['bonds']
            adjusted_allocation['stocks'] = max(0, base_allocation['stocks'] - difference)
        
        return {
            'allocation': adjusted_allocation,
            'rationale': f"Based on {risk_category} risk profile and age {age}",
            'breakdown': {
                'stocks': {
                    'domestic': adjusted_allocation['stocks'] * 0.7,
                    'international': adjusted_allocation['stocks'] * 0.3
                },
                'bonds': {
                    'government': adjusted_allocation['bonds'] * 0.6,
                    'corporate': adjusted_allocation['bonds'] * 0.4
                }
            }
        }
    
    def _get_specific_recommendations(self, user_data, risk_profile):
        """Get specific investment product recommendations"""
        risk_category = risk_profile['category']
        investment_amount = user_data.get('investment_amount', 10000)
        
        recommendations = []
        
        # Stock recommendations based on risk profile
        if risk_category in ['aggressive', 'moderate_aggressive']:
            recommendations.extend([
                {
                    'type': 'ETF',
                    'name': 'Total Stock Market Index Fund',
                    'symbol': 'VTI',
                    'allocation_percentage': 35,
                    'risk_level': 'medium-high',
                    'expected_return': '8-10%',
                    'reason': 'Broad market exposure with growth potential'
                },
                {
                    'type': 'ETF',
                    'name': 'International Stock Index Fund',
                    'symbol': 'VTIAX',
                    'allocation_percentage': 15,
                    'risk_level': 'medium-high',
                    'expected_return': '7-9%',
                    'reason': 'International diversification'
                }
            ])
        
        # Bond recommendations
        if risk_category in ['conservative', 'very_conservative', 'moderate']:
            recommendations.extend([
                {
                    'type': 'Bond Fund',
                    'name': 'Total Bond Market Index Fund',
                    'symbol': 'BND',
                    'allocation_percentage': 30,
                    'risk_level': 'low',
                    'expected_return': '3-5%',
                    'reason': 'Stable income and capital preservation'
                }
            ])
        
        # Alternative investments for higher risk profiles
        if risk_category == 'aggressive' and investment_amount > 50000:
            recommendations.append({
                'type': 'REIT',
                'name': 'Real Estate Investment Trust',
                'symbol': 'VNQ',
                'allocation_percentage': 8,
                'risk_level': 'medium',
                'expected_return': '6-8%',
                'reason': 'Real estate exposure and diversification'
            })
        
        return recommendations
    
    def _calculate_expected_returns(self, allocation):
        """Calculate expected returns based on allocation"""
        # Historical average returns (simplified)
        expected_returns = {
            'stocks': 0.08,  # 8%
            'bonds': 0.04,   # 4%
            'cash': 0.01,    # 1%
            'alternatives': 0.06  # 6%
        }
        
        portfolio_allocation = allocation['allocation']
        weighted_return = sum(
            portfolio_allocation[asset] / 100 * expected_returns[asset]
            for asset in portfolio_allocation
        )
        
        return {
            'expected_annual_return': weighted_return,
            'expected_annual_return_percentage': f"{weighted_return * 100:.1f}%",
            'risk_level': self._calculate_portfolio_risk(portfolio_allocation),
            'volatility_estimate': self._estimate_volatility(portfolio_allocation)
        }
    
    def _calculate_portfolio_risk(self, allocation):
        """Calculate overall portfolio risk level"""
        risk_weights = {
            'stocks': 3,
            'alternatives': 2,
            'bonds': 1,
            'cash': 0
        }
        
        weighted_risk = sum(
            allocation[asset] / 100 * risk_weights.get(asset, 1)
            for asset in allocation
        )
        
        if weighted_risk > 2.5:
            return 'High'
        elif weighted_risk > 1.5:
            return 'Medium'
        else:
            return 'Low'
    
    def _estimate_volatility(self, allocation):
        """Estimate portfolio volatility"""
        volatilities = {
            'stocks': 0.16,  # 16%
            'bonds': 0.04,   # 4%
            'cash': 0.01,    # 1%
            'alternatives': 0.12  # 12%
        }
        
        weighted_volatility = sum(
            allocation[asset] / 100 * volatilities[asset]
            for asset in allocation
        )
        
        return f"{weighted_volatility * 100:.1f}%"
    
    def _create_investment_timeline(self, user_data):
        """Create investment timeline with milestones"""
        timeline = []
        investment_amount = user_data.get('investment_amount', 10000)
        time_horizon = user_data.get('investment_timeline', 10)
        
        # Short-term milestone (1 year)
        timeline.append({
            'years': 1,
            'milestone': 'Portfolio establishment',
            'target': 'Fully invested according to allocation',
            'expected_value': investment_amount * 1.06
        })
        
        # Medium-term milestone (5 years)
        if time_horizon >= 5:
            timeline.append({
                'years': 5,
                'milestone': 'Mid-term review',
                'target': 'Portfolio rebalancing and review',
                'expected_value': investment_amount * (1.07 ** 5)
            })
        
        # Long-term milestone (10+ years)
        if time_horizon >= 10:
            timeline.append({
                'years': 10,
                'milestone': 'Long-term growth',
                'target': 'Significant portfolio growth',
                'expected_value': investment_amount * (1.08 ** 10)
            })
        
        return timeline
    
    def analyze_portfolio(self, portfolio_data):
        """Analyze existing investment portfolio"""
        try:
            holdings = portfolio_data.get('holdings', [])
            
            if not holdings:
                return {'error': 'No portfolio holdings provided'}
            
            # Calculate current allocation
            total_value = sum(holding.get('value', 0) for holding in holdings)
            current_allocation = self._calculate_current_allocation(holdings, total_value)
            
            # Analyze diversification
            diversification_analysis = self._analyze_diversification(holdings)
            
            # Performance analysis
            performance_analysis = self._analyze_performance(holdings)
            
            # Generate rebalancing recommendations
            rebalancing_recommendations = self._generate_rebalancing_recommendations(
                current_allocation, portfolio_data.get('target_allocation', {})
            )
            
            return {
                'total_value': total_value,
                'current_allocation': current_allocation,
                'diversification': diversification_analysis,
                'performance': performance_analysis,
                'rebalancing_recommendations': rebalancing_recommendations
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing portfolio: {str(e)}")
    
    def _calculate_current_allocation(self, holdings, total_value):
        """Calculate current asset allocation"""
        allocation = {'stocks': 0, 'bonds': 0, 'cash': 0, 'alternatives': 0}
        
        for holding in holdings:
            asset_type = holding.get('type', 'stocks').lower()
            value = holding.get('value', 0)
            percentage = (value / total_value * 100) if total_value > 0 else 0
            
            if asset_type in allocation:
                allocation[asset_type] += percentage
            else:
                allocation['alternatives'] += percentage
        
        return allocation
    
    def _analyze_diversification(self, holdings):
        """Analyze portfolio diversification"""
        sectors = {}
        geographies = {}
        
        for holding in holdings:
            sector = holding.get('sector', 'unknown')
            geography = holding.get('geography', 'domestic')
            value = holding.get('value', 0)
            
            sectors[sector] = sectors.get(sector, 0) + value
            geographies[geography] = geographies.get(geography, 0) + value
        
        return {
            'sector_diversification': sectors,
            'geographic_diversification': geographies,
            'diversification_score': self._calculate_diversification_score(sectors, geographies)
        }
    
    def _calculate_diversification_score(self, sectors, geographies):
        """Calculate diversification score (0-100)"""
        score = 0
        
        # Sector diversification (max 50 points)
        num_sectors = len(sectors)
        if num_sectors >= 8:
            score += 50
        else:
            score += num_sectors * 6.25
        
        # Geographic diversification (max 50 points)
        num_geographies = len(geographies)
        if num_geographies >= 4:
            score += 50
        else:
            score += num_geographies * 12.5
        
        return min(score, 100)
    
    def _analyze_performance(self, holdings):
        """Analyze portfolio performance"""
        total_return = 0
        total_value = 0
        
        for holding in holdings:
            value = holding.get('value', 0)
            return_rate = holding.get('return_ytd', 0)
            total_return += value * return_rate
            total_value += value
        
        avg_return = (total_return / total_value) if total_value > 0 else 0
        
        return {
            'ytd_return': avg_return,
            'ytd_return_percentage': f"{avg_return * 100:.2f}%",
            'performance_rating': self._get_performance_rating(avg_return)
        }
    
    def _get_performance_rating(self, return_rate):
        """Get performance rating based on return rate"""
        if return_rate > 0.15:
            return 'Excellent'
        elif return_rate > 0.10:
            return 'Good'
        elif return_rate > 0.05:
            return 'Average'
        elif return_rate > 0:
            return 'Below Average'
        else:
            return 'Poor'
    
    def _generate_rebalancing_recommendations(self, current_allocation, target_allocation):
        """Generate portfolio rebalancing recommendations"""
        if not target_allocation:
            return {'message': 'No target allocation provided'}
        
        recommendations = []
        
        for asset_class, target_pct in target_allocation.items():
            current_pct = current_allocation.get(asset_class, 0)
            difference = target_pct - current_pct
            
            if abs(difference) > 5:  # Only recommend if difference > 5%
                action = 'Increase' if difference > 0 else 'Decrease'
                recommendations.append({
                    'asset_class': asset_class,
                    'action': action,
                    'current_percentage': current_pct,
                    'target_percentage': target_pct,
                    'adjustment_needed': abs(difference)
                })
        
        return recommendations
    
    def get_market_insights(self):
        """Get AI-powered market insights"""
        try:
            # This would typically fetch real market data
            # For now, return sample insights
            insights = {
                'market_trend': 'Bullish',
                'key_insights': [
                    {
                        'category': 'Technology',
                        'insight': 'Tech stocks showing strong growth potential',
                        'recommendation': 'Consider increasing tech allocation by 5%'
                    },
                    {
                        'category': 'Bonds',
                        'insight': 'Rising interest rates affecting bond prices',
                        'recommendation': 'Consider shorter-duration bonds'
                    },
                    {
                        'category': 'International',
                        'insight': 'Emerging markets showing recovery signs',
                        'recommendation': 'Consider gradual increase in EM exposure'
                    }
                ],
                'risk_factors': [
                    'Inflation concerns',
                    'Geopolitical tensions',
                    'Interest rate volatility'
                ],
                'opportunities': [
                    'Dividend-paying stocks',
                    'Real estate investment trusts',
                    'Commodities for inflation hedge'
                ]
            }
            
            return insights
            
        except Exception as e:
            raise Exception(f"Error getting market insights: {str(e)}")