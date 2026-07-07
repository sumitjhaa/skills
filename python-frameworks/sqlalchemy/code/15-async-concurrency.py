"""Async SQLAlchemy — async engine, async sessions (simulated with aiosqlite)."""
from sqlalchemy import String, Integer, Float, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import asyncio

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)

    async with AsyncSessionLocal() as session:
        session.add_all([
            Item(name="Async Laptop", price=999.99),
            Item(name="Async Mouse", price=29.99),
            Item(name="Async Keyboard", price=89.99),
        ])
        await session.commit()

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item).order_by(Item.price))
        items = result.scalars().all()

    print("=== Async SQLAlchemy ===\n")
    print("1. Items (async):")
    for item in items:
        print(f"   [{item.id}] {item.name:20s} ${item.price}")

    async with AsyncSessionLocal() as session:
        laptop = await session.get(Item, 1)
        laptop.price = 899.99
        await session.commit()
        laptop = await session.get(Item, 1)
        print(f"\n2. Updated price (async): {laptop.name} = ${laptop.price}")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item).where(Item.price < 50))
        cheap = result.scalars().all()
        print(f"\n3. Cheap items (async): {[i.name for i in cheap]}")

    await engine.dispose()
    print("\n✅ Async operations completed successfully")

asyncio.run(main())
