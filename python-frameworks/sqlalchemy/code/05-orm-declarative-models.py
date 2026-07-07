"""ORM: Declarative Models — mapped_column, types, table args."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', ${self.price})"

Base.metadata.create_all(engine)

print("=== ORM: Declarative Models ===\n")
print(f"Registered models:")
for name, cls in Base.registry._class_registry.items():
    if hasattr(cls, "__tablename__"):
        cols = [(c.name, str(c.type)) for c in cls.__table__.columns]
        print(f"\n  {name} ({cls.__tablename__}):")
        for col_name, col_type in cols:
            print(f"    {col_name:12s} {col_type}")

print(f"\nTables in DB: {Base.metadata.tables.keys()}")
print("\nModels defined with SQLAlchemy 2.0 style (Mapped + mapped_column).")
