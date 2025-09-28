"""
Simple Options Service for Hedge Investments
Mock implementation that doesn't require external dependencies
"""

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleOptionsService:
    def __init__(self):
        """Initialize with mock data"""
        self.market_contracts = {
            'us_markets': [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology', 'current_price': 175.50, 'currency': 'USD'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology', 'current_price': 285.20, 'currency': 'USD'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology', 'current_price': 125.40, 'currency': 'USD'},
                {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'current_price': 135.80, 'currency': 'USD'},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Automotive', 'current_price': 245.30, 'currency': 'USD'},
                {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'sector': 'Technology', 'current_price': 420.15, 'currency': 'USD'},
                {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'sector': 'Technology', 'current_price': 295.80, 'currency': 'USD'},
                {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'sector': 'Communication Services', 'current_price': 385.60, 'currency': 'USD'},
                {'symbol': 'AMD', 'name': 'Advanced Micro Devices', 'sector': 'Technology', 'current_price': 98.40, 'currency': 'USD'},
                {'symbol': 'ORCL', 'name': 'Oracle Corp.', 'sector': 'Technology', 'current_price': 112.75, 'currency': 'USD'}
            ],
            'sa_markets': [
                {'symbol': 'SBK.JO', 'name': 'Standard Bank Group Ltd', 'sector': 'Financial Services', 'current_price': 185.20, 'currency': 'ZAR'},
                {'symbol': 'NED.JO', 'name': 'Nedbank Group Ltd', 'sector': 'Financial Services', 'current_price': 167.50, 'currency': 'ZAR'},
                {'symbol': 'FSR.JO', 'name': 'FirstRand Ltd', 'sector': 'Financial Services', 'current_price': 62.80, 'currency': 'ZAR'},
                {'symbol': 'ABG.JO', 'name': 'ABSA Group Ltd', 'sector': 'Financial Services', 'current_price': 168.40, 'currency': 'ZAR'},
                {'symbol': 'MTN.JO', 'name': 'MTN Group Ltd', 'sector': 'Telecommunications', 'current_price': 89.30, 'currency': 'ZAR'},
                {'symbol': 'VOD.JO', 'name': 'Vodacom Group Ltd', 'sector': 'Telecommunications', 'current_price': 145.60, 'currency': 'ZAR'},
                {'symbol': 'NPN.JO', 'name': 'Naspers Ltd', 'sector': 'Technology', 'current_price': 3250.00, 'currency': 'ZAR'},
                {'symbol': 'PRX.JO', 'name': 'Prosus NV', 'sector': 'Technology', 'current_price': 890.50, 'currency': 'ZAR'},
                {'symbol': 'SOL.JO', 'name': 'Sasol Ltd', 'sector': 'Energy', 'current_price': 325.80, 'currency': 'ZAR'},
                {'symbol': 'AGL.JO', 'name': 'Anglo American Plc', 'sector': 'Mining', 'current_price': 425.60, 'currency': 'ZAR'}
            ]
        }

    def get_market_contracts(self) -> Dict:
        """Get all market contracts with live price updates"""
        contracts = self.market_contracts.copy()
        
        # Add random price movements
        for market_type in ['us_markets', 'sa_markets']:
            for contract in contracts[market_type]:
                base_price = contract['current_price']
                change_percent = random.uniform(-5, 5)
                change = base_price * (change_percent / 100)
                new_price = base_price + change
                
                # Preserve the original currency when updating
                contract.update({
                    'current_price': round(new_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'volume': random.randint(10000, 1000000),
                    'market_status': 'OPEN',
                    'bid_price': round(new_price - 0.05, 2),
                    'ask_price': round(new_price + 0.05, 2),
                    'currency': contract.get('currency', 'USD')  # Preserve currency
                })
        
        return contracts

    def get_options_chain(self, symbol: str) -> Dict:
        """Generate options chain for a symbol"""
        try:
            logger.info(f"Generating options chain for {symbol}")
            
            # Find current price and currency for the symbol
            current_price = 100.0  # Default
            currency = 'USD'  # Default
            for market_type in ['us_markets', 'sa_markets']:
                for contract in self.market_contracts[market_type]:
                    if contract['symbol'] == symbol:
                        current_price = contract['current_price']
                        currency = contract.get('currency', 'USD')
                        break
            
            # Generate realistic options data
            calls = []
            puts = []
            
            # Generate strike prices around current price
            strikes = []
            for i in range(-5, 6):  # 11 strikes: -25% to +25%
                strike = round(current_price * (1 + i * 0.05), 2)
                strikes.append(strike)
            
            # Generate options for each strike
            for strike in strikes:
                # Call option
                moneyness_call = (current_price - strike) / current_price
                call_premium = max(0.10, current_price * 0.02 + max(0, moneyness_call * current_price) + random.uniform(0.5, 3.0))
                
                calls.append({
                    'strike': strike,
                    'premium': round(call_premium, 2),
                    'implied_volatility': round(random.uniform(0.15, 0.45), 3),
                    'delta': round(max(0.01, min(0.99, 0.5 + moneyness_call)), 3),
                    'volume': random.randint(10, 1000),
                    'open_interest': random.randint(50, 5000)
                })
                
                # Put option
                moneyness_put = (strike - current_price) / current_price
                put_premium = max(0.10, current_price * 0.02 + max(0, moneyness_put * current_price) + random.uniform(0.5, 3.0))
                
                puts.append({
                    'strike': strike,
                    'premium': round(put_premium, 2),
                    'implied_volatility': round(random.uniform(0.15, 0.45), 3),
                    'delta': round(max(-0.99, min(-0.01, -0.5 + moneyness_call)), 3),
                    'volume': random.randint(10, 1000),
                    'open_interest': random.randint(50, 5000)
                })
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'currency': currency,
                'calls': calls,
                'puts': puts,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating options chain for {symbol}: {str(e)}")
            raise e

    def calculate_long_strap_strategy(self, symbol: str, strike: float, expiry: str) -> Dict:
        """Calculate long strap strategy (2 calls + 1 put)"""
        try:
            options_data = self.get_options_chain(symbol)
            current_price = options_data['current_price']
            
            # Find options at the specified strike
            call_premium = 0
            put_premium = 0
            
            for call_option in options_data['calls']:
                if abs(call_option['strike'] - strike) < 0.01:
                    call_premium = call_option['premium']
                    break
            
            for put_option in options_data['puts']:
                if abs(put_option['strike'] - strike) < 0.01:
                    put_premium = put_option['premium']
                    break
            
            # Calculate strategy cost (2 calls + 1 put)
            strategy_cost = (2 * call_premium) + put_premium
            
            # Calculate breakeven points
            upper_breakeven = strike + strategy_cost
            lower_breakeven = strike - strategy_cost
            
            # Calculate profit/loss at various price points
            price_points = []
            for i in range(int(strike * 0.7), int(strike * 1.3), int(strike * 0.05)):
                price = float(i)
                
                # Calculate payoff
                call_payoff = max(0, price - strike) * 2  # 2 calls
                put_payoff = max(0, strike - price)  # 1 put
                total_payoff = call_payoff + put_payoff - strategy_cost
                
                price_points.append({
                    'price': price,
                    'payoff': round(total_payoff, 2)
                })
            
            return {
                'symbol': symbol,
                'strategy': 'Long Strap',
                'strike': strike,
                'expiry': expiry,
                'current_price': current_price,
                'currency': options_data.get('currency', 'USD'),
                'strategy_cost': round(strategy_cost, 2),
                'max_loss': round(-strategy_cost, 2),
                'upper_breakeven': round(upper_breakeven, 2),
                'lower_breakeven': round(lower_breakeven, 2),
                'profit_loss_chart': price_points,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating long strap for {symbol}: {str(e)}")
            return {'error': str(e)}

    def get_portfolio_analysis(self, symbols: List[str]) -> Dict:
        """Analyze portfolio of symbols"""
        try:
            contracts = []
            total_value = 0
            
            for symbol in symbols:
                # Get current price and currency
                current_price = 100.0
                currency = 'USD'
                for market_type in ['us_markets', 'sa_markets']:
                    for contract in self.market_contracts[market_type]:
                        if contract['symbol'] == symbol:
                            current_price = contract['current_price']
                            currency = contract.get('currency', 'USD')
                            break
                
                # Generate mock performance data
                annual_return = random.uniform(-15, 25)
                volatility = random.uniform(15, 35)
                sharpe_ratio = random.uniform(-0.5, 2.0)
                
                contract_data = {
                    'symbol': symbol,
                    'current_price': current_price,
                    'currency': currency,
                    'return': round(annual_return, 2),
                    'volatility': round(volatility, 2),
                    'sharpe_ratio': round(sharpe_ratio, 3),
                    'risk_level': 'Low' if volatility < 20 else 'Medium' if volatility < 30 else 'High',
                    'portfolio_weight': round(100.0 / len(symbols), 1)
                }
                contracts.append(contract_data)
                total_value += current_price
            
            # Calculate portfolio-level metrics
            portfolio_return = sum(c['return'] * c['portfolio_weight'] / 100 for c in contracts)
            portfolio_volatility = (sum((c['volatility'] * c['portfolio_weight'] / 100) ** 2 for c in contracts)) ** 0.5
            portfolio_sharpe = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
            
            return {
                'total_return': round(portfolio_return, 2),
                'annualized_return': round(portfolio_return * 0.8, 2),  # Slightly lower
                'volatility': round(portfolio_volatility, 2),
                'sharpe_ratio': round(portfolio_sharpe, 3),
                'max_drawdown': round(random.uniform(-25, -5), 2),
                'win_rate': round(random.uniform(45, 75), 1),
                'contracts': contracts,
                'total_value': round(total_value, 2),
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing portfolio: {str(e)}")
            return {'error': str(e)}

    def get_bulk_market_data(self, symbols: List[str]) -> Dict:
        """Get market data for multiple symbols"""
        try:
            market_data = {}
            
            for symbol in symbols:
                # Find base price and currency
                base_price = 100.0
                currency = 'USD'
                for market_type in ['us_markets', 'sa_markets']:
                    for contract in self.market_contracts[market_type]:
                        if contract['symbol'] == symbol:
                            base_price = contract['current_price']
                            currency = contract.get('currency', 'USD')
                            break
                
                # Generate live market data
                change_percent = random.uniform(-5, 5)
                change = base_price * (change_percent / 100)
                current_price = base_price + change
                
                market_data[symbol] = {
                    'symbol': symbol,
                    'last_price': round(current_price, 2),
                    'currency': currency,
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'volume': random.randint(10000, 1000000),
                    'bid_price': round(current_price - 0.05, 2),
                    'ask_price': round(current_price + 0.05, 2),
                    'market_status': 'OPEN',
                    'timestamp': datetime.now().isoformat()
                }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error getting bulk market data: {str(e)}")
            return {'error': str(e)}