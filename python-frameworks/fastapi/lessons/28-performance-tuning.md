# ⚡ Performance Tuning
<!-- ⏱️ 15 min | 🟢 Supplement -->

**What You'll Learn:** Profiling, caching strategies, N+1 problem, connection pooling, query optimization.

## Profiling

```python
import time
import functools

def profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}: {elapsed*1000:.1f}ms")
        return result
    return wrapper
```

## Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_data(param: str):
    # Expensive operation
    return result
```

For API-level caching:

```python
cache: dict[str, tuple[Any, float]] = {}

def get_cached(key: str, ttl: int = 60):
    if key in cache:
        val, exp = cache[key]
        if exp > time.time():
            return val
    return None

def set_cached(key: str, val: Any, ttl: int = 60):
    cache[key] = (val, time.time() + ttl)
```

## N+1 Query Problem

**Bad:** Query users, then query posts per user in a loop (N+1 queries).

**Good:** Use JOIN or eager loading:

```python
# Bad
users = db.query(User).all()
for user in users:
    posts = db.query(Post).filter(Post.user_id == user.id).all()

# Good
results = db.query(User).join(Post).all()
```

## Connection Pooling

```python
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
```

## Run the Code

```bash
python code/28-performance-tuning.py
```
