# 🏁 Integration: Full Blog App
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Combine routes, templates, DB, forms, sessions, error handling into a real blog.

## Features

- User registration, login, logout
- CRUD operations on blog posts
- Comments on posts
- Session-based auth
- Flash messages for feedback
- Comment count on home page

## Models

```python
class User(Model):
    username = ORMStr(unique=True)
    email = ORMStr(unique=True)
    password = ORMStr()

class Post(Model):
    title = ORMStr()
    content = ORMText()
    user_id = ORMInt()
    published = ORMBool(default=False)

class Comment(Model):
    content = ORMText()
    post_id = ORMInt()
    user_id = ORMInt()
```

## Routes Overview

| Method | Path | Description |
|--------|------|-------------|
| GET, POST | `/` | Home page with all posts |
| GET, POST | `/register` | User registration |
| GET, POST | `/login` | User login |
| GET | `/logout` | Logout |
| GET, POST | `/posts/new` | Create post (auth required) |
| GET | `/posts/<id>` | View post with comments |
| POST | `/posts/<id>/comment` | Add comment (auth required) |
| GET | `/posts/<id>/delete` | Delete post (owner only) |

## Key Pattern: Auth Guard

```python
if not app.session.get("user_id"):
    app.flash.flash("Please log in first", "warning")
    return {"error": "Login required"}
```

## Key Pattern: Ownership Check

```python
if p.user_id != app.session["user_id"]:
    app.flash.flash("Not your post", "error")
    return {"error": "Not authorized"}
```

## Running the Demo

```bash
python code/10-integration-blog.py
```

The demo registers users, creates posts, adds comments, tests auth guards, and prints stats.
