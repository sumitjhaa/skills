# 🎯 Operator Overloading
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Core -->

**What You'll Learn:** Overload every Python operator — unary, comparison, arithmetic, reflected, and in-place — with real-world Money, Vector, and Bitmask examples.

> 💡 **TL;DR — The whole point:** Operator overloading lets `MyClass` objects work with `+`, `-`, `*`, `==`, `<`, `+=`, and more — making custom types feel like built-ins.

## 🔗 Why This Matters
A `Money` class should support `a + b`, `a - b`, `a * 2`, `sum(moneys)`, `a < b`, `a += b`. A `Vector` needs `-v`, `v + w`, `v * 3`. Without overloading, you'd write `money.add(other)` everywhere.

## The Concept
Each operator maps to a dunder: `+` → `__add__`, `-x` → `__neg__`, `a += b` → `__iadd__`, `5 + obj` → `__radd__`. Python tries the left operand's method first, then falls back to the right operand's reflected method.

## Code Example — Unary Operators

```python
"""Vector2D: unary operators — neg, pos, abs, invert."""

class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __neg__(self):
        return Vector2D(-self.x, -self.y)       # -v

    def __pos__(self):
        return Vector2D(+self.x, +self.y)       # +v

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5     # abs(v)

    def __invert__(self):
        return Vector2D(~self.x, ~self.y)       # ~v (bitwise NOT)

    def __repr__(self):
        return f"V({self.x},{self.y})"


v = Vector2D(3, 4)
print(f"-v: {-v}, +v: {+v}")
print(f"abs(v): {abs(v):.1f}")
```

## Code Example — Comparison Operators

```python
"""Money: full comparison protocol — eq, ne, lt, le, gt, ge."""

from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency

    def __eq__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount == other.amount
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return self.amount < other.amount
        return NotImplemented

    def __repr__(self):
        return f"${self.amount:.2f}"


print(Money(100) == Money(100))   # True  (via __eq__)
print(Money(50) < Money(100))     # True  (via __lt__)
print(Money(50) <= Money(100))    # True  (via @total_ordering)
print(Money(100) > Money(50))     # True
```

## Code Example — Arithmetic & Reflected Operators

```python
"""Money: arithmetic + reflected operators."""

class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency

    def __add__(self, other):                        # m + other
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented

    def __radd__(self, other):                       # 5 + m  or  sum()
        if other == 0:
            return self
        if isinstance(other, (int, float)):
            return Money(self.amount + other, self.currency)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(self.amount - other.amount, self.currency)
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount * scalar, self.currency)
        return NotImplemented

    def __rmul__(self, scalar):                      # 3 * m
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Money(self.amount / scalar, self.currency)
        return NotImplemented

    def __repr__(self):
        return f"${self.amount:.2f}"


m = Money(100)
print(f"add: {m + Money(50)}")        # $150.00
print(f"radd: {sum([m, Money(25)])}")  # $125.00  (sum() starts at 0)
print(f"mul: {m * 2}")                # $200.00
print(f"rmul: {3 * m}")               # $300.00
```

## Code Example — In-Place Operators

```python
"""Money: in-place operators — iadd, isub, imul."""

class Money:
    def __init__(self, amount, currency="USD"):
        self.amount, self.currency = amount, currency

    def __iadd__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            self.amount += other.amount
            return self                              # MUST return self
        return NotImplemented

    def __isub__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            self.amount -= other.amount
            return self
        return NotImplemented

    def __repr__(self):
        return f"${self.amount:.2f}"


m = Money(100)
m += Money(25)
print(f"after +=: {m}")              # $125.00  (same object, modified in-place)
m -= Money(10)
print(f"after -=: {m}")              # $115.00
```

## Real-World Examples

### Bitmask Permissions (Flag-like)

```python
class Permissions:
    READ = 1; WRITE = 2; EXECUTE = 4

    def __init__(self, mask=0):
        self.mask = mask

    def __or__(self, other):
        return Permissions(self.mask | other.mask)   # READ | WRITE

    def __and__(self, other):
        return Permissions(self.mask & other.mask)   # perms & READ

    def __invert__(self):
        return Permissions(~self.mask)               # ~perms

    def __contains__(self, perm):
        return bool(self.mask & perm.mask)           # READ in perms

    def __repr__(self):
        return f"Perms({self.mask:03b})"


p = Permissions(Permissions.READ | Permissions.WRITE)
print(f"READ in p: {Permissions.READ in p}")         # True
```

### Query Builder (SQLAlchemy-style)

```python
class Query:
    def __init__(self, table):
        self._table = table
        self._filters = []

    def __gt__(self, other):
        print(f"  WHERE {self._table} > {other}")     # query > 5

    def __lt__(self, other):
        print(f"  WHERE {self._table} < {other}")     # query < 10

    def __and__(self, other):
        print(f"  AND condition")                     # q1 & q2

    def __invert__(self):
        print(f"  NOT condition")                     # ~query


q = Query("price")
q > 100                                              # WHERE price > 100
q < 50                                               # WHERE price < 50
```

## 🔍 How It Works

| Category | Operators | Dunders |
|----------|-----------|---------|
| **Unary** | `-x`, `+x`, `abs(x)`, `~x` | `__neg__`, `__pos__`, `__abs__`, `__invert__` |
| **Comparison** | `==`, `!=`, `<`, `<=`, `>`, `>=` | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` |
| **Arithmetic** | `+`, `-`, `*`, `/`, `//`, `%`, `divmod`, `**`, `<<`, `>>`, `&`, `\|`, `^` | `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__divmod__`, `__pow__`, `__lshift__`, `__rshift__`, `__and__`, `__or__`, `__xor__` |
| **Reflected** | `other + self` when `type(other)` fails | `__radd__`, `__rsub__`, `__rmul__`, ... |
| **In-Place** | `+=`, `-=`, `*=`, `/=` ... | `__iadd__`, `__isub__`, `__imul__`, ... |

**Reflected rule:** `a + b` calls `type(a).__add__(a, b)`. If it returns `NotImplemented`, Python calls `type(b).__radd__(b, a)`.

**In-place rule:** `a += b` calls `__iadd__`. For immutable types, fall back to `__add__`. For mutable types, modify `self` and **return `self`**.

## ⚠️ Common Pitfall

Returning `NotImplemented` (not `NotImplementedError`) when types don't match. This lets Python try the reflected operator. Raising `TypeError` or returning `False` breaks the fallback chain.

```python
# CORRECT: let Python try the other side
def __add__(self, other):
    if isinstance(other, MyType):
        return MyType(self.val + other.val)
    return NotImplemented

# WRONG: raises on type mismatch
def __add__(self, other):
    if not isinstance(other, MyType):
        raise TypeError("Unsupported type")
    return MyType(self.val + other.val)
```

## 🧠 Memory Aid

"`r` = reverse, `i` = in-place." `__radd__` handles `5 + obj`. `__iadd__` handles `obj += 5`. Forward is `__add__`.

## 🏃 Try It

1. Add `__floordiv__` and `__mod__` to `Money` (e.g., splitting $100 among 3 people).
2. Implement `__rsub__` on `Money` so `100 - Money(30)` works.
3. Create a `Vector2D` with `__add__`, `__sub__`, `__mul__` (dot product), and `__rmul__` (scalar).

## 🔗 Related

- [Dunder Methods](05-dunder-methods.md) — protocol dunders (`__contains__`, `__len__`, numeric conversions)
- [Dataclasses](08-dataclasses.md) — auto-generates `__eq__`, `__hash__`, `__lt__` with `order=True`

## ➡️ Next

[Properties](06-properties.md)
