# 🎯 Enums Deep
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `IntFlag`, `Flag`, `auto()`, `StrEnum`, `@unique`, and the functional API with real-world domains like permissions, state machines, and HTTP methods.

> 💡 **TL;DR — The whole point:** Enums define a fixed set of named constants. `IntFlag` and `Flag` let you combine them as bitmasks. `StrEnum` gives string-compatible enums. `@unique` guarantees no duplicate values.

## 🔗 Why This Matters
HTTP status codes, user roles, order statuses, file permissions — all are natural enum use cases. `IntFlag` powers Unix-style permission bitmasks. State machines use enums for valid state transitions.

## The Concept
- `Enum` — basic named constants with `name` and `value`
- `IntEnum` — enum values that are also `int` (comparable with integers)
- `StrEnum` — enum values that are also strings (Python 3.11+)
- `Flag` / `IntFlag` — combinable flags using `|`, `&`, `~` operators
- `auto()` — automatically assign values
- `@unique` — ensure no duplicate values

## Code Example
```python
"""Permissions system with IntFlag, HTTP methods with StrEnum, order states with auto()."""

from enum import Enum, IntFlag, auto, unique
from typing import Final

# ─── IntFlag: Unix-style permissions ───


class Permission(IntFlag):
    NONE = 0
    READ = auto()      # 1
    WRITE = auto()     # 2
    EXECUTE = auto()   # 4
    DELETE = auto()    # 8


def check_permission(user_perm: Permission, required: Permission) -> bool:
    return (user_perm & required) == required


admin = Permission.READ | Permission.WRITE | Permission.EXECUTE | Permission.DELETE
dev = Permission.READ | Permission.WRITE
viewer = Permission.READ

print(f"Admin can delete: {check_permission(admin, Permission.DELETE)}")  # True
print(f"Dev can execute: {check_permission(dev, Permission.EXECUTE)}")    # False
print(f"Perm value: {dev.value}")  # 3 (READ=1 | WRITE=2)

# ─── @unique: no duplicates ───


@unique
class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# ─── StrEnum (Python 3.11+): HTTP methods ───

try:
    from enum import StrEnum

    class HttpMethod(StrEnum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        PATCH = "PATCH"

    print(f"Method comparison: {HttpMethod.GET == 'GET'}")  # True — string compatible

except ImportError:
    pass  # Python < 3.11

# ─── Functional API ───
StatusCode = Enum("StatusCode", ["OK", "NOT_FOUND", "ERROR", "UNAUTHORIZED"])
print(f"Functional: {StatusCode.OK}, value={StatusCode.OK.value}")  # StatusCode.OK, value=1

# ─── State machine ───
print(f"\nOrder transitions:")
for status in OrderStatus:
    print(f"  {status.name} = {status.value}")
```

## 🔍 How It Works
- `auto()` assigns incrementing values: 1, 2, 4, 8 for `IntFlag` (powers of 2 for flags)
- `IntFlag` supports bitwise ops: `admin = READ | WRITE` means `1 | 2 = 3`
- `Flag` is like `IntFlag` but not an `int` subclass (safer)
- `@unique` raises `ValueError` if any two members have the same value
- Functional API: `Enum("Name", ["A", "B", "C"])` creates `Name.A = 1, Name.B = 2, ...`

## ⚠️ Common Pitfall
Forgetting that `auto()` on `IntFlag` uses powers of 2. On regular `Enum`, it uses sequential integers 1, 2, 3. Don't mix them up.

## 🧠 Memory Aid
"Enum = dropdown menu. Flag = checkbox group. IntFlag = checkboxes you can OR together. @unique = 'no repeats allowed.'"

## 🏃 Try It
Create a `Weekend` `Flag` with `SATURDAY` and `SUNDAY`. Write a function `is_weekend(day)` that checks if a single-day flag is on a weekend.

## 🔗 Related
- [Dataclasses](08-dataclasses.md) — enums and dataclasses pair well
- [SOLID Principles](16-oop-solid.md) — Open/Closed principle with enums

## ➡️ Next
[SOLID Principles](16-oop-solid.md)
