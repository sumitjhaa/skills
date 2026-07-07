# 📋 Core: Table & Metadata
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Define tables with `MetaData`, column types, constraints, create/drop.

## MetaData & Table

```python
from sqlalchemy import MetaData, Table, Column, Integer, String, Float

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), unique=True),
)
```

## Column Types

| Type | SQL | Python |
|------|-----|--------|
| `Integer` | INTEGER | int |
| `String(n)` | VARCHAR(n) | str |
| `Float` | FLOAT | float |
| `Boolean` | BOOLEAN | bool |
| `Text` | TEXT | str |
| `DateTime` | DATETIME | datetime |

## Creating & Dropping Tables

```python
metadata.create_all(engine)  # CREATE TABLE IF NOT EXISTS
metadata.drop_all(engine)    # DROP TABLE
```

## Column Constraints

```python
Column("id", Integer, primary_key=True)
Column("name", String(50), nullable=False)
Column("email", String(100), unique=True)
Column("price", Float, default=0.0)
Column("bio", Text, nullable=True)
```

<!-- 🤔 `create_all` is idempotent — safe to call multiple times. -->

## Run the Code

```bash
python code/02-core-table-metadata.py
```
