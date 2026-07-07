"""07-14-set-name-class-getitem.py — ORM-style: Field descriptor + generic collection."""

from typing import Any


class Field:
    def __init__(self, field_type: type, default: Any = None):
        self.field_type = field_type
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type, name: str):
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj: Any, value: Any):
        if not isinstance(value, self.field_type):
            raise TypeError(f"{self.name} must be {self.field_type.__name__}")
        obj.__dict__[self.name] = value


class ValidatedCollection:
    _item_type: type = object

    @classmethod
    def __class_getitem__(cls, item: type):
        new_cls = type(f"{cls.__name__}[{item.__name__}]", (cls,), {"_item_type": item})
        return new_cls

    def __init__(self, items: list | None = None):
        self._items = []
        for item in items or []:
            self._add(item)

    def _add(self, item: Any) -> None:
        if not isinstance(item, self._item_type):
            raise TypeError(f"Item must be {self._item_type.__name__}")
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
ints = IntList([1, 2, 3])
print(ints)

try:
    IntList(["a", "b"])
except TypeError as e:
    print(f"Validation: {e}")

print(f"Field names: id={Model.id.name}, name={Model.name.name}")
