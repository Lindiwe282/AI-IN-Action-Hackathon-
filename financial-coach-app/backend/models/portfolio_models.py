from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialize SQLAlchemy with no app yet
db = SQLAlchemy()

# User model to store user information
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(500))
    login_type = db.Column(db.String(50))  # 'google', 'github', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)
    wallets = db.relationship('Wallet', backref='user', lazy=True)
    session = db.relationship('UserSession', backref='user', lazy=True, uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'picture': self.picture,
            'login_type': self.login_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Portfolio model to store portfolio information
class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    portfolio_type = db.Column(db.String(50))  # 'static', 'tactical', etc.
    allocation = db.Column(db.Text)  # JSON string containing allocation data
    analysis = db.Column(db.Text)  # JSON string containing analysis data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stocks = db.relationship('PortfolioStock', backref='portfolio', lazy=True, cascade="all, delete-orphan")
    
    def set_allocation(self, allocation_data):
        self.allocation = json.dumps(allocation_data)
        
    def get_allocation(self):
        return json.loads(self.allocation) if self.allocation else []
    
    def set_analysis(self, analysis_data):
        self.analysis = json.dumps(analysis_data)
        
    def get_analysis(self):
        return json.loads(self.analysis) if self.analysis else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'portfolio_type': self.portfolio_type,
            'allocation': self.get_allocation(),
            'analysis': self.get_analysis(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'stocks': [stock.to_dict() for stock in self.stocks]
        }

# PortfolioStock model to store stocks in portfolios
class PortfolioStock(db.Model):
    __tablename__ = 'portfolio_stocks'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100))
    weight = db.Column(db.Float)
    last_price = db.Column(db.Float)
    price_updated_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'ticker': self.ticker,
            'name': self.name,
            'weight': self.weight,
            'last_price': self.last_price,
            'price_updated_at': self.price_updated_at.isoformat() if self.price_updated_at else None
        }

# Wallet model to store wallet information
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wallet_type = db.Column(db.String(50), default='investment')  # 'investment', 'tactical', etc.
    balance = db.Column(db.Float, default=350.0)
    cumulative_gain = db.Column(db.Float, default=0.0)  # Track cumulative gains/losses
    last_gain_update = db.Column(db.Date)  # Track last date gains were calculated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('WalletTransaction', backref='wallet', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'wallet_type': self.wallet_type,
            'balance': self.balance,
            'cumulative_gain': self.cumulative_gain,
            'last_gain_update': self.last_gain_update.isoformat() if self.last_gain_update else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# WalletTransaction model to store wallet transactions
class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50))  # 'deposit', 'withdrawal', 'gain', 'loss'
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# MarketData model to store cached market data
class MarketData(db.Model):
    __tablename__ = 'market_data'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float)
    change = db.Column(db.Float)
    change_percent = db.Column(db.Float)
    data = db.Column(db.Text)  # JSON string containing additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_data(self, data):
        self.data = json.dumps(data)
        
    def get_data(self):
        return json.loads(self.data) if self.data else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'price': self.price,
            'change': self.change,
            'change_percent': self.change_percent,
            'data': self.get_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# PortfolioPerformance model to track portfolio performance
class PortfolioPerformance(db.Model):
    __tablename__ = 'portfolio_performance'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float)
    change = db.Column(db.Float)
    change_percent = db.Column(db.Float)
    benchmark_value = db.Column(db.Float)  # S&P 500 value for the day
    benchmark_change = db.Column(db.Float)
    benchmark_change_percent = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'date': self.date.isoformat() if self.date else None,
            'value': self.value,
            'change': self.change,
            'change_percent': self.change_percent,
            'benchmark_value': self.benchmark_value,
            'benchmark_change': self.benchmark_change,
            'benchmark_change_percent': self.benchmark_change_percent
        }

