# 🎯 collections.abc & __match_args__ — Abstract Base Classes for Containers
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Create custom containers that pass `isinstance` checks via `collections.abc` and make classes work with `match`/`case` pattern matching.

> 💡 **TL;DR — The whole point:** `collections.abc` lets your custom list/dict/set pass `isinstance(x, Sequence)` by implementing the right methods. `__match_args__` enables elegant destructuring in `match` statements.

## 🔗 Why This Matters
Type-safe containers, immutable data structures, and algebraic data types are the building blocks of robust Python. `isinstance(x, Iterable)` is cleaner than `hasattr(x, '__iter__')`. `match`/`case` with custom classes replaces nested `if/elif` chains with declarative pattern matching.

## The Concept
- `Sequence` — implement `__getitem__` + `__len__`. `MutableSequence` adds `__setitem__`, `__delitem__`, `insert`
- `Mapping` — implement `__getitem__`, `__iter__`, `__len__`. `MutableMapping` adds `__setitem__`, `__delitem__`
- `__subclasshook__` — override this on a custom ABC to make classes pass `isinstance` without registration
- `__match_args__` — tuple of attribute names. Used by `match` to bind positional patterns. `match obj: case MyClass(x, y):` binds `obj.x` → `x`, `obj.y` → `y`

## Code Example
```python
"""ReadOnlyList(Sequence), ImmutableDict(Mapping), algebraic Card type."""

from collections.abc import Sequence, Mapping, Iterable


class ReadOnlyList(Sequence):
    def __init__(self, items):
        self._items = list(items)
    def __getitem__(self, index):
        return self._items[index]
    def __len__(self):
        return len(self._items)

rol = ReadOnlyList([1, 2, 3])
print(f"Is Sequence: {isinstance(rol, Sequence)}")  # True
print(f"Is Iterable: {isinstance(rol, Iterable)}")  # True
print(f"rol[1] = {rol[1]}")

class ImmutableDict(Mapping):
    def __init__(self, **kwargs):
        self._data = dict(kwargs)
    def __getitem__(self, key):
        return self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)

d = ImmutableDict(name="Alice", role="admin")
print(f"Is Mapping: {isinstance(d, Mapping)}")       # True
print(f"d['name'] = {d['name']}")

class Card:
    __match_args__ = ("rank", "suit")
    def __init__(self, rank: str, suit: str):
        self.rank, self.suit = rank, suit

def score(card) -> str:
    match card:
        case Card("A", _):
            return 11
        case Card("K", _) | Card("Q", _) | Card("J", _):
            return 10
        case Card(rank, _):
            return int(rank)
        case _:
            return 0

print(f"Ace of spades: {score(Card('A', 'spades'))}")
```

## 🔍 How It Works
- When you subclass `Sequence`, Python checks you implement `__getitem__` and `__len__`. The mixin methods (`__contains__`, `__reversed__`, `index`, `count`) come free
- `__subclasshook__` is a classmethod on ABCs. `Sequence.__subclasshook__` checks for `__getitem__` and `__len__` methods. This is why `list` passes `isinstance([], Sequence)` without registering
- `__match_args__` is read by the `match` statement's pattern compiler. Position `0` maps to attribute name at index 0 of the tuple. Use `_` as a wildcard in patterns. Use `|` for OR patterns

## ⚠️ Common Pitfall
Immutable dicts that inherit from `Mapping` still need to implement `__getitem__`, `__iter__`, `__len__`. `__match_args__` only works if the class constructor takes matching positional args — otherwise the pattern can't instantiate guard expressions. Set `__hash__ = None` if your mutable class inherits from `Hashable`.

## 🧠 Memory Aid
"ABCs = interface contracts. Sequence = `__getitem__` + `__len__`. Mapping = `__getitem__` + `__iter__` + `__len__`. `__match_args__` = 'these are the positional fields for pattern matching.' `isinstance(x, Iterable)` > `hasattr(x, '__iter__')`."

## 🏃 Try It
Create a `ValidatedList(MutableSequence)` that raises `TypeError` if you try to add a non-int element. Then create an `Expr` class with `__match_args__` for a simple AST evaluator (Number, Add, Multiply).

## 🔗 Related
- [OOP: ABCs](../07_oop/lessons/07-abstract-base-classes.md) — abstract base classes
- [Typing Deep](09-typing-deep.md) — Protocol as an alternative to ABCs

## ➡️ Next
[codecs, unicodedata, difflib, textwrap](19-codecs-unicodedata-difflib-textwrap.md)
