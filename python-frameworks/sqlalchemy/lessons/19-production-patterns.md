# 🏭 Production Patterns
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Connection pooling, environment configuration, logging, retry logic, connection health checks.

## Connection Pooling

```python
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

| Setting | Purpose |
|---------|---------|
| `pool_size` | Base connections |
| `max_overflow` | Extra connections permitted |
| `pool_pre_ping` | Check connection before use |
| `pool_recycle` | Max age of a connection (seconds) |

## Configuration

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
POOL_SIZE = int(os.environ.get("POOL_SIZE", 5))
```

## Logging

```python
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
```

## Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_db_connection():
    return create_engine(DATABASE_URL).connect()
```

## Session Management in Web Apps

```python
from contextlib import contextmanager

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

## Run the Code

```bash
python code/19-production-patterns.py
```
