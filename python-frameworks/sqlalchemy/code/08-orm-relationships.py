"""ORM: Relationships — one-to-many, many-to-one, backref, cascade."""
from sqlalchemy import create_engine, String, Integer, Float, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship
from datetime import datetime

engine = create_engine("sqlite:///:memory:", echo=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self): return f"User({self.name})"

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

alice = User(name="Alice")
bob = User(name="Bob")
session.add_all([alice, bob])
session.commit()

post1 = Post(title="Hello World", body="First post!", user_id=alice.id)
post2 = Post(title="SQLAlchemy Tips", body="Use relationships!", user_id=alice.id)
post3 = Post(title="Bob's Post", body="Hello from Bob", user_id=bob.id)
session.add_all([post1, post2, post3])
session.commit()

session.add_all([
    Comment(content="Great post!", post_id=post1.id),
    Comment(content="Thanks for sharing", post_id=post1.id),
    Comment(content="Very helpful", post_id=post2.id),
])
session.commit()

print("=== ORM: Relationships ===\n")

alice = session.get(User, 1)
print(f"1. {alice.name}'s posts:")
for p in alice.posts:
    print(f"   [{p.id}] {p.title} ({len(p.comments)} comments)")
    for c in p.comments:
        print(f"     💬 {c.content}")

print(f"\n2. Comment count per post:")
for p in session.query(Post).all():
    print(f"   '{p.title}': {len(p.comments)} comments")

# Cascade delete
session.delete(alice)
session.commit()
remaining = session.query(User).count()
posts_remaining = session.query(Post).count()
print(f"\n3. After deleting Alice: {remaining} users, {posts_remaining} posts (cascade works)")
session.close()
