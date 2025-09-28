from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import threading
import time
import logging
import signal
import sys
from dotenv import load_dotenv
from contextlib import contextmanager
import signal

# Optional imports that might not be available
try:
    import numpy as np
    import pandas as pd
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from services.sentiment import SentimentalAnalysis
    from controllers.investment_controller import InvestmentController
    from utils.yfinance_utils import yf_wrapper
    from utils.cache_manager import cached, cache
    from utils.async_handler import run_async, run_cpu_bound, cleanup as async_cleanup
    from utils.rate_limiter import rate_limited, general_api_limiter, yfinance_limiter
    PORTFOLIO_UTILS_AVAILABLE = True
except ImportError as e:
    PORTFOLIO_UTILS_AVAILABLE = False

# Load environment variables from config directory
config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
if os.path.exists(os.path.join(config_dir, 'dev.env')):
    load_dotenv(os.path.join(config_dir, 'dev.env'))
else:
    load_dotenv()  # Fallback to default .env

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress excessive logging from libraries
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)
logging.getLogger('yfinance').setLevel(logging.WARNING)

# Initialize Flask app
app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"]}}, 
     supports_credentials=True, 
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Database configuration with connection pooling
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/financial_coach.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 20
}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Import and initialize the models and database instance
from models.portfolio_models import User, Portfolio, PortfolioStock, Wallet, WalletTransaction, MarketData, PortfolioPerformance, Stock, db

# Initialize the database with the Flask app
db.init_app(app)

# SocketIO configuration with stability improvements
socketio = SocketIO(app, 
                    cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"], 
                    async_mode="threading",
                    logger=False,
                    engineio_logger=False,
                    ping_timeout=60,
                    max_http_buffer_size=1000000,
                    ping_interval=25)

# Initialize database tables
def init_db():
    """Initialize database with proper error handling"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")

# Initialize the analyzers and controllers (import from app_portfolio)
try:
    from app_portfolio import Analyzer, sentiment_analyzer, investment_controller
    logger.info("Successfully imported portfolio components")
except ImportError as e:
    logger.warning(f"Could not import portfolio components: {e}")
    # Create dummy objects to prevent errors
    class DummyAnalyzer:
        is_running = False
        def stock_analysis(self, tickers):
            return {'error': 'Portfolio analyzer not available', 'strategies': [], 'metadata': {'timestamp': '', 'tickers': tickers}}
    
    Analyzer = DummyAnalyzer()
    sentiment_analyzer = None
    investment_controller = None

# Import routes
from routes.planner import planner_bp
from routes.investment import investment_bp
from routes.loan import loan_bp
from routes.literacy import literacy_bp
from routes.fraud import fraud_bp
from routes.hedge import hedge_bp

# Only import portfolio and sentiment routes if they can be imported safely
try:
    from routes.portfolio import portfolio_bp
    from routes.sentiment import sentiment_bp
    PORTFOLIO_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Portfolio routes not available: {e}")
    PORTFOLIO_AVAILABLE = False

# Register blueprints
app.register_blueprint(planner_bp, url_prefix='/api/planner')
app.register_blueprint(investment_bp, url_prefix='/api/investment')
app.register_blueprint(loan_bp, url_prefix='/api/loan')
app.register_blueprint(literacy_bp, url_prefix='/api/literacy')
app.register_blueprint(fraud_bp, url_prefix='/api/fraud')
app.register_blueprint(hedge_bp, url_prefix='/api/hedge')

if PORTFOLIO_AVAILABLE:
    app.register_blueprint(portfolio_bp)  # Already has /api prefix
    app.register_blueprint(sentiment_bp)  # Already has /api/sentiment prefix

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Financial Coach API is running!',
        'version': '1.0.0',
        'port': 5000,
        'frontend_port': 3000
    })

@app.route('/api/health')
def api_health():
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    services = ['planner', 'investment', 'loan', 'literacy', 'fraud', 'hedge']
    if PORTFOLIO_AVAILABLE:
        services.extend(['portfolio', 'sentiment'])
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'services': services,
        'analyzer_running': Analyzer.is_running if hasattr(Analyzer, 'is_running') else False
    })

@app.route('/api/investment/portfolio')
def get_investment_portfolio():
    """Get sample investment portfolio"""
    try:
        # Sample investment portfolio data
        portfolio = [
            {'symbol': 'AAPL', 'current_price': 175.20, 'quantity': 25.5, 'sector': 'Technology'},
            {'symbol': 'GOOGL', 'current_price': 142.80, 'quantity': 15.0, 'sector': 'Technology'},
            {'symbol': 'MSFT', 'current_price': 415.30, 'quantity': 12.0, 'sector': 'Technology'},
            {'symbol': 'JPM', 'current_price': 155.90, 'quantity': 20.0, 'sector': 'Financial'},
            {'symbol': 'JNJ', 'current_price': 162.40, 'quantity': 18.0, 'sector': 'Healthcare'},
        ]
        
        return jsonify({
            'success': True,
            'portfolio': portfolio,
            'total_holdings': len(portfolio)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hedge/portfolio')
def get_hedge_portfolio():
    """Get sample hedge fund portfolio"""
    try:
        # Sample hedge fund portfolio data
        portfolio = [
            {'symbol': 'NVDA', 'current_price': 485.60, 'quantity': 8.5, 'strategy': 'Growth'},
            {'symbol': 'TSLA', 'current_price': 248.90, 'quantity': 12.0, 'strategy': 'Momentum'},
            {'symbol': 'AMD', 'current_price': 162.30, 'quantity': 15.0, 'strategy': 'Tech Growth'},
            {'symbol': 'NFLX', 'current_price': 445.20, 'quantity': 6.0, 'strategy': 'Media'},
            {'symbol': 'META', 'current_price': 518.70, 'quantity': 7.5, 'strategy': 'Social Media'},
        ]
        
        return jsonify({
            'success': True,
            'portfolio': portfolio,
            'total_holdings': len(portfolio)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    try:
        logger.info(f"Client connected: {request.sid}")
        emit('connected', {'data': 'Connected to server'})
    except Exception as e:
        logger.error(f"Error in handle_connect: {str(e)}")

@socketio.on('disconnect')  
def handle_disconnect():
    """Handle client disconnection"""
    try:
        logger.info(f"Client disconnected: {request.sid}")
    except Exception as e:
        logger.error(f"Error in handle_disconnect: {str(e)}")

@socketio.on('ping')
def handle_ping():
    """Handle ping requests for connection monitoring"""
    try:
        emit('pong', {'timestamp': time.time()})
    except Exception as e:
        logger.error(f"Error in handle_ping: {str(e)}")

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Configuration based on environment
    ENV = os.getenv('FLASK_ENV', 'development')
    
    if ENV == 'production':
        # Production settings
        logger.info("Starting Financial Coach API in production mode on port 5000")
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,
            log_output=False
        )
    else:
        # Development settings
        logger.info("Starting Financial Coach API in development mode on port 5000")
        logger.info("Frontend should be running on port 3000")
        socketio.run(
            app, 
            debug=True, 
            port=5000, 
            host='0.0.0.0',
            use_reloader=False  # Disable reloader to avoid signal handler issues
        )