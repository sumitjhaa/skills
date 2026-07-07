"""Core: Joins & Subqueries — join tables, subqueries, aggregations."""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, func, join, text

engine = create_engine("sqlite:///:memory:", echo=False)
metadata = MetaData()

users = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)
orders = Table("orders", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("product", String(100)),
    Column("amount", Float),
    Column("status", String(20), default="pending"),
)
metadata.create_all(engine)

with engine.connect() as conn:
    conn.execute(users.insert().values([
        {"name": "Alice"}, {"name": "Bob"}, {"name": "Charlie"},
    ]))
    conn.execute(orders.insert().values([
        {"user_id": 1, "product": "Laptop", "amount": 999.99, "status": "shipped"},
        {"user_id": 1, "product": "Mouse", "amount": 29.99, "status": "shipped"},
        {"user_id": 2, "product": "Book", "amount": 19.99, "status": "pending"},
        {"user_id": 2, "product": "Desk", "amount": 299.99, "status": "pending"},
        {"user_id": 1, "product": "Monitor", "amount": 199.99, "status": "delivered"},
    ]))
    conn.commit()

# INNER JOIN
with engine.connect() as conn:
    j = users.join(orders, users.c.id == orders.c.user_id)
    stmt = select(users.c.name, orders.c.product, orders.c.amount).select_from(j)
    rows = conn.execute(stmt).all()

print("=== Core: Joins & Subqueries ===\n")
print("1. User orders (INNER JOIN):")
for r in rows:
    print(f"   {r.name:8s} {r.product:10s} ${r.amount}")

# LEFT JOIN with aggregation
with engine.connect() as conn:
    j = users.outerjoin(orders, users.c.id == orders.c.user_id)
    stmt = select(users.c.name, func.coalesce(func.sum(orders.c.amount), 0).label("total")).select_from(j).group_by(users.c.name)
    rows = conn.execute(stmt).all()

print("\n2. User totals (LEFT JOIN + GROUP BY):")
for r in rows:
    print(f"   {r.name:8s} spent ${r.total:.2f}")

# Subquery
with engine.connect() as conn:
    subq = select(orders.c.user_id, func.sum(orders.c.amount).label("total")).group_by(orders.c.user_id).subquery()
    stmt = select(users.c.name, subq.c.total).join(subq, users.c.id == subq.c.user_id)
    rows = conn.execute(stmt).all()

print("\n3. High spenders (subquery):")
for r in rows:
    if r.total > 100:
        print(f"   {r.name}: ${r.total:.2f}")
