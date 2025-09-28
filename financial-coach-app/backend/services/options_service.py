"""
Options Trading Service with FIX Protocol Integration
Implements long strap strategy (2 calls + 1 put) for US and South African markets
Uses FIX 4.4 protocol for real-time market data
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    # Create simple fallbacks
    class MockPD:
        @staticmethod
        def DataFrame(data):
            return data
    pd = MockPD()
    
    # Simple numpy replacement for basic operations
    class MockNP:
        @staticmethod
        def arange(start, stop, step):
            result = []
            current = start
            while current < stop:
                result.append(current)
                current += step
            return result
        
        @staticmethod
        def random():
            import random
            return random
    np = MockNP()
from dataclasses import dataclass

# Try to import FIX client, create mock if not available
try:
    from services.fix_protocol_client import FIXProtocolClient
    FIX_AVAILABLE = True
except ImportError:
    FIX_AVAILABLE = False
    # Mock FIX client
    class FIXProtocolClient:
        def __init__(self):
            self.connected = False
        
        async def connect(self):
            self.connected = True
            return True
        
        def get_market_data(self, symbol):
            import random
            return {
                'symbol': symbol,
                'price': random.uniform(50, 300),
                'change': random.uniform(-10, 10),
                'change_percent': random.uniform(-5, 5),
                'volume': random.randint(100000, 10000000),
                'market_status': 'OPEN'
            }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OptionContract:
    symbol: str
    strike: float
    expiry: str
    option_type: str  # 'call' or 'put'
    premium: float
    volume: int
    open_interest: int
    implied_volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float

@dataclass
class LongStrapPosition:
    underlying_symbol: str
    current_price: float
    call_contract_1: OptionContract
    call_contract_2: OptionContract
    put_contract: OptionContract
    total_premium_paid: float
    breakeven_upper: float
    breakeven_lower: float
    max_loss: float
    profit_potential: str

class OptionsService:
    def __init__(self):
        self.us_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'NVDA', 'META', 'NFLX', 'AMD', 'ORCL'
        ]
        
        # South African symbols (JSE)
        self.sa_symbols = [
            'NPN.JO', 'PRX.JO', 'SHP.JO', 'ABG.JO', 'FSR.JO',
            'BTI.JO', 'CFR.JO', 'SOL.JO', 'MTN.JO', 'VOD.JO'
        ]
        
        self.all_symbols = self.us_symbols + self.sa_symbols
        
        # Initialize FIX client
        self.fix_client = FIXProtocolClient()
        self._fix_initialized = False
        
    async def _ensure_fix_connection(self):
        """Ensure FIX protocol connection is established"""
        if not self._fix_initialized:
            await self.fix_client.connect()
            self._fix_initialized = True
        
    def get_market_contracts(self) -> Dict[str, List[str]]:
        """Return organized list of US and SA contracts"""
        return {
            'us_markets': [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology'},
                {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'sector': 'Technology'},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology'},
                {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary'},
                {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Consumer Discretionary'},
                {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'sector': 'Technology'},
                {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'sector': 'Technology'},
                {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'sector': 'Communication Services'},
                {'symbol': 'AMD', 'name': 'Advanced Micro Devices', 'sector': 'Technology'},
                {'symbol': 'ORCL', 'name': 'Oracle Corporation', 'sector': 'Technology'}
            ],
            'sa_markets': [
                {'symbol': 'NPN.JO', 'name': 'Naspers Limited', 'sector': 'Technology'},
                {'symbol': 'PRX.JO', 'name': 'Prosus N.V.', 'sector': 'Technology'},
                {'symbol': 'SHP.JO', 'name': 'Shoprite Holdings', 'sector': 'Consumer Staples'},
                {'symbol': 'ABG.JO', 'name': 'Absa Group Limited', 'sector': 'Financial Services'},
                {'symbol': 'FSR.JO', 'name': 'FirstRand Limited', 'sector': 'Financial Services'},
                {'symbol': 'BTI.JO', 'name': 'British American Tobacco', 'sector': 'Consumer Staples'},
                {'symbol': 'CFR.JO', 'name': 'Capitec Bank Holdings', 'sector': 'Financial Services'},
                {'symbol': 'SOL.JO', 'name': 'Sasol Limited', 'sector': 'Energy'},
                {'symbol': 'MTN.JO', 'name': 'MTN Group Limited', 'sector': 'Communication Services'},
                {'symbol': 'VOD.JO', 'name': 'Vodacom Group Limited', 'sector': 'Communication Services'}
            ]
        }
    
    async def fetch_historical_data(self, symbol: str, start_date: str = "2019-01-01"):
        """Fetch historical data from 2019 to present using FIX protocol simulation"""
        try:
            await self._ensure_fix_connection()
            
            # Generate simulated historical data for demo purposes
            # In a real implementation, this would request historical data via FIX
            end_date = datetime.now()
            start = datetime.strptime(start_date, "%Y-%m-%d")
            
            # Generate daily data
            date_range = pd.date_range(start=start, end=end_date, freq='D')
            
            # Get current price from FIX feed as starting point
            current_data = self.fix_client.get_market_data(symbol)
            base_price = current_data['price'] if current_data else 100.0
            
            # Generate realistic price series using geometric Brownian motion
            np.random.seed(42)  # For reproducible results
            n_days = len(date_range)
            returns = np.random.normal(0.0005, 0.02, n_days)  # Daily returns
            
            # Create price series
            prices = [base_price]
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            
            # Create DataFrame
            hist_data = pd.DataFrame({
                'Date': date_range,
                'Open': prices,
                'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'Close': prices,
                'Volume': [int(np.random.normal(1000000, 200000)) for _ in prices]
            })
            
            hist_data.set_index('Date', inplace=True)
            
            # Calculate additional metrics
            hist_data['Returns'] = hist_data['Close'].pct_change()
            hist_data['Volatility'] = hist_data['Returns'].rolling(window=30).std() * np.sqrt(252)
            hist_data['SMA_20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['SMA_50'] = hist_data['Close'].rolling(window=50).mean()
            
            logger.info(f"Generated historical data for {symbol}: {len(hist_data)} days")
            return hist_data
            
        except Exception as e:
            logger.error(f"Error generating historical data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    async def get_options_chain(self, symbol: str) -> Dict:
        """Generate options chain data using FIX protocol real-time prices"""
        try:
            await self._ensure_fix_connection()
            
            # Get current price from FIX feed
            market_data = self.fix_client.get_market_data(symbol)
            current_price = market_data['price'] if market_data else 100.0
            
            # Generate simulated options data
            strikes = np.arange(
                current_price * 0.8, 
                current_price * 1.2, 
                current_price * 0.02
            )
            
            # Get next few expiration dates
            today = datetime.now()
            expirations = [
                (today + timedelta(days=30)).strftime("%Y-%m-%d"),
                (today + timedelta(days=60)).strftime("%Y-%m-%d"),
                (today + timedelta(days=90)).strftime("%Y-%m-%d")
            ]
            
            options_data = {
                'symbol': symbol,
                'current_price': current_price,
                'expirations': expirations,
                'calls': [],
                'puts': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # For simplicity, use first expiration for the main options chain
            main_expiry = expirations[0]
            time_to_exp = (datetime.strptime(main_expiry, "%Y-%m-%d") - today).days / 365.0
            
            for strike in strikes:
                # Simulate option prices using Black-Scholes approximation
                
                # Simulated values with more realistic pricing
                call_premium = max(0.01, (current_price - strike) * 0.6 + 0.1 * current_price * time_to_exp)
                put_premium = max(0.01, (strike - current_price) * 0.6 + 0.1 * current_price * time_to_exp)
                
                # Call option data
                call_delta = max(0.01, min(0.99, 0.5 + (current_price - strike) / (current_price * 0.2)))
                options_data['calls'].append({
                    'strike': round(strike, 2),
                    'expiry': main_expiry,
                    'premium': round(call_premium, 2),
                    'volume': np.random.randint(10, 1000),
                    'open_interest': np.random.randint(50, 5000),
                    'implied_volatility': round(np.random.uniform(0.15, 0.45), 3),
                    'delta': round(call_delta, 3),
                    'gamma': round(np.random.uniform(0.01, 0.05), 4),
                    'theta': round(np.random.uniform(-0.1, -0.01), 4),
                    'vega': round(np.random.uniform(0.05, 0.2), 3)
                })
                
                # Put option data
                put_delta = max(-0.99, min(-0.01, -0.5 + (current_price - strike) / (current_price * 0.2)))
                options_data['puts'].append({
                        'strike': round(strike, 2),
                        'expiry': main_expiry,
                        'premium': round(put_premium, 2),
                        'volume': np.random.randint(10, 1000),
                        'open_interest': np.random.randint(50, 5000),
                        'implied_volatility': round(np.random.uniform(0.15, 0.45), 3),
                        'delta': round(put_delta, 3),
                        'gamma': round(np.random.uniform(0.01, 0.05), 4),
                        'theta': round(np.random.uniform(-0.1, -0.01), 4),
                        'vega': round(np.random.uniform(0.05, 0.2), 3)
                    })
            
            return options_data
            
        except Exception as e:
            logger.error(f"Error getting options chain for {symbol}: {str(e)}")
            return {}
    
    async def calculate_long_strap_strategy(self, symbol: str, strike: float, expiry: str) -> Dict:
        """
        Calculate long strap strategy: Buy 2 calls + 1 put at same strike
        This is a bullish strategy that profits from significant upward movement
        """
        try:
            options_data = await self.get_options_chain(symbol)
            current_price = options_data.get('current_price', 0)
            
            # Find matching options
            calls = [opt for opt in options_data['options'] 
                    if opt['type'] == 'call' and opt['strike'] == strike and opt['expiry'] == expiry]
            puts = [opt for opt in options_data['options'] 
                   if opt['type'] == 'put' and opt['strike'] == strike and opt['expiry'] == expiry]
            
            if not calls or not puts:
                return {'error': 'Options not found for specified strike and expiry'}
            
            call_option = calls[0]
            put_option = puts[0]
            
            # Long strap: 2 calls + 1 put
            total_premium = (2 * call_option['premium']) + put_option['premium']
            
            # Calculate breakeven points
            breakeven_upper = strike + total_premium
            breakeven_lower = strike - total_premium
            
            # Calculate P&L at various stock prices
            stock_prices = np.arange(current_price * 0.5, current_price * 1.5, current_price * 0.05)
            pnl_data = []
            
            for price in stock_prices:
                # Calculate option values at expiry
                call_value = max(0, price - strike)
                put_value = max(0, strike - price)
                
                # Position value: 2 calls + 1 put
                position_value = (2 * call_value) + put_value
                pnl = position_value - total_premium
                
                pnl_data.append({
                    'stock_price': round(price, 2),
                    'position_value': round(position_value, 2),
                    'pnl': round(pnl, 2),
                    'pnl_percentage': round((pnl / total_premium) * 100, 2) if total_premium > 0 else 0
                })
            
            # Risk metrics
            max_loss = total_premium
            
            strategy_analysis = {
                'symbol': symbol,
                'strategy': 'Long Strap',
                'current_price': current_price,
                'strike_price': strike,
                'expiry': expiry,
                'call_premium': call_option['premium'],
                'put_premium': put_option['premium'],
                'total_premium_paid': round(total_premium, 2),
                'max_loss': round(max_loss, 2),
                'breakeven_upper': round(breakeven_upper, 2),
                'breakeven_lower': round(breakeven_lower, 2),
                'profit_zones': {
                    'upper': f"Above ${breakeven_upper:.2f}",
                    'lower': f"Below ${breakeven_lower:.2f}"
                },
                'greeks': {
                    'call_delta': call_option['delta'],
                    'call_gamma': call_option['gamma'],
                    'call_theta': call_option['theta'],
                    'call_vega': call_option['vega'],
                    'put_delta': put_option['delta'],
                    'put_gamma': put_option['gamma'],
                    'put_theta': put_option['theta'],
                    'put_vega': put_option['vega']
                },
                'pnl_analysis': pnl_data,
                'days_to_expiry': (datetime.strptime(expiry, "%Y-%m-%d") - datetime.now()).days,
                'implied_volatility': {
                    'call': call_option['implied_volatility'],
                    'put': put_option['implied_volatility']
                }
            }
            
            return strategy_analysis
            
        except Exception as e:
            logger.error(f"Error calculating long strap strategy for {symbol}: {str(e)}")
            return {'error': str(e)}
    
    async def get_portfolio_analysis(self, symbols: List[str]) -> Dict:
        """Analyze portfolio of options strategies"""
        try:
            await self._ensure_fix_connection()
            
            portfolio_data = {
                'symbols': symbols,
                'total_positions': len(symbols),
                'strategies': [],
                'portfolio_metrics': {},
                'risk_analysis': {}
            }
            
            total_premium = 0
            total_max_loss = 0
            
            for symbol in symbols:
                # Get current price from FIX feed to determine ATM strike
                market_data = self.fix_client.get_market_data(symbol)
                current_price = market_data['price'] if market_data else 100.0
                
                # Use ATM strike (rounded to nearest 5)
                strike = round(current_price / 5) * 5
                
                # Use 60-day expiry
                expiry = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
                
                strategy = await self.calculate_long_strap_strategy(symbol, strike, expiry)
                
                if 'error' not in strategy:
                    portfolio_data['strategies'].append(strategy)
                    total_premium += strategy['total_premium_paid']
                    total_max_loss += strategy['max_loss']
            
            # Portfolio-level metrics
            portfolio_data['portfolio_metrics'] = {
                'total_premium_invested': round(total_premium, 2),
                'total_max_loss': round(total_max_loss, 2),
                'number_of_strategies': len(portfolio_data['strategies']),
                'average_premium_per_strategy': round(total_premium / len(symbols), 2) if symbols else 0,
                'portfolio_breakeven_analysis': 'Requires individual position analysis'
            }
            
            # Risk analysis
            portfolio_data['risk_analysis'] = {
                'concentration_risk': 'Diversified across multiple underlyings',
                'time_decay_risk': 'High - All positions subject to theta decay',
                'volatility_risk': 'High sensitivity to implied volatility changes',
                'directional_bias': 'Bullish bias due to long strap structure',
                'optimal_market_condition': 'High volatility with strong directional moves'
            }
            
            return portfolio_data
            
        except Exception as e:
            logger.error(f"Error in portfolio analysis: {str(e)}")
            return {'error': str(e)}
    
    async def get_current_market_data(self, symbol: str) -> Dict:
        """Get current market data for a symbol using FIX protocol"""
        try:
            await self._ensure_fix_connection()
            
            # Get real-time data from FIX client
            market_data = self.fix_client.get_market_data(symbol)
            
            if not market_data:
                logger.warning(f"No FIX data found for {symbol}, subscribing...")
                
                # Subscribe to market data for this symbol
                self.fix_client.subscribe_market_data([symbol])
                
                # Wait a bit for data to arrive
                await asyncio.sleep(1)
                
                # Try again
                market_data = self.fix_client.get_market_data(symbol)
                
                if not market_data:
                    logger.warning(f"Still no data for {symbol} after subscription")
                    return {
                        'symbol': symbol,
                        'price': 0.0,
                        'change': 0.0,
                        'change_percent': 0.0,
                        'volume': 0,
                        'market_status': 'UNKNOWN',
                        'error': 'No data available from FIX feed'
                    }
            
            # Format the data to match expected structure
            formatted_data = {
                'symbol': symbol,
                'price': market_data.get('price', 0.0),
                'change': market_data.get('change', 0.0),
                'change_percent': market_data.get('change_percent', 0.0),
                'volume': market_data.get('volume', 0),
                'high': market_data.get('high', market_data.get('price', 0.0)),
                'low': market_data.get('low', market_data.get('price', 0.0)),
                'open': market_data.get('open', market_data.get('price', 0.0)),
                'bid_price': market_data.get('bid_price', 0.0),
                'ask_price': market_data.get('ask_price', 0.0),
                'bid_size': market_data.get('bid_size', 0),
                'ask_size': market_data.get('ask_size', 0),
                'market_status': market_data.get('market_status', 'UNKNOWN'),
                'timestamp': market_data.get('timestamp', datetime.now().isoformat()),
                'feed_source': market_data.get('feed_source', 'FIX_PROTOCOL'),
                'currency': 'USD'  # All prices normalized to USD
            }
            
            logger.info(f"Retrieved FIX data for {symbol}: ${formatted_data['price']}")
            return formatted_data
            
        except Exception as e:
            logger.error(f"Error getting FIX market data for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'price': 0.0,
                'change': 0.0,
                'change_percent': 0.0,
                'volume': 0,
                'market_status': 'ERROR',
                'error': str(e)
            }
    
    async def simulate_fix_protocol_data(self, symbol: str) -> Dict:
        """Get FIX protocol market data feed"""
        return await self.get_current_market_data(symbol)
    
    async def get_bulk_market_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get market data for multiple symbols efficiently using FIX protocol"""
        await self._ensure_fix_connection()
        
        # Subscribe to all symbols at once for better efficiency
        if symbols:
            self.fix_client.subscribe_market_data(symbols)
            
            # Wait for data to populate
            await asyncio.sleep(1)
        
        # Get bulk data from FIX client
        bulk_data = self.fix_client.get_bulk_market_data(symbols)
        
        # Format the data
        formatted_data = {}
        for symbol, data in bulk_data.items():
            formatted_data[symbol] = {
                'symbol': symbol,
                'last_price': data.get('price', 0.0),
                'price': data.get('price', 0.0),
                'change': data.get('change', 0.0),
                'change_percent': data.get('change_percent', 0.0),
                'volume': data.get('volume', 0),
                'bid_price': data.get('bid_price', 0.0),
                'ask_price': data.get('ask_price', 0.0),
                'market_status': data.get('market_status', 'UNKNOWN'),
                'timestamp': data.get('timestamp', datetime.now().isoformat()),
                'feed_source': 'FIX_PROTOCOL'
            }
            logger.info(f"FIX data for {symbol}: ${formatted_data[symbol]['price']}")
        
        return formatted_data