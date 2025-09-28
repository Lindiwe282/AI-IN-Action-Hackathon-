"""
Hedge Investments Controller
Handles options trading strategies with FIX protocol integration
"""

from flask import Blueprint, request, jsonify
from services.options_service import OptionsService
import logging
import numpy as np
from datetime import datetime, timedelta
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize options service
options_service = OptionsService()

def run_async(coro):
    """Helper function to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        # If loop is already running, create a new task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return loop.run_until_complete(coro)

def get_market_contracts():
    """Get list of US and South African market contracts"""
    try:
        contracts = options_service.get_market_contracts()
        
        return {
            'success': True,
            'data': contracts,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting market contracts: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_options_chain():
    """Get options chain for a specific symbol"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        if not symbol:
            return {
                'success': False,
                'error': 'Symbol is required'
            }
        
        # Generate simple options data directly
        import random
        
        # Mock current price
        current_price = random.uniform(50, 400)
        
        # Generate options chain
        calls = []
        puts = []
        
        # Generate strikes around current price
        for i in range(-5, 6):  # 11 strikes total
            strike = round(current_price + (current_price * 0.05 * i), 2)
            
            # Call options
            call_premium = max(0.10, (current_price - strike) + random.uniform(0.50, 5.00))
            calls.append({
                'strike': strike,
                'premium': round(call_premium, 2),
                'implied_volatility': round(random.uniform(0.15, 0.45), 3),
                'delta': round(random.uniform(0.20, 0.80), 3),
                'volume': random.randint(10, 1000),
                'open_interest': random.randint(50, 5000)
            })
            
            # Put options
            put_premium = max(0.10, (strike - current_price) + random.uniform(0.50, 5.00))
            puts.append({
                'strike': strike,
                'premium': round(put_premium, 2),
                'implied_volatility': round(random.uniform(0.15, 0.45), 3),
                'delta': round(random.uniform(-0.80, -0.20), 3),
                'volume': random.randint(10, 1000),
                'open_interest': random.randint(50, 5000)
            })
        
        options_data = {
            'symbol': symbol,
            'current_price': current_price,
            'calls': calls,
            'puts': puts,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'data': options_data,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting options chain: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def calculate_long_strap():
    """Calculate long strap strategy analysis"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        strike = data.get('strike')
        expiry = data.get('expiry')
        
        if not all([symbol, strike, expiry]):
            return {
                'success': False,
                'error': 'Symbol, strike, and expiry are required'
            }
        
        # Validate inputs
        try:
            strike = float(strike)
            datetime.strptime(expiry, "%Y-%m-%d")
        except (ValueError, TypeError):
            return {
                'success': False,
                'error': 'Invalid strike price or expiry date format (YYYY-MM-DD)'
            }
        
        strategy_analysis = run_async(options_service.calculate_long_strap_strategy(symbol, strike, expiry))
        
        if 'error' in strategy_analysis:
            return {
                'success': False,
                'error': strategy_analysis['error']
            }
        
        return {
            'success': True,
            'data': strategy_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating long strap strategy: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_portfolio_analysis():
    """Analyze portfolio of hedge investment strategies"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return {
                'success': False,
                'error': 'At least one symbol is required'
            }
        
        # Validate symbols
        if not isinstance(symbols, list) or len(symbols) > 20:
            return {
                'success': False,
                'error': 'Symbols must be a list with maximum 20 items'
            }
        
        # Generate mock portfolio analysis
        import random
        
        total_return = random.uniform(-15, 25)
        annualized_return = random.uniform(-10, 20)
        volatility = random.uniform(15, 35)
        sharpe_ratio = random.uniform(-0.5, 2.0)
        max_drawdown = random.uniform(-25, -5)
        win_rate = random.uniform(45, 75)
        
        contracts = []
        for symbol in symbols:
            contracts.append({
                'symbol': symbol,
                'current_price': random.uniform(50, 400),
                'return': random.uniform(-20, 30),
                'risk_level': random.choice(['Low', 'Medium', 'High']),
                'sharpe_ratio': random.uniform(-0.5, 2.0),
                'portfolio_weight': 100.0 / len(symbols)
            })
        
        portfolio_analysis = {
            'total_return': round(total_return, 2),
            'annualized_return': round(annualized_return, 2),
            'volatility': round(volatility, 2),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'max_drawdown': round(max_drawdown, 2),
            'win_rate': round(win_rate, 1),
            'contracts': contracts,
            'analysis_date': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'data': portfolio_analysis,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in portfolio analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_historical_analysis():
    """Get historical analysis for hedge strategies"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        start_date = data.get('start_date', '2019-01-01')
        
        if not symbol:
            return {
                'success': False,
                'error': 'Symbol is required'
            }
        
        # Validate date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return {
                'success': False,
                'error': 'Invalid start_date format (YYYY-MM-DD)'
            }
        
        historical_data = run_async(options_service.fetch_historical_data(symbol, start_date))
        
        if historical_data.empty:
            return {
                'success': False,
                'error': f'No historical data found for {symbol}'
            }
        
        # Convert to JSON-serializable format
        historical_json = historical_data.reset_index().to_dict('records')
        
        # Calculate summary statistics
        returns = historical_data['Returns'].dropna()
        summary_stats = {
            'total_return': ((historical_data['Close'].iloc[-1] / historical_data['Close'].iloc[0]) - 1) * 100,
            'annualized_return': (((historical_data['Close'].iloc[-1] / historical_data['Close'].iloc[0]) ** (252 / len(historical_data))) - 1) * 100,
            'volatility': returns.std() * np.sqrt(252) * 100,
            'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0,
            'max_drawdown': ((historical_data['Close'] / historical_data['Close'].cummax()) - 1).min() * 100,
            'data_points': len(historical_data),
            'start_date': historical_data.index[0].strftime('%Y-%m-%d'),
            'end_date': historical_data.index[-1].strftime('%Y-%m-%d')
        }
        
        return {
            'success': True,
            'data': {
                'symbol': symbol,
                'historical_data': historical_json[-252:],  # Last year of data for performance
                'summary_statistics': summary_stats,
                'current_price': historical_data['Close'].iloc[-1],
                'average_volume': int(historical_data['Volume'].mean())
            },
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in historical analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_fix_market_data():
    """Get real-time market data via FIX protocol"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return {
                'success': False,
                'error': 'At least one symbol is required'
            }
        
        if not isinstance(symbols, list) or len(symbols) > 50:
            return {
                'success': False,
                'error': 'Symbols must be a list with maximum 50 items'
            }
        
        market_data = run_async(options_service.get_bulk_market_data(symbols))
        
        return {
            'success': True,
            'data': market_data,
            'timestamp': datetime.now().isoformat(),
            'session_info': 'FIX.4.4 Protocol Session'
        }
        
    except Exception as e:
        logger.error(f"Error getting FIX market data: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }