"""Advanced Querying — subqueries, window functions, CTEs, hybrid attributes."""
from sqlalchemy import create_engine, String, Integer, Float, ForeignKey, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship, column_property
from datetime import date

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str] = mapped_column(String(100))
    product: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Float)
    order_date: Mapped[date] = mapped_column(default=date.today)
    region: Mapped[str] = mapped_column(String(50))

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

orders_data = [
    ("Alice", "Laptop", 999.99, "2024-01-15", "NA"),
    ("Bob", "Mouse", 29.99, "2024-01-16", "NA"),
    ("Alice", "Monitor", 299.99, "2024-02-01", "NA"),
    ("Charlie", "Book", 19.99, "2024-02-15", "EU"),
    ("Bob", "Keyboard", 89.99, "2024-03-01", "NA"),
    ("Alice", "Desk", 499.99, "2024-03-15", "NA"),
    ("Diana", "Laptop", 1099.99, "2024-04-01", "EU"),
    ("Charlie", "Mouse", 24.99, "2024-04-10", "EU"),
    ("Bob", "Monitor", 349.99, "2024-05-01", "NA"),
    ("Alice", "Mouse", 29.99, "2024-05-15", "NA"),
]
for c, p, a, d, r in orders_data:
    session.add(Order(customer=c, product=p, amount=a, order_date=date.fromisoformat(d), region=r))
session.commit()

print("=== Advanced Querying ===\n")

# Subquery: customers with above-average orders
avg_amount = session.query(func.avg(Order.amount)).scalar()
above_avg = session.query(Order.customer, func.sum(Order.amount).label("total")).group_by(Order.customer).having(func.sum(Order.amount) > avg_amount).all()
print(f"1. Customers with total > avg (${avg_amount:.2f}):")
for c, t in above_avg:
    print(f"   {c}: ${t:.2f}")

# Window function: rank customers by spend
print("\n2. Customer ranking (window function):")
stmt = text("""
    SELECT customer, SUM(amount) as total,
           RANK() OVER (ORDER BY SUM(amount) DESC) as rank
    FROM orders GROUP BY customer ORDER BY rank
""")
with engine.connect() as conn:
    rows = conn.execute(stmt).all()
    for r in rows:
        print(f"   #{r.rank} {r.customer:10s} ${r.total:.2f}")

# CTE: running total by date
print("\n3. Alice's running total (CTE):")
stmt = text("""
    WITH alice_orders AS (
        SELECT order_date, amount,
               SUM(amount) OVER (ORDER BY order_date) as running_total
        FROM orders WHERE customer = 'Alice'
    )
    SELECT * FROM alice_orders
""")
with engine.connect() as conn:
    rows = conn.execute(stmt).all()
    for r in rows:
        print(f"   {r.order_date}: ${r.amount:.2f} → ${r.running_total:.2f}")

# Group by with subtotals
print("\n4. Sales by region:")
region_totals = session.query(Order.region, func.sum(Order.amount)).group_by(Order.region).all()
for r, t in region_totals:
    print(f"   {r}: ${t:.2f}")

# Top product per customer
print("\n5. Each customer's most expensive purchase:")
stmt = text("""
    SELECT customer, product, amount, max_amount
    FROM (
        SELECT customer, product, amount,
               MAX(amount) OVER (PARTITION BY customer) as max_amount
        FROM orders
    ) WHERE amount = max_amount
""")
with engine.connect() as conn:
    rows = conn.execute(stmt).all()
    for r in rows:
        print(f"   {r.customer:10s} {r.product:10s} ${r.amount}")

session.close()
