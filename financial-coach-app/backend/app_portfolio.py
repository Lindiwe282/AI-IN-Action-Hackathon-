from flask import jsonify, Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import yfinance as yf
import threading 
import time
from datetime import datetime, timedelta
from scipy.optimize import Bounds, minimize
import json
import logging
import numpy as np
import pandas as pd
from services.sentiment import SentimentalAnalysis
from controllers.investment_controller import InvestmentController
import os
from dotenv import load_dotenv
from contextlib import contextmanager
import signal
import sys
from utils.yfinance_utils import yf_wrapper  # Import our wrapper
from utils.cache_manager import cached, cache
from utils.async_handler import run_async, run_cpu_bound, cleanup as async_cleanup
from utils.rate_limiter import rate_limited, general_api_limiter, yfinance_limiter

# Load environment variables from config directory
config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
load_dotenv(os.path.join(config_dir, 'dev.env'))
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

app = Flask(__name__)

# Database configuration with connection pooling
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///instance/stocks.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 20
}

# Import db instance from models and initialize it with our app
from models.portfolio_models import db
db.init_app(app)

# Import the models after initializing SQLAlchemy
from models.portfolio_models import User, Portfolio, PortfolioStock, Wallet, WalletTransaction, MarketData, PortfolioPerformance, Stock

# CORS configuration with explicit frontend origins
CORS(app, 
     resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}}, 
     supports_credentials=True, 
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# SocketIO configuration with stability improvements
socketio = SocketIO(app, 
                    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
                    async_mode="threading",
                    logger=False,  # Disable verbose logging to fix weird connections
                    engineio_logger=False,
                    ping_timeout=60,
                    max_http_buffer_size=1000000,
                    ping_interval=25)

# Thread-safe analyzer instance management
analyzer_lock = threading.Lock()
active_threads = []

