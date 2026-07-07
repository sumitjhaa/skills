# 🔗 ORM: Many-to-Many
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Association tables, `secondary` relationships, many-to-many queries.

## Association Table

```python
from sqlalchemy import Table, Column, ForeignKey

book_authors = Table(
    "book_authors", Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)
```

## Many-to-Many Models

```python
class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    authors: Mapped[list["Author"]] = relationship(
        secondary=book_authors, back_populates="books"
    )

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    books: Mapped[list["Book"]] = relationship(
        secondary=book_authors, back_populates="authors"
    )
```

## Creating Many-to-Many

```python
alice = Author(name="Alice")
bob = Author(name="Bob")
book = Book(title="Python Handbook", authors=[alice, bob])
session.add(book)
session.commit()
```

## Querying

```python
# Books by an author
author = session.query(Author).filter(Author.name == "Alice").first()
author.books  # All books Alice co-authored

# Co-authors
bobs_books = session.query(Book).join(book_authors).join(Author).filter(Author.name == "Bob").all()
```

## Complex Queries

```python
# Books with 3+ authors
from sqlalchemy import func
multi = session.query(Book).join(book_authors)\
    .group_by(Book.id).having(func.count() > 2).all()
```

<!-- 🤔 The association table is managed automatically — no need to insert into it manually. -->

## Run the Code

```bash
python code/09-orm-many-to-many.py
```
