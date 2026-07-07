"""Testing with SQLAlchemy — test fixtures, rollback strategies, factories."""
from sqlalchemy import create_engine, String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)

class TestResult:
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.error = None

    def __str__(self):
        icon = "✅" if self.passed else "❌"
        return f"{icon} {self.name}" + (f" — {self.error}" if self.error else "")

def test(name):
    def deco(f):
        def wrapper():
            r = TestResult(name)
            try:
                f()
                r.passed = True
            except AssertionError as e:
                r.error = str(e)
            except Exception as e:
                r.error = f"{type(e).__name__}: {e}"
            results.append(r)
            return r
        return wrapper
    return deco

def setup():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    session.add(Product(name="Test Product", price=29.99, stock=10))
    session.commit()
    return session, engine

results = []

@test("Create product")
def test_create():
    s, eng = setup()
    p = Product(name="New", price=9.99, stock=5)
    s.add(p)
    s.commit()
    assert p.id is not None
    assert s.query(Product).count() == 2
    s.close()

@test("Read product")
def test_read():
    s, eng = setup()
    p = s.query(Product).filter(Product.name == "Test Product").first()
    assert p is not None
    assert p.price == 29.99
    assert p.stock == 10
    s.close()

@test("Update product")
def test_update():
    s, eng = setup()
    p = s.query(Product).first()
    p.price = 24.99
    s.commit()
    s.refresh(p)
    assert p.price == 24.99
    s.close()

@test("Delete product")
def test_delete():
    s, eng = setup()
    p = s.query(Product).first()
    s.delete(p)
    s.commit()
    assert s.query(Product).count() == 0
    s.close()

@test("Validation: negative price")
def test_negative_price():
    s, eng = setup()
    p = Product(name="Bad", price=-5.0, stock=1)
    s.add(p)
    s.commit()
    p2 = s.query(Product).filter(Product.name == "Bad").first()
    assert p2.price < 0
    s.close()

@test("Transaction rollback")
def test_rollback():
    s, eng = setup()
    p = Product(name="Rollback", price=50.0)
    s.add(p)
    s.rollback()
    assert s.query(Product).filter(Product.name == "Rollback").count() == 0
    s.close()

@test("Bulk insert")
def test_bulk():
    s, eng = setup()
    s.add_all([Product(name=f"Bulk {i}", price=i * 10.0) for i in range(100)])
    s.commit()
    assert s.query(Product).count() == 101
    s.close()

print("=== Testing with SQLAlchemy ===\n")

for t in test_create, test_read, test_update, test_delete, test_negative_price, test_rollback, test_bulk:
    r = t()
    print(f"  {r}")

passed = sum(1 for r in results if r.passed)
print(f"\nResults: {passed}/{len(results)} passed")
