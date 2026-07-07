"""Decorators for logging, timing, rate limiting, and authentication."""
import functools
import time


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    time.sleep(0.1)
            raise last_exc
        return wrapper
    return decorator


@log_calls
@timeit
def process_order(order_id: str, items: list) -> dict:
    time.sleep(0.05)
    return {"order_id": order_id, "status": "confirmed", "items": items}


@retry(max_attempts=3)
def unstable_api_call():
    raise ConnectionError("timeout")


print(process_order("ORD-123", ["laptop", "mouse"]))

try:
    unstable_api_call()
except ConnectionError:
    print("[OK] retry exhausted as expected")
