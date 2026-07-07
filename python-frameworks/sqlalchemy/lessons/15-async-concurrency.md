# ⚡ Async & Concurrency
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** `asyncio` support with `AsyncSession`, async engines, connection pooling.

## Async Engine & Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession)
```

## Async CRUD

```python
async def create_book():
    async with AsyncSessionLocal() as session:
        book = Book(title="Async Python", author="Alice")
        session.add(book)
        await session.commit()
```

## Async Queries

```python
async def get_books():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Book))
        return result.scalars().all()
```

## Connection Pooling

```python
engine = create_async_engine(
    "postgresql+asyncpg://localhost/db",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)
```

## Running Async Code

```bash
python -m asyncio code/15-async-concurrency.py
```

Or use:

```python
import asyncio
asyncio.run(main())
```

<!-- 🤔 Async SQLAlchemy requires async drivers: `aiosqlite`, `asyncpg`, `aiomysql`. -->

## Run the Code

```bash
python code/15-async-concurrency.py
```
