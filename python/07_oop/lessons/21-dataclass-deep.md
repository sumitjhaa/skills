# 🎯 Dataclass Deep
<!-- ⏱️ 14 min | 🟡 Difficulty | 🧠 Applied -->

**What You'll Learn:** Advanced dataclass features — `field()` options, `__post_init__`, `replace()`, and `KW_ONLY` — using user profiles.

> 💡 **TL;DR — The whole point:** Beyond the basics, dataclasses give you field-level metadata, computed sort indexes, immutable `replace()`, and keyword-only fields to prevent positional misuse.

## 🔗 Why This Matters
User profiles need email validation, age ranges, optional tags, and internal notes. `field(metadata=...)` encodes business rules, `__post_init__` validates, and `replace()` creates updated copies of frozen-like instances without mutation.

## The Concept
`field()` controls per-field behaviour: `default_factory` for mutable types, `init=False` for computed fields, `repr=False` for secrets, `metadata` for validation rules. `__post_init__` runs after the auto-generated `__init__`. `replace()` returns a new instance with specified fields changed. `KW_ONLY` (Python 3.10+) forces fields to be keyword-only.

## Code Example
```python
"""@dataclass deep: field options, post_init, InitVar, replace — user profiles"""
from dataclasses import dataclass, field, replace
import re

@dataclass(order=True)
class User:
    sort_index: int = field(init=False, repr=False)
    user_id: str
    name: str
    email: str
    age: int = field(default=18, metadata={"min": 13, "max": 120})
    tags: list[str] = field(default_factory=list, compare=False)
    _internal_note: str = field(default="", repr=False)

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError(f"Invalid email: {self.email}")
        meta = self.__dataclass_fields__["age"].metadata
        if not (meta["min"] <= self.age <= meta["max"]):
            raise ValueError(f"Age {self.age} out of range [{meta['min']}-{meta['max']}]")
        self.sort_index = self.age

users = [
    User("u1", "Alice", "alice@example.com", 30, ["admin"]),
    User("u2", "Bob", "bob@example.com", 25, ["user"]),
    User("u3", "Charlie", "charlie@test.com", 35),
]
for u in sorted(users):
    print(f"  {u.name} ({u.age})")
alice2 = replace(users[0], age=31)
print(f"Alice updated: {alice2.age}, tags same: {alice2.tags == users[0].tags}")
```

## 🔍 How It Works
- `sort_index` is computed in `__post_init__` and excluded from `__init__` and `__repr__`
- `tags` uses `default_factory=list` to avoid the mutable-default gotcha; `compare=False` keeps tags out of equality/sorting
- `_internal_note` is prefixed with `_` convention + `repr=False` — hidden from output
- `order=True` generates `__lt__`, `__le__`, etc. — users sort by fields in declaration order (then `sort_index` = age)
- `replace()` creates a new `User` with `age=31`; the original is unchanged

## ⚠️ Common Pitfall
`field(compare=False)` on `_internal_note` means it's excluded from comparison — but if you accidentally include it in `sort_index` logic, sorting breaks. Also, `order=True` sorts by ALL fields, so `sort_index` must be first (or use `compare=False` on fields that shouldn't affect order).

## 🧠 Memory Aid
"Dataclass fields are ingredients: `default_factory` is the prep station, `metadata` is the recipe card, `__post_init__` is the quality check, `replace()` is the clone machine."

## 🏃 Try It
Add a `phone` field with `KW_ONLY` so it must be passed as `phone="..."`. Use `field(metadata={"pattern": r"\d{10}"})` and validate it in `__post_init__`.

## 🔗 Related
- [Dataclasses](08-dataclasses.md) — the basics: frozen, order, default_factory

## ➡️ Next
[Enum Patterns](22-enum-patterns.md)
