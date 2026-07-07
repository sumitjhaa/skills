# ⚡ Async DB with asyncpg
<!-- ⏱️ 15 min | 🟢 Supplement -->

**What You'll Learn:** Connection pooling, async queries, async endpoints, performance benefits.

## Install

```bash
pip install asyncpg databases
```

## Connection Pool

```python
import asyncpg

async def connect():
    pool = await asyncpg.create_pool(
        "postgresql://user:pass@localhost/db",
        min_size=2,
        max_size=10,
    )
    return pool
```

<!-- 🗄️ Pools reuse connections — essential for production. Avoid creating a new connection per request. -->

## Async Query

```python
async def get_users(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        return [dict(row) for row in rows]
```

## Using `databases` Library

```python
from databases import Database

database = Database("postgresql://user:pass@localhost/db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

## Async Endpoints

```python
@app.get("/users")
async def list_users():
    query = "SELECT id, username, email FROM users"
    rows = await database.fetch_all(query)
    return {"users": rows}
```

<!-- 🔄 Async endpoints don't block the event loop. Handle many concurrent requests with fewer threads. -->

## Sync vs Async

| Sync | Async | When to Use |
|------|-------|-------------|
| `db.query(...).all()` | `await conn.fetch(...)` | High concurrency |
| Blocking | Non-blocking | I/O-bound workloads |
| Simpler code | Slightly more complex | Default until perf matters |

## Run the Code

```bash
python code/13-async-db-asyncpg.py
```
