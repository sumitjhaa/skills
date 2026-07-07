"""SQLAlchemy models, session pattern, CRUD with FastAPI."""
from typing import Any, Optional
from datetime import datetime
import json


# ======================== Simulated SQLAlchemy ========================

class Column:
    def __init__(self, type_: str, primary_key=False, default=None, nullable=True, index=False, unique=False):
        self.type_ = type_
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.index = index
        self.unique = unique


class Integer(Column):
    def __init__(self, primary_key=False, default=None):
        super().__init__("integer", primary_key=primary_key, default=default)


class String(Column):
    def __init__(self, max_length=255, nullable=False, default=None, unique=False):
        super().__init__("string", nullable=nullable, default=default, unique=unique)


class Float(Column):
    def __init__(self, default=None, nullable=True):
        super().__init__("float", nullable=nullable, default=default)


class Boolean(Column):
    def __init__(self, default=False):
        super().__init__("boolean", default=default)


class DateTime(Column):
    def __init__(self, default=None):
        super().__init__("datetime", default=default)


class ForeignKey(Column):
    def __init__(self, ref: str):
        super().__init__("foreign_key")
        self.ref = ref


class DeclarativeMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "Base":
            cls.__tablename__ = namespace.get("__tablename__", name.lower())
            cls._columns = {}
            for attr, val in namespace.items():
                if isinstance(val, Column):
                    cls._columns[attr] = val
            cls._pk_column = next((k for k, v in cls._columns.items() if v.primary_key), "id")
        return cls


class Base(metaclass=DeclarativeMeta):
    id: int = Integer(primary_key=True)


class Session:
    def __init__(self):
        self._store: dict[str, dict[int, dict]] = {}
        self._sequences: dict[str, int] = {}

    def _ensure_store(self, model_class):
        name = model_class.__tablename__
        if name not in self._store:
            self._store[name] = {}
            self._sequences[name] = 0

    def add(self, instance):
        model_class = type(instance)
        name = model_class.__tablename__
        self._ensure_store(model_class)
        self._sequences[name] += 1
        pk = self._sequences[name]
        setattr(instance, model_class._pk_column, pk)
        self._store[name][pk] = instance

    def commit(self):
        pass

    def query(self, model_class):
        return Query(self, model_class)

    def delete(self, instance):
        model_class = type(instance)
        name = model_class.__tablename__
        pk = getattr(instance, model_class._pk_column)
        self._store[name].pop(pk, None)


class Query:
    def __init__(self, session: Session, model_class):
        self._session = session
        self._model_class = model_class
        self._filters = []

    def filter(self, **kwargs):
        self._filters.append(kwargs)
        return self

    def all(self) -> list:
        name = self._model_class.__tablename__
        results = list(self._session._store.get(name, {}).values())
        for f in self._filters:
            results = [r for r in results if all(getattr(r, k, None) == v for k, v in f.items())]
        return results

    def first(self) -> Optional[Any]:
        results = self.all()
        return results[0] if results else None

    def get(self, pk) -> Optional[Any]:
        name = self._model_class.__tablename__
        return self._session._store.get(name, {}).get(pk)

    def count(self) -> int:
        return len(self.all())


# ======================== Models ========================

class User(Base):
    __tablename__ = "users"
    username: str = String(max_length=50, unique=True)
    email: str = String(max_length=100, unique=True)
    hashed_password: str = String(max_length=255)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(Base):
    __tablename__ = "posts"
    title: str = String(max_length=200)
    content: str = String(max_length=5000)
    user_id: int = Integer()
    created_at: datetime = DateTime(default=datetime.now)

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


# ======================== App with DB ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.db = Session()

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== CRUD Endpoints ========================

@app.post("/users")
def create_user(username: str, email: str, password: str):
    existing = app.db.query(User).filter(username=username).first()
    if existing:
        return {"error": "Username already exists"}
    user = User()
    user.username = username
    user.email = email
    user.hashed_password = f"hashed_{password}"
    app.db.add(user)
    app.db.commit()
    return {"id": user.id, "username": user.username, "email": user.email}


@app.get("/users")
def list_users():
    users = app.db.query(User).all()
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = app.db.query(User).get(user_id)
    if not user:
        return {"error": "User not found"}
    return {"id": user.id, "username": user.username, "email": user.email}


@app.post("/posts")
def create_post(title: str, content: str, user_id: int):
    user = app.db.query(User).get(user_id)
    if not user:
        return {"error": "User not found"}
    post = Post()
    post.title = title
    post.content = content
    post.user_id = user_id
    app.db.add(post)
    app.db.commit()
    return {"id": post.id, "title": post.title, "user_id": post.user_id}


@app.get("/posts")
def list_posts():
    posts = app.db.query(Post).all()
    return {"posts": [{"id": p.id, "title": p.title, "user_id": p.user_id} for p in posts]}


@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    posts = app.db.query(Post).filter(user_id=user_id).all()
    return {"user_id": user_id, "posts": [{"id": p.id, "title": p.title} for p in posts]}


# ======================== Demo ========================
print("=== SQLAlchemy + FastAPI Demo ===\n")

# Create users
print("1. Creating users:")
u1 = app("POST", "/users", username="alice", email="alice@example.com", password="secret")
print(f"   {u1}")
u2 = app("POST", "/users", username="bob", email="bob@example.com", password="pass123")
print(f"   {u2}")

# Duplicate user
print("\n2. Duplicate username:")
dup = app("POST", "/users", username="alice", email="alice2@example.com", password="test")
print(f"   {dup}")

# List users
print("\n3. All users:")
users = app("GET", "/users")
for u in users["data"]["users"]:
    print(f"   - {u}")

# Get single user
print("\n4. Get user 1:")
u = app("GET", "/users/1")
print(f"   {u}")

# Create posts
print("\n5. Creating posts:")
p1 = app("POST", "/posts", title="Hello World", content="First post!", user_id=1)
print(f"   {p1}")
p2 = app("POST", "/posts", title="FastAPI Tips", content="Some tips...", user_id=1)
print(f"   {p2}")
p3 = app("POST", "/posts", title="Bob's Post", content="By Bob", user_id=2)
print(f"   {p3}")

# List posts
print("\n6. All posts:")
posts = app("GET", "/posts")
for p in posts["data"]["posts"]:
    print(f"   - {p}")

# User's posts
print("\n7. Alice's posts:")
alice_posts = app("GET", "/users/1/posts")
for p in alice_posts["data"]["posts"]:
    print(f"   - {p}")

print("\n8. Post count:")
print(f"   Users: {app.db.query(User).count()}")
print(f"   Posts: {app.db.query(Post).count()}")
