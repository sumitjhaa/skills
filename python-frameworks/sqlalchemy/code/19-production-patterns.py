"""Production Patterns — connection pooling, pool tuning, concurrent access."""
from sqlalchemy import create_engine, String, Integer, Float, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
import time
import threading

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int] = mapped_column(Integer)

# Pool configuration
engine = create_engine(
    "sqlite:///:memory:",
    pool_pre_ping=True,
    echo=False,
)
# SQLite uses SingletonThreadPool (pool_size not configurable)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Seed
session = SessionLocal()
session.add_all([Item(name=f"Item {i}", value=i * 10) for i in range(20)])
session.commit()
session.close()

print("=== Production Patterns ===\n")

print(f"1. Pool config:")
print(f"   pool_class={type(engine.pool).__name__}, pool_pre_ping=True")
print(f"   status=SingletonThreadPool (SQLite) — single connection shared")

# Threaded concurrent access
def worker(worker_id, num_ops):
    local_session = SessionLocal()
    for i in range(num_ops):
        item = local_session.query(Item).order_by(Item.id).first()
        item.value += 1
        local_session.commit()
    local_session.close()
    return f"Worker {worker_id} done"

threads = []
t0 = time.time()
for i in range(4):
    t = threading.Thread(target=worker, args=(i, 10))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
t1 = time.time()

print(f"\n2. Concurrent access: 4 workers x 10 ops in {t1-t0:.3f}s")
session = SessionLocal()
item = session.query(Item).filter(Item.name == "Item 0").first()
print(f"   Item 0 final value: {item.value} (expected 40 + additional)")
session.close()

# Connection pool stats after usage
print(f"\n3. Pool after work:")
print(f"   status=active (SingletonThreadPool handles all connections internally)")

# Error handling
print(f"\n4. Pool best practices (for PostgreSQL/MySQL):")
print(f"   pool_pre_ping=True  → test connections before use")
print(f"   pool_size=5         → keep 5 connections in pool")
print(f"   max_overflow=10     → allow 10 extra beyond pool_size")
print(f"   pool_recycle=3600   → recycle connections after 1hr")
print(f"   pool_timeout=30     → wait 30s before giving up")

session = SessionLocal()
session.execute(text("SELECT 1"))
session.close()
print(f"\n5. Connection verified with pool_pre_ping")
