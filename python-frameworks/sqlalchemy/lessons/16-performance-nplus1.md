# 🐢 Performance: N+1 Problem
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** What N+1 is, detecting it, eager loading strategies, profiling.

## The N+1 Problem

```python
# N+1: one query for users, then N queries for each user's posts
for user in session.query(User).all():
    print(user.name)
    for post in user.posts:  # Triggers a query each time!
        print(f"  - {post.title}")
```

This generates 1 (users) + N (posts) queries.

## Eager Loading

```python
from sqlalchemy.orm import selectinload, joinedload, subqueryload

# SELECT IN — second query loads all posts at once
users = session.query(User).options(selectinload(User.posts)).all()

# JOIN — single query with LEFT JOIN
users = session.query(User).options(joinedload(User.posts)).all()

# Subquery — loads through a subquery
users = session.query(User).options(subqueryload(User.posts)).all()
```

## When to Use Which

| Strategy | Queries | Best For |
|----------|---------|----------|
| `lazy` | N+1 | Default (on-demand loading) |
| `selectinload` | 2 | Most cases, no duplicates |
| `joinedload` | 1 | Single parent, few children |
| `subqueryload` | 2 | Complex queries with pagination |

## Profiling

```python
import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Or use echo=True on the engine
engine = create_engine("sqlite://", echo=True)
```

<!-- 🧠 Use `selectinload` as the default eager loading strategy — it avoids cartesian products. -->

## Run the Code

```bash
python code/16-performance-nplus1.py
```
