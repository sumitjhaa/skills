# 🧪 Testing
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Test fixtures with SQLAlchemy, transaction rollback strategy, factories, and mocking.

## Test Setup

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    conn = engine.connect()
    trans = conn.begin()
    session = Session(bind=conn)
    yield session
    session.close()
    trans.rollback()
    conn.close()
```

## Transaction Rollback Strategy

The key insight: wrap tests in a transaction and rollback after each test. This:
- Is faster than recreating tables
- Isolates tests
- Ensures clean state

## Test Examples

```python
def test_create_product(session):
    product = Product(name="Test", price=10.0)
    session.add(product)
    session.commit()
    assert product.id is not None

def test_query_products(session):
    session.add_all([Product(name="A"), Product(name="B")])
    session.commit()
    products = session.query(Product).all()
    assert len(products) == 2
```

## Factory Pattern

```python
class ProductFactory:
    @staticmethod
    def create(session, **kwargs):
        defaults = dict(name="Default", price=9.99, in_stock=True)
        defaults.update(kwargs)
        obj = Product(**defaults)
        session.add(obj)
        session.flush()
        return obj
```

## Run the Code

```bash
python -m pytest code/18-testing.py -v
```
