"""Async SQLAlchemy: async sessions, async queries, relationship loading."""
from typing import Any, Optional
from datetime import datetime
import json
import asyncio


# ======================== Simulated Async SQLAlchemy ========================

class AsyncColumn:
    def __init__(self, type_: str, primary_key=False, default=None, nullable=True, index=False):
        self.type_ = type_
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.index = index


class AsyncInteger(AsyncColumn):
    def __init__(self, primary_key=False):
        super().__init__("integer", primary_key=primary_key)


class AsyncString(AsyncColumn):
    def __init__(self, max_length=255, nullable=False, default=None):
        super().__init__("string", nullable=nullable, default=default)


class AsyncFloat(AsyncColumn):
    def __init__(self, nullable=True, default=None):
        super().__init__("float", nullable=nullable, default=default)


class AsyncBoolean(AsyncColumn):
    def __init__(self, default=False):
        super().__init__("boolean", default=default)


class AsyncDateTime(AsyncColumn):
    def __init__(self, default=None):
        super().__init__("datetime", default=default)


class AsyncForeignKey:
    def __init__(self, ref: str):
        self.ref = ref


class AsyncRelationship:
    def __init__(self, back_populates: str | None = None):
        self.back_populates = back_populates
        self._loaded = False
        self._items: list = []


class AsyncDeclarativeMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "AsyncBase":
            cls.__tablename__ = namespace.get("__tablename__", name.lower())
            cls._columns = {}
            cls._relationships = {}
            for attr, val in namespace.items():
                if isinstance(val, AsyncColumn):
                    cls._columns[attr] = val
                elif isinstance(val, AsyncRelationship):
                    cls._relationships[attr] = val
            cls._pk_column = next((k for k, v in cls._columns.items() if v.primary_key), "id")
        return cls


class AsyncBase(metaclass=AsyncDeclarativeMeta):
    id: int = AsyncInteger(primary_key=True)


class AsyncSession:
    """Simulates SQLAlchemy async session."""
    def __init__(self):
        self._store: dict[str, dict[int, dict]] = {}
        self._sequences: dict[str, int] = {}
        self._closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        self._closed = True

    def _ensure(self, model_class):
        name = model_class.__tablename__
        if name not in self._store:
            self._store[name] = {}
            self._sequences[name] = 0

    async def add(self, instance):
        model_class = type(instance)
        name = model_class.__tablename__
        self._ensure(model_class)
        self._sequences[name] += 1
        pk = self._sequences[name]
        setattr(instance, model_class._pk_column, pk)
        await asyncio.sleep(0.001)
        self._store[name][pk] = instance

    async def commit(self):
        await asyncio.sleep(0.001)

    async def flush(self):
        await asyncio.sleep(0.001)

    async def execute(self, stmt) -> "AsyncResult":
        await asyncio.sleep(0.001)
        return AsyncResult(self, stmt)

    async def refresh(self, instance):
        await asyncio.sleep(0.001)

    async def delete(self, instance):
        model_class = type(instance)
        name = model_class.__tablename__
        pk = getattr(instance, model_class._pk_column)
        self._store[name].pop(pk, None)
        await asyncio.sleep(0.001)


class AsyncResult:
    def __init__(self, session: AsyncSession, stmt):
        self._session = session
        self._stmt = stmt

    async def scalars(self) -> "AsyncScalars":
        return AsyncScalars(self._session, self._stmt)

    async def all(self) -> list:
        return [1]  # Placeholder


class AsyncScalars:
    def __init__(self, session: AsyncSession, stmt):
        self._session = session
        self._stmt = stmt

    async def all(self) -> list:
        parts = str(self._stmt).split(":")
        if len(parts) == 2:
            table_name = parts[1].strip()
            return list(self._session._store.get(table_name, {}).values())
        return []

    async def first(self) -> Optional[Any]:
        items = await self.all()
        return items[0] if items else None


class AsyncSelect:
    """Simulates SQLAlchemy select()."""
    def __init__(self, model_class):
        self._model_class = model_class
        self._where = {}
        self._order = None
        self._limit_val = None
        self._offset_val = None

    def where(self, **kwargs):
        self._where.update(kwargs)
        return self

    def order_by(self, col):
        self._order = col
        return self

    def limit(self, n: int):
        self._limit_val = n
        return self

    def offset(self, n: int):
        self._offset_val = n
        return self

    def __str__(self):
        return f"select:{self._model_class.__tablename__}"


