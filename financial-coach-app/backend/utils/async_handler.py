import asyncio
import threading
import concurrent.futures
import logging
import functools
import time
import os
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Thread pool for running CPU-bound tasks
cpu_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=min(32, (os.cpu_count() or 1) * 5),
    thread_name_prefix="cpu_worker"
)

# Thread pool for I/O-bound tasks (like API calls)
io_executor = concurrent.futures.ThreadPoolExecutor(
    max_workers=25,  # Higher count for I/O tasks
    thread_name_prefix="io_worker"
)

@contextmanager
def timing(operation_name):
    """Context manager to time operations for performance monitoring"""
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        logger.debug(f"{operation_name} completed in {elapsed:.4f} seconds")

def run_in_executor(executor, func, *args, **kwargs):
    """Run a synchronous function in the specified executor"""
    return executor.submit(func, *args, **kwargs).result()

def run_async(func):
    """
    Decorator to run a synchronous function asynchronously
    For I/O bound operations like API calls, database operations
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return io_executor.submit(func, *args, **kwargs)
    return wrapper

def run_cpu_bound(func):
    """
    Decorator to run a CPU-bound function in a separate thread
    For heavy computational tasks like portfolio optimization
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return cpu_executor.submit(func, *args, **kwargs)
    return wrapper

def batch_process(items, processor_func, max_workers=10, chunk_size=None):
    """
    Process a list of items in parallel batches
    
    Args:
        items: List of items to process
        processor_func: Function that processes a single item
        max_workers: Maximum number of parallel workers
        chunk_size: Size of batches to process together
    
    Returns:
        List of results in the same order as the input
    """
    if not items:
        return []
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        if chunk_size:
            # Process in chunks
            chunks = [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]
            
            # Define a chunk processor function
            def process_chunk(chunk):
                return [processor_func(item) for item in chunk]
                
            # Submit all chunks for processing
            futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
            
            # Collect results
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.extend(future.result())
            
            return results
        else:
            # Process individual items
            futures = [executor.submit(processor_func, item) for item in items]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

def cleanup():
    """Cleanup function to shut down thread pools properly"""
    io_executor.shutdown(wait=False)
    cpu_executor.shutdown(wait=False)