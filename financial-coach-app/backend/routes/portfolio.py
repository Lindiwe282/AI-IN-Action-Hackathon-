from flask import Blueprint, jsonify, request
import logging
import threading
from contextlib import contextmanager
from datetime import datetime
from flask_socketio import SocketIO
from models.portfolio_models import Stock, db

logger = logging.getLogger(__name__)

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api')

# Thread-safe analyzer instance management
analyzer_lock = threading.Lock()
active_threads = []

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

@portfolio_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Import here to avoid circular imports
    from app_portfolio import Analyzer
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'database': db_status,
        'analyzer_running': Analyzer.is_running
    })

@portfolio_bp.route('/start', methods=['POST'])
def start():
    """Start the strategy with thread management"""
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        
        if not tickers:
            return jsonify({'error': 'No tickers found'}), 400
        
        # Clean and validate tickers
        tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
        
        # Import here to avoid circular imports
        from app_portfolio import Analyzer, active_threads
        
        with analyzer_lock:
            if Analyzer.is_running:
                return jsonify({'message': 'Strategy is already running'}), 200
            
            # Clean up old threads
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

@portfolio_bp.route('/stop', methods=['POST'])
def stop():
    """Stop the strategy gracefully"""
    try:
        # Import here to avoid circular imports
        from app_portfolio import Analyzer, active_threads
        
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

@portfolio_bp.route('/stocks', methods=['GET'])
def get_stocks():
    """Get all stocks"""
    try:
        stocks = Stock.query.all()
        stock_list = [stock.stock_info() for stock in stocks]
        logger.info(f"Fetched {len(stock_list)} stocks from database")
        return jsonify(stock_list)
    except Exception as e:
        logger.error(f"Error fetching stocks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/stocks', methods=['POST'])
def create_stock():
    """Create a new stock"""
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

@portfolio_bp.route('/analysis', methods=['POST'])
def get_analysis():
    """Get portfolio analysis"""
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
        
        # Import here to avoid circular imports
        from app_portfolio import Analyzer
        
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
    """Generate recommendations based on analysis results"""
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

# Investment suggestions endpoint
@portfolio_bp.route('/investment-suggestions', methods=['POST'])
def get_investment_suggestions():
    """Generate investment suggestions based on user profile"""
    try:
        data = request.get_json()
        
        # Extract user profile data
        age = data.get('age', 30)
        monthly_income = data.get('monthly_income', 5000)
        current_savings = data.get('current_savings', 10000)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        investment_experience = data.get('investment_experience', 'beginner')
        investment_timeline = data.get('investment_timeline', 10)
        current_portfolio = data.get('current_portfolio', [])
        
        # Import here to avoid circular imports
        from app_portfolio import Analyzer
        
        # Run portfolio analysis if portfolio is provided
        if current_portfolio and len(current_portfolio) > 0:
            analysis_result = Analyzer.stock_analysis(current_portfolio)
            
            if analysis_result.get('success', False):
                return jsonify({
                    'success': True,
                    'message': 'Investment analysis completed successfully',
                    'user_profile': {
                        'age': age,
                        'risk_tolerance': risk_tolerance,
                        'investment_timeline': investment_timeline
                    },
                    'analysis': analysis_result.get('data', {})
                })
            else:
                return jsonify({
                    'success': False,
                    'error': analysis_result.get('error', 'Analysis failed')
                }), 400
        else:
            return jsonify({
                'success': True,
                'message': 'Investment profile created successfully',
                'user_profile': {
                    'age': age,
                    'risk_tolerance': risk_tolerance,
                    'investment_timeline': investment_timeline
                },
                'suggestions': [
                    'Start with diversified index funds',
                    'Consider your risk tolerance when selecting investments',
                    'Regularly review and rebalance your portfolio'
                ]
            })
            
    except Exception as e:
        logger.error(f"Error in investment suggestions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Stock prices endpoint
@portfolio_bp.route('/stock-prices', methods=['GET'])
def get_stock_prices_batch():
    """Get current stock prices for multiple tickers"""
    try:
        # Import here to avoid circular imports
        from utils.yfinance_utils import yf_wrapper
        from utils.rate_limiter import rate_limited, general_api_limiter
        
        tickers = request.args.get('tickers', '')
        ticker_list = tickers.split(',') if tickers else []
        
        if not ticker_list:
            return jsonify([]), 200
            
        results = []
        for ticker in ticker_list:
            try:
                # Use the cached wrapper
                stock_data = yf_wrapper.get_stock_info(ticker.strip())
                results.append({
                    'ticker': ticker.strip(),
                    'price': stock_data.get('currentPrice'),
                    'change': stock_data.get('change'),
                    'change_percent': stock_data.get('changePercent'),
                })
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {e}")
                results.append({
                    'ticker': ticker.strip(),
                    'price': None,
                    'change': None,
                    'change_percent': None,
                    'error': str(e)
                })
                
        return jsonify(results), 200
        
    except Exception as e:
        logger.error(f"Error in stock prices API: {e}")
        return jsonify({'error': str(e)}), 500

# Alias routes for frontend compatibility
@portfolio_bp.route('/optimize-portfolio', methods=['POST'])
def optimize_portfolio():
    """Alias for analysis endpoint for frontend compatibility"""
    return get_analysis()