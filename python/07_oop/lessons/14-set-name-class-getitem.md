# 🎯 \_\_set\_name\_\_ & \_\_class\_getitem\_\_
<!-- ⏱️ 16 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Use `__set_name__` for descriptor protocol awareness and `__class_getitem__` to make your classes generic-compatible.

> 💡 **TL;DR — The whole point:** `__set_name__` tells a descriptor what attribute name it's assigned to. `__class_getitem__` enables `MyClass[T]` syntax for generic types.

## 🔗 Why This Matters
ORM frameworks like SQLAlchemy use `__set_name__` to know which column name a field descriptor is bound to. Libraries like Pydantic use `__class_getitem__` so you can type hint `List[int]` or `Optional[str]`.

## The Concept
- `__set_name__(self, owner, name)` is called when a descriptor is assigned as a class attribute — it tells the descriptor what attribute name it was given
- `__class_getitem__(cls, item)` enables `MyClass[SomeType]` syntax without making the class generic (`Generic[T]`)

## Code Example
```python
"""ORM-inspired: Field descriptor using __set_name__ + generic validation using __class_getitem__."""

from typing import Any, get_type_hints


class Field:
    def __init__(self, field_type: type, default: Any = None):
        self.field_type = field_type
        self.default = default
        self.name = ""  # Will be set by __set_name__

    def __set_name__(self, owner: type, name: str):
        self.name = name
        print(f"[Descriptor] {owner.__name__}.{name} = Field({self.field_type.__name__})")

    def __get__(self, obj: Any, objtype: type | None = None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj: Any, value: Any):
        if not isinstance(value, self.field_type):
            raise TypeError(f"{self.name} must be {self.field_type.__name__}, got {type(value).__name__}")
        obj.__dict__[self.name] = value


class ValidatedCollection:
    """A generic-style collection using __class_getitem__."""
    _item_type: type = object

    @classmethod
    def __class_getitem__(cls, item: type):
        if not isinstance(item, type):
            raise TypeError("item must be a type")
        new_cls = type(f"{cls.__name__}[{item.__name__}]", (cls,), {"_item_type": item})
        print(f"[Generic] Created {new_cls.__name__}")
        return new_cls

    def __init__(self, items: list | None = None):
        self._items = []
        for item in items or []:
            self._add(item)

    def _add(self, item: Any) -> None:
        if not isinstance(item, self._item_type):
            raise TypeError(f"Item must be {self._item_type.__name__}, got {type(item).__name__}")
        self._items.append(item)

    def add(self, item: Any) -> None:
        self._add(item)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._items})"


class Model:
    id = Field(int, 0)
    name = Field(str, "")
    email = Field(str, "")


IntList = ValidatedCollection[int]
StrList = ValidatedCollection[str]

ints = IntList([1, 2, 3])
print(ints)

try:
    IntList(["a", "b"])  # TypeError
except TypeError as e:
    print(f"Validation works: {e}")

# __set_name__ in action
print(f"\nField names: Model.id.name={Model.id.name}, Model.name.name={Model.name.name}")
```

## 🔍 How It Works
- `Field.__set_name__` is automatically called when Python processes the `class Model:` body
- `Model.id` is a `Field` descriptor — `__get__` and `__set__` control access
- `__class_getitem__` is a class method that returns a dynamically created subclass
- `IntList = ValidatedCollection[int]` creates `ValidatedCollection[int]` with `_item_type = int`
- Unlike `Generic[T]`, `__class_getitem__` doesn't require subclassing `Generic`

## ⚠️ Common Pitfall
`__class_getitem__` vs `__getitem__`: `__class_getitem__` is for `cls[item]` on the class itself. `__getitem__` is for `obj[item]` on instances. Don't confuse them.

## 🧠 Memory Aid
"`__set_name__` = 'hi, I'm assigned as attribute X'. `__class_getitem__` = 'I can be parameterized like List[int]'."

## 🏃 Try It
Create a `Required` descriptor using `__set_name__` that raises `AttributeError` if a field is accessed before being set. Build a `UserProfile` model with it.

## 🔗 Related
- [Metaclasses](12-metaclasses.md) — class-level metaprogramming
- [Dataclasses](08-dataclasses.md) — field definitions

## ➡️ Next
[Enums Deep](15-enum-deep.md)
