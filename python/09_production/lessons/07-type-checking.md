# 🎯 Type Checking
<!-- ⏱️ 13 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use mypy/pyright for static type checking, configure `pyproject.toml`, handle gradual typing, and third-party library stubs.

> 💡 **TL;DR — The whole point:** Type hints + a type checker catch 15-20% of bugs before runtime. Mypy is the standard — it validates your type annotations at compile time.

## 🔗 Why This Matters
A function that expects `int` but gets `str` crashes at runtime. Mypy catches this when you save the file — before you even run the tests. In production codebases, this saves thousands of debugging hours.

## The Concept
- **Static type checking**: mypy analyzes your code without running it
- **Gradual typing**: add types incrementally — start with public API, work inward
- **Strict mode**: `--strict` enables all checks (no implicit Any, no untyped defs)
- **Stubs**: `.pyi` files describe types for untyped libraries

## Code Example
```python
"""E-commerce: typed functions and classes, with type-checking annotations."""

from typing import TypedDict, Optional, Union, overload
from datetime import datetime


# ─── TypedDict for structured data ───
class ProductDict(TypedDict):
    sku: str
    name: str
    price: float
    in_stock: bool


# ─── Typed function ───
def apply_discount(price: float, discount_pct: float) -> float:
    """Apply a percentage discount to a price."""
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(price * (1 - discount_pct / 100), 2)


# ─── Overload ───
@overload
def parse_product(data: str) -> ProductDict: ...


@overload
def parse_product(data: bytes) -> ProductDict: ...


def parse_product(data: Union[str, bytes]) -> ProductDict:
    import json
    if isinstance(data, bytes):
        data = data.decode()
    raw: dict = json.loads(data)
    return ProductDict(
        sku=raw["sku"],
        name=raw["name"],
        price=float(raw["price"]),
        in_stock=bool(raw.get("in_stock", True)),
    )


# ─── Optional and Union ───
def find_product(sku: str) -> Optional[ProductDict]:
    """Find product by SKU. Returns None if not found."""
    products: list[ProductDict] = [
        {"sku": "LAP-001", "name": "Laptop", "price": 1499.99, "in_stock": True},
    ]
    for p in products:
        if p["sku"] == sku:
            return p
    return None


# ─── Generic ───
from typing import TypeVar, Generic

T = TypeVar("T")


class Result(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Optional[str] = None):
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        return self.error is None

    def unwrap(self) -> T:
        if self.error:
            raise RuntimeError(self.error)
        return self.value  # type: ignore[return-value]


# ─── Usage (type checker validates these) ───
product = find_product("LAP-001")
if product:
    discounted = apply_discount(product["price"], 10)
    print(f"Discounted: ${discounted:.2f}")

parsed = parse_product('{"sku": "MOU-001", "name": "Mouse", "price": 29.99}')
print(f"Parsed: {parsed['name']}")

result: Result[float] = Result(value=100.0)
print(f"Result: {result.unwrap()}")
```

## 🔍 How It Works
- mypy checks types without running the code: `mypy src/`
- `pyproject.toml` config: `[tool.mypy] strict = true`
- Gradual typing: add `: type` annotations, then run mypy. Fix errors, repeat
- `# type: ignore[code]` suppresses specific errors
- `--strict` mode: no `Any`, no untyped defs, no untyped calls
- Third-party stubs: `types-requests`, `types-python-dateutil`, etc.

## ⚠️ Common Pitfall
`Any` defeats type checking entirely. Use `Any` only as a last resort — prefer `object`, `Union`, or `TypeVar`. Also, mypy can't check dynamic code (e.g., `setattr()`, `__getattr__`).

## 🧠 Memory Aid
"mypy = compile-time type validation. `: type` annotations = contract. `--strict` = no loopholes. `# type: ignore` = 'I know what I'm doing' (usually not)."

## 🏃 Try It
Run `mypy --strict` on the code above. Fix any errors. Then remove the type hint from `apply_discount` and see what mypy reports about the untyped function.

## 🔗 Related
- [Typing Deep](../08_advanced/lessons/09-typing-deep.md) — advanced typing features
- [Pre-commit & Makefile](12-precommit-makefile.md) — running mypy in CI

## ➡️ Next
[Virtual Environments](08-virtual-envs.md)
