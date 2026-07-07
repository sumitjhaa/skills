# 🗄️ Database with SQLAlchemy
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Define models, CRUD operations, relationships, querying.

## Install

```bash
pip install flask-sqlalchemy
```

## Configuration

```python
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
```

## Defining Models

```python
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
```

## Relationships

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", backref="posts")
```

## CRUD Operations

```python
# Create
user = User(username="alice", email="alice@test.com")
db.session.add(user)
db.session.commit()

# Read
User.query.all()
User.query.get(1)
User.query.filter_by(username="alice").first()

# Update
user.email = "new@test.com"
db.session.commit()

# Delete
db.session.delete(user)
db.session.commit()
```

## Querying

```python
# Filtering
users = User.query.filter(User.is_active == True).all()

# Ordering
posts = Post.query.order_by(Post.created_at.desc()).all()

# Joins
posts = Post.query.join(User).filter(User.username == "alice").all()

# Aggregation
count = User.query.count()
```

<!-- 🧠 Use `db.create_all()` to create tables. Use Alembic/Flask-Migrate for schema changes in production. -->

## Run the Code

```bash
python code/06-database-sqlalchemy.py
```
