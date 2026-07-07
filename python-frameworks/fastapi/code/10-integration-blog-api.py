"""Integration: Full blog API — combines all Phase 01 concepts."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import re


# ======================== Core ========================
class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail


class FastAPI:
    def __init__(self):
        self.routes = []

    def get(self, path: str):
        def dec(f):
            self.routes.append({"path": path, "method": "GET", "handler": f})
            return f
        return dec

    def post(self, path: str):
        def dec(f):
            self.routes.append({"path": path, "method": "POST", "handler": f})
            return f
        return dec

    def put(self, path: str):
        def dec(f):
            self.routes.append({"path": path, "method": "PUT", "handler": f})
            return f
        return dec

    def delete(self, path: str):
        def dec(f):
            self.routes.append({"path": path, "method": "DELETE", "handler": f})
            return f
        return dec

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        # Parse path params
        for route in self.routes:
            if route["method"] != method:
                continue
            rp = route["path"].strip("/").split("/")
            pp = path.strip("/").split("/")
            if len(rp) != len(pp):
                continue
            params = {}
            match = True
            for r_seg, p_seg in zip(rp, pp):
                if r_seg.startswith("{") and r_seg.endswith("}"):
                    params[r_seg[1:-1]] = p_seg
                elif r_seg != p_seg:
                    match = False
                    break
            if match:
                try:
                    # Type coercion
                    for k, v in params.items():
                        params[k] = int(v) if v.isdigit() else v
                    result = route["handler"](**params, **kwargs)
                    return {"status": 200, "data": result}
                except HTTPException as e:
                    return {"status": e.status_code, "data": {"detail": e.detail}}
                except Exception as e:
                    return {"status": 500, "data": {"detail": str(e)}}
        return {"status": 404, "data": {"detail": "Not Found"}}


# ======================== Data Store ========================
POSTS: list[dict] = []
PK = 1


def seed():
    global POSTS, PK
    POSTS = [
        {"id": 1, "title": "Hello FastAPI", "content": "Getting started with FastAPI", "author": "alice", "is_published": True, "created_at": "2024-01-15"},
        {"id": 2, "title": "Path Parameters", "content": "Using path and query params", "author": "alice", "is_published": True, "created_at": "2024-01-20"},
        {"id": 3, "title": "Draft: Advanced", "content": "Advanced FastAPI concepts", "author": "bob", "is_published": False, "created_at": "2024-02-01"},
    ]
    PK = 4


seed()


# ======================== App ========================
app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "FastAPI Blog API",
        "version": "1.0.0",
        "endpoints": {
            "GET  /": "Root",
            "GET  /posts/": "List posts",
            "POST /posts/": "Create post",
            "GET  /posts/{id}": "Get post detail",
            "PUT  /posts/{id}": "Update post",
            "DELETE /posts/{id}": "Delete post",
            "GET  /posts/search/": "Search posts",
        },
    }


@app.get("/posts/")
def list_posts(page: int = 1, page_size: int = 10):
    published = [p for p in POSTS if p["is_published"]]
    start = (page - 1) * page_size
    end = start + page_size
    page_items = published[start:end]
    return {
        "items": page_items,
        "total": len(published),
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-len(published) // page_size)),
    }


@app.get("/posts/search/")
def search_posts(q: str = ""):
    if not q:
        return {"results": POSTS[:5]}
    results = [
        p for p in POSTS
        if q.lower() in p["title"].lower() or q.lower() in p["content"].lower()
    ]
    return {"query": q, "count": len(results), "results": results}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        raise HTTPException(404, f"Post {post_id} not found")
    return post


@app.post("/posts/")
def create_post(title: str, content: str, author: str = "anonymous"):
    errors = []
    if not title or len(title) < 3:
        errors.append("Title must be at least 3 characters")
    if not content:
        errors.append("Content is required")
    if errors:
        return {"status": 422, "data": {"detail": errors}}
    global PK
    post = {
        "id": PK,
        "title": title,
        "content": content,
        "author": author,
        "is_published": False,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    PK += 1
    POSTS.append(post)
    return post


@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str = None, content: str = None, is_published: bool = None):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        raise HTTPException(404, f"Post {post_id} not found")
    if title is not None:
        post["title"] = title
    if content is not None:
        post["content"] = content
    if is_published is not None:
        post["is_published"] = is_published
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    global POSTS
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        raise HTTPException(404, f"Post {post_id} not found")
    POSTS = [p for p in POSTS if p["id"] != post_id]
    return {"message": f"Post {post_id} deleted"}


# ======================== Demo ========================
print("=" * 60)
print("🌐 FASTAPI BLOG API — INTEGRATION DEMO")
print("=" * 60)

tests = [
    ("GET", "/", {}),
    ("GET", "/posts/", {}),
    ("GET", "/posts/1", {}),
    ("GET", "/posts/999", {}),
    ("POST", "/posts/", {"title": "New Post", "content": "Created via API", "author": "alice"}),
    ("PUT", "/posts/1", {"title": "Updated Title"}),
    ("DELETE", "/posts/3", {}),
    ("GET", "/posts/search/", {"q": "fastapi"}),
]

for method, path, kwargs in tests:
    result = app(method, path, **kwargs)
    status = result["status"]
    icon = "✅" if status == 200 else "⚠️" if status == 422 else "❌"
    data_preview = json.dumps(result["data"])[:80]
    print(f"\n  {icon} {method:6s} {path:25s} → {status}")
    print(f"     {data_preview}{'...' if len(json.dumps(result['data'])) > 80 else ''}")

print(f"\n{'='*60}")
print("FINAL STATE")
print(f"{'='*60}")
print(f"  Total posts: {len(POSTS)}")
for p in POSTS:
    print(f"  #{p['id']} '{p['title']}' by {p['author']} (published={p['is_published']})")
