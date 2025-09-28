"""
Hedge Investments Routes
API endpoints for hedge investment strategies and FIX protocol integration
"""

from flask import Blueprint, request, jsonify
from controllers.simple_hedge_controller import (
    get_market_contracts,
    get_options_chain,
    calculate_long_strap,
    get_portfolio_analysis,
    get_historical_analysis,
    get_fix_market_data
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint for hedge routes
hedge_bp = Blueprint('hedge', __name__, url_prefix='/api/hedge')

@hedge_bp.route('/contracts', methods=['GET'])
def contracts():
    """
    Get all market contracts (US and South African)
    Returns enhanced contract data with current market prices
    """
    try:
        result = get_market_contracts()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in contracts endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/options-chain', methods=['POST'])
def options_chain():
    """
    Get options chain for a specific symbol
    
    Request Body:
    {
        "symbol": "AAPL"
    }
    """
    try:
        result = get_options_chain()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in options-chain endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/long-strap', methods=['POST'])
def long_strap():
    """
    Calculate long strap strategy analysis
    
    Request Body:
    {
        "symbol": "AAPL",
        "strike": 150.0,
        "expiry": "2024-12-20"
    }
    """
    try:
        result = calculate_long_strap()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in long-strap endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/portfolio-analysis', methods=['POST'])
def portfolio_analysis():
    """
    Analyze portfolio of hedge investment strategies
    
    Request Body:
    {
        "symbols": ["AAPL", "MSFT", "GOOGL"]
    }
    """
    try:
        result = get_portfolio_analysis()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in portfolio-analysis endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/historical-analysis', methods=['POST'])
def historical_analysis():
    """
    Get historical analysis for hedge strategies
    
    Request Body:
    {
        "symbol": "AAPL",
        "start_date": "2019-01-01"  // Optional, defaults to 2019-01-01
    }
    """
    try:
        result = get_historical_analysis()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in historical-analysis endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/fix-market-data', methods=['POST'])
def fix_market_data():
    """
    Get real-time market data via FIX protocol
    
    Request Body:
    {
        "symbols": ["AAPL", "MSFT", "GOOGL", "SBK.JO", "NED.JO"]
    }
    """
    try:
        result = get_fix_market_data()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in fix-market-data endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@hedge_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for hedge services
    """
    try:
        from services.simple_options_service import SimpleOptionsService
        
        # Test basic service initialization
        options_service = SimpleOptionsService()
        contracts = options_service.get_market_contracts()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'services': {
                'options_service': 'operational',
                'fix_protocol': 'simulated',
                'contracts_available': len(contracts['us_markets']) + len(contracts['sa_markets'])
            },
            'timestamp': str(datetime.now())
        }), 200
        
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': str(datetime.now())
        }), 500

# Error handlers for the blueprint
@hedge_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'success': False,
        'error': 'Bad request',
        'message': 'Invalid request data or parameters'
    }), 400

@hedge_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Not found',
        'message': 'Endpoint not found'
    }), 404

@hedge_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

# CORS headers for all hedge routes
@hedge_bp.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Import datetime after creating routes to avoid circular imports
from datetime import datetime