"""ORM: Session Management — sessionmaker, CRUD via ORM."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float, default=0.0)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# CREATE
session = SessionLocal()
session.add_all([
    Book(title="Python 101", author="Alice", price=29.99),
    Book(title="SQLAlchemy Guide", author="Bob", price=39.99),
    Book(title="FastAPI Cookbook", author="Alice", price=49.99),
])
session.commit()
print("=== ORM: Session & CRUD ===\n")
print("1. Created 3 books")

# READ all
books = session.query(Book).all()
print("\n2. All books:")
for b in books:
    print(f"   [{b.id}] {b.title:25s} by {b.author:8s} ${b.price}")

# READ with filter
alice_books = session.query(Book).filter(Book.author == "Alice").all()
print(f"\n3. Alice's books ({len(alice_books)}):")
for b in alice_books:
    print(f"   {b.title}")

# UPDATE
book = session.query(Book).filter(Book.title == "Python 101").first()
book.price = 24.99
session.commit()
book = session.get(Book, 1)
print(f"\n4. After update: {book.title} = ${book.price}")

# DELETE
book = session.query(Book).filter(Book.title == "FastAPI Cookbook").first()
session.delete(book)
session.commit()
count = session.query(Book).count()
print(f"5. After delete: {count} books remaining")
session.close()
