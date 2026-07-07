"""Integration: Full Blog App — combines routes, templates, DB, forms, sessions, error handling."""
from typing import Any, Optional
from datetime import datetime
import json
import re


# ======================== ORM (from lesson 06) ========================

class ORMColumn:
    def __init__(self, type_, primary_key=False, default=None, nullable=True, unique=False):
        self.type_ = type_
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.unique = unique

class ORMInt(ORMColumn):
    def __init__(self, pk=False): super().__init__("int", primary_key=pk)
class ORMStr(ORMColumn):
    def __init__(self, max_len=255, nullable=False, default=None, unique=False): super().__init__("str", nullable=nullable, default=default, unique=unique)
class ORMText(ORMColumn):
    def __init__(self): super().__init__("text", nullable=False)
class ORMBool(ORMColumn):
    def __init__(self, default=False): super().__init__("bool", default=default)
class ORMDT(ORMColumn):
    def __init__(self): super().__init__("datetime")

class ModelMeta(type):
    def __new__(mcs, name, bases, ns):
        cls = super().__new__(mcs, name, bases, ns)
        if name != "Model":
            cls.__tablename__ = ns.get("__tablename__", name.lower())
            cls._cols = {k: v for k, v in ns.items() if isinstance(v, ORMColumn)}
            cls._pk = next((k for k, v in cls._cols.items() if v.primary_key), "id")
        return cls

class Model(metaclass=ModelMeta):
    id = ORMInt(pk=True)

class Store:
    def __init__(self):
        self._data: dict[str, dict[int, Model]] = {}
        self._seq: dict[str, int] = {}
    def add(self, m):
        t = type(m).__tablename__
        self._data.setdefault(t, {})
        self._seq.setdefault(t, 0)
        self._seq[t] += 1
        setattr(m, type(m)._pk, self._seq[t])
        self._data[t][self._seq[t]] = m
    def all(self, cls): return list(self._data.get(cls.__tablename__, {}).values())
    def get(self, cls, pk): return self._data.get(cls.__tablename__, {}).get(pk)
    def filter(self, cls, **kw):
        return [m for m in self.all(cls) if all(getattr(m, k, None) == v for k, v in kw.items())]
    def first(self, cls, **kw):
        r = self.filter(cls, **kw); return r[0] if r else None
    def delete(self, m):
        self._data.get(type(m).__tablename__, {}).pop(getattr(m, type(m)._pk), None)
    def count(self, cls): return len(self.all(cls))

db = Store()


# ======================== Models ========================

class User(Model):
    __tablename__ = "users"
    username = ORMStr(unique=True)
    email = ORMStr(unique=True)
    password = ORMStr()
    created_at = ORMDT()

class Post(Model):
    __tablename__ = "posts"
    title = ORMStr()
    content = ORMText()
    user_id = ORMInt()
    published = ORMBool(default=False)
    created_at = ORMDT()

class Comment(Model):
    __tablename__ = "comments"
    content = ORMText()
    post_id = ORMInt()
    user_id = ORMInt()
    created_at = ORMDT()


# ======================== Session & Flash ========================

class Session:
    def __init__(self):
        self._data: dict = {}
    def __getitem__(self, k): return self._data[k]
    def __setitem__(self, k, v): self._data[k] = v
    def get(self, k, d=None): return self._data.get(k, d)
    def pop(self, k, d=None): return self._data.pop(k, d)
    def clear(self): self._data.clear()
    def to_dict(self): return dict(self._data)

class Flash:
    def __init__(self):
        self._msgs = []
    def flash(self, msg, cat="info"):
        self._msgs.append({"msg": msg, "cat": cat})
    def get(self):
        msgs = list(self._msgs); self._msgs.clear(); return msgs


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes = []
        self.session = Session()
        self.flash = Flash()

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
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

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                msgs = self.flash.get()
                if msgs: result["_flashes"] = msgs
                return {"status": 200, "data": result}
            params = self._match_route(r["path"], path)
            if method in r["methods"] and params is not None:
                result = r["handler"](**params, **kw)
                msgs = self.flash.get()
                if msgs: result["_flashes"] = msgs
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Auth ========================

@app.route("/register", methods=["GET", "POST"])
def register(**kw):
    if kw:
        if db.first(User, username=kw.get("username")):
            app.flash.flash("Username taken", "error")
            return {"error": "Username exists"}
        u = User(); u.username = kw.get("username"); u.email = kw.get("email"); u.password = kw.get("password")
        db.add(u)
        app.session["user_id"] = u.id; app.session["username"] = u.username
        app.flash.flash(f"Welcome, {u.username}!", "success")
        return {"user": {"id": u.id, "username": u.username, "email": u.email}}
    return {"form": {"username": "", "email": "", "password": ""}}

