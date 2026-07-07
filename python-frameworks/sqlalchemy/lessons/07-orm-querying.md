# 🔍 ORM: Querying
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Query methods, filtering, ordering, joins, aggregates, eager loading.

## Filtering

```python
# Equality
books = session.query(Book).filter(Book.author == "Alice").all()

# Multiple conditions
books = session.query(Book).filter(
    Book.price < 50,
    Book.rating > 4.0
).all()

# IN clause
books = session.query(Book).filter(Book.author.in_(["Alice", "Bob"])).all()

# LIKE
books = session.query(Book).filter(Book.title.like("%Python%")).all()
```

## Ordering

```python
books = session.query(Book).order_by(Book.price.desc()).all()
books = session.query(Book).order_by(Book.rating.desc()).limit(3).all()
```

## Joins

```python
results = session.query(Book, Author).join(Author).filter(Author.name == "Alice").all()
for r in results:
    print(r.Book.title, r.Author.name)
```

## Aggregates

```python
from sqlalchemy import func

stats = session.query(
    func.count(Book.id).label("count"),
    func.avg(Book.price).label("avg_price"),
    func.max(Book.rating).label("max_rating"),
).first()

print(stats.count, stats.avg_price, stats.max_rating)
```

## Loading Relationships

```python
author = session.query(Author).filter(Author.name == "Alice").first()
for book in author.books:  # Uses relationship
    print(book.title)
```

<!-- 🤔 Relationships use lazy loading by default. For performance, use `selectinload()` or `joinedload()`. -->

## Run the Code

```bash
python code/07-orm-querying.py
```
