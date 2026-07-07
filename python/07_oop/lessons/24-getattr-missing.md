# 🎯 `__getattr__` & `__missing__`
<!-- ⏱️ 13 min | 🔴 Difficulty | 🧠 Applied -->

**What You'll Learn:** Intercept attribute lookups with `__getattr__` vs `__getattribute__`, and handle missing dictionary keys with `__missing__`.

> 💡 **TL;DR — The whole point:** `__getattr__` lets you define fallback behaviour for missing attributes (dynamic API endpoints), while `__missing__` gives dict subclasses custom key-not-found responses instead of raising `KeyError`.

## 🔗 Why This Matters
An API client should accept `client.users` and dynamically generate `https://api.example.com/v1/users` without predefining every endpoint. A dict subclass should return a friendly default instead of crashing on missing keys. Both patterns make your objects more forgiving and dynamic.

## The Concept
- **`__getattr__`** is called only when normal attribute lookup fails — perfect for dynamic fallbacks
- **`__getattribute__`** is called on *every* attribute access (use with caution — easy to recurse)
- **`__missing__`** is called by `dict.__getitem__` when a key is not in the dict — no `KeyError`
- **`__dir__`** customizes what `dir(obj)` shows, improving discoverability

## Code Example
```python
"""__getattr__, __getattribute__, __missing__ — dynamic attribute handling"""

class DefaultDict(dict):
    def __missing__(self, key):
        return f"<{key}: not found>"

class APIClient:
    BASE = "https://api.example.com/v1"

    def __getattr__(self, name):
        return f"{self.BASE}/{name}"

    def __dir__(self):
        return super().__dir__() + ["users", "orders", "products"]

d = DefaultDict({"name": "Alice"})
print(f"name={d['name']}, missing={d['xyz']}")

api = APIClient()
print(f"Users URL: {api.users}")
print(f"Orders URL: {api.orders}")
print(f"Known endpoints: {'users' in dir(api)}")
```

## 🔍 How It Works
- `DefaultDict` subclasses `dict` and overrides `__missing__` — `d['xyz']` returns `"<xyz: not found>"` instead of raising `KeyError`
- `APIClient.__getattr__` intercepts any undefined attribute — `api.users` becomes `"https://api.example.com/v1/users"`
- `__dir__` adds `"users"`, `"orders"`, `"products"` to the standard dir listing — IDE autocompletion works
- Real attributes (like `api.BASE`) are never routed through `__getattr__` because they exist in `__dict__`
- `__getattr__` only fires for attributes NOT found through normal lookup (instance `__dict__` then class hierarchy)

## ⚠️ Common Pitfall
`__getattr__` + `__getattribute__` confusion: `__getattr__` is safe and targeted (only missing attrs). `__getattribute__` runs on EVERY access and is easy to recurse (e.g., `self.x` inside `__getattribute__` calls itself). Use `__getattr__` unless you truly need to intercept every lookup.

## 🧠 Memory Aid
"`__getattr__` = last resort safety net. `__missing__` = friendly librarian who says 'we don't have that, but here's a note' instead of 'ERROR: NOT FOUND'."

## 🏃 Try It
Create a `CaseInsensitiveDict(dict)` that overrides `__missing__` to look up lowercase keys. If `d["Name"]` fails, try `d["name"]`.

## 🔗 Related
- [Properties](06-properties.md) — attribute access control with `@property`
- [Dunder Methods](05-dunder-methods.md) — `__getattribute__`, `__setattr__`, `__delattr__`

## ➡️ Next
*(Last nitigrity lesson — revisit topics from Phase 07 to reinforce.)*