# Enhanced Portfolio Analyzer with error handling
class PortfolioAnalyzer:
    def __init__(self):
        self.is_running = False
        self.time_update = 30
        self._stop_event = threading.Event()
        
    def get_current_market_data(self, tickers):
        """Fetch market data with retry logic"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                end_date = datetime.now()
                # Use our cached wrapper
                database = yf_wrapper.download_data(tickers, start='2012-01-01', end=end_date, 
                                     interval='1d', progress=False, auto_adjust=True)
                
                if database.empty:
                    raise ValueError("No data retrieved from yfinance")
                
                database = database['Close']
                data = database.dropna().pct_change(1).dropna()
                
                if data.empty:
                    raise ValueError("Insufficient data after processing")
                
                return data
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    raise
    
    def Sharpe_Ratio_Criterion(self, weight, data):
        try:
            portfolio_return = np.multiply(data, np.transpose(weight))
            portfolio_return = portfolio_return.sum(axis=1)
            mean = np.mean(portfolio_return, axis=0)
            std = np.std(portfolio_return, axis=0)
            
            # Avoid division by zero
            if std == 0 or np.isnan(std):
                return 0
            
            criterion = mean/std
            criterion = -criterion
            return criterion
        except Exception as e:
            logger.error(f"Error in Sharpe Ratio calculation: {str(e)}")
            return 0
    
    def mv_Criterion(self, weight, data):
        try:
            Lambda = 3
            W = 1
            Wbar = 1.0025  # Changed from (1+0.25)/100 to avoid numerical issues
            
            portfolio_return = np.multiply(data, np.transpose(weight))
            portfolio_return = portfolio_return.sum(axis=1)
            
            mean = np.mean(portfolio_return, axis=0)
            variance = np.var(portfolio_return, axis=0)  # Use variance instead of std for stability
            
            # Fixed the mathematical formula with proper parentheses
            term1 = (Wbar**(-1-Lambda)) / (1+Lambda)
            term2 = (Wbar**(-Lambda)) * W * mean
            term3 = (Wbar**(-1-Lambda)) * Lambda * 0.5 * (W**2) * variance
            
            criterion = term1 + term2 - term3
            
            # Add small penalty for extreme weights to improve stability
            weight_penalty = 0.001 * np.sum((weight - 1/len(weight))**2)
            criterion -= weight_penalty
            
            return -1 * criterion
        except Exception as e:
            logger.error(f"Error in MV criterion calculation: {str(e)}")
            return 1e6  # Return large positive value to discourage this solution
        
    def mv_Criterion_weights(self, data):
        try:
            n = data.shape[1]
            
            # Better initial guess - use random weights that sum to 1
            x0 = np.random.random(n)
            x0 = x0 / np.sum(x0)  # Normalize to sum to 1
            
            # Fixed constraint - weights should sum to 1, not absolute sum
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = [(0.001, 0.999) for i in range(0, n)]  # Avoid exact 0 or 1 for numerical stability
            
            # Try optimization with different methods if first one fails
            methods = ['SLSQP', 'trust-constr']
            
            for method in methods:
                try:
                    res = minimize(self.mv_Criterion, x0, args=(data,), method=method,
                                  constraints=cons, bounds=bounds, 
                                  options={'disp': False, 'maxiter': 2000, 'ftol': 1e-9})
                    
                    if res.success and np.isfinite(res.fun):
                        # Normalize weights to ensure they sum to exactly 1
                        weights = res.x / np.sum(res.x)
                        
                        # Additional validation
                        if np.all(weights >= 0) and np.abs(np.sum(weights) - 1.0) < 1e-6:
                            logger.info(f"MV optimization successful with {method}")
                            return weights
                        else:
                            logger.warning(f"MV optimization with {method} produced invalid weights")
                    else:
                        logger.warning(f"MV optimization with {method} did not converge: {res.message}")
                        
                except Exception as e:
                    logger.error(f"Error with {method}: {str(e)}")
                    continue
                    
                # Try different initial guess for next method
                x0 = np.random.random(n)
                x0 = x0 / np.sum(x0)
            
            # If all methods fail, return equal weights but log the failure
            logger.warning("All MV optimization methods failed, using equal weights")
            return np.ones(n) / n
            
        except Exception as e:
            logger.error(f"Error in MV weight optimization: {str(e)}")
            return np.ones(data.shape[1]) / data.shape[1]
    
    def sr_Criterion_weights(self, data):
        try:
            n = data.shape[1]
            x0 = np.random.random(n)
            x0 = x0 / np.sum(x0)  # Better initial guess
            
            # Fixed constraint - weights should sum to 1
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = [(0.001, 0.999) for i in range(0, n)]  # Avoid exact boundaries
            
            res = minimize(self.Sharpe_Ratio_Criterion, x0, args=(data,), method="SLSQP",
                          constraints=cons, bounds=bounds, 
                          options={'disp': False, 'maxiter': 2000, 'ftol': 1e-9})
            
            if res.success and np.isfinite(res.fun):
                # Normalize weights to ensure they sum to exactly 1
                weights = res.x / np.sum(res.x)
                
                if np.all(weights >= 0) and np.abs(np.sum(weights) - 1.0) < 1e-6:
                    return weights
                    
            logger.warning("SR optimization did not converge properly")
            return np.ones(n) / n  # Return equal weights as fallback
            
        except Exception as e:
            logger.error(f"Error in SR weight optimization: {str(e)}")
            return np.ones(data.shape[1]) / data.shape[1]
        
    def execute_trade(self, data):
        weight = []
        optimum_weights_mv_criterion = self.mv_Criterion_weights(data)
        optimum_weights_sr_criterion = self.sr_Criterion_weights(data)
        weight.append(optimum_weights_mv_criterion)
        weight.append(optimum_weights_sr_criterion)
        return weight
    
    def get_strategy_recommendation(self, strategies):
        """Determine which strategy to recommend based on metrics"""
        if not strategies:
            return "No recommendation available"
        
        try:
            # Get the best strategy based on Sharpe ratio
            best_strategy = max(strategies, key=lambda x: x['metrics']['sharpe_ratio'])
            
            # Get market conditions
            market_conditions = self.get_market_conditions()
            
            # Make recommendation based on market conditions and strategy performance
            if market_conditions['condition'] == 'bear':
                # In bear markets, prefer lower volatility
                lowest_vol_strategy = min(strategies, key=lambda x: x['metrics']['volatility'])
                return f"Use {lowest_vol_strategy['name']} for lower volatility in bearish conditions"
            elif market_conditions['condition'] == 'bull':
                # In bull markets, prefer higher returns
                highest_return_strategy = max(strategies, key=lambda x: x['metrics']['total_return'])
                return f"Use {highest_return_strategy['name']} for maximum returns in bullish conditions"
            else:
                # Neutral market - use best Sharpe ratio
                return f"Use {best_strategy['name']} for balanced risk-adjusted returns"
        except Exception as e:
            logger.error(f"Error in strategy recommendation: {str(e)}")
            return "Unable to generate recommendation"
    
    def get_market_conditions(self):
        """Analyze current market conditions with error handling"""
        try:
            # Define key market indicators
            market_indicators = {
                '^GSPC': {'name': 'S&P 500', 'weight': 0.3},
                '^DJI': {'name': 'Dow Jones', 'weight': 0.2},
                '^IXIC': {'name': 'NASDAQ', 'weight': 0.2},
                '^VIX': {'name': 'VIX', 'weight': 0.3}
            }
            
            market_scores = []
            vix_level = None
            
            for symbol, info in market_indicators.items():
                try:
                    # Use our cached wrapper
                    hist = yf_wrapper.get_history(symbol, period="1mo")  # Get 1 month of data
                    
                    if hist.empty:
                        continue
                    
                    # Calculate various timeframe returns
                    daily_return = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100 if len(hist) > 1 else 0
                    weekly_return = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100 if len(hist) > 5 else 0
                    monthly_return = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100 if len(hist) > 0 else 0
                    
                    # Special handling for VIX (inverse relationship)
                    if symbol == '^VIX':
                        vix_level = hist['Close'].iloc[-1]
                        # VIX scoring: High VIX = bearish, Low VIX = bullish
                        if vix_level > 30:
                            score = -2  # Very bearish
                        elif vix_level > 25:
                            score = -1.5  # Bearish
                        elif vix_level > 20:
                            score = -0.5  # Slightly bearish
                        elif vix_level > 15:
                            score = 0  # Neutral
                        else:
                            score = 1  # Bullish
                        market_scores.append(score * info['weight'])
                    else:
                        # For other indices, positive returns = bullish
                        if monthly_return > 5:
                            score = 2  # Very bullish
                        elif monthly_return > 2:
                            score = 1.5  # Bullish
                        elif monthly_return > 0:
                            score = 0.5  # Slightly bullish
                        elif monthly_return > -2:
                            score = -0.5  # Slightly bearish
                        elif monthly_return > -5:
                            score = -1.5  # Bearish
                        else:
                            score = -2  # Very bearish
                        
                        market_scores.append(score * info['weight'])
                        
                except Exception as e:
                    logger.warning(f"Error fetching {symbol}: {str(e)}")
                    continue
            
            # Calculate weighted average market score
            if market_scores:
                avg_score = sum(market_scores)
                
                # Determine market condition based on score
                if avg_score > 1:
                    condition = "bull"
                    description = "Strong Bullish"
                    confidence = min(abs(avg_score) / 2 * 100, 100)
                elif avg_score > 0.3:
                    condition = "bull"
                    description = "Bullish"
                    confidence = min(abs(avg_score) / 2 * 100, 100)
                elif avg_score >= -0.3:
                    condition = "neutral"
                    description = "Neutral"
                    confidence = 50 + (abs(avg_score) * 50)
                elif avg_score >= -1:
                    condition = "bear"
                    description = "Bearish"
                    confidence = min(abs(avg_score) / 2 * 100, 100)
                else:
                    condition = "bear"
                    description = "Strong Bearish"
                    confidence = min(abs(avg_score) / 2 * 100, 100)
                
                # Additional market analysis
                momentum = "positive" if avg_score > 0 else "negative"
                volatility_status = "high" if vix_level and vix_level > 25 else "moderate" if vix_level and vix_level > 18 else "low"
                
                return {
                    'condition': condition,  # bull/bear/neutral as required
                    'description': description,
                    'score': round(avg_score, 2),
                    'confidence': round(confidence, 1),
                    'momentum': momentum,
                    'volatility': volatility_status,
                    'vix_level': round(vix_level, 2) if vix_level else None,
                    'analysis_date': datetime.now().isoformat()
                }
            else:
                # Default return if analysis fails
                return {
                    'condition': 'neutral',
                    'description': 'Unable to determine',
                    'score': 0,
                    'confidence': 0,
                    'momentum': 'neutral',
                    'volatility': 'moderate',
                    'vix_level': None,
                    'analysis_date': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in get_market_conditions: {str(e)}")
            # Return default neutral condition on error
            return {
                'condition': 'neutral',
                'description': 'Analysis Error',
                'score': 0,
                'confidence': 0,
                'momentum': 'neutral',
                'volatility': 'moderate',
                'vix_level': None,
                'analysis_date': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def stock_analysis(self, tickers):
        """Perform stock analysis with comprehensive error handling"""
        try:
            strategy_names = ["Mean Variance Criterion", "Sharpe Ratio Criterion"]
            data = self.get_current_market_data(tickers)
            
            if data.empty:
                raise ValueError("No valid data for analysis")
            
            weights = self.execute_trade(data)
            
            optimum_return = {
                'strategies': [],
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'tickers': tickers,
                    'market_conditions': self.get_market_conditions()  # bull/bear/neutral
                }
            }
            
            for strategy_idx, weight in enumerate(weights):
                try:
                    strategy_name = strategy_names[strategy_idx]
                    portfolio_return = np.multiply(data, np.transpose(weight))
                    portfolio_return = portfolio_return.sum(axis=1)
                    
                    # Calculate additional metrics
                    returns_array = portfolio_return.flatten() if len(portfolio_return.shape) > 1 else portfolio_return
                    
                    # Ensure we have valid data
                    if len(returns_array) == 0:
                        logger.warning(f"No returns data for {strategy_name}")
                        continue
                    
                    cumulative_returns = (1 + returns_array).cumprod() - 1
                    total_return_value = cumulative_returns.iloc[-1] if len(cumulative_returns) > 0 else 0
                    
                    n_days = len(returns_array)
                    n_years = n_days / 252 
                    annualized_return = (1 + total_return_value) ** (1/n_years) - 1 if n_years > 0 else 0
                    
                    # FIXED: Calculate annualized Sharpe ratio (assuming 252 trading days)
                    daily_sharpe = np.mean(returns_array) / np.std(returns_array) if np.std(returns_array) != 0 else 0
                    annualized_sharpe = daily_sharpe * np.sqrt(252)
                    
                    strategy_data = {
                        'name': strategy_name,
                        'portfolio_return': portfolio_return.tolist(),
                        'metrics': {
                            'total_return': float(total_return_value),  # FIXED: Compounded return
                            'annualized_return': float(annualized_return), 
                            'avg_daily_return': float(np.mean(returns_array)),
                            'volatility': float(np.std(returns_array)),
                            'sharpe_ratio': float(annualized_sharpe),  # FIXED: Annualized Sharpe ratio
                            'years_analyzed': round(n_years, 1)
                        },
                        'ticker_allocation': {ticker: float(w) for ticker, w in zip(tickers, weight)}
                    }
                    
                    optimum_return['strategies'].append(strategy_data)
                    
                except Exception as e:
                    logger.error(f"Error processing {strategy_name}: {str(e)}")
                    continue
            
            if optimum_return['strategies']:
                optimum_return['comparison'] = {
                    'best_performer': max(optimum_return['strategies'], key=lambda x: x['metrics']['total_return'])['name'],
                    'lowest_risk': min(optimum_return['strategies'], key=lambda x: x['metrics']['volatility'])['name'],
                    'recommendation': self.get_strategy_recommendation(optimum_return['strategies'])
                }
            else:
                optimum_return['comparison'] = {
                    'best_performer': 'N/A',
                    'lowest_risk': 'N/A',
                    'recommendation': 'Insufficient data for analysis'
                }
        
            return optimum_return
            
        except Exception as e:
            logger.error(f"Error in stock_analysis: {str(e)}")
            return {
                'error': str(e),
                'strategies': [],
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'tickers': tickers,
                    'market_conditions': self.get_market_conditions()
                },
                'comparison': {
                    'best_performer': 'N/A',
                    'lowest_risk': 'N/A',
                    'recommendation': 'Analysis failed'
                }
            }
            
    def run_strategy(self, tickers):
        """Run strategy with proper thread management"""
        logger.info(f"Initializing the strategy with tickers: {tickers}")
        self.is_running = True
        self._stop_event.clear()
        
        strategy_names = ["Mean Variance Criterion", "Sharpe Ratio Criterion"]
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.is_running and not self._stop_event.is_set():
            try:
                data = self.get_current_market_data(tickers)
                weights_list = self.execute_trade(data)
                
                result = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'strategies': []
                }
                
                for strategy_idx, weights in enumerate(weights_list):
                    strategy_name = strategy_names[strategy_idx]
                    formatted_weights = {ticker: float(weight) for ticker, weight in zip(tickers, weights)}
                    result['strategies'].append({
                        'name': strategy_name,
                        'weights': formatted_weights
                    })
                
                # Emit to all connected clients
                socketio.emit('strategy_update', result, namespace='/')
                logger.info(f"Strategy update emitted successfully")
                
                # Reset error counter on success
                consecutive_errors = 0
            
                # Wait for next update or stop signal
                self._stop_event.wait(self.time_update)
            
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"Error in strategy execution ({consecutive_errors}/{max_consecutive_errors}): {str(e)}")
                
                if consecutive_errors >= max_consecutive_errors:
                    logger.error("Too many consecutive errors, stopping strategy")
                    self.is_running = False
                    break
                
                # Exponential backoff on errors
                self._stop_event.wait(min(10 * (2 ** consecutive_errors), 300))
        
        self.is_running = False
        logger.info("Strategy execution stopped")
                
    def stop_strategy(self):
        """Gracefully stop the strategy"""
        self.is_running = False
        self._stop_event.set()
        logger.info("Stop signal sent to strategy")

# Create an instance of the analyzer and controllers
Analyzer = PortfolioAnalyzer()
sentiment_analyzer = SentimentalAnalysis(api_key=os.getenv("ALPHA_VANTAGE_API_KEY"))
investment_controller = InvestmentController()


# Context manager for database sessions
@contextmanager
def get_db_session():
    """Provide a transactional scope for database operations"""
    try:
        yield db.session
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.session.close()

# Create tables if they don't exist - with error handling
def init_db():
    """Initialize database with proper error handling"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")

