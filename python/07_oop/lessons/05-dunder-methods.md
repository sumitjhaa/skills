# 🎯 Dunder Methods — Protocols & Conversions
<!-- ⏱️ 18 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Master Python's protocol dunder methods — container, numeric, math, lifecycle, and copy protocols — using playlist, vector, and file-path domains.

> 💡 **TL;DR — The whole point:** Dunder methods hook your objects into Python's built-in protocols (`in`, `len()`, `int()`, `round()`, `copy.copy()`, etc.) so they behave like first-class Python citizens.

## 🔗 Why This Matters
A `Playlist` object should support `"song" in playlist`, `len(playlist)`, `playlist[0]`, `reversed(playlist)`. A `Temperature` should work with `int()`, `round()`, `f"{obj:fmt}"`. These protocols make your classes intuitive and idiomatic.

## The Concept
Every Python built-in maps to a dunder: `in` → `__contains__`, `len()` → `__len__`, `int()` → `__int__`, `round()` → `__round__`, `reversed()` → `__reversed__`, `dir()` → `__dir__`. Implement the dunder, get the feature for free.

## Code Example — Container Protocol

```python
"""Playlist: container/sequence protocol — contains, len, get/set/del item, reversed."""

class Playlist:
    def __init__(self, songs):
        self._songs = songs

    def __contains__(self, song):
        return song in self._songs          # "song" in playlist

    def __len__(self):
        return len(self._songs)              # len(playlist)

    def __getitem__(self, i):
        return self._songs[i]                # playlist[0]

    def __setitem__(self, i, v):
        self._songs[i] = v                   # playlist[0] = "X"

    def __delitem__(self, i):
        del self._songs[i]                   # del playlist[0]

    def __reversed__(self):
        return Playlist(list(reversed(self._songs)))  # reversed(playlist)

    def __bool__(self):
        return len(self._songs) > 0          # if playlist: ...


pl = Playlist(["Bohemian Rhapsody", "Stairway to Heaven"])
print(f"'Stairway' in pl: {'Stairway' in pl}")  # True
print(f"len: {len(pl)}")                       # 2
for song in reversed(pl):                      # iterator protocol
    print(f"  {song}")
```

## Code Example — Numeric Conversion Protocol

```python
"""Vector2D: numeric conversions — int, float, bool, index, round, format."""

import math

class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __int__(self):
        return int(math.sqrt(self.x**2 + self.y**2))   # int(vector) → 5

    def __float__(self):
        return math.sqrt(self.x**2 + self.y**2)         # float(vector) → 5.0

    def __bool__(self):
        return self.x != 0 or self.y != 0               # bool(Vector2D(0,0)) → False

    def __index__(self):
        return int(self)                                 # bin(), hex(), oct()

    def __round__(self, ndigits=0):
        return Vector2D(round(self.x, ndigits),          # round(v, 1)
                        round(self.y, ndigits))

    def __format__(self, fmt):
        if fmt == "polar":
            return f"({math.hypot(self.x,self.y):.1f}∠{math.degrees(math.atan2(self.y,self.x)):.1f}°)"
        return f"({self.x}, {self.y})"


v = Vector2D(3, 4)
print(f"int: {int(v)}, float: {float(v):.1f}")          # int: 5, float: 5.0
print(f"round: {round(v, 1)}")                          # (3.0, 4.0)
print(f"polar: {v:polar}")                               # (5.0∠53.1°)
print(f"hex: {hex(v)}")                                  # 0x5  (via __index__)
```

## Code Example — Math/Rounding Protocol

```python
"""Duration: math protocol — ceil, floor, round, trunc."""

import math

class Duration:
    def __init__(self, seconds):
        self.seconds = seconds

    def __ceil__(self):
        return Duration(math.ceil(self.seconds))         # math.ceil(d)

    def __floor__(self):
        return Duration(math.floor(self.seconds))        # math.floor(d)

    def __round__(self, ndigits=0):
        return Duration(round(self.seconds, ndigits))    # round(d)

    def __trunc__(self):
        return Duration(int(self.seconds))               # math.trunc(d)

    def __str__(self):
        return f"{self.seconds}s"


d = Duration(12.7)
print(f"ceil: {math.ceil(d)}, floor: {math.floor(d)}")   # 13s, 12s
print(f"round: {round(d)}, trunc: {math.trunc(d)}")      # 13s, 12s
```

