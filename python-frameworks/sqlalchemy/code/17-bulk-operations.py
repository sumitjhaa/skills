"""Bulk Operations — bulk_insert, bulk_update, upsert, batch operations."""
from sqlalchemy import create_engine, String, Integer, Float, insert, update, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
import time

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

print("=== Bulk Operations ===\n")

# Bulk insert
t0 = time.time()
session = SessionLocal()
session.execute(
    insert(Product),
    [{"name": f"Product {i}", "price": round(i * 10.0, 2), "stock": i * 5} for i in range(1000)]
)
session.commit()
t1 = time.time()
count = session.query(Product).count()
print(f"1. Bulk insert: 1000 records in {t1-t0:.3f}s ({count} total)")

# Bulk update
t0 = time.time()
session.execute(
    update(Product).where(Product.stock > 0).values(stock=Product.stock + 10)
)
session.commit()
t1 = time.time()
sample = session.execute(select(Product).limit(3)).scalars().all()
print(f"2. Bulk update: +10 stock in {t1-t0:.3f}s")
for p in sample:
    print(f"   {p.name}: stock={p.stock}")

# Bulk upsert simulation
t0 = time.time()
session.execute(
    insert(Product).values([
        {"name": "New Product A", "price": 99.99, "stock": 20},
        {"name": "New Product B", "price": 49.99, "stock": 15},
    ])
)
session.commit()
t1 = time.time()
print(f"\n3. Bulk insert additional products: {t1-t0:.3f}s")
count = session.query(Product).count()
print(f"   Total products now: {count}")

# Bulk delete
t0 = time.time()
session.execute(delete(Product).where(Product.stock == 0))
session.commit()
t1 = time.time()
remaining = session.query(Product).count()
print(f"\n4. Bulk delete (stock=0): {t1-t0:.3f}s, {remaining} remaining")

# Batch processing (chunked)
t0 = time.time()
all_ids = [r.id for r in session.execute(select(Product.id)).all()]
for chunk_start in range(0, len(all_ids), 100):
    chunk = all_ids[chunk_start:chunk_start + 100]
    session.execute(
        update(Product).where(Product.id.in_(chunk)).values(price=Product.price * 1.1)
    )
session.commit()
t1 = time.time()
print(f"\n5. Batch update (chunks of 100): {t1-t0:.3f}s, 10% price increase")

session.close()
