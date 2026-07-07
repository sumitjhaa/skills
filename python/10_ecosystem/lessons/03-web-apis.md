# 🌐 Web & APIs
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Built-in `http.server`, `urllib`, third-party `requests` and `httpx`, REST API principles, HTTP status codes, and JSON APIs for social-media data.

> 💡 **TL;DR — The whole point:** Python makes HTTP trivial. `urllib` is built-in but clunky. `requests`/`httpx` are ergonomic and production-ready. FastAPI builds type-safe APIs with auto-docs.

## 🔗 Why This Matters
Every social-media analytics tool talks to APIs — Twitter API for tweets, Instagram Graph API for posts, OpenAI API for content analysis. Understanding HTTP clients and REST principles means you can integrate any API.

## The Concept
- **`urllib.request`** — built-in HTTP client (no install needed)
- **`requests`** — the de facto standard HTTP library
- **`httpx`** — modern async-capable alternative
- **REST methods:** GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- **Status codes:** 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Server Error

## Code Example
```python
"""Social-media: fetch posts and users from a REST API."""

import json
from urllib.request import urlopen, Request


BASE_URL = "https://jsonplaceholder.typicode.com"


def get_posts() -> list[dict]:
    """GET /posts — fetch all posts."""
    with urlopen(f"{BASE_URL}/posts") as resp:
        return json.loads(resp.read())


def get_post(post_id: int) -> dict:
    """GET /posts/{id} — fetch a single post."""
    with urlopen(f"{BASE_URL}/posts/{post_id}") as resp:
        return json.loads(resp.read())


def create_post(title: str, body: str, user_id: int = 1) -> dict:
    """POST /posts — create a new post."""
    data = json.dumps({"title": title, "body": body, "userId": user_id}).encode()
    req = Request(f"{BASE_URL}/posts", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urlopen(req) as resp:
        return json.loads(resp.read())


# Using requests (third-party, install with: pip install requests)
def using_requests() -> None:
    import requests
    resp = requests.get(f"{BASE_URL}/posts/1")
    post = resp.json()
    print(f"Requests: Post 1 — {post['title']}")

    # Sessions reuse connections
    with requests.Session() as session:
        for post_id in range(1, 4):
            p = session.get(f"{BASE_URL}/posts/{post_id}").json()
            print(f"  Post {post_id}: {p['title'][:30]}...")


posts = get_posts()
print(f"Got {len(posts)} posts from API")

post = get_post(1)
print(f"Post 1: {post['title']}")

new_post = create_post("Async in Python", "asyncio is the future!")
print(f"Created post {new_post['id']}")
```

## 🔍 How It Works
- `urlopen(url)` — opens a URL, returns a file-like object; `.read()` gets the body
- `json.loads(resp.read())` — parses JSON response body into Python dicts/lists
- `Request(url, data, method="POST")` — custom HTTP method with request body
- `requests.Session()` — pools TCP connections for performance, persists cookies
- Status codes: check `resp.status` (urllib) or `resp.status_code` (requests)
- Always handle errors: `try/except` around network calls; check status codes

## ⚠️ Common Pitfall
Forgetting to decode/encode JSON. `urlopen().read()` returns bytes — you need `json.loads()` for responses and `json.dumps().encode()` for request bodies. `requests` does this automatically.

## 🧠 Memory Aid
"urllib = built-in but manual JSON. requests = automatic JSON + sessions. GET = fetch. POST = create. 200 = OK. 404 = not found. 500 = server broke."

## 🏃 Try It
Fetch all comments for post ID 1 from `https://jsonplaceholder.typicode.com/comments?postId=1`. Print the email addresses of commenters. Use `requests` to do it in one line.

## 🔗 Related
- [HTTPX & Requests Deep](../09_production/lessons/14-httpx-requests-deep.md) — advanced HTTP patterns
- [FastAPI Deep](06-fastapi-deep.md) — building APIs with FastAPI

## ➡️ Next
[Data Science Introduction](04-data-science-intro.md)
