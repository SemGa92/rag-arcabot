import asyncio
from functools import wraps



def async_retry(max_retries: int=3, delay: int=1):
    """Decorator for async retry on specific root."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}", flush=True)
                    await asyncio.sleep(delay)
            raise ValueError(f"Failed after {max_retries} attempts")
        return wrapper
    return decorator
