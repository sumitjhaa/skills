"""08-01-decorators-deep.py — E-commerce: decorators for logging, timing, retry."""

from functools import wraps
import time


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  -> {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"  Retry {attempt + 1}/{max_attempts}: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


@log_calls
@retry(max_attempts=2)
def fetch_product_price(product_id: int) -> float:
    if product_id < 0:
        raise ValueError("Invalid ID")
    return 99.99


@CountCalls
def discount(price: float, percent: float) -> float:
    return price * (1 - percent / 100)


print(f"Price: ${fetch_product_price(42):.2f}")
print(f"Discounted: ${discount(100, 10):.2f}")
print(f"discount called {discount.count} times")
print(f"Name preserved: {fetch_product_price.__name__}")
