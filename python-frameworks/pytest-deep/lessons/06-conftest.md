# 📁 Conftest
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Shared fixtures across test files, conftest hierarchy.

## What is conftest.py?

A file where you put shared fixtures, hooks, and plugins. Pytest automatically discovers `conftest.py` in each directory.

```
tests/
├── conftest.py          # Fixtures for all tests
├── test_users.py
└── test_orders.py
```

## Shared Fixture Example

```python
# tests/conftest.py
import pytest

@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.close()
```

```python
# tests/test_users.py
def test_create_user(db_session):  # Injected from conftest
    ...

# tests/test_orders.py
def test_create_order(db_session):  # Same fixture
    ...
```

## Conftest Hierarchy

```
project/
├── conftest.py           # Session-scoped fixtures (DB engine)
├── tests/
│   ├── conftest.py       # Module-scoped fixtures (test data)
│   ├── unit/
│   │   └── conftest.py   # Unit-test specific fixtures
│   └── integration/
│       └── conftest.py   # Integration-test specific fixtures
```

Lower-level conftest overrides higher-level fixtures.

<!-- 🤔 Conftest files can be in subdirectories — fixtures are available to all tests in that subtree. -->

## Run the Code

```bash
pytest code/06-conftest/ -v
```
