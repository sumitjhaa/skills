"""Async database with asyncpg: connection pool, async queries, error handling."""
from typing import Any, Optional
from datetime import datetime
import json
import asyncio


# ======================== Simulated asyncpg ========================

class AsyncConnection:
    """Simulates a single database connection."""
    def __init__(self, conn_id: int):
        self.conn_id = conn_id
        self.closed = False

    async def fetch(self, query: str, *args) -> list[dict]:
        if self.closed:
            raise RuntimeError("Connection closed")
        await asyncio.sleep(0.001)
        return [{"result": query, "args": args}]

    async def execute(self, query: str, *args) -> str:
        if self.closed:
            raise RuntimeError("Connection closed")
        await asyncio.sleep(0.001)
        return f"INSERT 0 1"

    async def close(self):
        self.closed = True


class AsyncPool:
    """Simulates a connection pool."""
    def __init__(self, min_size: int = 2, max_size: int = 10):
        self.min_size = min_size
        self.max_size = max_size
        self._conns: list[AsyncConnection] = []
        self._next_id = 0
        self._stats = {"acquired": 0, "released": 0, "created": 0}

    async def acquire(self) -> AsyncConnection:
        if self._conns:
            conn = self._conns.pop()
        else:
            self._next_id += 1
            conn = AsyncConnection(self._next_id)
            self._stats["created"] += 1
        self._stats["acquired"] += 1
        return conn

    async def release(self, conn: AsyncConnection):
        self._conns.append(conn)
        self._stats["released"] += 1

    async def close(self):
        for conn in self._conns:
            await conn.close()
        self._conns.clear()

    def status(self) -> dict:
        return {
            "available": len(self._conns),
            "acquired": self._stats["acquired"],
            "released": self._stats["released"],
            "created": self._stats["created"],
            "total_connections": self._stats["created"],
        }


class InMemoryDB:
    """In-memory database that mimics asyncpg query patterns."""
    def __init__(self):
        self.tables: dict[str, dict[int, dict]] = {}
        self.sequences: dict[str, int] = {}

    def ensure_table(self, name: str):
        if name not in self.tables:
            self.tables[name] = {}
            self.sequences[name] = 0

    async def execute(self, query: str, *args) -> Any:
        parts = query.strip().split()
        if not parts:
            return None
        await asyncio.sleep(0.001)

        if parts[0].upper() == "INSERT":
            table = parts[2]
            self.ensure_table(table)
            self.sequences[table] += 1
            pk = self.sequences[table]
            self.tables[table][pk] = {"id": pk}
            return pk

        elif parts[0].upper() == "SELECT":
            table = parts[3]
            self.ensure_table(table)
            return list(self.tables[table].values())

        elif parts[0].upper() == "DELETE":
            table = parts[2]
            self.ensure_table(table)
            self.tables[table].clear()
            return "DELETE 1"

        return None

    async def fetch(self, query: str, table: str | None = None) -> list[dict]:
        if table is None:
            return []
        self.ensure_table(table)
        return list(self.tables[table].values())

    async def fetchrow(self, query: str, *args) -> dict | None:
        result = await self.fetch(query, *args)
        return result[0] if result else None


# ======================== Async App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.db = InMemoryDB()

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func, "async": True})
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "POST", "handler": func, "async": True})
            return func
        return decorator

    async def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                handler = route["handler"]
                result = await handler(**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Async Endpoints ========================

@app.post("/users")
async def create_user(username: str, email: str):
    pk = await app.db.execute("INSERT INTO users VALUES ...", username, email)
    return {"id": pk, "username": username, "email": email}


@app.get("/users")
async def list_users():
    users = []
    for uid, data in app.db.tables.get("users", {}).items():
        users.append({"id": uid, **data})
    return {"users": users}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user_data = app.db.tables.get("users", {}).get(user_id)
    if not user_data:
        return {"error": "User not found"}
    return {"id": user_id, **user_data}


@app.post("/posts")
async def create_post(title: str, content: str, user_id: int):
    pk = await app.db.execute("INSERT INTO posts VALUES ...", title, content, user_id)
    return {"id": pk, "title": title, "user_id": user_id}


@app.get("/posts")
async def list_posts():
    posts = []
    for pid, data in app.db.tables.get("posts", {}).items():
        posts.append({"id": pid, **data})
    return {"posts": posts}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "async": True}


# ======================== Demo ========================
async def main():
    print("=== Async DB (asyncpg) Demo ===\n")

    # Create pool
    pool = AsyncPool(min_size=2, max_size=5)
    print(f"1. Pool created: {pool.status()}\n")

    # Acquire connections
    conn1 = await pool.acquire()
    conn2 = await pool.acquire()
    print(f"2. Acquired 2 connections")
    print(f"   Pool status: {pool.status()}\n")

    # Create users
    print("3. Creating users (async):")
    u1 = await app("POST", "/users", username="alice", email="alice@example.com")
    print(f"   {u1}")
    u2 = await app("POST", "/users", username="bob", email="bob@example.com")
    print(f"   {u2}\n")

    # List users
    print("4. Listing users:")
    users = await app("GET", "/users")
    for u in users["data"]["users"]:
        print(f"   - {u}")

    # Create posts
    print("\n5. Creating posts (async):")
    p1 = await app("POST", "/posts", title="Async Post 1", content="Async content", user_id=1)
    print(f"   {p1}")
    p2 = await app("POST", "/posts", title="Async Post 2", content="More async", user_id=1)
    print(f"   {p2}\n")

    # Health check
    health = await app("GET", "/health")
    print(f"6. Health: {health}\n")

    # Release connections
    await pool.release(conn1)
    await pool.release(conn2)
    print(f"7. Connections released")
    print(f"   Pool status: {pool.status()}\n")

    # Pool stats
    print(f"8. Pool lifetime stats:")
    print(f"   Connections created: {pool._stats['created']}")
    print(f"   Acquire count:       {pool._stats['acquired']}")
    print(f"   Release count:        {pool._stats['released']}")

    await pool.close()


asyncio.run(main())
