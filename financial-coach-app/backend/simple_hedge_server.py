#!/usr/bin/env python3
"""
Simple Flask server for hedge investments functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Mock data for contracts
MOCK_CONTRACTS = {
    'us_markets': [
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology', 'current_price': 175.50, 'change': 2.30, 'change_percent': 1.33, 'market_status': 'OPEN'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology', 'current_price': 285.20, 'change': -1.80, 'change_percent': -0.63, 'market_status': 'OPEN'},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology', 'current_price': 125.40, 'change': 3.20, 'change_percent': 2.62, 'market_status': 'OPEN'},
        {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'current_price': 135.80, 'change': -2.10, 'change_percent': -1.52, 'market_status': 'OPEN'},
        {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Automotive', 'current_price': 245.30, 'change': 8.70, 'change_percent': 3.68, 'market_status': 'OPEN'},
        {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'sector': 'Technology', 'current_price': 420.15, 'change': 12.50, 'change_percent': 3.06, 'market_status': 'OPEN'},
        {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'sector': 'Technology', 'current_price': 295.80, 'change': -4.20, 'change_percent': -1.40, 'market_status': 'OPEN'},
        {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'sector': 'Communication Services', 'current_price': 385.60, 'change': 7.90, 'change_percent': 2.09, 'market_status': 'OPEN'},
        {'symbol': 'AMD', 'name': 'Advanced Micro Devices', 'sector': 'Technology', 'current_price': 98.40, 'change': -1.60, 'change_percent': -1.60, 'market_status': 'OPEN'},
        {'symbol': 'ORCL', 'name': 'Oracle Corp.', 'sector': 'Technology', 'current_price': 112.75, 'change': 1.25, 'change_percent': 1.12, 'market_status': 'OPEN'}
    ],
    'sa_markets': [
        {'symbol': 'SBK.JO', 'name': 'Standard Bank Group Ltd', 'sector': 'Financial Services', 'current_price': 185.20, 'change': 3.40, 'change_percent': 1.87, 'market_status': 'OPEN'},
        {'symbol': 'NED.JO', 'name': 'Nedbank Group Ltd', 'sector': 'Financial Services', 'current_price': 167.50, 'change': -2.10, 'change_percent': -1.24, 'market_status': 'OPEN'},
        {'symbol': 'FSR.JO', 'name': 'FirstRand Ltd', 'sector': 'Financial Services', 'current_price': 62.80, 'change': 1.20, 'change_percent': 1.95, 'market_status': 'OPEN'},
        {'symbol': 'ABG.JO', 'name': 'ABSA Group Ltd', 'sector': 'Financial Services', 'current_price': 168.40, 'change': -1.80, 'change_percent': -1.06, 'market_status': 'OPEN'},
        {'symbol': 'MTN.JO', 'name': 'MTN Group Ltd', 'sector': 'Telecommunications', 'current_price': 89.30, 'change': 2.10, 'change_percent': 2.41, 'market_status': 'OPEN'},
        {'symbol': 'VOD.JO', 'name': 'Vodacom Group Ltd', 'sector': 'Telecommunications', 'current_price': 145.60, 'change': -0.90, 'change_percent': -0.61, 'market_status': 'OPEN'},
        {'symbol': 'NPN.JO', 'name': 'Naspers Ltd', 'sector': 'Technology', 'current_price': 3250.00, 'change': 85.00, 'change_percent': 2.69, 'market_status': 'OPEN'},
        {'symbol': 'PRX.JO', 'name': 'Prosus NV', 'sector': 'Technology', 'current_price': 890.50, 'change': 22.30, 'change_percent': 2.57, 'market_status': 'OPEN'},
        {'symbol': 'SOL.JO', 'name': 'Sasol Ltd', 'sector': 'Energy', 'current_price': 325.80, 'change': -8.40, 'change_percent': -2.51, 'market_status': 'OPEN'},
        {'symbol': 'AGL.JO', 'name': 'Anglo American Plc', 'sector': 'Mining', 'current_price': 425.60, 'change': 12.80, 'change_percent': 3.10, 'market_status': 'OPEN'}
    ]
}

def generate_random_price_update(base_price):
    """Generate random price with realistic movement"""
    change_percent = random.uniform(-5, 5)
    change = base_price * (change_percent / 100)
    new_price = base_price + change
    return {
        'price': round(new_price, 2),
        'change': round(change, 2),
        'change_percent': round(change_percent, 2),
        'volume': random.randint(10000, 1000000),
        'bid_price': round(new_price - 0.05, 2),
        'ask_price': round(new_price + 0.05, 2)
    }

@app.route('/api/hedge/contracts', methods=['GET'])
def get_contracts():
    """Get all market contracts"""
    try:
        # Add some random price movements
        contracts = MOCK_CONTRACTS.copy()
        for market in ['us_markets', 'sa_markets']:
            for contract in contracts[market]:
                updates = generate_random_price_update(contract['current_price'])
                contract.update(updates)
        
        return jsonify({
            'success': True,
            'data': contracts,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting contracts: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hedge/options-chain', methods=['POST'])
def get_options_chain():
    """Get options chain for a symbol"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'Symbol is required'
            }), 400
        
        # Find the current price from our contracts
        current_price = 100.0  # Default
        for market in ['us_markets', 'sa_markets']:
            for contract in MOCK_CONTRACTS[market]:
                if contract['symbol'] == symbol:
                    current_price = contract['current_price']
                    break
        
        # Generate options chain
        calls = []
        puts = []
        
        # Generate strikes around current price
        strikes = []
        for i in range(-5, 6):  # 11 strikes total
            strike = round(current_price + (current_price * 0.05 * i), 2)
            strikes.append(strike)
        
        for strike in strikes:
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
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'current_price': current_price,
                'calls': calls,
                'puts': puts,
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting options chain: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hedge/fix-market-data', methods=['POST'])
def get_fix_market_data():
    """Get market data for multiple symbols"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'At least one symbol is required'
            }), 400
        
        market_data = {}
        for symbol in symbols:
            # Find base price
            base_price = 100.0
            for market in ['us_markets', 'sa_markets']:
                for contract in MOCK_CONTRACTS[market]:
                    if contract['symbol'] == symbol:
                        base_price = contract['current_price']
                        break
            
            # Generate live data
            updates = generate_random_price_update(base_price)
            market_data[symbol] = {
                'symbol': symbol,
                'last_price': updates['price'],
                'change': updates['change'],
                'change_percent': updates['change_percent'],
                'volume': updates['volume'],
                'bid_price': updates['bid_price'],
                'ask_price': updates['ask_price'],
                'market_status': 'OPEN',
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify({
            'success': True,
            'data': market_data,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting market data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hedge/portfolio-analysis', methods=['POST'])
def get_portfolio_analysis():
    """Analyze portfolio performance"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'At least one symbol is required'
            }), 400
        
        # Generate mock analysis
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
        
        return jsonify({
            'success': True,
            'data': {
                'total_return': round(total_return, 2),
                'annualized_return': round(annualized_return, 2),
                'volatility': round(volatility, 2),
                'sharpe_ratio': round(sharpe_ratio, 3),
                'max_drawdown': round(max_drawdown, 2),
                'win_rate': round(win_rate, 1),
                'contracts': contracts,
                'analysis_date': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/hedge/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'services': {
            'contracts': 'operational',
            'options': 'operational',
            'portfolio_analysis': 'operational',
            'fix_protocol': 'simulated'
        },
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Hedge Investments API is running!',
        'endpoints': [
            '/api/hedge/contracts',
            '/api/hedge/options-chain',
            '/api/hedge/fix-market-data',
            '/api/hedge/portfolio-analysis',
            '/api/hedge/health'
        ]
    })

if __name__ == '__main__':
    logger.info("Starting Hedge Investments API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)