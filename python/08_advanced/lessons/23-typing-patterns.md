# 🎯 Typing Patterns: NewType, Annotated, cast, Final, TYPE_CHECKING
<!-- ⏱️ 14 min | 🔴 Advanced | 🧠 Applied -->

**What You'll Learn:** Use `NewType`, `Annotated`, `cast`, `Final`, and `TYPE_CHECKING` for type-safe production APIs.

> 💡 **TL;DR — The whole point:** Advanced typing gives you compile-time safety without runtime cost — `NewType` creates distinct types from primitives, `Annotated` attaches metadata, `Final` prevents reassignment, and `TYPE_CHECKING` avoids circular imports.

## 🔗 Why This Matters
APIs need type-safe IDs (not just any `int`). Middleware validation benefits from metadata on fields (e.g., port range). Mypy catches `Final` reassignment errors. Circular imports between modules are avoided with `TYPE_CHECKING`.

## The Concept
`NewType` creates a subtype of `int`/`str` that mypy treats as distinct (but is the same at runtime). `Annotated[T, metadata]` attaches extra info to a type for tools/frameworks. `cast(Type, value)` tells mypy "trust me, it's this type." `Final` makes a variable read-only. `TYPE_CHECKING` is `True` only during type-checking, so guarded imports are invisible at runtime.

## Code Example
```python
"""typing patterns: NewType, cast, Annotated, TYPE_CHECKING — production APIs"""
from typing import NewType, Annotated, cast, TYPE_CHECKING, Final, Literal
from dataclasses import dataclass

# NewType: type-safe distinct integer types (caught by mypy, int at runtime)
UserId = NewType('UserId', int)
def get_user(uid: UserId) -> dict:
    return {"id": uid, "name": f"user_{uid}"}

# Annotated: attach metadata for validation / OpenAPI schema generation (3.9+)
@dataclass
class Config:
    port: Annotated[int, "Must be 1024-65535"] = 8080
    env: Literal["dev", "staging", "production"] = "dev"

# Final: prevent reassignment (mypy catches reassignment errors)
MAX_RETRIES: Final = 3

# cast: tell mypy what you know it can't prove (use sparingly)
def process_item(item: object):
    number = cast(int, item)  # "Trust me, it's an int"
    return number * 2  # Without cast, mypy errors on object.__mul__

# TYPE_CHECKING: avoid circular imports at runtime (only import during type-check)
if TYPE_CHECKING:
    from some_module import SomeType  # Never executed at runtime

# NamedTuple with defaults (Python 3.6.1+)
from typing import NamedTuple
class Point(NamedTuple):
    x: float = 0.0
    y: float = 0.0

# Usage
uid = UserId(42)
print(f"  User: {get_user(uid)}")  # UserId is int at runtime
cfg = Config(env="production")
print(f"  Config: {cfg}")
print(f"  Processed: {process_item(5)}")
print(f"  Point: {Point(3.0, 4.0)}")
```

## 🔍 How It Works
- `NewType('Name', BaseType)` creates a callable that returns `BaseType` — mypy sees it as a distinct type, catching `UserId` passed where a regular `int` is expected
- `Annotated[Type, meta]` stores metadata in `__metadata__` — used by Pydantic, FastAPI, and custom validators
- `Final` prevents reassignment — mypy errors on `MAX_RETRIES = 5`
- `cast(Type, value)` erases the static type to `Type` — no runtime effect, use only when you know more than mypy
- `TYPE_CHECKING` is a `False` constant at runtime — imports under `if TYPE_CHECKING:` are only resolved by the type checker

## ⚠️ Common Pitfall
`NewType` does NOT create a new class — `isinstance(UserId(42), UserId)` raises `TypeError`. Use `NewType` only for type-checking, not runtime type discrimination. For real distinct classes, use a wrapper class.

## 🧠 Memory Aid
"NewType = 'same int, different label for mypy.' Final = 'set once, never change.' cast = 'trust me, I know the type.' TYPE_CHECKING = 'imports only mypy sees.'"

## 🏃 Try It
Define `OrderId = NewType('OrderId', int)` and write a function that accepts only `OrderId`. Try passing a plain `int` — observe the mypy error. Use `cast` to fix it.

## 🔗 Related
- [Typing Deep](09-typing-deep.md) — `Protocol`, `TypeVar`, `Generic`
- [Typing Deep II](11-typing-deep-ii.md) — `Literal`, `TypedDict`, `overload`

## ➡️ Next
[pathlib Deep](24-pathlib-deep.md)
