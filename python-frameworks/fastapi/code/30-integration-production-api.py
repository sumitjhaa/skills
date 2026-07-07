"""Integration: Production API — combines all Phase 03 patterns into one deployable app."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import time
import threading
import functools
import traceback
import os


# ======================== Logger ========================

class Logger:
    def __init__(self, service: str = "prod-api"):
        self.service = service
        self.logs: list[dict] = []

    def info(self, msg: str, **kw):
        entry = {"ts": datetime.utcnow().isoformat() + "Z", "service": self.service, "level": "INFO", "msg": msg, **kw}
        self.logs.append(entry)
        return entry

    def error(self, msg: str, **kw):
        entry = {"ts": datetime.utcnow().isoformat() + "Z", "service": self.service, "level": "ERROR", "msg": msg, **kw}
        self.logs.append(entry)
        return entry

    def export(self, n: int = 10): return self.logs[-n:]

log = Logger()


# ======================== Metrics ========================

class Metrics:
    def __init__(self):
        self.counters: dict[str, int] = {}
        self.durations: list[float] = []
        self.start = time.time()

    def inc(self, name: str):
        self.counters[name] = self.counters.get(name, 0) + 1

    def observe(self, ms: float):
        self.durations.append(ms)

    def snapshot(self) -> dict:
        d = self.durations
        return {
            "uptime": round(time.time() - self.start, 1),
            "requests": self.counters.get("requests", 0),
            "errors": self.counters.get("errors", 0),
            "avg_duration_ms": round(sum(d) / len(d), 1) if d else 0,
            "p95_ms": round(sorted(d)[int(len(d) * 0.95)], 1) if d else 0,
        }

metrics = Metrics()


# ======================== Health ========================

class Health:
    def __init__(self):
        self.checks: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable):
        self.checks[name] = fn

    def check(self) -> dict:
        results = {}
        ok = True
        for name, fn in self.checks.items():
            try:
                r = fn()
                results[name] = r
                if not r.get("healthy", False):
                    ok = False
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                ok = False
        return {"status": "healthy" if ok else "degraded", "checks": results}

health = Health()
health.register("database", lambda: {"healthy": True, "latency_ms": 1.2})
health.register("redis", lambda: {"healthy": True, "connected_clients": 3})
health.register("disk", lambda: {"healthy": True, "free_gb": 32})


# ======================== Rate Limiter ========================

class TokenBucket:
    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last = time.time()
        self.lock = threading.Lock()

    def consume(self) -> bool:
        with self.lock:
            now = time.time()
            self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
            self.last = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

rate_limiter = TokenBucket(rate=10, burst=20)


# ======================== Cache ========================

class Cache:
    def __init__(self):
        self._data: dict[str, tuple] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        if key in self._data:
            val, exp = self._data[key]
            if exp > time.time():
                self.hits += 1
                return val
            del self._data[key]
        self.misses += 1
        return None

    def set(self, key: str, val: Any, ttl: int = 30):
        self._data[key] = (val, time.time() + ttl)

    def clear(self):
        self._data.clear()

    def stats(self):
        total = self.hits + self.misses
        return {"size": len(self._data), "hits": self.hits, "misses": self.misses, "hit_rate": round(self.hits / total * 100, 1) if total else 0}

cache = Cache()


# ======================== DB ========================

class DB:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self.posts: dict[int, dict] = {}
        self._next = {"users": 1, "posts": 1}

    def create_user(self, u: str, e: str) -> dict:
        uid = self._next["users"]; self._next["users"] += 1
        user = {"id": uid, "username": u, "email": e, "created_at": datetime.now().isoformat()}
        self.users[uid] = user; return user

    def get_user(self, uid: int) -> dict | None:
        return self.users.get(uid)

    def list_users(self) -> list:
        return list(self.users.values())

    def create_post(self, title: str, content: str, uid: int) -> dict:
        pid = self._next["posts"]; self._next["posts"] += 1
        post = {"id": pid, "title": title, "content": content, "user_id": uid, "created_at": datetime.now().isoformat()}
        self.posts[pid] = post; return post

    def get_post(self, pid: int) -> dict | None:
        return self.posts.get(pid)

    def list_posts(self) -> list:
        return list(self.posts.values())

    def stats(self):
        return {"users": len(self.users), "posts": len(self.posts)}

db = DB()


# ======================== Background Tasks ========================

class BackgroundTasks:
    def __init__(self):
        self.tasks: list[dict] = []
        self._next_id = 1

    def add(self, name: str, fn: Callable, *args) -> int:
        tid = self._next_id; self._next_id += 1
        t = threading.Thread(target=self._run, args=(tid, name, fn, *args), daemon=True)
        self.tasks.append({"id": tid, "name": name, "status": "running"})
        t.start()
        return tid

    def _run(self, tid: int, name: str, fn: Callable, *args):
        try:
            fn(*args)
            for t in self.tasks:
                if t["id"] == tid:
                    t["status"] = "completed"
        except Exception as e:
            for t in self.tasks:
                if t["id"] == tid:
                    t["status"] = "failed"
                    t["error"] = str(e)

    def list(self):
        return self.tasks[-10:]

bg = BackgroundTasks()


def send_email(user_id: int, subject: str):
    time.sleep(0.1)
    return f"Email sent to user {user_id}: {subject}"


# ======================== WebSocket Sim ========================

class WSManager:
    def __init__(self):
        self.rooms: dict[str, list[str]] = {}
        self._next = 0

    def connect(self, room: str = "general"):
        self._next += 1
        cid = f"ws_{self._next}"
        self.rooms.setdefault(room, []).append(cid)
        return cid

    def disconnect(self, cid: str):
        for room, conns in self.rooms.items():
            if cid in conns:
                conns.remove(cid)

    def broadcast(self, room: str, msg: dict):
        self.rooms.get(room, [])
        return len(self.rooms.get(room, []))

    def stats(self):
        return {r: len(c) for r, c in self.rooms.items()}

ws = WSManager()


# ======================== FastAPI ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def get(self, path: str):
        def deco(f):
            self.routes.append({"path": path, "method": "GET", "handler": f}); return f
        return deco

    def post(self, path: str):
        def deco(f):
            self.routes.append({"path": path, "method": "POST", "handler": f}); return f
        return deco

    def delete(self, path: str):
        def deco(f):
            self.routes.append({"path": path, "method": "DELETE", "handler": f}); return f
        return deco

    def __call__(self, method: str, path: str, **kw) -> dict:
        metrics.inc("requests")
        start = time.time()
        if not rate_limiter.consume():
            metrics.inc("errors")
            return {"status": 429, "data": {"error": "rate_limited"}}

        for r in self.routes:
            if r["method"] == method and r["path"] == path:
                try:
                    result = r["handler"](**kw)
                    duration = (time.time() - start) * 1000
                    metrics.observe(duration)
                    return {"status": 200, "data": result}
                except Exception as e:
                    metrics.inc("errors")
                    log.error(f"Handler error: {e}", path=path, traceback=traceback.format_exc())
                    return {"status": 500, "data": {"error": "internal_error"}}

        return {"status": 404, "data": {"detail": "Not Found"}}

app = FastAPI()


# ======================== Production Endpoints ========================

@app.get("/health")
def get_health():
    return health.check()

@app.get("/metrics")
def get_metrics():
    return {**metrics.snapshot(), "cache": cache.stats(), "db": db.stats(), "ws": ws.stats()}

@app.get("/logs")
def get_logs():
    return {"logs": log.export(20)}

# Users
@app.post("/users")
def create_user(username: str, email: str):
    user = db.create_user(username, email)
    tid = bg.add("send_welcome", send_email, user["id"], "Welcome!")
    log.info("User created", user_id=user["id"], username=username)
    return {"user": user, "background_task": tid}

@app.get("/users")
def list_users():
    cached = cache.get("users:list")
    if cached:
        return {"users": cached, "cached": True}
    users = db.list_users()
    cache.set("users:list", users, ttl=10)
    return {"users": users, "cached": False}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    cached = cache.get(f"users:{user_id}")
    if cached:
        return {"user": cached, "cached": True}
    user = db.get_user(user_id)
    if not user:
        return {"error": "not_found"}
    cache.set(f"users:{user_id}", user, ttl=30)
    return {"user": user, "cached": False}

# Posts
@app.post("/posts")
def create_post(title: str, content: str, user_id: int):
    if not db.get_user(user_id):
        return {"error": "user_not_found"}
    post = db.create_post(title, content, user_id)
    cache.clear()
    log.info("Post created", post_id=post["id"], user_id=user_id)
    return {"post": post}

@app.get("/posts")
def list_posts():
    return {"posts": db.list_posts()}

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = db.get_post(post_id)
    if not post:
        return {"error": "not_found"}
    return {"post": post}

# WebSocket
@app.post("/ws/connect")
def ws_connect(room: str = "general"):
    cid = ws.connect(room)
    return {"conn_id": cid, "room": room}

@app.post("/ws/{conn_id}/broadcast")
def ws_broadcast(conn_id: str, room: str = "general", message: str = ""):
    count = ws.broadcast(room, {"from": conn_id, "message": message, "ts": datetime.now().isoformat()})
    return {"broadcast_to": count, "room": room}

# Cache control
@app.delete("/cache")
def clear_cache():
    cache.clear()
    return {"cache": "cleared"}

# Tasks
@app.get("/tasks")
def list_tasks():
    return {"tasks": bg.list()}

# OpenAPI
@app.get("/openapi.json")
def openapi():
    return {
        "openapi": "3.0.3",
        "info": {"title": "Production API", "version": "3.0.0", "description": "Full production API with monitoring"},
        "paths": {
            "/health": {"get": {"summary": "Health check"}},
            "/metrics": {"get": {"summary": "Metrics"}},
            "/users": {"post": {"summary": "Create user"}, "get": {"summary": "List users"}},
            "/posts": {"post": {"summary": "Create post"}, "get": {"summary": "List posts"}},
        },
    }


# ======================== Seed Data ========================
for i in range(3):
    db.create_user(f"user{i}", f"user{i}@test.com")
db.create_post("Welcome", "First post!", 1)
db.create_post("Tutorial", "Learn FastAPI", 1)
db.create_post("News", "Production release!", 2)

ws.connect("general")
ws.connect("general")
ws.connect("random")


# ======================== Demo ========================
print("=" * 70)
print("  INTEGRATION: PRODUCTION API")
print("  All Phase 03 patterns combined")
print("=" * 70)

# 1. Health
print("\n1. Health check:")
print(json.dumps(app("GET", "/health")["data"], indent=2))

# 2. Create users
print("\n2. Create users:")
for i in range(3):
    r = app("POST", "/users", username=f"new_user_{i}", email=f"new{i}@test.com")
    print(f"   Created: {r['data']['user']['username']} (task: {r['data']['background_task']})")

# 3. List users (with caching)
print("\n3. List users (first call):")
r1 = app("GET", "/users")
print(f"   Cached: {r1['data']['cached']}, count: {len(r1['data']['users'])}")

print("\n4. List users (cached):")
r2 = app("GET", "/users")
print(f"   Cached: {r2['data']['cached']}, count: {len(r2['data']['users'])}")

# 5. Create posts
print("\n5. Create posts:")
for i in range(3):
    r = app("POST", "/posts", title=f"Post {i}", content=f"Content {i}", user_id=1)
    print(f"   Created: {r['data']['post']['title']}")

# 6. WebSocket
print("\n6. WebSocket connections:")
r = app("POST", "/ws/connect", room="general")
print(f"   Connected: {r['data']['conn_id']}")
r = app("POST", f"/ws/{r['data']['conn_id']}/broadcast", room="general", message="Hello production!")
print(f"   Broadcast to: {r['data']['broadcast_to']} clients")

# 7. Background tasks
print("\n7. Background tasks:")
r = app("GET", "/tasks")
for t in r["data"]["tasks"]:
    print(f"   [{t['id']}] {t['name']}: {t['status']}")

# 8. Metrics
print("\n8. Production metrics:")
print(json.dumps(app("GET", "/metrics")["data"], indent=2))

# 9. Rate limiting (exhaust it)
print("\n9. Rate limiting (sending 25 rapid requests):")
limited = 0
for i in range(25):
    r = app("GET", "/health")
    if r["status"] == 429:
        limited += 1
print(f"   Rate limited: {limited}/25 requests")

# 10. Error handling
print("\n10. Error cases:")
r = app("GET", "/users/999")
print(f"   Not found: {r['data']}")
r = app("POST", "/posts", title="Orphan", content="No user", user_id=999)
print(f"   Missing user: {r['data']}")

# 11. Log audit
print("\n11. Recent logs:")
for entry in log.export(5):
    print(f"   [{entry['level']}] {entry['msg']}")

# 12. Clear cache
print("\n12. Cache cleared:")
r = app("DELETE", "/cache")
print(f"   {r['data']}")
print(f"   Cache stats: {cache.stats()}")

print("\n" + "=" * 70)
print("  ✅ PRODUCTION API INTEGRATION COMPLETE")
print("  FastAPI skill: All 3 phases done!")
print("=" * 70)
