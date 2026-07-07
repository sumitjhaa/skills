"""Events & Hooks — before_insert, after_update, event listeners."""
from sqlalchemy import create_engine, String, Integer, Float, DateTime, func, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    table_name: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(20))
    record_id: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(default=func.now())

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[int] = mapped_column(Integer, default=1)

audit_log: list[dict] = []

@event.listens_for(Product, "before_insert")
def product_before_insert(mapper, connection, target):
    target.version = 1
    audit_log.append({"table": "products", "action": "insert", "id": target.id or "pending", "time": datetime.now().isoformat()})

@event.listens_for(Product, "before_update")
def product_before_update(mapper, connection, target):
    target.version += 1
    audit_log.append({"table": "products", "action": "update", "id": target.id, "time": datetime.now().isoformat()})

@event.listens_for(Product, "after_delete")
def product_after_delete(mapper, connection, target):
    audit_log.append({"table": "products", "action": "delete", "id": target.id, "time": datetime.now().isoformat()})

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("=== Events & Hooks ===\n")

session.add(Product(name="Laptop", price=999.99, stock=10))
session.add(Product(name="Mouse", price=29.99, stock=50))
session.commit()
print("1. Inserted 2 products")

product = session.query(Product).filter(Product.name == "Laptop").first()
product.price = 899.99
product.stock = 8
session.commit()
print("2. Updated Laptop price and stock")

product = session.query(Product).filter(Product.name == "Mouse").first()
session.delete(product)
session.commit()
print("3. Deleted Mouse")

print("\n4. Audit log:")
for entry in audit_log:
    print(f"   {entry['action']:8s} {entry['table']:10s} id={entry['id']} @ {entry['time'][:19]}")

product = session.query(Product).first()
print(f"\n5. Version tracking: {product.name} v{product.version}")

# Validation event example
@event.listens_for(Product, "before_insert")
def validate_price(mapper, connection, target):
    if target.price < 0:
        raise ValueError(f"Negative price not allowed: {target.price}")

print("\n6. Validation event active — negative prices will be rejected")

session.close()
