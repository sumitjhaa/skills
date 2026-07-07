# 🎯 Mock & Patch Patterns: Mock(spec=), patch.dict, PropertyMock, AsyncMock
<!-- ⏱️ 14 min | 🔴 Advanced | 🧠 Applied -->

**What You'll Learn:** Use `Mock(spec=)`, `patch.dict`, `PropertyMock`, and `AsyncMock` for production testing of APIs, env vars, and async code.

> 💡 **TL;DR — The whole point:** `Mock(spec=Database)` prevents method name typos, `patch.dict(os.environ)` temporarily sets env vars for testing, `PropertyMock` mocks `@property` attributes, and `AsyncMock` mocks async functions for asyncio tests.

## 🔗 Why This Matters
Tests should fail on real bugs, not on typos in mock method names. Environment variables must be overridden temporarily for tests. Async code (HTTP clients, DB drivers) needs async mocks. These patterns make tests reliable and safe.

## The Concept
`Mock(spec=SomeClass)` restricts the mock to only methods/attributes that exist on `SomeClass` — calling a typo'd method raises `AttributeError`. `patch.dict(dict, values)` temporarily replaces dict items within a context. `PropertyMock` is used as the return value for `PropertyMock` on a class to mock `@property` attributes. `AsyncMock` returns an awaitable that can be used in `await` expressions.

## Code Example
```python
"""Mock patterns: API mocking, env vars, properties — production testing techniques"""
from unittest.mock import Mock, patch, PropertyMock, AsyncMock, MagicMock
import os

# --- 1. spec: strict mock that only allows real method names (prevents typos) ---
class Database:
    def query(self, sql): return [{"id": 1}]
    def insert(self, data): return 42

mock_db = Mock(spec=Database)
mock_db.query.return_value = [{"id": 1, "name": "Mocked"}]  # OK: query() exists
# mock_db.xyz()  # Would raise AttributeError — spec prevents typos

# --- 2. patch.dict: temporarily set env vars for testing (restored on exit) ---
with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///test.db", "DEBUG": "1"}):
    print(f"Test DB: {os.environ['DATABASE_URL']}")  # sqlite:///test.db
# Outside context: env vars restored to original

# --- 3. PropertyMock: mock @property attributes on objects ---
mock_obj = MagicMock()
type(mock_obj).is_authenticated = PropertyMock(return_value=True)
print(f"Is authenticated: {mock_obj.is_authenticated}")  # True

# --- 4. AsyncMock: mock async functions (for asyncio tests) ---
async_handler = AsyncMock()
async_handler.return_value = 42
# In asyncio: result = await async_handler() → returns 42

print("Mock spec OK, env patched OK, PropertyMock OK, AsyncMock OK")
```

## 🔍 How It Works
- `Mock(spec=Class)` creates a mock that only exposes the Class's real attributes — `mock_db.xyz()` raises `AttributeError`, catching typos early
- `patch.dict(target, values)` temporarily sets `target[key] = value` inside the `with` block; restores originals on exit — even if an exception occurs
- `PropertyMock(return_value=X)` when assigned to `type(obj).attr` makes `obj.attr` always return `X`
- `AsyncMock()` is a `MagicMock` subclass where `__call__` returns an awaitable — `await async_handler()` returns `return_value`
- `MagicMock` is `Mock` that does magic method lookup (needed for `PropertyMock` on `type()`)

## ⚠️ Common Pitfall
`PropertyMock` must be set on the **type**, not the instance — `type(mock_obj).attr = PropertyMock(...)`. Setting it on the instance directly (`mock_obj.attr = PropertyMock(...)`) assigns the mock object itself, not its return value.

## 🧠 Memory Aid
"spec = 'mock with guardrails.' patch.dict = 'temporary env vars.' PropertyMock on type() = 'mock a @property.' AsyncMock = 'mock for await.'"

## 🏃 Try It
Write a function `get_api_key()` that reads from `os.environ["API_KEY"]`. Test it with `patch.dict` to set `API_KEY` to `"test-key-123"` and verify the function returns it. Then test the `KeyError` case when the env var is missing.

## 🔗 Related
- [Testing with pytest](../../../09_production/lessons/04-testing-pytest.md) — pytest fixtures, parametrize, and mocking patterns

## ➡️ Next
This is the final lesson in Phase 08.
