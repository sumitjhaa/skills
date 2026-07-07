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
