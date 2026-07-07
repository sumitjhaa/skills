# 🔌 Engine & Connections
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create a database engine, connect, execute raw SQL, manage connections.

## Engine

The `Engine` is the starting point for any SQLAlchemy application. It represents a database connection pool.

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:", echo=False)
# PostgreSQL: postgresql://user:pass@localhost/db
# MySQL:      mysql://user:pass@localhost/db
```

## Executing Raw SQL

```python
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"))
    conn.commit()
```

## Parameterized Queries

```python
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO users (name, email) VALUES (:name, :email)"),
        [{"name": "Alice", "email": "alice@test.com"},
         {"name": "Bob", "email": "bob@test.com"}]
    )
    conn.commit()
```

## Reading Results

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(f"{row.id}: {row.name} ({row.email})")
```

## Connection Management

- Always use `with engine.connect()` — it auto-closes
- Call `conn.commit()` for writes
- Use `engine.begin()` for auto-commit context managers

<!-- 🤔 `sqlite:///:memory:` creates an in-memory DB. For persistent files use `sqlite:///app.db`. -->

## Run the Code

```bash
python code/01-engine-connections.py
```
