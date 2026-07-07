# 🔗 ORM: Relationships
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** One-to-many, many-to-one, `back_populates`, cascade delete.

## One-to-Many / Many-to-One

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
```

## Using Relationships

```python
alice = User(name="Alice")
session.add(alice)
session.flush()

post = Post(title="Hello", user_id=alice.id)
session.add(post)
session.commit()

# Access from parent
alice.posts  # [Post('Hello')]

# Access from child
post.user  # User('Alice')
```

## Cascade Delete

```python
class User(Base):
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

session.delete(alice)  # Also deletes all posts
```

## Chained Relationships

```python
class Comment(Base):
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")

# Access through chain
post.user.name  # Author's name
post.comments   # All comments on the post
```

<!-- 🧠 Always use `back_populates` (not `backref`) for clarity in SQLAlchemy 2.0. -->

## Run the Code

```bash
python code/08-orm-relationships.py
```