@app.route("/login", methods=["GET", "POST"])
def login(**kw):
    if kw:
        u = db.first(User, username=kw.get("username"))
        if not u or u.password != kw.get("password"):
            app.flash.flash("Invalid credentials", "error")
            return {"error": "Invalid credentials"}
        app.session["user_id"] = u.id; app.session["username"] = u.username
        app.flash.flash(f"Welcome back, {u.username}!", "success")
        return {"message": "Login successful"}
    return {"form": {"username": "", "password": ""}}

@app.route("/logout")
def logout():
    app.session.clear()
    app.flash.flash("Logged out", "info")
    return {"message": "Logged out"}


# ======================== Blog CRUD ========================

@app.route("/")
def home():
    posts = db.all(Post)
    result = []
    for p in posts:
        author = db.get(User, p.user_id)
        result.append({"id": p.id, "title": p.title, "author": author.username if author else "unknown", "published": p.published, "comment_count": len(db.filter(Comment, post_id=p.id))})
    user = app.session.get("username")
    return {"posts": result, "total": len(result), "user": user}


@app.route("/posts/new", methods=["GET", "POST"])
def create_post(**kw):
    if not app.session.get("user_id"):
        app.flash.flash("Please log in", "warning")
        return {"error": "Login required"}
    if kw:
        p = Post(); p.title = kw.get("title"); p.content = kw.get("content")
        p.user_id = app.session["user_id"]; p.published = kw.get("published", "false") in ("true", "1")
        db.add(p)
        app.flash.flash("Post created!", "success")
        return {"post": {"id": p.id, "title": p.title}, "redirect": "/"}
    return {"form": {"title": "", "content": ""}}

@app.route("/posts/<int:post_id>")
def view_post(post_id, **kw):
    p = db.get(Post, post_id)
    if not p:
        app.flash.flash("Post not found", "error")
        return {"error": "Not found"}
    author = db.get(User, p.user_id)
    comments = db.filter(Comment, post_id=post_id)
    enriched = []
    for c in comments:
        cu = db.get(User, c.user_id)
        enriched.append({"id": c.id, "content": c.content, "author": cu.username if cu else "unknown"})
    return {"post": {"id": p.id, "title": p.title, "content": p.content, "author": author.username if author else "unknown", "published": p.published}, "comments": enriched, "comment_count": len(enriched)}

@app.route("/posts/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id, **kw):
    if not app.session.get("user_id"):
        app.flash.flash("Login to comment", "warning")
        return {"error": "Login required"}
    if not db.get(Post, post_id):
        return {"error": "Post not found"}
    c = Comment(); c.content = kw.get("content", ""); c.post_id = post_id; c.user_id = app.session["user_id"]
    db.add(c)
    app.flash.flash("Comment added!", "success")
    return {"comment": {"id": c.id, "content": c.content}}

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id, **kw):
    if not app.session.get("user_id"):
        return {"error": "Login required"}
    p = db.get(Post, post_id)
    if not p: return {"error": "Not found"}
    if p.user_id != app.session["user_id"]:
        app.flash.flash("Not your post", "error")
        return {"error": "Not authorized"}
    for c in db.filter(Comment, post_id=post_id): db.delete(c)
    db.delete(p)
    app.flash.flash("Post deleted", "info")
    return {"deleted": True, "redirect": "/"}


# ======================== Demo ========================
print("=" * 60)
print("  INTEGRATION: FLASK BLOG APP")
print("=" * 60)

print("\n1. Register users:")
for u in [("alice", "alice@test.com", "pass1"), ("bob", "bob@test.com", "pass2")]:
    r = app("POST", "/register", username=u[0], email=u[1], password=u[2])
    print(f"   Registered: {r['data']['user']['username']}")

print("\n2. Create posts as Alice:")
for title, content in [("Hello World", "My first post!"), ("Flask Tips", "Use blueprints!"), ("Python News", "3.13 released")]:
    r = app("POST", "/posts/new", title=title, content=content, published="true")
    print(f"   Created: {r['data']['post']['title']}")

print("\n3. Bob logs in and comments:")
r = app("POST", "/login", username="bob", password="pass2")
for c in ["Great post!", "Thanks for sharing!", "Very helpful"]:
    r = app("POST", "/posts/1/comment", content=c)
    print(f"   Comment: {r['data']['comment']['content']}")

print("\n4. Home page (all posts with comment counts):")
r = app("GET", "/")
for p in r["data"]["posts"]:
    print(f"   [{p['id']}] {p['title']} — by {p['author']} ({p['comment_count']} comments)")

print("\n5. View post 1 with comments:")
r = app("GET", "/posts/1")
print(f"   Title: {r['data']['post']['title']}")
for c in r["data"]["comments"]:
    print(f"   💬 {c['author']}: {c['content']}")

print("\n6. Logout and try creating:")
r = app("GET", "/logout")
r = app("POST", "/posts/new", title="Unauthorized", content="Hacked")
print(f"   {r['data']}")
for msg in r["data"].get("_flashes", []):
    print(f"   💬 [{msg['cat']}] {msg['msg']}")

print(f"\n7. Stats:")
print(f"   Users: {db.count(User)}, Posts: {db.count(Post)}, Comments: {db.count(Comment)}")
