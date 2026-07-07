"""ORM: Many-to-Many — association tables, secondary, hybrid attributes."""
from sqlalchemy import create_engine, String, Integer, Float, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

book_authors = Table(
    "book_authors", Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    authors: Mapped[list["Author"]] = relationship(secondary=book_authors, back_populates="books")

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    books: Mapped[list["Book"]] = relationship(secondary=book_authors, back_populates="authors")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

alice = Author(name="Alice")
bob = Author(name="Bob")
charlie = Author(name="Charlie")
session.add_all([alice, bob, charlie])
session.commit()

book1 = Book(title="Python Handbook", authors=[alice, bob])
book2 = Book(title="Advanced SQL", authors=[bob, charlie])
book3 = Book(title="Web Development", authors=[alice, charlie])
book4 = Book(title="Data Science 101", authors=[alice, bob, charlie])
session.add_all([book1, book2, book3, book4])
session.commit()

print("=== ORM: Many-to-Many ===\n")

print("1. Books per author:")
for author in session.query(Author).all():
    titles = [b.title for b in author.books]
    print(f"   {author.name:10s} → {', '.join(titles)}")

print("\n2. Authors per book:")
for book in session.query(Book).all():
    names = [a.name for a in book.authors]
    print(f"   '{book.title:30s}' by {', '.join(names)}")

# Query co-authored with specific author
bobs_books = session.query(Book).join(book_authors).join(Author).filter(Author.name == "Bob").all()
print(f"\n3. Books co-authored by Bob: {[b.title for b in bobs_books]}")

# Books with multiple authors
from sqlalchemy import func
multi = session.query(Book).join(book_authors).group_by(Book.id).having(func.count() > 2).all()
print(f"4. Books with 3+ authors: {[b.title for b in multi]}")
session.close()
