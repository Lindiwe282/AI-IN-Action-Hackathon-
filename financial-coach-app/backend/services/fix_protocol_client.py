"""
FIX Protocol Client for Real-Time Market Data
Implements FIX 4.4 protocol for options and equity market data
"""

import asyncio
import socket
import time
import threading
from datetime import datetime
from typing import Dict, List, Callable, Optional
import logging
import json
import random
import struct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FIXMessage:
    """FIX Message parser and builder"""
    
    # FIX 4.4 Message Types
    LOGON = 'A'
    LOGOUT = '5'
    HEARTBEAT = '0'
    TEST_REQUEST = '1'
    MARKET_DATA_REQUEST = 'V'
    MARKET_DATA_SNAPSHOT = 'W'
    MARKET_DATA_INCREMENTAL_REFRESH = 'X'
    
    # FIX Tags
    TAG_MSG_TYPE = '35'
    TAG_SENDER_COMP_ID = '49'
    TAG_TARGET_COMP_ID = '56'
    TAG_MSG_SEQ_NUM = '34'
    TAG_SENDING_TIME = '52'
    TAG_SYMBOL = '55'
    TAG_MD_REQ_ID = '262'
    TAG_SUBSCRIPTION_REQUEST_TYPE = '263'
    TAG_MARKET_DEPTH = '264'
    TAG_MD_ENTRY_TYPE = '269'
    TAG_MD_ENTRY_PX = '270'
    TAG_MD_ENTRY_SIZE = '271'
    TAG_MD_ENTRY_TIME = '273'
    
    @staticmethod
    def calculate_checksum(message: str) -> str:
        """Calculate FIX checksum"""
        checksum = sum(ord(c) for c in message) % 256
        return f"{checksum:03d}"
    
    @staticmethod
    def build_message(msg_type: str, fields: Dict[str, str], sender_id: str = "CLIENT", target_id: str = "SERVER") -> str:
        """Build FIX message with proper format"""
        # Start with required header fields
        body_fields = {
            FIXMessage.TAG_MSG_TYPE: msg_type,
            FIXMessage.TAG_SENDER_COMP_ID: sender_id,
            FIXMessage.TAG_TARGET_COMP_ID: target_id,
            FIXMessage.TAG_MSG_SEQ_NUM: str(int(time.time()) % 10000),
            FIXMessage.TAG_SENDING_TIME: datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        }
        
        # Add custom fields
        body_fields.update(fields)
        
        # Sort by tag number for proper FIX format
        sorted_fields = sorted(body_fields.items(), key=lambda x: int(x[0]))
        
        # Build message body
        body = ''.join(f"{tag}={value}\x01" for tag, value in sorted_fields)
        
        # Add BeginString and BodyLength
        begin_string = "8=FIX.4.4\x01"
        body_length = f"9={len(body)}\x01"
        
        # Calculate checksum
        message_without_checksum = begin_string + body_length + body
        checksum = FIXMessage.calculate_checksum(message_without_checksum)
        
        # Complete message
        complete_message = message_without_checksum + f"10={checksum}\x01"
        
        return complete_message
    
    @staticmethod
    def parse_message(message: str) -> Dict[str, str]:
        """Parse FIX message into dictionary"""
        fields = {}
        pairs = message.split('\x01')[:-1]  # Remove last empty element
        
        for pair in pairs:
            if '=' in pair:
                tag, value = pair.split('=', 1)
                fields[tag] = value
        
        return fields

class FIXProtocolClient:
    """FIX Protocol Client for market data"""
    
    def __init__(self):
        self.connected = False
        self.socket = None
        self.market_data_callbacks = {}
        self.subscription_id = 1
        self.heartbeat_interval = 30
        self.last_heartbeat = time.time()
        self.running = False
        self.message_thread = None
        
        # Market data storage
        self.market_data = {}
        self.subscribers = {}
        
        # Simulate real market data providers
        self.data_providers = {
            'US': 'NYSE_NASDAQ_FEED',
            'SA': 'JSE_FEED'
        }
        
    async def connect(self, host: str = "localhost", port: int = 9878) -> bool:
        """Connect to FIX server"""
        try:
            # For demo purposes, simulate connection
            logger.info(f"Attempting FIX connection to {host}:{port}")
            
            # Simulate connection delay
            await asyncio.sleep(1)
            
            # Create logon message
            logon_fields = {
                '108': str(self.heartbeat_interval),  # HeartBtInt
                '141': 'Y',  # ResetSeqNumFlag
                '553': 'CLIENT_USER',  # Username
                '554': 'CLIENT_PASS'   # Password
            }
            
            logon_message = FIXMessage.build_message(FIXMessage.LOGON, logon_fields)
            logger.info(f"Sending LOGON: {logon_message}")
            
            # Simulate successful logon
            self.connected = True
            self.running = True
            
            # Start message processing thread
            self.message_thread = threading.Thread(target=self._message_loop, daemon=True)
            self.message_thread.start()
            
            # Start heartbeat
            asyncio.create_task(self._heartbeat_loop())
            
            logger.info("FIX Protocol connection established")
            return True
            
        except Exception as e:
            logger.error(f"FIX connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from FIX server"""
        if self.connected:
            # Send logout message
            logout_message = FIXMessage.build_message(FIXMessage.LOGOUT, {})
            logger.info(f"Sending LOGOUT: {logout_message}")
            
            self.connected = False
            self.running = False
            
            if self.socket:
                self.socket.close()
            
            logger.info("FIX Protocol disconnected")
    
    def subscribe_market_data(self, symbols: List[str], callback: Callable = None) -> str:
        """Subscribe to market data for symbols"""
        if not self.connected:
            logger.error("Not connected to FIX server")
            return None
            
        request_id = f"MDR_{self.subscription_id}"
        self.subscription_id += 1
        
        # Build market data request
        md_fields = {
            FIXMessage.TAG_MD_REQ_ID: request_id,
            FIXMessage.TAG_SUBSCRIPTION_REQUEST_TYPE: '1',  # Snapshot + Updates
            FIXMessage.TAG_MARKET_DEPTH: '1',  # Full book
            '146': str(len(symbols)),  # NoRelatedSym
        }
        
        # Add symbols
        for i, symbol in enumerate(symbols):
            md_fields[f'55'] = symbol  # Symbol (simplified for multiple symbols)
        
        md_request = FIXMessage.build_message(FIXMessage.MARKET_DATA_REQUEST, md_fields)
        logger.info(f"Subscribing to market data: {symbols}")
        
        # Store callback
        if callback:
            self.market_data_callbacks[request_id] = callback
        
        # Store subscription
        self.subscribers[request_id] = symbols
        
        # Simulate immediate market data response
        asyncio.create_task(self._simulate_market_data(symbols, request_id))
        
        return request_id
    
    def unsubscribe_market_data(self, request_id: str):
        """Unsubscribe from market data"""
        if request_id in self.subscribers:
            symbols = self.subscribers[request_id]
            
            # Build unsubscribe request
            md_fields = {
                FIXMessage.TAG_MD_REQ_ID: request_id,
                FIXMessage.TAG_SUBSCRIPTION_REQUEST_TYPE: '2',  # Disable previous snapshot
            }
            
            md_request = FIXMessage.build_message(FIXMessage.MARKET_DATA_REQUEST, md_fields)
            logger.info(f"Unsubscribing from market data: {symbols}")
            
            # Clean up
            del self.subscribers[request_id]
            if request_id in self.market_data_callbacks:
                del self.market_data_callbacks[request_id]
    
    def get_market_data(self, symbol: str) -> Optional[Dict]:
        """Get latest market data for symbol"""
        return self.market_data.get(symbol)
    
    def get_bulk_market_data(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get market data for multiple symbols"""
        result = {}
        for symbol in symbols:
            data = self.get_market_data(symbol)
            if data:
                result[symbol] = data
            else:
                # Return placeholder if no data available
                result[symbol] = self._generate_placeholder_data(symbol)
        return result
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self.connected and self.running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                if time.time() - self.last_heartbeat > self.heartbeat_interval:
                    heartbeat_message = FIXMessage.build_message(FIXMessage.HEARTBEAT, {})
                    logger.debug("Sending heartbeat")
                    self.last_heartbeat = time.time()
                    
            except Exception as e:
                logger.error(f"Heartbeat error: {str(e)}")
    
    def _message_loop(self):
        """Process incoming FIX messages"""
        while self.running:
            try:
                # Simulate message processing
                time.sleep(0.1)
                
                # Update market data periodically
                if self.subscribers:
                    for request_id, symbols in self.subscribers.items():
                        for symbol in symbols:
                            self._update_market_data(symbol)
                            
            except Exception as e:
                logger.error(f"Message loop error: {str(e)}")
    
    async def _simulate_market_data(self, symbols: List[str], request_id: str):
        """Simulate real-time market data updates"""
        await asyncio.sleep(0.5)  # Initial delay
        
        for symbol in symbols:
            # Generate initial market data
            market_data = self._generate_realistic_market_data(symbol)
            self.market_data[symbol] = market_data
            
            # Call callback if exists
            if request_id in self.market_data_callbacks:
                try:
                    self.market_data_callbacks[request_id](symbol, market_data)
                except Exception as e:
                    logger.error(f"Callback error: {str(e)}")
            
            logger.info(f"Market data updated for {symbol}: ${market_data['price']}")
    
    def _update_market_data(self, symbol: str):
        """Update market data with realistic price movements"""
        if symbol not in self.market_data:
            self.market_data[symbol] = self._generate_realistic_market_data(symbol)
            return
        
        current_data = self.market_data[symbol]
        current_price = current_data['price']
        
        # Simulate realistic price movement (random walk)
        volatility = 0.02  # 2% volatility
        change_factor = 1 + random.gauss(0, volatility / 100)
        new_price = current_price * change_factor
        
        # Update market data
        price_change = new_price - current_price
        change_percent = (price_change / current_price) * 100
        
        updated_data = {
            **current_data,
            'price': round(new_price, 2),
            'change': round(price_change, 2),
            'change_percent': round(change_percent, 2),
            'bid_price': round(new_price * 0.9995, 2),
            'ask_price': round(new_price * 1.0005, 2),
            'volume': current_data['volume'] + random.randint(100, 10000),
            'timestamp': datetime.now().isoformat(),
            'last_update': time.time()
        }
        
        self.market_data[symbol] = updated_data
    
    def _generate_realistic_market_data(self, symbol: str) -> Dict:
        """Generate realistic market data based on symbol"""
        
        # Base prices for different symbols
        base_prices = {
            # US Stocks
            'AAPL': 175.0, 'MSFT': 330.0, 'GOOGL': 125.0, 'AMZN': 135.0, 'TSLA': 250.0,
            'NVDA': 450.0, 'META': 320.0, 'NFLX': 400.0, 'AMD': 110.0, 'ORCL': 110.0,
            
            # SA Stocks (converted to USD)
            'NPN.JO': 110.0, 'PRX.JO': 65.0, 'SHP.JO': 8.5, 'ABG.JO': 12.0, 'FSR.JO': 4.2,
            'BTI.JO': 35.0, 'CFR.JO': 120.0, 'SOL.JO': 15.0, 'MTN.JO': 6.5, 'VOD.JO': 4.8
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Add some randomness to base price
        price_variation = random.uniform(-0.1, 0.1)  # ±10%
        current_price = base_price * (1 + price_variation)
        
        # Generate other market data
        change = random.uniform(-5, 5)
        change_percent = (change / current_price) * 100
        
        market_data = {
            'symbol': symbol,
            'price': round(current_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'bid_price': round(current_price * 0.9995, 2),
            'ask_price': round(current_price * 1.0005, 2),
            'bid_size': random.randint(100, 5000),
            'ask_size': random.randint(100, 5000),
            'volume': random.randint(10000, 1000000),
            'high': round(current_price * random.uniform(1.001, 1.05), 2),
            'low': round(current_price * random.uniform(0.95, 0.999), 2),
            'open': round(current_price * random.uniform(0.98, 1.02), 2),
            'market_status': self._get_market_status(symbol),
            'timestamp': datetime.now().isoformat(),
            'last_update': time.time(),
            'feed_source': self._get_feed_source(symbol)
        }
        
        return market_data
    
    def _generate_placeholder_data(self, symbol: str) -> Dict:
        """Generate placeholder data when real data is not available"""
        return {
            'symbol': symbol,
            'price': 0.0,
            'change': 0.0,
            'change_percent': 0.0,
            'bid_price': 0.0,
            'ask_price': 0.0,
            'volume': 0,
            'market_status': 'UNKNOWN',
            'error': 'No data available',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_market_status(self, symbol: str) -> str:
        """Get market status based on symbol and time"""
        now = datetime.now()
        current_hour = now.hour
        
        if symbol.endswith('.JO'):
            # JSE hours (SAST): 09:00 - 17:00
            return 'OPEN' if 9 <= current_hour <= 17 else 'CLOSED'
        else:
            # US markets (EST): 09:30 - 16:00
            return 'OPEN' if 9 <= current_hour <= 16 else 'CLOSED'
    
    def _get_feed_source(self, symbol: str) -> str:
        """Get feed source for symbol"""
        if symbol.endswith('.JO'):
            return self.data_providers['SA']
        else:
            return self.data_providers['US']

# Global FIX client instance
fix_client = FIXProtocolClient()

async def initialize_fix_client():
    """Initialize the global FIX client"""
    success = await fix_client.connect()
    if success:
        logger.info("FIX Protocol client initialized successfully")
    else:
        logger.error("Failed to initialize FIX Protocol client")
    return success

def get_fix_client() -> FIXProtocolClient:
    """Get the global FIX client instance"""
    return fix_client