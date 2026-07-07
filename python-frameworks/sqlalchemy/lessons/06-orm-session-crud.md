# 💾 ORM: Session & CRUD
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Session management, CRUD operations via ORM, `sessionmaker`.

## Session Setup

```python
from sqlalchemy.orm import Session, sessionmaker

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
```

## Create

```python
book = Book(title="Python 101", author="Alice", price=29.99)
session.add(book)
session.commit()
# book.id is now set
```

Batch create:

```python
session.add_all([
    Book(title="Book 1", author="Alice", price=19.99),
    Book(title="Book 2", author="Bob", price=29.99),
])
session.commit()
```

## Read

```python
# All
books = session.query(Book).all()

# By primary key
book = session.get(Book, 1)

# Filtered
books = session.query(Book).filter(Book.author == "Alice").all()

# First matching
book = session.query(Book).filter(Book.title == "Python 101").first()
```

## Update

```python
book = session.get(Book, 1)
book.price = 24.99
session.commit()
```

## Delete

```python
book = session.query(Book).filter(Book.title == "Old Book").first()
session.delete(book)
session.commit()
```

## Session Best Practices

- One session per request (in web apps)
- Always close: `session.close()`
- Commit on success, rollback on error
- Use `sessionmaker()` as a factory

<!-- 🧠 `session.get(Model, pk)` is the most efficient way to load by primary key. -->

## Run the Code

```bash
python code/06-orm-session-crud.py
```
