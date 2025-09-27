from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize database
db = SQLAlchemy()

def init_app(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return db

def get_db_connection():
    """Get database connection"""
    return db

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile information
    monthly_income = db.Column(db.Float, default=0.0)
    monthly_expenses = db.Column(db.Float, default=0.0)
    current_savings = db.Column(db.Float, default=0.0)
    total_debt = db.Column(db.Float, default=0.0)
    dependents = db.Column(db.Integer, default=0)
    risk_tolerance = db.Column(db.String(20), default='medium')
    investment_experience = db.Column(db.String(20), default='beginner')
    
    # Relationships
    financial_plans = db.relationship('FinancialPlan', backref='user', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    investments = db.relationship('Investment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'monthly_income': self.monthly_income,
            'monthly_expenses': self.monthly_expenses,
            'current_savings': self.current_savings,
            'total_debt': self.total_debt,
            'dependents': self.dependents,
            'risk_tolerance': self.risk_tolerance,
            'investment_experience': self.investment_experience,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FinancialPlan(db.Model):
    """Financial plan model"""
    __tablename__ = 'financial_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)  # retirement, emergency, investment, etc.
    
    # Plan details (stored as JSON)
    budget_allocation = db.Column(db.JSON)
    savings_goals = db.Column(db.JSON)
    recommendations = db.Column(db.JSON)
    risk_assessment = db.Column(db.JSON)
    timeline = db.Column(db.JSON)
    
    # Plan status
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    target_amount = db.Column(db.Float)
    current_progress = db.Column(db.Float, default=0.0)
    target_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FinancialPlan {self.plan_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'plan_type': self.plan_type,
            'budget_allocation': self.budget_allocation,
            'savings_goals': self.savings_goals,
            'recommendations': self.recommendations,
            'risk_assessment': self.risk_assessment,
            'timeline': self.timeline,
            'status': self.status,
            'target_amount': self.target_amount,
            'current_progress': self.current_progress,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Transaction(db.Model):
    """Transaction model for fraud detection and analysis"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Transaction details
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # debit, credit, transfer
    category = db.Column(db.String(50))  # food, transportation, entertainment, etc.
    merchant = db.Column(db.String(100))
    merchant_category = db.Column(db.String(50))
    
    # Location and timing
    location = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Fraud detection
    is_flagged = db.Column(db.Boolean, default=False)
    fraud_score = db.Column(db.Float, default=0.0)
    fraud_reasons = db.Column(db.JSON)
    
    # Status
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed, disputed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.id}: ${self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'merchant': self.merchant,
            'merchant_category': self.merchant_category,
            'location': self.location,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_flagged': self.is_flagged,
            'fraud_score': self.fraud_score,
            'fraud_reasons': self.fraud_reasons,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Investment(db.Model):
    """Investment holdings model"""
    __tablename__ = 'investments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Investment details
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    investment_type = db.Column(db.String(50), nullable=False)  # stock, bond, etf, mutual_fund
    sector = db.Column(db.String(50))
    
    # Holdings
    shares = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float)
    current_value = db.Column(db.Float)
    
    # Performance
    total_return = db.Column(db.Float, default=0.0)
    ytd_return = db.Column(db.Float, default=0.0)
    
    # Dates
    purchase_date = db.Column(db.Date, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Investment {self.symbol}: {self.shares} shares>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'name': self.name,
            'investment_type': self.investment_type,
            'sector': self.sector,
            'shares': self.shares,
            'purchase_price': self.purchase_price,
            'current_price': self.current_price,
            'current_value': self.current_value,
            'total_return': self.total_return,
            'ytd_return': self.ytd_return,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LoanApplication(db.Model):
    """Loan application model"""
    __tablename__ = 'loan_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Loan details
    loan_type = db.Column(db.String(50), nullable=False)  # mortgage, auto, personal, etc.
    loan_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float)
    term_months = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Float)
    
    # Applicant information
    credit_score = db.Column(db.Integer)
    employment_years = db.Column(db.Float)
    down_payment = db.Column(db.Float, default=0.0)
    debt_to_income_ratio = db.Column(db.Float)
    
    # AI analysis results
    affordability_score = db.Column(db.Float)
    approval_likelihood = db.Column(db.String(20))
    ai_recommendations = db.Column(db.JSON)
    risk_factors = db.Column(db.JSON)
    
    # Application status
    status = db.Column(db.String(20), default='draft')  # draft, submitted, approved, denied
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='loan_applications')
    
    def __repr__(self):
        return f'<LoanApplication {self.id}: {self.loan_type} ${self.loan_amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'loan_type': self.loan_type,
            'loan_amount': self.loan_amount,
            'interest_rate': self.interest_rate,
            'term_months': self.term_months,
            'monthly_payment': self.monthly_payment,
            'credit_score': self.credit_score,
            'employment_years': self.employment_years,
            'down_payment': self.down_payment,
            'debt_to_income_ratio': self.debt_to_income_ratio,
            'affordability_score': self.affordability_score,
            'approval_likelihood': self.approval_likelihood,
            'ai_recommendations': self.ai_recommendations,
            'risk_factors': self.risk_factors,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FinancialTip(db.Model):
    """Financial literacy tips model"""
    __tablename__ = 'financial_tips'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # budgeting, saving, investing, debt
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    tags = db.Column(db.JSON)  # Array of tags
    
    # Engagement metrics
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    
    # Status
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FinancialTip {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'views': self.views,
            'likes': self.likes,
            'shares': self.shares,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }