import yfinance as yf
import time
import logging
import pandas as pd
from functools import wraps
from datetime import datetime, timedelta
from .cache_manager import cached
from .rate_limiter import rate_limited, yfinance_limiter
from .async_handler import run_async, timing

logger = logging.getLogger(__name__)

class YFinanceWrapper:
    def __init__(self):
        self._last_request_time = 0
        self._min_request_interval = 0.5  # Minimum seconds between requests
        self._cache = {}  # Simple in-memory cache
        self._cache_ttl = {}  # Time-to-live for cache entries
        
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request)
        
        self._last_request_time = time.time()
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def download(self, tickers, **kwargs):
        """Wrapper for yf.download with caching, rate limiting and error handling"""
        with timing("yfinance download"):
            try:
                # Explicitly set parameters to avoid conflicts
                params = {
                    'progress': False,
                    'threads': False,  # Disable threading to avoid rate limit issues
                }
                
                # Add kwargs to params without overwriting our explicit settings
                for key, value in kwargs.items():
                    if key not in params:
                        params[key] = value
                
                # Let yfinance handle the session internally
                data = yf.download(tickers, **params)
                
                return data
                
            except Exception as e:
                logger.error(f"Error downloading data for {tickers}: {str(e)}")
                # Return empty DataFrame instead of raising
                return pd.DataFrame()
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def get_ticker_info(self, ticker):
        """Get ticker info with caching and rate limiting"""
        with timing(f"get_ticker_info {ticker}"):
            try:
                stock = yf.Ticker(ticker)
                return stock.info
            except Exception as e:
                logger.error(f"Error getting info for {ticker}: {str(e)}")
                return {}
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def get_ticker_history(self, ticker, **kwargs):
        """Get ticker history with caching and rate limiting"""
        with timing(f"get_ticker_history {ticker}"):
            try:
                stock = yf.Ticker(ticker)
                history = stock.history(**kwargs)
                return history
            except Exception as e:
                logger.error(f"Error getting history for {ticker}: {str(e)}")
                return pd.DataFrame()
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def get_history(self, ticker, **kwargs):
        """Alias for get_ticker_history for compatibility"""
        return self.get_ticker_history(ticker, **kwargs)
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def download_data(self, tickers, **kwargs):
        """Clean wrapper for download method to avoid duplicate parameters"""
        # Remove parameters that are already set in the download method
        if 'progress' in kwargs:
            del kwargs['progress']
        if 'threads' in kwargs:
            del kwargs['threads']
            
        # Call the download method with the cleaned kwargs
        return self.download(tickers, **kwargs)
    
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def get_multiple_tickers_last_day(self, tickers):
        """Get last day's data for multiple tickers with caching and rate limiting"""
        with timing(f"get_multiple_tickers_last_day"):
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)  # Get a bit more data for stability
            
            try:
                # Use our download method to ensure consistent behavior
                data = self.download(
                    tickers,
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d')
                )
                
                # Handle single ticker case
                if isinstance(data, pd.Series) or (isinstance(data, pd.DataFrame) and 'Close' in data.columns):
                    if 'Close' in data.columns:
                        last_prices = data['Close'].iloc[-1]
                    else:
                        last_prices = data.iloc[-1]
                    return last_prices
                
                # Handle multiple tickers case
                if 'Close' in data.columns.get_level_values(0):
                    last_prices = data['Close'].iloc[-1]
                    return last_prices
                
                return pd.Series()
                
            except Exception as e:
                logger.error(f"Error getting last day data for {tickers}: {str(e)}")
                return pd.Series()
    
    @cached(ttl=60)  # Cache results for 1 minute only for quotes
    @rate_limited(yfinance_limiter)
    def get_quotes(self, tickers):
        """Get current quotes for tickers with short caching period"""
        with timing(f"get_quotes for {len(tickers) if isinstance(tickers, list) else 1} tickers"):
            if isinstance(tickers, str):
                tickers = [tickers]
                
            try:
                data = {}
                for ticker in tickers:
                    stock = yf.Ticker(ticker)
                    try:
                        data[ticker] = {
                            'price': stock.info.get('currentPrice') or stock.info.get('regularMarketPrice'),
                            'change': stock.info.get('regularMarketChange'),
                            'changePercent': stock.info.get('regularMarketChangePercent'),
                            'volume': stock.info.get('regularMarketVolume'),
                            'timestamp': datetime.now().isoformat()
                        }
                    except Exception as e:
                        logger.warning(f"Error getting quote for {ticker}: {str(e)}")
                        data[ticker] = {'error': str(e)}
                
                return data
                
            except Exception as e:
                logger.error(f"Error getting quotes: {str(e)}")
                return {}
                
    @cached(ttl=300)  # Cache results for 5 minutes
    @rate_limited(yfinance_limiter)
    def get_stock_info(self, ticker):
        """Get stock info with enhanced error handling"""
        try:
            info = self.get_ticker_info(ticker)
            if not info:
                # Fallback to history data if info is empty
                hist = self.get_history(ticker, period="5d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change = current_price - prev_price
                    change_percent = (change / prev_price * 100) if prev_price > 0 else 0
                    
                    return {
                        'currentPrice': float(current_price),
                        'change': float(change),
                        'changePercent': float(change_percent),
                        'previousClose': float(prev_price)
                    }
            return info
        except Exception as e:
            logger.error(f"Error getting stock info for {ticker}: {str(e)}")
            return {}

# Create a singleton instance
yf_wrapper = YFinanceWrapper()