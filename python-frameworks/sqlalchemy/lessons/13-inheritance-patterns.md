# 🧬 Inheritance Patterns
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Single Table Inheritance, Joined Table Inheritance, polymorphic queries.

## Single Table Inheritance (STI)

All classes map to one table with a discriminator column.

```python
class Animal(Base):
    __tablename__ = "animals"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))  # discriminator
    name: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "animal"}

class Dog(Animal):
    breed: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {"polymorphic_identity": "dog"}

class Cat(Animal):
    __mapper_args__ = {"polymorphic_identity": "cat"}
```

## Joined Table Inheritance (JTI)

Each class has its own table, joined via FK.

```python
class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str]
    model: Mapped[str]
    type: Mapped[str]
    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "vehicle"}

class Car(Vehicle):
    __tablename__ = "cars"
    id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    doors: Mapped[int]
    __mapper_args__ = {"polymorphic_identity": "car"}
```

## Querying

```python
# All animals (returns Dog and Cat instances)
session.query(Animal).all()

# Just dogs
session.query(Dog).all()

# Filter by subtype columns
session.query(Dog).filter(Dog.breed == "Labrador").all()
```

<!-- 🤔 STI is faster for queries (single table). JTI is more normalized. -->

## Run the Code

```bash
python code/13-inheritance-patterns.py
```
