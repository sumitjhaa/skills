# ⚡ Async SQLAlchemy
<!-- ⏱️ 15 min | 🟢 Supplement -->

**What You'll Learn:** Async engine, async sessions, async CRUD with SQLAlchemy 1.4+.

## Install

```bash
pip install sqlalchemy[asyncio] asyncpg
```

## Async Engine & Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
```

## Async CRUD

```python
async def get_users():
    async with AsyncSessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()

async def create_user(username: str, email: str):
    async with AsyncSessionLocal() as session:
        user = User(username=username, email=email)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
```

<!-- 🔄 Async sessions use `async with` context managers. Always `await` execute/commit/refresh. -->

## Async vs Sync

| Sync | Async |
|------|-------|
| `Session()` | `AsyncSession()` |
| `session.query(...)` | `await session.execute(select(...))` |
| `session.commit()` | `await session.commit()` |
| `result.scalars().all()` | `await result.scalars().all()` |

## Async Dependency

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

## Run the Code

```bash
python code/24-async-sqlalchemy.py
```
