"""SQLAlchemy Deep — ORM models, relationships, sessions, queries.
Run: python 10-07-sqlalchemy-deep.py
"""

from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy import create_engine, select, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


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


Base.metadata.create_all(engine)


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
        stmt = select(User).where(User.username == username).options(selectinload(User.posts))
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
