import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
import pickle

class FraudService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained fraud detection model"""
        try:
            model_path = os.path.join('models', 'fraud_model.pkl')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                # Initialize a basic model if no pre-trained model exists
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                # Train with sample data for demonstration
                self._train_basic_model()
        except Exception as e:
            print(f"Error loading fraud model: {e}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self._train_basic_model()
    
    def _train_basic_model(self):
        """Train a basic fraud detection model with sample data"""
        try:
            # Generate sample training data
            np.random.seed(42)
            n_samples = 1000
            
            # Features: amount, time_of_day, merchant_category, location_risk
            X = np.random.rand(n_samples, 4)
            X[:, 0] *= 10000  # Transaction amount
            X[:, 1] *= 24     # Hour of day
            X[:, 2] *= 10     # Merchant category
            X[:, 3] *= 5      # Location risk score
            
            # Generate labels (fraud/not fraud)
            # Higher amounts, late hours, and high risk locations more likely to be fraud
            fraud_probability = (X[:, 0] > 5000).astype(int) * 0.3 + \
                              (X[:, 1] > 22).astype(int) * 0.2 + \
                              (X[:, 1] < 6).astype(int) * 0.2 + \
                              (X[:, 3] > 3).astype(int) * 0.4
            
            y = (np.random.rand(n_samples) < fraud_probability).astype(int)
            
            # Train the model
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            
        except Exception as e:
            print(f"Error training basic model: {e}")
    
    def detect_fraud(self, transaction_data):
        """Detect potential fraud in transaction data"""
        try:
            # Extract features from transaction data
            features = self._extract_transaction_features(transaction_data)
            
            # Prepare features for model
            feature_array = np.array([features]).reshape(1, -1)
            feature_array_scaled = self.scaler.transform(feature_array)
            
            # Get fraud probability
            fraud_probability = self.model.predict_proba(feature_array_scaled)[0][1]
            is_fraud = fraud_probability > 0.5
            
            # Generate risk factors
            risk_factors = self._analyze_risk_factors(transaction_data, features)
            
            return {
                'is_fraud': bool(is_fraud),
                'fraud_probability': float(fraud_probability),
                'risk_level': self._get_risk_level(fraud_probability),
                'risk_factors': risk_factors,
                'recommendations': self._get_fraud_recommendations(fraud_probability, risk_factors)
            }
            
        except Exception as e:
            raise Exception(f"Error in fraud detection: {str(e)}")
    
    def _extract_transaction_features(self, transaction_data):
        """Extract features from transaction data for ML model"""
        amount = float(transaction_data.get('amount', 0))
        time_of_day = int(transaction_data.get('hour', 12))
        merchant_category = self._encode_merchant_category(transaction_data.get('merchant_category', 'retail'))
        location_risk = self._calculate_location_risk(transaction_data.get('location', 'domestic'))
        
        return [amount, time_of_day, merchant_category, location_risk]
    
    def _encode_merchant_category(self, category):
        """Encode merchant category to numeric value"""
        categories = {
            'retail': 1, 'restaurant': 2, 'gas': 3, 'grocery': 4,
            'online': 5, 'atm': 6, 'pharmacy': 7, 'entertainment': 8,
            'travel': 9, 'other': 10
        }
        return categories.get(category.lower(), 10)
    
    def _calculate_location_risk(self, location):
        """Calculate location-based risk score"""
        risk_scores = {
            'domestic': 1, 'canada': 2, 'europe': 2, 'asia': 3,
            'south_america': 4, 'africa': 4, 'unknown': 5
        }
        return risk_scores.get(location.lower(), 5)
    
    def _analyze_risk_factors(self, transaction_data, features):
        """Analyze specific risk factors in the transaction"""
        risk_factors = []
        
        amount, time_of_day, merchant_category, location_risk = features
        
        # High amount risk
        if amount > 5000:
            risk_factors.append({
                'factor': 'High transaction amount',
                'severity': 'high',
                'description': f'Transaction amount ${amount:,.2f} is unusually high'
            })
        
        # Unusual time risk
        if time_of_day < 6 or time_of_day > 22:
            risk_factors.append({
                'factor': 'Unusual transaction time',
                'severity': 'medium',
                'description': f'Transaction at {time_of_day}:00 is outside normal hours'
            })
        
        # Location risk
        if location_risk > 3:
            risk_factors.append({
                'factor': 'High-risk location',
                'severity': 'high',
                'description': 'Transaction from high-risk geographical location'
            })
        
        # Merchant category risk
        if merchant_category in [5, 6]:  # Online or ATM
            risk_factors.append({
                'factor': 'High-risk merchant category',
                'severity': 'medium',
                'description': 'Transaction type has higher fraud risk'
            })
        
        return risk_factors
    
    def _get_risk_level(self, fraud_probability):
        """Determine risk level based on fraud probability"""
        if fraud_probability < 0.3:
            return 'Low'
        elif fraud_probability < 0.7:
            return 'Medium'
        else:
            return 'High'
    
    def _get_fraud_recommendations(self, fraud_probability, risk_factors):
        """Generate recommendations based on fraud analysis"""
        recommendations = []
        
        if fraud_probability > 0.7:
            recommendations.append({
                'action': 'Block transaction',
                'priority': 'critical',
                'description': 'High fraud probability detected - immediate action required'
            })
        elif fraud_probability > 0.5:
            recommendations.append({
                'action': 'Manual review',
                'priority': 'high',
                'description': 'Transaction requires manual verification'
            })
        elif fraud_probability > 0.3:
            recommendations.append({
                'action': 'Monitor closely',
                'priority': 'medium',
                'description': 'Monitor account for additional suspicious activity'
            })
        else:
            recommendations.append({
                'action': 'Approve',
                'priority': 'low',
                'description': 'Transaction appears legitimate'
            })
        
        # Add specific recommendations based on risk factors
        for factor in risk_factors:
            if factor['factor'] == 'High transaction amount':
                recommendations.append({
                    'action': 'Verify with customer',
                    'priority': 'high',
                    'description': 'Contact customer to verify large transaction'
                })
        
        return recommendations
    
    def analyze_patterns(self, transaction_history):
        """Analyze transaction patterns for anomalies"""
        try:
            transactions = transaction_history.get('transactions', [])
            
            if not transactions:
                return {'error': 'No transaction history provided'}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(transactions)
            
            # Analyze patterns
            patterns = {
                'velocity_analysis': self._analyze_velocity(df),
                'amount_analysis': self._analyze_amounts(df),
                'time_analysis': self._analyze_timing(df),
                'location_analysis': self._analyze_locations(df),
                'anomaly_score': self._calculate_anomaly_score(df)
            }
            
            return patterns
            
        except Exception as e:
            raise Exception(f"Error analyzing patterns: {str(e)}")
    
    def _analyze_velocity(self, df):
        """Analyze transaction velocity"""
        if len(df) < 2:
            return {'status': 'insufficient_data'}
        
        # Calculate transactions per day
        df['date'] = pd.to_datetime(df['timestamp'])
        daily_counts = df.groupby(df['date'].dt.date).size()
        
        avg_daily = daily_counts.mean()
        max_daily = daily_counts.max()
        
        velocity_risk = 'low'
        if max_daily > avg_daily * 3:
            velocity_risk = 'high'
        elif max_daily > avg_daily * 2:
            velocity_risk = 'medium'
        
        return {
            'avg_daily_transactions': avg_daily,
            'max_daily_transactions': max_daily,
            'velocity_risk': velocity_risk
        }
    
    def _analyze_amounts(self, df):
        """Analyze transaction amounts for anomalies"""
        amounts = df['amount'].astype(float)
        
        mean_amount = amounts.mean()
        std_amount = amounts.std()
        
        # Find outliers (amounts > 2 standard deviations from mean)
        outliers = amounts[abs(amounts - mean_amount) > 2 * std_amount]
        
        return {
            'mean_amount': mean_amount,
            'std_amount': std_amount,
            'outlier_count': len(outliers),
            'outlier_amounts': outliers.tolist()
        }
    
    def _analyze_timing(self, df):
        """Analyze transaction timing patterns"""
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        # Find unusual hours (before 6 AM or after 10 PM)
        unusual_hours = df[(df['hour'] < 6) | (df['hour'] > 22)]
        
        return {
            'unusual_hour_count': len(unusual_hours),
            'unusual_hour_percentage': len(unusual_hours) / len(df) * 100
        }
    
    def _analyze_locations(self, df):
        """Analyze transaction locations"""
        location_counts = df['location'].value_counts() if 'location' in df.columns else {}
        
        return {
            'unique_locations': len(location_counts),
            'location_distribution': location_counts.to_dict() if len(location_counts) > 0 else {}
        }
    
    def _calculate_anomaly_score(self, df):
        """Calculate overall anomaly score"""
        score = 0
        
        # Velocity score
        daily_counts = df.groupby(pd.to_datetime(df['timestamp']).dt.date).size()
        if daily_counts.max() > daily_counts.mean() * 3:
            score += 30
        
        # Amount score
        amounts = df['amount'].astype(float)
        outliers = amounts[abs(amounts - amounts.mean()) > 2 * amounts.std()]
        score += min(len(outliers) * 10, 40)
        
        # Timing score
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        unusual_hours = df[(df['hour'] < 6) | (df['hour'] > 22)]
        score += min(len(unusual_hours) * 5, 30)
        
        return min(score, 100)  # Cap at 100
    
    def get_security_recommendations(self, user_data):
        """Generate security recommendations based on user profile"""
        try:
            recommendations = []
            
            # Check account security features
            has_2fa = user_data.get('has_2fa', False)
            if not has_2fa:
                recommendations.append({
                    'type': 'security_enhancement',
                    'priority': 'high',
                    'recommendation': 'Enable two-factor authentication',
                    'description': 'Add an extra layer of security to your account'
                })
            
            # Check transaction monitoring
            has_alerts = user_data.get('has_transaction_alerts', False)
            if not has_alerts:
                recommendations.append({
                    'type': 'monitoring',
                    'priority': 'medium',
                    'recommendation': 'Enable transaction alerts',
                    'description': 'Get notified of all account activity'
                })
            
            # Check recent activity
            recent_activity = user_data.get('recent_suspicious_activity', False)
            if recent_activity:
                recommendations.append({
                    'type': 'immediate_action',
                    'priority': 'critical',
                    'recommendation': 'Review recent transactions',
                    'description': 'Verify all recent account activity'
                })
            
            # Password security
            last_password_change = user_data.get('last_password_change_days', 365)
            if last_password_change > 90:
                recommendations.append({
                    'type': 'account_security',
                    'priority': 'medium',
                    'recommendation': 'Update password',
                    'description': 'Change password regularly for better security'
                })
            
            return {
                'security_score': self._calculate_security_score(user_data),
                'recommendations': recommendations
            }
            
        except Exception as e:
            raise Exception(f"Error generating security recommendations: {str(e)}")
    
    def _calculate_security_score(self, user_data):
        """Calculate security score based on user profile"""
        score = 0
        
        if user_data.get('has_2fa', False):
            score += 30
        
        if user_data.get('has_transaction_alerts', False):
            score += 20
        
        if not user_data.get('recent_suspicious_activity', False):
            score += 25
        
        last_password_change = user_data.get('last_password_change_days', 365)
        if last_password_change <= 30:
            score += 25
        elif last_password_change <= 90:
            score += 15
        
        return min(score, 100)