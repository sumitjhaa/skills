"""Database with Flask-SQLAlchemy: models, CRUD, relationships, queries."""
from typing import Any, Optional
from datetime import datetime
import json
import re


# ======================== Simulated ORM ========================

class ORMColumn:
    def __init__(self, type_: str, primary_key=False, default=None, nullable=True, unique=False):
        self.type_ = type_
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.unique = unique


class ORMInteger(ORMColumn):
    def __init__(self, primary_key=False, default=None):
        super().__init__("integer", primary_key=primary_key, default=default)


class ORMString(ORMColumn):
    def __init__(self, max_length=255, nullable=False, default=None, unique=False):
        super().__init__("string", nullable=nullable, default=default, unique=unique)


class ORMText(ORMColumn):
    def __init__(self, nullable=False):
        super().__init__("text", nullable=nullable)


class ORMFloat(ORMColumn):
    def __init__(self, default=0.0):
        super().__init__("float", default=default)


class ORMBoolean(ORMColumn):
    def __init__(self, default=False):
        super().__init__("boolean", default=default)


class ORMDateTime(ORMColumn):
    def __init__(self, default=None):
        super().__init__("datetime", default=default)


class ORMMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "ORMModel":
            cls.__tablename__ = namespace.get("__tablename__", name.lower())
            cls._columns = {}
            for attr, val in namespace.items():
                if isinstance(val, ORMColumn):
                    cls._columns[attr] = val
            cls._pk_column = next((k for k, v in cls._columns.items() if v.primary_key), "id")
        return cls


class ORMModel(metaclass=ORMMeta):
    id: int = ORMInteger(primary_key=True)

    def __repr__(self):
        pk = getattr(self, self._pk_column, None)
        return f"<{type(self).__name__}(id={pk})>"


class ModelStore:
    """In-memory store simulating a database."""
    def __init__(self):
        self._stores: dict[str, dict[int, ORMModel]] = {}
        self._seq: dict[str, int] = {}

    def add(self, model: ORMModel):
        name = model.__tablename__
        if name not in self._stores:
            self._stores[name] = {}
            self._seq[name] = 0
        self._seq[name] += 1
        setattr(model, model._pk_column, self._seq[name])
        self._stores[name][self._seq[name]] = model

    def all(self, model_class) -> list:
        return list(self._stores.get(model_class.__tablename__, {}).values())

    def get(self, model_class, pk: int) -> Optional[ORMModel]:
        return self._stores.get(model_class.__tablename__, {}).get(pk)

    def filter(self, model_class, **kwargs) -> list:
        results = self.all(model_class)
        for key, val in kwargs.items():
            results = [r for r in results if getattr(r, key, None) == val]
        return results

    def first(self, model_class, **kwargs) -> Optional[ORMModel]:
        results = self.filter(model_class, **kwargs)
        return results[0] if results else None

    def delete(self, model: ORMModel):
        name = model.__tablename__
        pk = getattr(model, model._pk_column)
        self._stores.get(name, {}).pop(pk, None)

    def count(self, model_class) -> int:
        return len(self.all(model_class))


db = ModelStore()


# ======================== Models ========================

class User(ORMModel):
    __tablename__ = "users"
    username: str = ORMString(max_length=50, unique=True)
    email: str = ORMString(max_length=100, unique=True)
    is_active: bool = ORMBoolean(default=True)
    created_at: datetime = ORMDateTime(default=datetime.now)


