# 🎯 Metaclasses
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** How `type()` creates classes, write custom metaclasses, understand metaclass conflicts, and see real-world applications in ORMs.

> 💡 **TL;DR — The whole point:** A metaclass is the class of a class. Just as a class creates objects, a metaclass creates classes. `type` is the default metaclass.

## 🔗 Why This Matters
Frameworks like Django, SQLAlchemy, and Pydantic use metaclasses to transform class definitions into database schemas, validation rules, and APIs. Understanding metaclasses demystifies "magic" framework code.

## The Concept
- `type` is the default metaclass. `type('Name', (bases,), {'attr': value})` creates a class dynamically
- Custom metaclasses inherit from `type` and override `__new__` to modify class creation
- `metaclass` keyword in class definition selects the metaclass

## Code Example
```python
"""ORM-inspired: Metaclass that auto-generates table names and validates fields."""


def snake_to_upper(name: str) -> str:
    return "".join("_" + c if c.isupper() else c for c in name).upper().lstrip("_")


class ModelMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)

        # Auto-generate table name
        namespace["__tablename__"] = namespace.get("__tablename__", snake_to_upper(name))

        # Validate that all "fields" have defaults
        for key, value in namespace.items():
            if isinstance(value, Field) and value.default is None and not value.nullable:
                raise TypeError(f"{name}.{key} is required but has no default")

        print(f"[Meta] Created model {name} → table {namespace['__tablename__']}")
        return super().__new__(mcs, name, bases, namespace)


class Field:
    def __init__(self, field_type: type, default=None, nullable: bool = False):
        self.field_type = field_type
        self.default = default
        self.nullable = nullable


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self) -> str:
        fields = []
        values = []
        for key in dir(self):
            if isinstance(getattr(type(self), key, None), Field):
                fields.append(key)
                values.append(getattr(self, key))
        return f"INSERT INTO {self.__tablename__} ({', '.join(fields)}) VALUES ({', '.join(map(str, values))})"


class User(Model):
    __tablename__ = "users"
    id = Field(int, default=0)
    name = Field(str, nullable=False)
    email = Field(str)


user = User(id=1, name="Alice", email="alice@example.com")
print(user.save())
print(f"Table: {User.__tablename__}")
```

## 🔍 How It Works
- `ModelMeta.__new__` intercepts class creation — it runs when you define `class User(Model):`
- `super().__new__(mcs, name, bases, namespace)` creates the actual class
- Metaclasses can validate, modify, or reject class definitions
- Metaclass conflicts happen when a class inherits from classes with different metaclasses
- Django's `Model` metaclass transforms fields into database column definitions

## ⚠️ Common Pitfall
Metaclass conflicts: if two parent classes have different metaclasses, and neither is a subclass of the other, you get `TypeError: metaclass conflict`. Always create a common base metaclass.

## 🧠 Memory Aid
"Class is blueprint for objects. Metaclass is blueprint for classes. `type` = metaclass factory."

## 🏃 Try It
Create a `SingletonMeta` metaclass that makes any class using it a singleton. Use it to create a `DatabaseConnection` class.

## 🔗 Related
- [Slots & New](10-slots-new.md) — `__new__` in object creation
- [\_\_init_subclass\_\_](13-init-subclass.md) — modern alternative to metaclasses for simple cases

## ➡️ Next
[__init_subclass__](13-init-subclass.md)