# UserSession model to persist user session state across login/logout
class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Portfolio state
    final_portfolio = db.Column(db.Text)  # JSON string of portfolio weights
    final_portfolio_analysis = db.Column(db.Text)  # JSON string of analysis
    final_market_analysis = db.Column(db.Text)  # JSON string of market analysis
    
    # Tactical analysis state
    tactical_analysis_results = db.Column(db.Text)  # JSON string
    tactical_portfolio = db.Column(db.Text)  # JSON string
    tactical_capital = db.Column(db.Float, default=10000.0)
    
    # Investment state
    investment_capital = db.Column(db.Float, default=350.0)
    cumulative_gain = db.Column(db.Float, default=0.0)
    last_gain_update = db.Column(db.String(50))  # Date string for tracking daily updates
    
    # Legacy session data field (for backwards compatibility)
    session_data = db.Column(db.Text)  # JSON string containing additional session state
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_session_data(self, data):
        self.session_data = json.dumps(data)
        
    def get_session_data(self):
        return json.loads(self.session_data) if self.session_data else {}
    
    def set_final_portfolio(self, portfolio_data):
        """Set final portfolio as JSON string"""
        self.final_portfolio = json.dumps(portfolio_data) if portfolio_data else None
    
    def get_final_portfolio(self):
        """Get final portfolio as Python object"""
        return json.loads(self.final_portfolio) if self.final_portfolio else []
    
    def set_final_portfolio_analysis(self, analysis_data):
        """Set final portfolio analysis as JSON string"""
        self.final_portfolio_analysis = json.dumps(analysis_data) if analysis_data else None
    
    def get_final_portfolio_analysis(self):
        """Get final portfolio analysis as Python object"""
        return json.loads(self.final_portfolio_analysis) if self.final_portfolio_analysis else {}
    
    def set_final_market_analysis(self, market_data):
        """Set final market analysis as JSON string"""
        self.final_market_analysis = json.dumps(market_data) if market_data else None
    
    def get_final_market_analysis(self):
        """Get final market analysis as Python object"""
        return json.loads(self.final_market_analysis) if self.final_market_analysis else {}
    
    def set_tactical_analysis_results(self, results_data):
        """Set tactical analysis results as JSON string"""
        self.tactical_analysis_results = json.dumps(results_data) if results_data else None
    
    def get_tactical_analysis_results(self):
        """Get tactical analysis results as Python object"""
        return json.loads(self.tactical_analysis_results) if self.tactical_analysis_results else []
    
    def set_tactical_portfolio(self, portfolio_data):
        """Set tactical portfolio as JSON string"""
        self.tactical_portfolio = json.dumps(portfolio_data) if portfolio_data else None
    
    def get_tactical_portfolio(self):
        """Get tactical portfolio as Python object"""
        return json.loads(self.tactical_portfolio) if self.tactical_portfolio else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'final_portfolio': self.get_final_portfolio(),
            'final_portfolio_analysis': self.get_final_portfolio_analysis(),
            'final_market_analysis': self.get_final_market_analysis(),
            'tactical_analysis_results': self.get_tactical_analysis_results(),
            'tactical_portfolio': self.get_tactical_portfolio(),
            'tactical_capital': self.tactical_capital,
            'investment_capital': self.investment_capital,
            'cumulative_gain': self.cumulative_gain,
            'last_gain_update': self.last_gain_update,
            'session_data': self.get_session_data(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# New Models for Derivatives Trading
class FuturesContract(db.Model):
    __tablename__ = 'futures_contracts'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    exchange = db.Column(db.String(50), nullable=False)
    contract_size = db.Column(db.Float, nullable=False)
    tick_size = db.Column(db.Float, nullable=False)
    margin_requirement = db.Column(db.Float, default=1000.0)
    sector = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'exchange': self.exchange,
            'contractSize': self.contract_size,
            'tickSize': self.tick_size,
            'marginRequirement': self.margin_requirement,
            'sector': self.sector,
            'description': self.description
        }

class DerivativesAnalysis(db.Model):
    __tablename__ = 'derivatives_analysis'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contract_symbol = db.Column(db.String(10), nullable=False)
    strategy_type = db.Column(db.String(50), default='long_strap')
    initial_capital = db.Column(db.Float, nullable=False)
    final_capital = db.Column(db.Float, nullable=False)
    total_return = db.Column(db.Float, nullable=False)
    annualized_return = db.Column(db.Float, nullable=False)
    sharpe_ratio = db.Column(db.Float)
    max_drawdown = db.Column(db.Float)
    var_95 = db.Column(db.Float)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    analysis_data = db.Column(db.JSON)  # Store daily/yearly returns
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('derivatives_analyses', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'contractSymbol': self.contract_symbol,
            'strategyType': self.strategy_type,
            'initialCapital': self.initial_capital,
            'finalCapital': self.final_capital,
            'totalReturn': self.total_return,
            'annualizedReturn': self.annualized_return,
            'sharpeRatio': self.sharpe_ratio,
            'maxDrawdown': self.max_drawdown,
            'var95': self.var_95,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'analysisData': self.analysis_data,
            'createdAt': self.created_at.isoformat()
        }

class DerivativesPriceHistory(db.Model):
    __tablename__ = 'derivatives_price_history'
    id = db.Column(db.Integer, primary_key=True)
    contract_symbol = db.Column(db.String(10), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, default=0)
    
    # Unique constraint on symbol and date
    __table_args__ = (db.UniqueConstraint('contract_symbol', 'date'),)
    
    def to_dict(self):
        return {
            'symbol': self.contract_symbol,
            'date': self.date.isoformat(),
            'open': self.open_price,
            'high': self.high_price,
            'low': self.low_price,
            'close': self.close_price,
            'volume': self.volume
        }

# Stock model for basic stock information
class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    detail = db.Column(db.String(500))
    
    def stock_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'ticker': self.ticker,
            'detail': self.detail
        }