import math

class LoanCalculator:
    """Financial calculator for loan calculations"""
    
    def calculate_payment(self, principal, rate, term):
        """
        Calculate monthly loan payment
        
        Args:
            principal (float): Loan amount
            rate (float): Monthly interest rate (as decimal, e.g., 0.05/12 for 5% APR)
            term (int): Number of months
        
        Returns:
            dict: Payment details
        """
        if rate == 0:
            monthly_payment = principal / term
        else:
            monthly_payment = principal * (rate * (1 + rate)**term) / ((1 + rate)**term - 1)
        
        total_payment = monthly_payment * term
        total_interest = total_payment - principal
        
        return {
            'monthly_payment': round(monthly_payment, 2),
            'total_payment': round(total_payment, 2),
            'total_interest': round(total_interest, 2),
            'principal': principal,
            'interest_rate': rate * 12 * 100,  # Convert to annual percentage
            'term_months': term
        }
    
    def calculate_affordable_loan(self, monthly_payment, rate, term):
        """
        Calculate maximum affordable loan amount
        
        Args:
            monthly_payment (float): Maximum monthly payment
            rate (float): Monthly interest rate
            term (int): Number of months
        
        Returns:
            float: Maximum loan amount
        """
        if rate == 0:
            return monthly_payment * term
        
        return monthly_payment * ((1 + rate)**term - 1) / (rate * (1 + rate)**term)
    
    def calculate_payoff_time(self, balance, payment, rate):
        """
        Calculate time to pay off a loan
        
        Args:
            balance (float): Current loan balance
            payment (float): Monthly payment
            rate (float): Monthly interest rate
        
        Returns:
            dict: Payoff details
        """
        if payment <= balance * rate:
            return {
                'months': float('inf'),
                'message': 'Payment too low - will never pay off'
            }
        
        if rate == 0:
            months = balance / payment
        else:
            months = -math.log(1 - (balance * rate) / payment) / math.log(1 + rate)
        
        years = months / 12
        
        return {
            'months': round(months, 1),
            'years': round(years, 1),
            'total_payments': round(payment * months, 2),
            'total_interest': round(payment * months - balance, 2)
        }
    
    def calculate_amortization_schedule(self, principal, rate, term, num_payments=None):
        """
        Generate amortization schedule
        
        Args:
            principal (float): Loan amount
            rate (float): Monthly interest rate
            term (int): Number of months
            num_payments (int): Number of payments to show (default: all)
        
        Returns:
            list: Amortization schedule
        """
        if num_payments is None:
            num_payments = term
        
        monthly_payment = self.calculate_payment(principal, rate, term)['monthly_payment']
        
        schedule = []
        remaining_balance = principal
        
        for payment_num in range(1, min(num_payments + 1, term + 1)):
            interest_payment = remaining_balance * rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            schedule.append({
                'payment_number': payment_num,
                'payment_amount': round(monthly_payment, 2),
                'principal_payment': round(principal_payment, 2),
                'interest_payment': round(interest_payment, 2),
                'remaining_balance': round(max(0, remaining_balance), 2)
            })
            
            if remaining_balance <= 0:
                break
        
        return schedule
    
    def calculate_extra_payment_savings(self, principal, rate, term, extra_payment):
        """
        Calculate savings from extra payments
        
        Args:
            principal (float): Loan amount
            rate (float): Monthly interest rate
            term (int): Number of months
            extra_payment (float): Additional monthly payment
        
        Returns:
            dict: Savings analysis
        """
        # Standard loan
        standard = self.calculate_payment(principal, rate, term)
        
        # Loan with extra payments
        enhanced_payment = standard['monthly_payment'] + extra_payment
        enhanced_payoff = self.calculate_payoff_time(principal, enhanced_payment, rate)
        
        # Calculate savings
        standard_total = standard['total_payment']
        enhanced_total = enhanced_payoff['total_payments']
        interest_savings = standard_total - enhanced_total
        time_savings_months = term - enhanced_payoff['months']
        
        return {
            'original_payment': standard['monthly_payment'],
            'new_payment': enhanced_payment,
            'extra_payment': extra_payment,
            'original_term_months': term,
            'new_term_months': enhanced_payoff['months'],
            'time_savings_months': round(time_savings_months, 1),
            'time_savings_years': round(time_savings_months / 12, 1),
            'interest_savings': round(interest_savings, 2),
            'original_total_interest': standard['total_interest'],
            'new_total_interest': enhanced_payoff['total_interest']
        }
    
    def calculate_refinance_analysis(self, current_balance, current_rate, current_term_remaining, 
                                   new_rate, new_term, closing_costs=0):
        """
        Analyze refinancing benefits
        
        Args:
            current_balance (float): Current loan balance
            current_rate (float): Current monthly interest rate
            current_term_remaining (int): Months remaining on current loan
            new_rate (float): New monthly interest rate
            new_term (int): New loan term in months
            closing_costs (float): Refinancing costs
        
        Returns:
            dict: Refinancing analysis
        """
        # Current loan payments
        current_payment = self.calculate_payment(current_balance, current_rate, current_term_remaining)
        
        # New loan payments
        new_payment = self.calculate_payment(current_balance + closing_costs, new_rate, new_term)
        
        # Calculate break-even point
        monthly_savings = current_payment['monthly_payment'] - new_payment['monthly_payment']
        
        if monthly_savings <= 0:
            break_even_months = float('inf')
        else:
            break_even_months = closing_costs / monthly_savings
        
        # Total cost comparison
        current_total_cost = current_payment['monthly_payment'] * current_term_remaining
        new_total_cost = new_payment['total_payment']
        net_savings = current_total_cost - new_total_cost
        
        return {
            'current_monthly_payment': current_payment['monthly_payment'],
            'new_monthly_payment': new_payment['monthly_payment'],
            'monthly_savings': round(monthly_savings, 2),
            'closing_costs': closing_costs,
            'break_even_months': round(break_even_months, 1) if break_even_months != float('inf') else 'Never',
            'break_even_years': round(break_even_months / 12, 1) if break_even_months != float('inf') else 'Never',
            'current_total_remaining_payments': round(current_total_cost, 2),
            'new_total_payments': round(new_total_cost, 2),
            'net_savings': round(net_savings, 2),
            'recommended': net_savings > 0 and break_even_months < 60  # Recommend if positive savings and break-even < 5 years
        }


