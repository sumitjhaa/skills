"""Inheritance Patterns — single table, joined table, concrete table."""
from sqlalchemy import create_engine, String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

# Single Table Inheritance
class Animal(Base):
    __tablename__ = "animals"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(20))
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "animal"}

class Dog(Animal):
    __mapper_args__ = {"polymorphic_identity": "dog"}
    breed: Mapped[str] = mapped_column(String(50), nullable=True)

class Cat(Animal):
    __mapper_args__ = {"polymorphic_identity": "cat"}
    indoor: Mapped[bool] = mapped_column(default=True)

# Joined Table Inheritance
class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(20))
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "vehicle"}

class Car(Vehicle):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    doors: Mapped[int] = mapped_column(default=4)
    __mapper_args__ = {"polymorphic_identity": "car"}

class Motorcycle(Vehicle):
    __tablename__ = "motorcycles"
    id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    has_sidecar: Mapped[bool] = mapped_column(default=False)
    __mapper_args__ = {"polymorphic_identity": "motorcycle"}

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

session.add_all([
    Dog(name="Rex", breed="German Shepherd"),
    Dog(name="Buddy", breed="Golden Retriever"),
    Cat(name="Whiskers", indoor=True),
    Cat(name="Tom", indoor=False),
])
session.commit()

session.add_all([
    Car(brand="Toyota", doors=4),
    Car(brand="Ferrari", doors=2),
    Motorcycle(brand="Harley", has_sidecar=False),
    Motorcycle(brand="BMW", has_sidecar=True),
])
session.commit()

print("=== Inheritance Patterns ===\n")

print("1. Single Table Inheritance (animals):")
for a in session.query(Animal).all():
    if isinstance(a, Dog):
        print(f"   🐕 {a.name} — {a.breed}")
    elif isinstance(a, Cat):
        icon = "🏠" if a.indoor else "🌳"
        print(f"   🐱 {a.name} — {icon}")

print("\n2. Joined Table Inheritance (vehicles):")
for v in session.query(Vehicle).all():
    if isinstance(v, Car):
        print(f"   🚗 {v.brand} ({v.doors} doors)")
    elif isinstance(v, Motorcycle):
        sc = "w/ sidecar" if v.has_sidecar else ""
        print(f"   🏍️ {v.brand} {sc}")

print(f"\n3. Query by subtype:")
dogs = session.query(Dog).all()
print(f"   Dogs: {[d.name for d in dogs]}")
cars = session.query(Car).all()
print(f"   Cars: {[c.brand for c in cars]}")

session.close()
