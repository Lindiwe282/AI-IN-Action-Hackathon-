import time
import logging
import threading
from functools import wraps

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter to prevent exceeding API call limits
    """
    def __init__(self, max_calls, period):
        """
        Initialize rate limiter
        
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.RLock()
        
    def can_call(self):
        """Check if a call can be made within the rate limit"""
        with self.lock:
            now = time.time()
            # Remove calls older than the period
            self.calls = [call_time for call_time in self.calls if now - call_time <= self.period]
            return len(self.calls) < self.max_calls
    
    def add_call(self):
        """Record a call was made"""
        with self.lock:
            self.calls.append(time.time())
    
    def wait_until_available(self):
        """Wait until a call can be made within the rate limit"""
        while True:
            with self.lock:
                now = time.time()
                # Remove calls older than the period
                self.calls = [call_time for call_time in self.calls if now - call_time <= self.period]
                
                if len(self.calls) < self.max_calls:
                    # We can make a call now
                    return
                
                # Calculate how long to wait
                oldest_call = self.calls[0]
                wait_time = self.period - (now - oldest_call) + 0.1  # Add a small buffer
            
            if wait_time > 0:
                logger.debug(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                time.sleep(min(wait_time, self.period))  # Don't wait longer than one period

# Create rate limiters for different APIs
yfinance_limiter = RateLimiter(max_calls=2, period=1)  # 2 calls per second
general_api_limiter = RateLimiter(max_calls=10, period=1)  # 10 calls per second

def rate_limited(limiter):
    """
    Decorator to apply rate limiting to a function
    
    Args:
        limiter: The RateLimiter instance to use
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait_until_available()
            limiter.add_call()
            return func(*args, **kwargs)
        return wrapper
    return decorator