# 🗄️ SQLAlchemy Deep
<!-- ⏱️ 20 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** SQLAlchemy 2.0 ORM — `DeclarativeBase`, mapped columns, relationships, sessions, async sessions, migrations with Alembic, and query patterns.

> 💡 **TL;DR — The whole point:** SQLAlchemy is the Django ORM's smarter cousin. Define models as Python classes, get auto-generated SQL. Relationships load related data lazily or eagerly. Sessions manage transactions.

## 🔗 Why This Matters
A social-media analytics platform stores users, posts, comments, likes, and daily metrics. Writing raw SQL for every query is error-prone and hard to maintain. SQLAlchemy gives you a Pythonic API with migration support for schema changes.

## The Concept
- **`DeclarativeBase`** — base class for all models
- **`Mapped`** — type-annotated column definition (SQLAlchemy 2.0 style)
- **`relationship()`** — links between models (lazy loading by default)
- **`Session`** — transactional unit of work
- **`select()`** — SQLAlchemy 2.0 query API
- **Alembic** — schema migrations

## Code Example
```python
"""Social-media: SQLAlchemy 2.0 ORM models and queries."""

from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy import create_engine, select, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


# ─── Engine & Base ───
engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ─── Models ───
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(280))
    likes: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    author: Mapped["User"] = relationship(back_populates="posts")


# ─── Create tables ───
Base.metadata.create_all(engine)


# ─── Session & CRUD ───
def seed_data() -> None:
    with Session(engine) as session:
        alice = User(username="alice", email="alice@example.com")
        bob = User(username="bob", email="bob@example.com")
        session.add_all([alice, bob])
        session.flush()

        session.add_all([
            Post(content="Python SQLAlchemy is great!", author=alice, likes=42),
            Post(content="Async/await changed my life", author=alice, likes=99),
            Post(content="FastAPI + SQLAlchemy = dream team", author=bob, likes=150),
        ])
        session.commit()


def get_user_with_posts(username: str) -> Optional[User]:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)


def top_posts(min_likes: int = 50) -> Sequence[Post]:
    with Session(engine) as session:
        stmt = select(Post).where(Post.likes >= min_likes).order_by(Post.likes.desc())
        return session.scalars(stmt).all()


def user_post_count() -> Sequence[tuple[str, int]]:
    with Session(engine) as session:
        stmt = (
            select(User.username, func.count(Post.id))
            .join(Post, User.id == Post.user_id)
            .group_by(User.id)
        )
        return session.execute(stmt).all()


seed_data()

alice = get_user_with_posts("alice")
print(f"User: {alice.username}, Posts: {len(alice.posts)}")

top = top_posts(min_likes=50)
print(f"Top posts: {[p.content[:30] for p in top]}")

counts = user_post_count()
for username, post_count in counts:
    print(f"  {username}: {post_count} posts")
```

## 🔍 How It Works
- `Mapped[int]` + `mapped_column()` — type-safe column definition (SQLAlchemy 2.0 style)
- `relationship(back_populates="posts")` — creates Python-side link; loads related objects
- `Session(engine)` — transactional scope; commit() persists, close() returns to pool
- `session.scalar(select(...))` — returns one result or None
- `session.scalars(...).all()` — returns all matching rows
- `func.count(Post.id)` — SQL aggregate function inside a select
- `cascade="all, delete-orphan"` — deleting a User deletes their Posts

## ⚠️ Common Pitfall
N+1 query problem: iterating over `user.posts` inside a loop issues a separate SQL query for each user. Fix with `selectinload()` or `joinedload()`: `select(User).options(selectinload(User.posts))`.

## 🧠 Memory Aid
"`Mapped` = column type. `relationship` = model link. `Session` = transaction. `select()` = query builder. `scalar()` = one row. `scalars()` = many rows. N+1 = bad → `selectinload`."

## 🏃 Try It
Define a `Comment` model (id, content, post_id, user_id, created_at) with a relationship to Post. Write a query that fetches a Post with all its Comments eagerly loaded using `selectinload`.

## 🔗 Related
- [Data Science Introduction](04-data-science-intro.md) — SQLite basics
- [Pydantic & Settings](../09_production/lessons/13-pydantic-settings.md) — validation

## ➡️ Next
[NumPy & Pandas Deep](08-numpy-pandas-deep.md)
