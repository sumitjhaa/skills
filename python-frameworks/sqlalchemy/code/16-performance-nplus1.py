"""Performance & N+1 — eager loading strategies, selectinload, joinedload."""
from sqlalchemy import create_engine, String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship, selectinload, joinedload, subqueryload
import time

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

cats = [Category(name=f"Cat{i}") for i in range(10)]
session.add_all(cats)
session.commit()

for c in cats:
    session.add_all([Product(name=f"{c.name}-Prod{j}", category_id=c.id) for j in range(10)])
session.commit()

print("=== Performance & N+1 ===\n")

# N+1 query (lazy loading)
t0 = time.time()
cats = session.query(Category).all()
for c in cats:
    _ = len(c.products)  # triggers N queries
t1 = time.time()
print(f"1. N+1 (lazy): {len(cats)} queries for {len(cats)} categories — {t1-t0:.3f}s")

# Eager with selectinload
session.close()
t0 = time.time()
cats = session.query(Category).options(selectinload(Category.products)).all()
for c in cats:
    _ = len(c.products)
t1 = time.time()
print(f"2. selectinload: 2 queries total — {t1-t0:.3f}s")

# Eager with joinedload
session.close()
t0 = time.time()
cats = session.query(Category).options(joinedload(Category.products)).all()
for c in cats:
    _ = len(c.products)
t1 = time.time()
print(f"3. joinedload:  1 query (LEFT OUTER JOIN) — {t1-t0:.3f}s")

# subqueryload
session.close()
t0 = time.time()
cats = session.query(Category).options(subqueryload(Category.products)).all()
for c in cats:
    _ = len(c.products)
t1 = time.time()
print(f"4. subqueryload: 2 queries (subquery) — {t1-t0:.3f}s")

print(f"\n5. Strategy recommendations:")
print("   selectinload  → best for to-many (simple, 2 queries)")
print("   joinedload    → best for to-one (single query)")
print("   subqueryload  → good for to-many with limits/offsets")
print("   lazyload (default) → only when accessing rarely")

session.close()
