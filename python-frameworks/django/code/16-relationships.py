"""Model relationships: forward/reverse queries, select_related, prefetch_related."""
from dataclasses import dataclass, field
from typing import Any, Optional


# --- In-memory store ---
TABLES = {
    "Author": [],
    "Post": [],
    "Comment": [],
}
PK_COUNTERS = {"Author": 1, "Post": 1, "Comment": 1}


def _next_pk(model: str) -> int:
    pk = PK_COUNTERS[model]
    PK_COUNTERS[model] += 1
    return pk


def _add(model: str, **fields) -> dict:
    obj = {"id": _next_pk(model), **fields}
    TABLES[model].append(obj)
    return obj


def _table(model: str) -> list[dict]:
    return TABLES[model]


_add("Author", name="Alice", email="alice@example.com")
_add("Author", name="Bob", email="bob@example.com")
_add("Author", name="Charlie", email="charlie@example.com")

alice, bob, charlie = 1, 2, 3

_add("Post", title="Hello Django", author_id=alice, likes=12)
_add("Post", title="Django Models", author_id=bob, likes=5)
_add("Post", title="Advanced ORM", author_id=alice, likes=8)
_add("Post", title="Python Tips", author_id=charlie, likes=3)
_add("Post", title="Django REST", author_id=1, likes=15)

_posts = _table("Post")
_add("Comment", text="Great post!", post_id=_posts[0]["id"], author_id=2)
_add("Comment", text="Thanks!", post_id=_posts[0]["id"], author_id=1)
_add("Comment", text="Nice article", post_id=_posts[1]["id"], author_id=3)
_add("Comment", text="Very helpful", post_id=_posts[2]["id"], author_id=2)


# --- Forward query (Post → Author) ---
def forward_lookup(post: dict) -> Optional[dict]:
    for a in _table("Author"):
        if a["id"] == post.get("author_id"):
            return a
    return None


# --- Reverse query (Author → Posts) ---
def reverse_lookup(author: dict) -> list[dict]:
    return [p for p in _table("Post") if p["author_id"] == author["id"]]


# --- select_related: JOIN Posts with Authors ---
def select_related(posts: list[dict], field_name: str, target_model: str) -> list[dict]:
    lookup = f"{field_name}_id"
    target_table = _table(target_model)
    cache = {t["id"]: t for t in target_table}
    result = []
    for p in posts:
        row = dict(p)
        fk = p.get(lookup)
        if fk in cache:
            row[field_name] = cache[fk]
        result.append(row)
    return result


# --- prefetch_related: Fetch related objects for multiple parents ---
def prefetch_related(posts: list[dict], fk_field: str, target_model: str) -> list[dict]:
    target_table = _table(target_model)
    post_ids = [p["id"] for p in posts]
    related = {}
    for t in target_table:
        parent_id = t.get(fk_field)
        if parent_id in post_ids:
            related.setdefault(parent_id, []).append(t)
    result = []
    for p in posts:
        row = dict(p)
        row[f"{target_model.lower()}s"] = related.get(p["id"], [])
        result.append(row)
    return result


print("--- Forward: Post → Author ---")
for p in _posts[:3]:
    author = forward_lookup(p)
    print(f"  '{p['title']}' by {author['name'] if author else '?'}")

print("\n--- Reverse: Author → Posts ---")
for author in _table("Author"):
    posts = reverse_lookup(author)
    titles = [p["title"] for p in posts]
    print(f"  {author['name']}: {titles}")

print("\n--- select_related (simulated JOIN) ---")
joined = select_related(_posts[:4], "author", "Author")
for p in joined:
    a = p.get("author", {})
    print(f"  '{p['title']}' — {a.get('name', '?')}")

print("\n--- prefetch_related (simulated batch) ---")
prefetched = prefetch_related(_posts[:3], "post_id", "Comment")
for p in prefetched:
    comments = p.get("comments", [])
    texts = [c["text"] for c in comments]
    print(f"  '{p['title']}': {texts}")