## Code Example — Object Lifecycle Protocol

```python
"""FileSystemPath: lifecycle — del, sizeof, format, fspath."""

import os
import sys

class FileSystemPath:
    def __init__(self, path):
        self.path = path

    def __del__(self):
        print(f"Cleanup: {self.path}")                   # destructor

    def __sizeof__(self):
        return sys.getsizeof(self.path) + 32              # sys.getsizeof()

    def __format__(self, fmt):
        if fmt == "abs":
            return os.path.abspath(self.path)
        return self.path

    def __fspath__(self):
        return self.path                                  # os.path functions


fp = FileSystemPath("/tmp/data.csv")
print(f"formatted: {fp:abs}")                             # /tmp/data.csv
print(f"sizeof: {sys.getsizeof(fp)} bytes")
print(f"os.path.exists: {os.path.exists(fp)}")           # via __fspath__
```

## Code Example — Other Protocols (dir, match_args, copy)

```python
"""Card: dir, match_args, copy/deepcopy."""

from copy import copy, deepcopy

class Card:
    __match_args__ = ("rank", "suit")                     # match/case support

    def __init__(self, rank, suit):
        self.rank, self.suit = rank, suit

    def __dir__(self):
        return ["rank", "suit", "display"]                # customize dir()

    def __copy__(self):
        return Card(self.rank, self.suit)                  # copy.copy()

    @property
    def display(self):
        return f"{self.rank} of {self.suit}"


c = Card("Ace", "Spades")
print(f"dir: {[d for d in dir(c) if not d.startswith('_')]}")  # ['rank', 'suit', 'display']
c2 = copy(c)
print(f"copy: {c2.display}")

match c:
    case Card("Ace", "Spades"):
        print("Ace of Spades matched!")
```

## 🔍 How It Works

| Protocol | Dunders | Trigger |
|----------|---------|---------|
| **Container** | `__contains__`, `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__reversed__` | `in`, `len()`, `[]`, `del []`, `reversed()` |
| **Numeric** | `__int__`, `__float__`, `__complex__`, `__bool__`, `__index__` | `int()`, `float()`, `complex()`, truthiness, `hex()` |
| **Math** | `__ceil__`, `__floor__`, `__round__`, `__trunc__` | `math.ceil()`, `math.floor()`, `round()`, `math.trunc()` |
| **Lifecycle** | `__del__`, `__sizeof__`, `__format__`, `__fspath__` | destructor, `sys.getsizeof()`, `f"{obj:fmt}"`, `os.path` |
| **Other** | `__dir__`, `__length_hint__`, `__match_args__`, `__copy__`, `__deepcopy__` | `dir()`, `list()` hint, `match/case`, `copy.copy()` |

## ⚠️ Common Pitfall

Forgetting `__index__` when you need `hex()`, `bin()`, or `range[start:stop:step]` with custom numeric types. Without `__index__`, Python requires a plain `int`.

## 🧠 Memory Aid

"`__X__` = built-in X support." If you want `in`, implement `__contains__`. If you want `int()`, implement `__int__`. Each built-in has one hook.

## 🏃 Try It

1. Add `__length_hint__` to an iterator class that estimates remaining items.
2. Add `__deepcopy__` to `Playlist` that deep-copies song strings.
3. Create a `Temperature` class supporting `__ceil__`, `__floor__`, `__round__`, and `f"{t:C}"` for Celsius.

## 🔗 Related

- [Operator Overloading](05-operator-overloading.md) — `+`, `-`, `*`, comparisons, in-place operators
- [Properties](06-properties.md) — `@property` as alternative to getter/setter dunders

## ➡️ Next

[Operator Overloading](05-operator-overloading.md)
