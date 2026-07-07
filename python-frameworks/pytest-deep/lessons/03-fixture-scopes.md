# 🎯 Fixture Scopes
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** function, class, module, session scopes — when to use each.

## Scope Options

```python
@pytest.fixture(scope="function")   # Default — created per test
@pytest.fixture(scope="class")      # Once per test class
@pytest.fixture(scope="module")     # Once per module
@pytest.fixture(scope="session")    # Once per pytest run
```

## Session-Scoped Example

```python
@pytest.fixture(scope="session")
def db_engine():
    return create_engine("sqlite:///test.db")

# All tests share the same engine
```

## Module-Scoped Example

```python
@pytest.fixture(scope="module")
def data():
    return load_big_dataset()  # Loaded once per file
```

## Scope Ordering

```
session → module → class → function
```

Inner scopes can request outer-scoped fixtures, not vice versa.

## When to Use

| Scope | Use Case |
|-------|----------|
| `function` | Default. Isolated state. |
| `class` | Group of related tests sharing setup. |
| `module` | Expensive setup shared across file. |
| `session` | DB engine, config, API client. |

<!-- 🤔 Use higher scopes for expensive resources (DB connections, API clients). -->

## Run the Code

```bash
pytest code/03-fixture-scopes.py -v
```
