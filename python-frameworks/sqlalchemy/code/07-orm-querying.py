"""ORM: Querying — filter, order_by, join, eager loading, aggregates."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

authors = [Author(name="Alice"), Author(name="Bob"), Author(name="Charlie")]
session.add_all(authors)
session.commit()

session.add_all([
    Book(title="Python Basics", price=29.99, rating=4.5, author_id=1),
    Book(title="Advanced Python", price=49.99, rating=4.8, author_id=1),
    Book(title="SQLAlchemy 101", price=39.99, rating=4.2, author_id=2),
    Book(title="Web Dev with Flask", price=44.99, rating=4.6, author_id=2),
    Book(title="Data Science Intro", price=34.99, rating=3.9, author_id=3),
    Book(title="Machine Learning", price=59.99, rating=4.7, author_id=3),
])
session.commit()

print("=== ORM: Querying ===\n")

# Filter
cheap = session.query(Book).filter(Book.price < 40).all()
print(f"1. Books under $40: {[b.title for b in cheap]}")

# Order by
top = session.query(Book).order_by(Book.rating.desc()).limit(3).all()
print(f"2. Top 3 rated: {[f'{b.title} ({b.rating})' for b in top]}")

# Join
results = session.query(Book, Author).join(Author).filter(Author.name == "Alice").all()
print(f"3. Alice's books: {[r.Book.title for r in results]}")

# Aggregates
stats = session.query(
    func.count(Book.id).label("count"),
    func.avg(Book.price).label("avg_price"),
    func.max(Book.rating).label("max_rating"),
).first()
print(f"4. Stats: {stats.count} books, avg ${stats.avg_price:.2f}, max rating {stats.max_rating}")

# Eager loading
alice = session.query(Author).filter(Author.name == "Alice").first()
print(f"5. {alice.name}'s books (via relationship): {[b.title for b in alice.books]}")

session.close()
