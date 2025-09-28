"""
Simple Hedge Controller
Uses the simple options service without complex dependencies
"""

from flask import request, jsonify
from services.simple_options_service import SimpleOptionsService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize service
options_service = SimpleOptionsService()

def get_market_contracts():
    """Get all market contracts"""
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
        if not data:
            return {
                'success': False,
                'error': 'Request body is required'
            }
            
        symbol = data.get('symbol')
        
        if not symbol:
            return {
                'success': False,
                'error': 'Symbol is required'
            }
        
        logger.info(f"Getting options chain for {symbol}")
        options_data = options_service.get_options_chain(symbol)
        
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
        if not data:
            return {
                'success': False,
                'error': 'Request body is required'
            }
            
        symbol = data.get('symbol')
        strike = data.get('strike')
        expiry = data.get('expiry')
        
        if not all([symbol, strike, expiry]):
            return {
                'success': False,
                'error': 'Symbol, strike, and expiry are required'
            }
        
        try:
            strike = float(strike)
        except (ValueError, TypeError):
            return {
                'success': False,
                'error': 'Strike price must be a number'
            }
        
        strategy_analysis = options_service.calculate_long_strap_strategy(symbol, strike, expiry)
        
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
        if not data:
            return {
                'success': False,
                'error': 'Request body is required'
            }
            
        symbols = data.get('symbols', [])
        
        if not symbols:
            return {
                'success': False,
                'error': 'At least one symbol is required'
            }
        
        if not isinstance(symbols, list) or len(symbols) > 20:
            return {
                'success': False,
                'error': 'Symbols must be a list with maximum 20 items'
            }
        
        portfolio_analysis = options_service.get_portfolio_analysis(symbols)
        
        if 'error' in portfolio_analysis:
            return {
                'success': False,
                'error': portfolio_analysis['error']
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
        if not data:
            return {
                'success': False,
                'error': 'Request body is required'
            }
            
        symbol = data.get('symbol')
        
        if not symbol:
            return {
                'success': False,
                'error': 'Symbol is required'
            }
        
        # Mock historical analysis
        return {
            'success': True,
            'data': {
                'symbol': symbol,
                'total_return': round(random.uniform(-20, 30), 2),
                'annualized_return': round(random.uniform(-15, 25), 2),
                'volatility': round(random.uniform(15, 40), 2),
                'sharpe_ratio': round(random.uniform(-0.5, 2.5), 3),
                'max_drawdown': round(random.uniform(-30, -5), 2),
                'analysis_period': '5 years',
                'data_points': 1260
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
    """Get real-time market data via FIX protocol simulation"""
    try:
        data = request.get_json()
        if not data:
            return {
                'success': False,
                'error': 'Request body is required'
            }
            
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
        
        market_data = options_service.get_bulk_market_data(symbols)
        
        if 'error' in market_data:
            return {
                'success': False,
                'error': market_data['error']
            }
        
        return {
            'success': True,
            'data': market_data,
            'timestamp': datetime.now().isoformat(),
            'session_info': 'FIX.4.4 Protocol Simulation'
        }
        
    except Exception as e:
        logger.error(f"Error getting FIX market data: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# Import random for historical analysis
import random