# Initialize database
init_db()

# Register blueprints
from routes.portfolio import portfolio_bp
from routes.investment import investment_bp
from routes.sentiment import sentiment_bp

app.register_blueprint(portfolio_bp)
app.register_blueprint(investment_bp)
app.register_blueprint(sentiment_bp)

# Legacy API Routes - keeping for backward compatibility

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'database': db_status,
        'analyzer_running': Analyzer.is_running
    })

@app.route('/api/start', methods=['POST'])
def start():
    """Start the strategy with thread management"""
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers:
            return jsonify({'error': 'No tickers found'}), 400
        
        # Clean and validate tickers
        tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
        
        with analyzer_lock:
            if Analyzer.is_running:
                return jsonify({'message': 'Strategy is already running'}), 200
            
            # Clean up old threads
            global active_threads
            active_threads = [t for t in active_threads if t.is_alive()]
            
            # Start new thread
            thread = threading.Thread(
                target=Analyzer.run_strategy, 
                args=(tickers,),
                name=f"StrategyThread-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            )
            thread.daemon = True
            thread.start()
            active_threads.append(thread)
        
        return jsonify({
            'message': 'Strategy started successfully',
            'tickers': tickers
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting strategy: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop():
    """Stop the strategy gracefully"""
    try:
        with analyzer_lock:
            if not Analyzer.is_running:
                return jsonify({'message': 'Strategy is not running'}), 200
            
            Analyzer.stop_strategy()
            
            # Wait for thread to finish (with timeout)
            for thread in active_threads:
                if thread.is_alive():
                    thread.join(timeout=5)
        
        return jsonify({'message': 'Strategy has been stopped'}), 200
        
    except Exception as e:
        logger.error(f"Error stopping strategy: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Get all stocks - keeping original simple format for compatibility"""
    try:
        stocks = Stock.query.all()
        stock_list = [stock.stock_info() for stock in stocks]
        logger.info(f"Fetched {len(stock_list)} stocks from database")
        return jsonify(stock_list)  # Return simple array like original
    except Exception as e:
        logger.error(f"Error fetching stocks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stocks', methods=['POST'])
def create_stock():
    """Create a new stock - keeping original functionality"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name') or not data.get('ticker'):
            return jsonify({'error': 'Name and ticker are required'}), 400
        
        with get_db_session():
            stock = Stock(
                name=data.get('name'),
                ticker=data.get('ticker').upper(),
                detail=data.get('detail', '')
            )
            db.session.add(stock)
        
        logger.info(f"Created stock: {stock.ticker}")
        return jsonify(stock.stock_info()), 201
        
    except Exception as e:
        logger.error(f"Error creating stock: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/analysis', methods=['POST'])
def get_analysis():
    """Get portfolio analysis - enhanced with error handling"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        tickers = data.get('tickers', [])
        
        # Support both single ticker string and array
        if isinstance(tickers, str):
            tickers = [tickers]
        
        if not tickers:
            return jsonify({'error': 'No tickers provided'}), 400
        
        # Clean and validate tickers
        tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
        
        # Limit number of tickers to prevent abuse
        if len(tickers) > 20:
            return jsonify({'error': 'Maximum 20 tickers allowed'}), 400
        
        # Get the analysis
        optimum_portfolio = Analyzer.stock_analysis(tickers)
        
                # Check for errors in analysis
        if 'error' in optimum_portfolio:
            return jsonify({
                'success': False,
                'error': optimum_portfolio['error'],
                'message': 'Failed to analyze portfolio'
            }), 500
        
        # Add portfolio-level insights
        portfolio_insights = {
            'portfolio_size': len(tickers),
            'analysis_timestamp': datetime.now().isoformat(),
            'recommendations': get_portfolio_recommendations(optimum_portfolio)
        }
        
        return jsonify({
            'success': True,
            'data': optimum_portfolio,
            'insights': portfolio_insights
        })
    
    except Exception as e:
        logger.error(f"Error getting analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze portfolio'
        }), 500

def get_portfolio_recommendations(analysis):
    """Generate recommendations based on analysis results - keeping original logic"""
    try:
        market_condition = analysis['metadata']['market_conditions']['condition']
        
        recommendations = []
        
        # Market-based recommendations
        if market_condition == 'bear':
            recommendations.append({
                'type': 'warning',
                'message': 'Market conditions are bearish. Consider defensive stocks to make to counter the bearish.'
            })
        elif market_condition == 'bull':
            recommendations.append({
                'type': 'success',
                'message': 'Market conditions are favorable for growth stocks as well as blue chip stocks.'
            })
        
        # Strategy-based recommendations
        strategies = analysis.get('strategies', [])
        if strategies:
            sharpe_ratios = [s['metrics']['sharpe_ratio'] for s in strategies]
            best_sharpe = max(sharpe_ratios)
            
            if best_sharpe > 1:
                recommendations.append({
                    'type': 'success',
                    'message': 'Portfolio shows strong risk-adjusted returns.'
                })
            elif best_sharpe < 0.5:
                recommendations.append({
                    'type': 'warning',
                    'message': 'Consider rebalancing for better risk-adjusted returns.'
                })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return [{
            'type': 'error',
            'message': 'Unable to generate recommendations'
        }]

@app.route('/api/investment-suggestions', methods=['POST'])
def get_investment_suggestions():
    """Get AI-powered investment suggestions"""
    try:
        return investment_controller.get_investment_suggestions()
    except Exception as e:
        logger.error(f"Error getting investment suggestions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio-analysis', methods=['POST'])
def get_portfolio_analysis():
    """Analyze user's portfolio using investment controller"""
    try:
        return investment_controller.analyze_portfolio()
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-insights', methods=['GET'])
def get_market_insights():
    """Get AI-powered market insights"""
    try:
        return investment_controller.get_market_insights()
    except Exception as e:
        logger.error(f"Error getting market insights: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/api/market-indices', methods=['GET'])
@cached(ttl=300)  # Cache for 5 minutes
@rate_limited(general_api_limiter)
def get_market_indices():
    """Get current market indices data"""
    try:
        indices = {
            '^GSPC': 'S&P 500',
            '^IXIC': 'NASDAQ',
            '^DJI': 'Dow Jones',
            '^VIX': 'VIX'
        }
        
        market_data = []
        
        for symbol, name in indices.items():
            try:
                # Use our cached wrapper
                hist = yf_wrapper.get_history(symbol, period="2d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
                    # Calculate change if we have at least 2 data points
                    if len(hist) >= 2:
                        previous_price = hist['Close'].iloc[-2]
                        change = ((current_price - previous_price) / previous_price) * 100
                    else:
                        # For single-day data (like VIX sometimes), try to get intraday change
                        try:
                            # Get more historical data to calculate daily change
                            extended_hist = yf_wrapper.get_history(symbol, period="5d")
                            if len(extended_hist) >= 2:
                                previous_price = extended_hist['Close'].iloc[-2]
                                change = ((current_price - previous_price) / previous_price) * 100
                            else:
                                # Fall back to open vs close for intraday change
                                open_price = hist['Open'].iloc[-1]
                                change = ((current_price - open_price) / open_price) * 100
                        except:
                            change = 0.0  # Default to 0 if we can't calculate change
                    
                    market_data.append({
                        'symbol': symbol,
                        'name': name,
                        'value': round(current_price, 2),
                        'change': round(change, 2),
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    logger.warning(f"No data available for {symbol}")
                    
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {str(e)}")
                continue
        
        return jsonify({
            'success': True,
            'data': market_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching market indices: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500
        
        
# Rate limiting decorator
from functools import wraps
from collections import defaultdict

rate_limit_storage = defaultdict(list)

def rate_limit(max_calls=10, time_window=60):
    """Rate limit decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            rate_limit_storage[client_ip] = [
                timestamp for timestamp in rate_limit_storage[client_ip]
                if current_time - timestamp < time_window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_calls:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': time_window
                }), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/sentiment/news/<ticker>', methods=['GET'])
@rate_limit(max_calls=10, time_window=60)
def get_news_articles(ticker):
    """Get news articles with sentiment for a ticker"""
    try:
        # Clean ticker
        ticker = ticker.strip().upper()
        if not ticker:
            return jsonify({'error': 'Invalid ticker symbol'}), 400
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 50)  # Limit max articles per page
        
        # Get sentiment data
        sentiment_data = sentiment_analyzer.get_sentiment_info(ticker)
        
        # Check if we have an error but still some data (stale cache)
        if sentiment_data.get('error'):
            logger.warning(f"Sentiment API error for {ticker}: {sentiment_data['error']}")
            if sentiment_data.get('stale'):
                # Add a warning to the response
                sentiment_data['warning'] = 'Using cached data due to API issues'
        
        articles = sentiment_data.get('articles', [])
        
        # Prepare articles in the format you want
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'time_published': article.get('time_published', ''),
                'authors': article.get('authors', []),
                'summary': article.get('summary', ''),
                'banner_image': article.get('banner_image', ''),
                'source': article.get('source', ''),
                'topics': article.get('topics', []),
                'overall_sentiment_score': article.get('overall_sentiment_score', 0),
                'overall_sentiment_label': article.get('overall_sentiment_label', ''),
                'ticker_sentiments': article.get('ticker_sentiments', [])
            })
        
        # Pagination
        total_articles = len(formatted_articles)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_articles = formatted_articles[start_idx:end_idx]
        
        response_data = {
            'success': True,
            'ticker': ticker,
            'articles': paginated_articles,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_articles,
                'pages': (total_articles + per_page - 1) // per_page if per_page > 0 else 0
            },
            'aggregate_sentiment': sentiment_data.get('aggregate_metrics', {})
        }
        
        # Add warning if using stale data
        if sentiment_data.get('warning'):
            response_data['warning'] = sentiment_data['warning']
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching news articles: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch news articles',
            'ticker': ticker,
            'articles': [],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': 0,
                'pages': 0
            },
            'aggregate_sentiment': {
                'average_sentiment': 0,
                'articles_analyzed': 0,
                'sentiment_trend': 'neutral',
                'confidence_level': 'Low'
            }
        }), 500
@app.route('/api/sentiment/article-analysis', methods=['POST'])
def analyze_article():
    """Analyze a specific article - for the modal popup"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get the article data from frontend
        article = data.get('article', {})
        if not article:
            return jsonify({'error': 'No article data provided'}), 400
        
        # Prepare detailed analysis for the modal
        detailed_analysis = {
            'article_info': {
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'source': article.get('source', ''),
                'authors': article.get('authors', []),
                'published': article.get('time_published', ''),
                'summary': article.get('summary', '')
            },
            'sentiment_overview': {
                'overall_score': article.get('overall_sentiment_score', 0),
                'overall_label': article.get('overall_sentiment_label', ''),
                'interpretation': sentiment_analyzer.interpret_sentiment(
                    article.get('overall_sentiment_score', 0)
                ).__dict__  # Convert to dict for JSON serialization
            },
            'ticker_analysis': []
        }
        
        # Analyze each ticker mentioned in the article
        # Check both 'ticker_sentiments' and 'ticker_sentiment' for compatibility
        ticker_sentiments = article.get('ticker_sentiments', []) or article.get('ticker_sentiment', [])
        
        for ticker_sentiment in ticker_sentiments:
            # Make sure we have the actual sentiment score
            sentiment_score = float(ticker_sentiment.get('ticker_sentiment_score', 0) or ticker_sentiment.get('sentiment_score', 0))
            relevance_score = float(ticker_sentiment.get('relevance_score', 0))
            
            # Create proper sentiment data
            sentiment_data = {
                'ticker': ticker_sentiment.get('ticker', ''),
                'ticker_sentiment_score': sentiment_score,
                'ticker_sentiment_label': ticker_sentiment.get('ticker_sentiment_label', ticker_sentiment.get('sentiment_label', 'Neutral')),
                'relevance_score': relevance_score
            }
            
            ticker_analysis = sentiment_analyzer.analyze_ticker_sentiment(sentiment_data)
            
            # Add visual indicators for the UI
            ticker_analysis['visual'] = {
                'color': ticker_analysis['color_code'],
                'icon': ticker_analysis['icon'],
                'should_invest': ticker_analysis['signal'] in ['BUY', 'STRONG BUY'],
                'risk_color': {
                    'Low': '#00C851',
                    'Moderate': '#FFBB33',
                    'Moderate-High': '#FF8800',
                    'High': '#FF4444'
                }.get(ticker_analysis['risk_level'], '#FFBB33')
            }
            
            detailed_analysis['ticker_analysis'].append(ticker_analysis)
        
        # Sort tickers by relevance score
        detailed_analysis['ticker_analysis'].sort(
            key=lambda x: x['relevance_score'], 
            reverse=True
        )
        
        # Add investment summary
        buy_signals = [t for t in detailed_analysis['ticker_analysis'] 
                      if t['signal'] in ['BUY', 'STRONG BUY']]
        sell_signals = [t for t in detailed_analysis['ticker_analysis'] 
                       if t['signal'] in ['SELL', 'STRONG SELL']]
        
        detailed_analysis['investment_summary'] = {
            'total_tickers': len(detailed_analysis['ticker_analysis']),
            'buy_signals': len(buy_signals),
            'sell_signals': len(sell_signals),
            'hold_signals': len(detailed_analysis['ticker_analysis']) - len(buy_signals) - len(sell_signals),
            'top_pick': buy_signals[0] if buy_signals else None,
            'avoid': sell_signals[0] if sell_signals else None
        }
        
        return jsonify({
            'success': True,
            'analysis': detailed_analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze article'
        }), 500
        
        
@app.route('/api/sentiment/ticker-summary/<ticker>', methods=['GET'])
@rate_limited(general_api_limiter)
def get_ticker_sentiment_summary(ticker):
    """Get sentiment summary for a specific ticker - for header display"""
    try:
        # Clean ticker
        ticker = ticker.strip().upper()
        if not ticker:
            return jsonify({'error': 'Invalid ticker symbol'}), 400
        
        # Get sentiment summary
        summary = sentiment_analyzer.get_sentiment_summary(ticker)
        
        return jsonify({
            'success': True,
            'data': {
                'ticker': ticker,
                'average_sentiment': summary.get('average_sentiment', 0),
                'recommendation': summary.get('recommendation', 'HOLD'),
                'confidence': summary.get('confidence', 'Low'),
                'trend': summary.get('trend', 'Stable'),
                'summary': summary.get('quick_summary', 'No data available')
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting ticker sentiment summary: {str(e)}")
        return jsonify({
            'success': True,  # Return success with default values
            'data': {
                'ticker': ticker,
                'average_sentiment': 0,
                'recommendation': 'HOLD',
                'confidence': 'Low',
                'trend': 'Stable',
                'summary': 'Unable to fetch sentiment data'
            }
        })

@app.route('/api/sentiment/article-tickers', methods=['POST'])
def get_article_ticker_sentiments(ticker):
    """Get detailed ticker sentiments from an article"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        article = data.get('article', {})
        if not article:
            return jsonify({'error': 'No article data provided'}), 400
        
        # Extract ticker sentiments from the article
        ticker_sentiments = article.get('ticker_sentiment', [])
        analyzed_sentiments = []
        
        for ts in ticker_sentiments:
            # Get the actual sentiment score from the API data
            sentiment_score = float(ts.get('ticker_sentiment_score', 0))
            relevance_score = float(ts.get('relevance_score', 0))
            
            # Analyze the sentiment
            analysis = sentiment_analyzer.analyze_ticker_sentiment({
                'ticker': ts.get('ticker', ''),
                'ticker_sentiment_score': sentiment_score,
                'ticker_sentiment_label': ts.get('ticker_sentiment_label', 'Neutral'),
                'relevance_score': relevance_score
            })
            
            analyzed_sentiments.append(analysis)
        
        return jsonify({
            'success': True,
            'ticker_sentiments': analyzed_sentiments
        })
        
    except Exception as e:
        logger.error(f"Error analyzing article ticker sentiments: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze ticker sentiments'
        }), 500



@app.route('/api/stock-prices', methods=['GET'])
@rate_limited(general_api_limiter)
def get_stock_prices_batch():
    try:
        tickers = request.args.get('tickers', '')
        ticker_list = tickers.split(',') if tickers else []
        
        if not ticker_list:
            return jsonify([]), 200
            
        results = []
        for ticker in ticker_list:
            try:
                # Use the cached wrapper
                stock_data = yf_wrapper.get_stock_info(ticker)
                results.append({
                    'ticker': ticker,
                    'price': stock_data['currentPrice'] if 'currentPrice' in stock_data else None,
                    'change': stock_data['change'] if 'change' in stock_data else None,
                    'change_percent': stock_data['changePercent'] if 'changePercent' in stock_data else None,
                })
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {e}")
                results.append({
                    'ticker': ticker,
                    'price': None,
                    'change': None,
                    'change_percent': None,
                    'error': str(e)
                })
                
        return jsonify(results), 200
        
    except Exception as e:
        logger.error(f"Error in stock prices API: {e}")
        return jsonify({'error': str(e)}), 500
    
    
# SocketIO event handlers - enhanced with error handling
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    try:
        
        logger.info(f"Client connected: {request.sid}")
        emit('connected', {'data': 'Connected to server'})
    except Exception as e:
        logger.error(f"Error in handle_connect: {str(e)}")

@socketio.on('disconnect')  
def handle_disconnect(sid=None):
    """Handle client disconnection"""
    try:
        # Use sid parameter if provided, otherwise use request.sid
        client_sid = sid if sid else getattr(request, 'sid', 'unknown')
        logger.info(f"Client disconnected: {client_sid}")
    except Exception as e:
        logger.error(f"Error in handle_disconnect: {str(e)}")
    
@socketio.on('ping')
def handle_ping():
    """Handle ping requests for connection monitoring"""
    try:
        emit('pong', {'timestamp': datetime.now().isoformat()})
    except Exception as e:
        logger.error(f"Error in handle_ping: {str(e)}")

@socketio.on_error()
def error_handler(e):
    """Global SocketIO error handler"""
    logger.error(f"SocketIO Error: {str(e)}")
    return False

@socketio.on_error()
def error_handler(e):
    """Global error handler for SocketIO"""
    logger.error(f"SocketIO Error: {e}")

# Error handlers for HTTP routes
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# Rate limiting decorator
from functools import wraps
from collections import defaultdict

rate_limit_storage = defaultdict(list)

def rate_limit(max_calls=10, time_window=60):
    """Rate limit decorator"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            rate_limit_storage[client_ip] = [
                timestamp for timestamp in rate_limit_storage[client_ip]
                if current_time - timestamp < time_window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_calls:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'retry_after': time_window
                }), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Apply rate limiting to analysis endpoint
get_analysis = rate_limit(max_calls=5, time_window=60)(get_analysis)

# Utility function for cleaning up stale connections
def cleanup_old_connections():
    """Periodically clean up stale connections"""
    while True:
        try:
            time.sleep(300)  # Run every 5 minutes
            with app.app_context():
                # Clean up any stale database connections
                db.engine.dispose()
                logger.info("Cleaned up database connections")
        except Exception as e:
            logger.error(f"Error in cleanup task: {str(e)}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_connections, daemon=True)
cleanup_thread.start()

# Main execution block
if __name__ == '__main__':
    # Graceful shutdown handler
    def signal_handler(sig, frame):
        """Handle shutdown signals gracefully"""
        logger.info('Shutting down gracefully...')
        
        # Stop the analyzer if running
        if Analyzer.is_running:
            Analyzer.stop_strategy()
        
        # Give threads time to finish
        time.sleep(2)
        
        # Cleanup resources
        cache.shutdown()
        async_cleanup()
        
        sys.exit(0)
    
    # Register signal handlers (only in main thread)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Configuration based on environment
    ENV = os.getenv('FLASK_ENV', 'development')
    
    if ENV == 'production':
        # Production settings
        socketio.run(
            app,
            host='0.0.0.0',
            port=int(os.getenv('PORT', 3000)),
            debug=False,
            use_reloader=False,
            log_output=False
        )
    else:
        # Development settings - keeping original
        socketio.run(
            app, 
            debug=True, 
            port=3000, 
            host='127.0.0.1'
        )
    
    # Cleanup on shutdown
    cache.shutdown()
    async_cleanup()

# Export key components for testing
__all__ = ['app', 'db', 'socketio', 'Stock', 'PortfolioAnalyzer']