# ⚡ Async MongoDB with Motor
<!-- ⏱️ 14 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Use Motor, the async MongoDB driver for Python, in an asyncio application — with CRUD, aggregation, and connection pooling.

> 💡 **TL;DR — The whole point:** `motor` is to `pymongo` what `httpx.AsyncClient` is to `requests` — it lets you talk to MongoDB without blocking the event loop. Use it in FastAPI/asyncio apps.

## 🔗 Why This Matters
If you're building an async application (FastAPI, aiohttp, Discord bot), using `pymongo` (sync) blocks the event loop and kills performance. Motor provides the same API but with `async/await` — no blocking, no thread pool workarounds.

## The Concept

| Motor | PyMongo Equivalent | What It Does |
|-------|-------------------|--------------|
| `AsyncIOMotorClient` | `MongoClient` | Connect to MongoDB |
| `client.db.collection` | Same | Access collection |
| `await coll.find_one()` | `coll.find_one()` | Find one document |
| `await coll.find().to_list()` | `list(coll.find())` | Find many documents |
| `await coll.insert_one()` | Same | Insert one document |
| `await coll.aggregate().to_list()` | Same | Aggregation pipeline |
| `await coll.create_index()` | Same | Create an index |

## Code Example

```python
"""Async MongoDB with Motor — CRUD and aggregation."""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "motor_demo"
COLLECTION = "products"


async def demo():
    # Connect
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLLECTION]

    # Clean slate
    await coll.drop()

    # ---- Create ----
    laptop = await coll.insert_one({
        "name": "Laptop Pro",
        "price": 1499.99,
        "category": "electronics",
        "stock": 50,
        "tags": ["laptop", "pro"],
        "created_at": datetime.now(timezone.utc),
    })
    print(f"Inserted: {laptop.inserted_id}")

    phones = await coll.insert_many([
        {"name": "Phone X", "price": 999.99, "category": "electronics", "stock": 100},
        {"name": "Phone Mini", "price": 699.99, "category": "electronics", "stock": 200},
    ])
    print(f"Inserted {len(phones.inserted_ids)} phones")

    # ---- Read ----
    pro_laptop = await coll.find_one({"name": "Laptop Pro"})
    print(f"Found: {pro_laptop['name']} — ${pro_laptop['price']}")

    cursor = coll.find({"category": "electronics"}).sort("price", 1)
    electronics = await cursor.to_list(length=10)
    print(f"Electronics ({len(electronics)}): {[e['name'] for e in electronics]}")

    # ---- Update ----
    result = await coll.update_one(
        {"name": "Laptop Pro"},
        {"$inc": {"stock": -1}, "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    print(f"Updated: {result.modified_count} document(s)")

    # ---- Aggregation ----
    pipeline = [
        {"$match": {"category": "electronics"}},
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}, "total_stock": {"$sum": "$stock"}}},
    ]
    cursor = coll.aggregate(pipeline)
    result = await cursor.to_list(length=10)
    if result:
        print(f"Avg price: ${result[0]['avg_price']:.2f}, Total stock: {result[0]['total_stock']}")

    # ---- Index ----
    await coll.create_index("price")
    indexes = await coll.index_information()
    print(f"Indexes: {list(indexes.keys())}")

    # ---- Cleanup ----
    client.close()
    print("\n✅ Motor demo complete — async, non-blocking MongoDB access")


if __name__ == "__main__":
    asyncio.run(demo())
```

## 🔍 How It Works
- `AsyncIOMotorClient` is async from the ground up — every operation is `await`-ed
- `find().to_list(length=N)` replaces PyMongo's `list(cursor)` — you must specify a max length
- `aggregate().to_list()` works the same way with aggregation pipelines
- `$inc`, `$set`, `$push` are MongoDB update operators — Motor supports all of them
- `create_index("price")` creates a B-tree index for fast sorting/filtering by price
- `client.close()` must be called to free connection pool resources

## ⚠️ Common Pitfall
- Forgetting `await` — you'll get a coroutine object, not the result
- Not limiting `to_list()` — Motor requires an explicit `length` to prevent memory overflow
- Mixing sync PyMongo and async Motor in the same project — leads to event loop confusion
- Not handling `AutoReconnect` errors — Motor auto-reconnects but operations during disconnect fail

## 🧠 Memory Aid
"Motor = PyMongo + async/await. Create with `AsyncIOMotorClient`, query with `await coll.find()`, always `to_list(length)`."

## 🏃 Try It
Create a FastAPI route `GET /products?category=X&min_price=Y&max_price=Z` that queries MongoDB via Motor with filtering, sorting by price, and limiting to 20 results.

## 🔗 Related
- [Python & MongoDB](16-python-mongodb.md) — sync PyMongo CRUD (prerequisite)
- [Asyncio Intro](02-asyncio-intro.md) — async/await basics
- [FastAPI Deep](06-fastapi-deep.md) — FastAPI + Motor in production
- [SQLAlchemy Deep](07-sqlalchemy-deep.md) — async SQL alternative

## ➡️ Next
[20 — Selenium & Dynamic Scraping](20-selenium-dynamic-scraping.md)