class Post(ORMModel):
    __tablename__ = "posts"
    title: str = ORMString(max_length=200)
    content: str = ORMText()
    user_id: int = ORMInteger()
    published: bool = ORMBoolean(default=False)
    created_at: datetime = ORMDateTime(default=datetime.now)


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def deco(func):
            self.routes.append({"path": path, "methods": methods, "handler": func})
            return func
        return deco

    @staticmethod
    def _match_route(route_pattern: str, actual_path: str) -> dict | None:
        param_names = []
        def replacer(m):
            full = m.group(0)
            if ':' in full:
                typ, name = full.strip('<>').split(':')
            else:
                typ, name = 'str', full.strip('<>')
            param_names.append((name, typ))
            if typ == 'int': return r'(\d+)'
            if typ == 'float': return r'([0-9.]+)'
            if typ == 'path': return r'(.+)'
            return r'([^/]+)'
        regex = '^' + re.sub(r'<[^>]+>', replacer, route_pattern) + '$'
        m = re.match(regex, actual_path)
        if not m: return None
        return {name: int(val) if typ == 'int' else float(val) if typ == 'float' else val
                for (name, typ), val in zip(param_names, m.groups())}

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if method in route["methods"] and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
            params = self._match_route(route["path"], path)
            if method in route["methods"] and params is not None:
                result = route["handler"](**params, **kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()


# ======================== Routes ========================

@app.route("/users", methods=["GET", "POST"])
def users(**kwargs):
    if kwargs:
        user = User()
        user.username = kwargs.get("username", "")
        user.email = kwargs.get("email", "")
        db.add(user)
        return {"id": user.id, "username": user.username, "email": user.email}

    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in db.all(User)]}


@app.route("/users/<int:user_id>")
def get_user(user_id: int, **kwargs):
    user = db.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    posts = db.filter(Post, user_id=user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "post_count": len(posts),
    }


@app.route("/posts", methods=["GET", "POST"])
def posts(**kwargs):
    if kwargs:
        user = db.get(User, int(kwargs.get("user_id", 0)))
        if not user:
            return {"error": "User not found"}
        post = Post()
        post.title = kwargs.get("title", "")
        post.content = kwargs.get("content", "")
        post.user_id = user.id
        post.published = kwargs.get("published", "false") in ("true", "1", "yes")
        db.add(post)
        return {"id": post.id, "title": post.title, "user_id": post.user_id}

    all_posts = db.all(Post)
    result = []
    for p in all_posts:
        author = db.get(User, p.user_id)
        result.append({"id": p.id, "title": p.title, "author": author.username if author else "unknown", "published": p.published})
    return {"posts": result}


@app.route("/users/<int:user_id>/posts")
def user_posts(user_id: int, **kwargs):
    posts = db.filter(Post, user_id=user_id)
    return {"user_id": user_id, "posts": [{"id": p.id, "title": p.title, "published": p.published} for p in posts]}


@app.route("/stats")
def stats():
    return {
        "users": db.count(User),
        "posts": db.count(Post),
        "published_posts": len(db.filter(Post, published=True)),
    }


# ======================== Demo ========================
print("=== Database with SQLAlchemy Demo ===\n")

print("1. Creating users:")
for name, email in [("alice", "alice@test.com"), ("bob", "bob@test.com"), ("charlie", "charlie@test.com")]:
    r = app("POST", "/users", username=name, email=email)
    print(f"   Created: {r['data']}")

print("\n2. Creating posts:")
posts_data = [
    ("First Post", "Content 1", 1, True),
    ("Second Post", "Content 2", 1, True),
    ("Bob's Post", "Bob content", 2, False),
    ("Charlie's Post", "Charlie content", 3, True),
]
for title, content, uid, pub in posts_data:
    r = app("POST", "/posts", title=title, content=content, user_id=uid, published=str(pub).lower())
    print(f"   Created: {r['data']}")

print("\n3. All users:")
r = app("GET", "/users")
for u in r["data"]["users"]:
    print(f"   - {u['username']} ({u['email']})")

print("\n4. All posts with authors:")
r = app("GET", "/posts")
for p in r["data"]["posts"]:
    status = "✅" if p["published"] else "⏸️"
    print(f"   {status} [{p['id']}] {p['title']} — by {p['author']}")

print("\n5. Alice's posts:")
r = app("GET", "/users/1/posts")
for p in r["data"]["posts"]:
    print(f"   - {p['title']} (published: {p['published']})")

print("\n6. Stats:")
r = app("GET", "/stats")
print(f"   {json.dumps(r['data'])}")

print("\n7. Get single user:")
r = app("GET", "/users/1")
print(f"   {json.dumps(r['data'])}")
