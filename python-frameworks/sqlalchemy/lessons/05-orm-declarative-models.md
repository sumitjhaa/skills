# 🏗️ ORM: Declarative Models
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** SQLAlchemy 2.0 style models with `Mapped` and `mapped_column`.

## Declarative Base

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass
```

## Defining Models

```python
from sqlalchemy import String, Integer, Float, Boolean

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
```

## Column Types with Mapped

```python
from datetime import datetime
from sqlalchemy import DateTime, func

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

## Creating Tables

```python
Base.metadata.create_all(engine)
```

## Key Points

- `Mapped[type]` — the 2.0 way to declare column type
- `mapped_column(...)` — column options (type, constraints, defaults)
- `__tablename__` — required for each model
- `Base.metadata.create_all()` — creates all tables

<!-- 🤔 The `Mapped` annotation is optional but enables better type checking. -->

## Run the Code

```bash
python code/05-orm-declarative-models.py
```
