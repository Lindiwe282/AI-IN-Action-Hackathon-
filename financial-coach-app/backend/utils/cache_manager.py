import time
import logging
import threading
from functools import wraps
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheManager:
    """
    A memory cache manager with time-based expiration
    """
    def __init__(self):
        self._cache = {}
        self._lock = threading.RLock()
        self._cleanup_thread = None
        self._stop_cleanup = threading.Event()
        self._start_cleanup_thread()
        
    def _start_cleanup_thread(self):
        """Start the background thread to clean expired cache entries"""
        if self._cleanup_thread is None:
            self._cleanup_thread = threading.Thread(
                target=self._cleanup_worker,
                daemon=True
            )
            self._cleanup_thread.start()
    
    def _cleanup_worker(self):
        """Worker thread to periodically clean the cache"""
        while not self._stop_cleanup.is_set():
            try:
                self.cleanup()
            except Exception as e:
                logger.error(f"Error in cache cleanup: {str(e)}")
            time.sleep(300)  # Run cleanup every 5 minutes
    
    def cleanup(self):
        """Remove expired items from cache"""
        now = time.time()
        with self._lock:
            expired_keys = [
                key for key, (_, expiry) in self._cache.items()
                if expiry is not None and expiry < now
            ]
            for key in expired_keys:
                del self._cache[key]
                logger.debug(f"Removed expired cache entry: {key}")
    
    def get(self, key):
        """Get item from cache if it exists and hasn't expired"""
        with self._lock:
            cache_item = self._cache.get(key)
            if cache_item is None:
                return None
            
            value, expiry = cache_item
            if expiry is not None and expiry < time.time():
                del self._cache[key]
                return None
            
            return value
    
    def set(self, key, value, ttl=None):
        """Set an item in the cache with optional time-to-live in seconds"""
        with self._lock:
            expiry = time.time() + ttl if ttl is not None else None
            self._cache[key] = (value, expiry)
    
    def delete(self, key):
        """Remove an item from the cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self):
        """Clear all items from the cache"""
        with self._lock:
            self._cache.clear()
    
    def shutdown(self):
        """Shutdown the cleanup thread"""
        self._stop_cleanup.set()
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=1)
            self._cleanup_thread = None


# Create a global cache instance
cache = CacheManager()

def cached(ttl=300):
    """
    Decorator to cache function results with the specified TTL (in seconds)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache first
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # If not in cache, call the function
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            
            # Store in cache with the specified TTL
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator