"""functools patterns: caching, partials, singledispatch — real API/ML pipelines"""
from functools import cache, cached_property, partial, singledispatchmethod, reduce
import time

class DataAnalyzer:
    """ML data analysis with cached computations and dispatch by type"""
    def __init__(self, data):
        self._data = data

    @cached_property
    def normalized(self):
        """Computed once, cached for life — like @property but auto-cached.
           Use when value is expensive to compute and won't change."""
        print("  [Compute] Normalizing...")  # Would be real ML preprocessing
        return [x / max(self._data) for x in self._data]

    @singledispatchmethod  # Dispatch on FIRST argument type
    def analyze(self, arg):
        raise NotImplementedError(f"No handler for {type(arg)}")

    @analyze.register
    def _(self, arg: int):
        return f"Count: {arg} items"

    @analyze.register
    def _(self, arg: list):
        return f"List: {sum(arg)} total, {len(arg)} items"

# @cache: memoize pure function results (unbounded, unlike lru_cache)
@cache
def api_fetch(endpoint: str) -> dict:
    print(f"  Fetching {endpoint}...")  # Simulates HTTP request
    return {"status": "ok", "data": endpoint}

# partial: freeze arguments to create specialized functions
def send_email(to: str, subject: str, body: str) -> str:
    return f"To: {to} | Subject: {subject} | Body: {body[:20]}..."
send_alert = partial(send_email, to="ops@company.com", subject="URGENT: System Alert")

# Usage
obj = DataAnalyzer([10, 20, 30, 40, 50])
print(f"Normalized: {obj.normalized}")
print(f"Cached: {obj.normalized}")  # No [Compute] — uses cached value
print(f"Int: {obj.analyze(100)}")
print(f"List: {obj.analyze([1,2,3])}")
print(api_fetch("/users"))   # Prints [Compute]
print(api_fetch("/users"))   # Cached — no print
print(send_alert(body="Database is down on server-01"))
