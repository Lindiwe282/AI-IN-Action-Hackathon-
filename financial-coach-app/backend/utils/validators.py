import re
from typing import Dict, List, Any, Union

class InputValidator:
    """Validator class for API input validation"""
    
    @staticmethod
    def validate_planner_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
        """Validate financial planner input data"""
        errors = []
        
        # Required fields
        required_fields = ['monthly_income', 'monthly_expenses']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], (int, float)) or data[field] < 0:
                errors.append(f"{field} must be a non-negative number")
        
        # Optional but validated fields
        if 'age' in data:
            if not isinstance(data['age'], int) or data['age'] < 16 or data['age'] > 100:
                errors.append("Age must be between 16 and 100")
        
        if 'dependents' in data:
            if not isinstance(data['dependents'], int) or data['dependents'] < 0:
                errors.append("Dependents must be a non-negative integer")
        
        if 'risk_tolerance' in data:
            valid_risk_levels = ['low', 'medium', 'high']
            if data['risk_tolerance'].lower() not in valid_risk_levels:
                errors.append(f"Risk tolerance must be one of: {', '.join(valid_risk_levels)}")
        
        if 'current_savings' in data:
            if not isinstance(data['current_savings'], (int, float)) or data['current_savings'] < 0:
                errors.append("Current savings must be a non-negative number")
        
        if 'total_debt' in data:
            if not isinstance(data['total_debt'], (int, float)) or data['total_debt'] < 0:
                errors.append("Total debt must be a non-negative number")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_investment_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
        """Validate investment input data"""
        errors = []
        
        # Required fields
        if 'investment_amount' not in data:
            errors.append("Missing required field: investment_amount")
        elif not isinstance(data['investment_amount'], (int, float)) or data['investment_amount'] <= 0:
            errors.append("Investment amount must be a positive number")
        
        # Optional but validated fields
        if 'age' in data:
            if not isinstance(data['age'], int) or data['age'] < 16 or data['age'] > 100:
                errors.append("Age must be between 16 and 100")
        
        if 'risk_tolerance' in data:
            valid_risk_levels = ['low', 'medium', 'high']
            if data['risk_tolerance'].lower() not in valid_risk_levels:
                errors.append(f"Risk tolerance must be one of: {', '.join(valid_risk_levels)}")
        
        if 'investment_timeline' in data:
            if not isinstance(data['investment_timeline'], int) or data['investment_timeline'] < 1:
                errors.append("Investment timeline must be at least 1 year")
        
        if 'investment_experience' in data:
            valid_experience = ['beginner', 'intermediate', 'expert']
            if data['investment_experience'].lower() not in valid_experience:
                errors.append(f"Investment experience must be one of: {', '.join(valid_experience)}")
        
        if 'monthly_income' in data:
            if not isinstance(data['monthly_income'], (int, float)) or data['monthly_income'] < 0:
                errors.append("Monthly income must be a non-negative number")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_loan_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
        """Validate loan input data"""
        errors = []
        
        # Required fields for affordability check
        required_fields = ['monthly_income', 'loan_amount']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], (int, float)) or data[field] <= 0:
                errors.append(f"{field} must be a positive number")
        
        # Interest rate validation
        if 'interest_rate' in data:
            if not isinstance(data['interest_rate'], (int, float)) or data['interest_rate'] < 0 or data['interest_rate'] > 50:
                errors.append("Interest rate must be between 0% and 50%")
        
        # Loan term validation
        if 'loan_term_months' in data:
            if not isinstance(data['loan_term_months'], int) or data['loan_term_months'] < 1 or data['loan_term_months'] > 480:
                errors.append("Loan term must be between 1 and 480 months (40 years)")
        
        # Credit score validation
        if 'credit_score' in data:
            if not isinstance(data['credit_score'], int) or data['credit_score'] < 300 or data['credit_score'] > 850:
                errors.append("Credit score must be between 300 and 850")
        
        # Employment years validation
        if 'employment_years' in data:
            if not isinstance(data['employment_years'], (int, float)) or data['employment_years'] < 0:
                errors.append("Employment years must be a non-negative number")
        
        # Down payment validation
        if 'down_payment' in data:
            if not isinstance(data['down_payment'], (int, float)) or data['down_payment'] < 0:
                errors.append("Down payment must be a non-negative number")
        
        # Monthly debt payments validation
        if 'monthly_debt_payments' in data:
            if not isinstance(data['monthly_debt_payments'], (int, float)) or data['monthly_debt_payments'] < 0:
                errors.append("Monthly debt payments must be a non-negative number")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_fraud_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
        """Validate fraud detection input data"""
        errors = []
        
        # Required fields
        if 'amount' not in data:
            errors.append("Missing required field: amount")
        elif not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
            errors.append("Transaction amount must be a positive number")
        
        # Transaction time validation
        if 'hour' in data:
            if not isinstance(data['hour'], int) or data['hour'] < 0 or data['hour'] > 23:
                errors.append("Hour must be between 0 and 23")
        
        # Merchant category validation
        if 'merchant_category' in data:
            valid_categories = ['retail', 'restaurant', 'gas', 'grocery', 'online', 'atm', 
                              'pharmacy', 'entertainment', 'travel', 'other']
            if data['merchant_category'].lower() not in valid_categories:
                errors.append(f"Merchant category must be one of: {', '.join(valid_categories)}")
        
        # Location validation
        if 'location' in data:
            valid_locations = ['domestic', 'canada', 'europe', 'asia', 'south_america', 'africa', 'unknown']
            if data['location'].lower() not in valid_locations:
                errors.append(f"Location must be one of: {', '.join(valid_locations)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it's a valid US phone number (10 digits) or international (7-15 digits)
        return len(digits_only) >= 7 and len(digits_only) <= 15
    
    @staticmethod
    def validate_currency_amount(amount: Union[str, int, float]) -> Dict[str, Union[bool, float, str]]:
        """Validate and normalize currency amount"""
        if isinstance(amount, str):
            # Remove currency symbols and commas
            cleaned_amount = re.sub(r'[$,\s]', '', amount)
            try:
                amount = float(cleaned_amount)
            except ValueError:
                return {
                    'valid': False,
                    'error': 'Invalid currency format'
                }
        
        if not isinstance(amount, (int, float)):
            return {
                'valid': False,
                'error': 'Amount must be a number'
            }
        
        if amount < 0:
            return {
                'valid': False,
                'error': 'Amount cannot be negative'
            }
        
        if amount > 1000000000:  # 1 billion limit
            return {
                'valid': False,
                'error': 'Amount exceeds maximum limit'
            }
        
        return {
            'valid': True,
            'amount': round(amount, 2)
        }
    
    @staticmethod
    def validate_percentage(value: Union[str, int, float], min_val: float = 0, max_val: float = 100) -> Dict[str, Union[bool, float, str]]:
        """Validate percentage value"""
        if isinstance(value, str):
            # Remove percentage symbol
            cleaned_value = value.replace('%', '').strip()
            try:
                value = float(cleaned_value)
            except ValueError:
                return {
                    'valid': False,
                    'error': 'Invalid percentage format'
                }
        
        if not isinstance(value, (int, float)):
            return {
                'valid': False,
                'error': 'Percentage must be a number'
            }
        
        if value < min_val or value > max_val:
            return {
                'valid': False,
                'error': f'Percentage must be between {min_val}% and {max_val}%'
            }
        
        return {
            'valid': True,
            'percentage': round(value, 2)
        }
    
    @staticmethod
    def sanitize_string(input_string: str, max_length: int = 255) -> str:
        """Sanitize string input"""
        if not isinstance(input_string, str):
            return ""
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', input_string)
        
        # Limit length
        sanitized = sanitized[:max_length]
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Dict[str, Union[bool, str]]:
        """Validate date range"""
        try:
            from datetime import datetime
            
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start >= end:
                return {
                    'valid': False,
                    'error': 'Start date must be before end date'
                }
            
            # Check if dates are reasonable (not too far in the past or future)
            now = datetime.now()
            if start.year < 1900 or end.year > now.year + 50:
                return {
                    'valid': False,
                    'error': 'Date range is not reasonable'
                }
            
            return {
                'valid': True
            }
            
        except ValueError:
            return {
                'valid': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }


# Convenience functions
def validate_planner_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
    """Convenience function for planner input validation"""
    return InputValidator.validate_planner_input(data)

def validate_investment_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
    """Convenience function for investment input validation"""
    return InputValidator.validate_investment_input(data)

def validate_loan_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
    """Convenience function for loan input validation"""
    return InputValidator.validate_loan_input(data)

def validate_fraud_input(data: Dict[str, Any]) -> Dict[str, Union[bool, List[str]]]:
    """Convenience function for fraud input validation"""
    return InputValidator.validate_fraud_input(data)