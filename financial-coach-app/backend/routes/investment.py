from flask import Blueprint, jsonify, request
import logging
from controllers.investment_controller import InvestmentController
from utils.cache_manager import cached
from utils.rate_limiter import rate_limited, general_api_limiter
from utils.yfinance_utils import yf_wrapper
from datetime import datetime

logger = logging.getLogger(__name__)

investment_bp = Blueprint('investment', __name__, url_prefix='/api')
investment_controller = InvestmentController()

@investment_bp.route('/investment-suggestions', methods=['POST'])
def get_investment_suggestions():
    """Get AI-powered investment suggestions"""
    try:
        return investment_controller.get_investment_suggestions()
    except Exception as e:
        logger.error(f"Error getting investment suggestions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@investment_bp.route('/portfolio-analysis', methods=['POST'])
def get_portfolio_analysis():
    """Analyze user's portfolio using investment controller"""
    try:
        return investment_controller.analyze_portfolio()
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@investment_bp.route('/market-insights', methods=['GET'])
def get_market_insights():
    """Get AI-powered market insights"""
    try:
        return investment_controller.get_market_insights()
    except Exception as e:
        logger.error(f"Error getting market insights: {str(e)}")
        return jsonify({'error': str(e)}), 500

@investment_bp.route('/market-indices', methods=['GET'])
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

@investment_bp.route('/stock-prices', methods=['GET'])
@rate_limited(general_api_limiter)
def get_stock_prices_batch():
    """Get stock prices for multiple tickers"""
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

# Legacy route aliases for backward compatibility
@investment_bp.route('/suggestions', methods=['POST'])
def get_suggestions():
    """Legacy alias for investment suggestions"""
    return get_investment_suggestions()

@investment_bp.route('/analyze', methods=['POST'])
def analyze_portfolio():
    """Legacy alias for portfolio analysis"""
    return get_portfolio_analysis()

@investment_bp.route('/insights', methods=['GET'])
def get_market_insights_legacy():
    """Legacy alias for market insights"""
    return get_market_insights()