class SavingsCalculator:
    """Calculator for savings and investment scenarios"""
    
    def calculate_future_value(self, present_value, monthly_contribution, annual_rate, years):
        """
        Calculate future value of savings with regular contributions
        
        Args:
            present_value (float): Initial amount
            monthly_contribution (float): Monthly contribution
            annual_rate (float): Annual interest rate (as decimal)
            years (int): Number of years
        
        Returns:
            dict: Future value calculation
        """
        monthly_rate = annual_rate / 12
        months = years * 12
        
        # Future value of present amount
        fv_present = present_value * (1 + monthly_rate) ** months
        
        # Future value of annuity (monthly contributions)
        if monthly_rate == 0:
            fv_contributions = monthly_contribution * months
        else:
            fv_contributions = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        
        total_future_value = fv_present + fv_contributions
        total_contributions = present_value + (monthly_contribution * months)
        interest_earned = total_future_value - total_contributions
        
        return {
            'future_value': round(total_future_value, 2),
            'total_contributions': round(total_contributions, 2),
            'interest_earned': round(interest_earned, 2),
            'initial_amount': present_value,
            'monthly_contribution': monthly_contribution,
            'annual_rate': annual_rate * 100,
            'years': years
        }
    
    def calculate_retirement_needs(self, current_age, retirement_age, current_income, 
                                 income_replacement_ratio=0.8, inflation_rate=0.03):
        """
        Calculate retirement savings needs
        
        Args:
            current_age (int): Current age
            retirement_age (int): Planned retirement age
            current_income (float): Current annual income
            income_replacement_ratio (float): Percentage of income needed in retirement
            inflation_rate (float): Expected inflation rate
        
        Returns:
            dict: Retirement calculation
        """
        years_to_retirement = retirement_age - current_age
        retirement_years = 85 - retirement_age  # Assume living to 85
        
        # Calculate income needed in retirement (adjusted for inflation)
        annual_income_needed = current_income * income_replacement_ratio
        future_annual_income_needed = annual_income_needed * (1 + inflation_rate) ** years_to_retirement
        
        # Calculate total retirement savings needed
        # Using present value of annuity formula
        discount_rate = 0.04  # Assumed withdrawal rate in retirement
        real_return_rate = discount_rate - inflation_rate
        
        if real_return_rate <= 0:
            total_needed = future_annual_income_needed * retirement_years
        else:
            total_needed = future_annual_income_needed * (1 - (1 + real_return_rate) ** -retirement_years) / real_return_rate
        
        # Calculate required monthly savings
        savings_rate = 0.07  # Assumed investment return during accumulation
        monthly_savings_rate = savings_rate / 12
        months_to_retirement = years_to_retirement * 12
        
        if monthly_savings_rate == 0:
            required_monthly_savings = total_needed / months_to_retirement
        else:
            required_monthly_savings = total_needed * monthly_savings_rate / ((1 + monthly_savings_rate) ** months_to_retirement - 1)
        
        return {
            'years_to_retirement': years_to_retirement,
            'current_annual_income': current_income,
            'needed_annual_income_retirement': round(future_annual_income_needed, 2),
            'total_retirement_savings_needed': round(total_needed, 2),
            'required_monthly_savings': round(required_monthly_savings, 2),
            'required_annual_savings': round(required_monthly_savings * 12, 2),
            'savings_rate_percentage': round((required_monthly_savings * 12 / current_income) * 100, 1)
        }
    
    def calculate_emergency_fund_timeline(self, target_amount, monthly_contribution, current_savings=0):
        """
        Calculate timeline to build emergency fund
        
        Args:
            target_amount (float): Target emergency fund amount
            monthly_contribution (float): Monthly savings amount
            current_savings (float): Current savings amount
        
        Returns:
            dict: Emergency fund timeline
        """
        amount_needed = target_amount - current_savings
        
        if monthly_contribution <= 0:
            return {
                'error': 'Monthly contribution must be greater than 0'
            }
        
        months_needed = amount_needed / monthly_contribution
        years_needed = months_needed / 12
        
        # Generate milestone timeline
        milestones = []
        milestone_percentages = [25, 50, 75, 100]
        
        for percentage in milestone_percentages:
            milestone_amount = target_amount * (percentage / 100)
            if milestone_amount > current_savings:
                months_to_milestone = (milestone_amount - current_savings) / monthly_contribution
                milestones.append({
                    'percentage': percentage,
                    'amount': round(milestone_amount, 2),
                    'months': round(months_to_milestone, 1),
                    'years': round(months_to_milestone / 12, 1)
                })
        
        return {
            'target_amount': target_amount,
            'current_savings': current_savings,
            'amount_needed': round(amount_needed, 2),
            'monthly_contribution': monthly_contribution,
            'months_needed': round(months_needed, 1),
            'years_needed': round(years_needed, 1),
            'milestones': milestones
        }