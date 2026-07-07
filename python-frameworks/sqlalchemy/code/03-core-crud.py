"""Core: Insert, Select, Update, Delete — SQL Expression Language."""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, insert, update, delete

engine = create_engine("sqlite:///:memory:", echo=False)
metadata = MetaData()

products = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("price", Float, default=0.0),
    Column("category", String(50)),
)
metadata.create_all(engine)

# Insert
with engine.connect() as conn:
    stmt = insert(products).values([
        {"name": "Laptop", "price": 999.99, "category": "electronics"},
        {"name": "Mouse", "price": 29.99, "category": "electronics"},
        {"name": "Book", "price": 19.99, "category": "media"},
        {"name": "Chair", "price": 199.99, "category": "furniture"},
    ])
    conn.execute(stmt)
    conn.commit()

# Select all
with engine.connect() as conn:
    stmt = select(products)
    result = conn.execute(stmt)
    rows = result.all()

print("=== Core: CRUD Operations ===\n")
print("1. All products:")
for r in rows:
    print(f"   [{r.id}] {r.name:10s} ${r.price:<7.2f} ({r.category})")

# Select with filter
with engine.connect() as conn:
    stmt = select(products).where(products.c.category == "electronics")
    rows = conn.execute(stmt).all()

print("\n2. Electronics only:")
for r in rows:
    print(f"   {r.name}: ${r.price}")

# Update
with engine.connect() as conn:
    stmt = update(products).where(products.c.name == "Mouse").values(price=24.99)
    conn.execute(stmt)
    conn.commit()

with engine.connect() as conn:
    r = conn.execute(select(products).where(products.c.name == "Mouse")).first()
    print(f"\n3. After update: Mouse = ${r.price}")

# Delete
with engine.connect() as conn:
    stmt = delete(products).where(products.c.name == "Chair")
    conn.execute(stmt)
    conn.commit()

with engine.connect() as conn:
    count = conn.execute(select(products)).rowcount
    print(f"4. After delete: {count} products remaining")