def select(model_class):
    return AsyncSelect(model_class)


# ======================== Models ========================

class User(AsyncBase):
    __tablename__ = "users"
    username: str = AsyncString(max_length=50)
    email: str = AsyncString(max_length=100)
    is_active: bool = AsyncBoolean(default=True)
    posts = AsyncRelationship(back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(AsyncBase):
    __tablename__ = "posts"
    title: str = AsyncString(max_length=200)
    content: str = AsyncString(max_length=5000)
    user_id: int = AsyncInteger()
    author = AsyncRelationship(back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


# ======================== AsyncApp ========================

class AsyncAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.session_factory = lambda: AsyncSession()

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    async def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = await route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = AsyncAPI()


# ======================== Async Endpoints ========================

@app.post("/users")
async def create_user(username: str, email: str):
    async with app.session_factory() as session:
        user = User()
        user.username = username
        user.email = email
        await session.add(user)
        await session.commit()
        return {"id": user.id, "username": user.username, "email": user.email}


@app.get("/users")
async def list_users():
    async with app.session_factory() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = await result.scalars().all()
        return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with app.session_factory() as session:
        stmt = select(User).where(id=user_id)
        result = await session.execute(stmt)
        user = await result.scalars().first()
        if user is None:
            return {"error": "not_found"}
        return {"id": user.id, "username": user.username, "email": user.email, "is_active": user.is_active}


@app.post("/posts")
async def create_post(title: str, content: str, user_id: int):
    async with app.session_factory() as session:
        post = Post()
        post.title = title
        post.content = content
        post.user_id = user_id
        await session.add(post)
        await session.commit()
        return {"id": post.id, "title": post.title, "user_id": post.user_id}


@app.get("/posts")
async def list_posts():
    async with app.session_factory() as session:
        stmt = select(Post)
        result = await session.execute(stmt)
        posts = await result.scalars().all()
        return {"posts": [{"id": p.id, "title": p.title, "user_id": p.user_id} for p in posts]}


@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int):
    async with app.session_factory() as session:
        stmt = select(Post).where(user_id=user_id)
        result = await session.execute(stmt)
        posts = await result.scalars().all()
        return {"user_id": user_id, "posts": [{"id": p.id, "title": p.title} for p in posts]}


# ======================== Demo ========================
async def main():
    print("=== Async SQLAlchemy Demo ===\n")

    print("1. Creating users (async):")
    u1 = await app("POST", "/users", username="alice", email="alice@example.com")
    print(f"   {u1['data']}")
    u2 = await app("POST", "/users", username="bob", email="bob@example.com")
    print(f"   {u2['data']}")
    u3 = await app("POST", "/users", username="charlie", email="charlie@example.com")
    print(f"   {u3['data']}\n")

    print("2. Creating posts (async):")
    p1 = await app("POST", "/posts", title="Async Post 1", content="Content 1", user_id=1)
    print(f"   {p1['data']}")
    p2 = await app("POST", "/posts", title="Async Post 2", content="Content 2", user_id=1)
    print(f"   {p2['data']}")
    p3 = await app("POST", "/posts", title="Bob's Post", content="Bob content", user_id=2)
    print(f"   {p3['data']}\n")

    print("3. Listing users (async):")
    users = await app("GET", "/users")
    for u in users["data"]["users"]:
        print(f"   - {u}")

    print("\n4. Listing posts (async):")
    posts = await app("GET", "/posts")
    for p in posts["data"]["posts"]:
        print(f"   - {p}")

    print("\n5. Get single user:")
    user = await app("GET", "/users/1")
    print(f"   {user['data']}")

    print("\n6. Get user's posts:")
    user_posts = await app("GET", "/users/1/posts")
    for p in user_posts["data"]["posts"]:
        print(f"   - {p}")

    print("\n7. Async session context manager:")
    async with app.session_factory() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        all_users = await result.scalars().all()
        print(f"   Total users via async session: {len(all_users)}")
        # Auto-closes on exit


asyncio.run(main())
