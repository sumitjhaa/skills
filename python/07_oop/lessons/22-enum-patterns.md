# 🎯 Enum Patterns
<!-- ⏱️ 12 min | 🟡 Difficulty | 🧠 Applied -->

**What You'll Learn:** Combine `Flag`, `auto()`, enum-with-methods, and `StrEnum` patterns for permissions and HTTP status codes.

> 💡 **TL;DR — The whole point:** Enums can hold extra data (tuples), support bitwise combinations (`Flag`), have methods and properties, and even verify invariants — they're mini classes, not just constant lists.

## 🔗 Why This Matters
An `HTTPStatus` enum that bundles a numeric code, a message, and an `is_success` property keeps related logic together. A `Permission` `Flag` lets you combine `READ | WRITE` and check `p & READ` naturally — exactly how real ACL systems work.

## The Concept
- **`Flag`** with `auto()` gives powers-of-2 values for bitwise combinable permissions
- **Tuple-valued enums** override `__new__` to attach custom attributes (`.code`, `.message`)
- **Enum methods/properties** like `is_success` keep behaviour with the constant
- **`StrEnum`** (Python 3.11+) creates string-compatible enums
- **`@verify`** (Python 3.12+) enforces invariants like "no duplicate values"

## Code Example
```python
"""Enum patterns: Flag, StrEnum, auto — HTTP status, permissions, orders"""
from enum import Enum, Flag, auto

class Permission(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ALL = READ | WRITE | EXECUTE

class HTTPStatus(Enum):
    OK = (200, "Success")
    CREATED = (201, "Created")
    BAD_REQUEST = (400, "Bad request")
    NOT_FOUND = (404, "Not found")
    SERVER_ERROR = (500, "Server error")

    def __new__(cls, code: int, message: str):
        obj = object.__new__(cls)
        obj.code = code
        obj.message = message
        return obj

    @property
    def is_success(self):
        return 200 <= self.code < 300

p = Permission.READ | Permission.WRITE
print(f"Can execute: {bool(p & Permission.EXECUTE)}")
print(f"Has read: {bool(p & Permission.READ)}")

status = HTTPStatus.OK
print(f"{status.name}: {status.code} {status.message}, success={status.is_success}")
status404 = HTTPStatus.NOT_FOUND
print(f"{status404.name}: {status404.code} {status404.message}, success={status404.is_success}")
```

## 🔍 How It Works
- `Permission.READ | Permission.WRITE` creates a combined `Permission` with `value = 3` — bitwise OR
- `p & Permission.EXECUTE` evaluates to `0` (falsy) — `EXECUTE` is `4`, not in `3`
- `HTTPStatus.__new__` unpacks the `(code, message)` tuple and stores them as instance attributes
- `is_success` is a `@property` — reusable logic shared by every `HTTPStatus` member
- `auto()` on `Flag` generates powers of 2: `READ=1`, `WRITE=2`, `EXECUTE=4`

## ⚠️ Common Pitfall
Forgetting that `auto()` on `Flag` uses powers of 2, while on regular `Enum` it uses sequential integers `1, 2, 3`. Use `Flag` only when you intend bitwise combinations — otherwise just use `Enum`.

## 🧠 Memory Aid
"Enum = named slots. Flag = checkboxes you can OR together. `__new__` = luggage rack for extra data."

## 🏃 Try It
Add a `Permission.DELETE = auto()` member and rebuild the permissions. Add a `HTTPStatus` member for `FORBIDDEN = (403, "Forbidden")` — it should automatically get `is_success = False`.

## 🔗 Related
- [Enums Deep](15-enum-deep.md) — `IntFlag`, `@unique`, `StrEnum`, functional API

## ➡️ Next
[Descriptor Nitty](23-descriptor-nitty.md)
