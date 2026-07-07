"""Async MongoDB with Motor — CRUD and aggregation."""
import asyncio
from datetime import datetime, timezone

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError:
    print("Install Motor: pip install motor")
    print("This demo requires a running MongoDB instance.")
    print("\nFallback: showing the pattern without connecting.\n")

    async def demo():
        print("Motor pattern overview:")
        print("""
  client = AsyncIOMotorClient("mongodb://localhost:27017")
  db = client.mydb
  coll = db.products

  # Create
  result = await coll.insert_one({"name": "Laptop", "price": 1499.99})

  # Read
  doc = await coll.find_one({"name": "Laptop"})
  cursor = coll.find({"price": {"$gte": 500}}).sort("price", 1)
  items = await cursor.to_list(length=100)

  # Update
  await coll.update_one({"name": "Laptop"}, {"$inc": {"stock": -1}})

  # Aggregate
  pipeline = [{"$group": {"_id": "$category", "avg": {"$avg": "$price"}}}]
  results = await coll.aggregate(pipeline).to_list(length=50)

  # Index
  await coll.create_index("price")

  client.close()
        """)
    asyncio.run(demo())
    raise SystemExit(1)

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "motor_demo"
COLLECTION = "products"


async def demo():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLLECTION]

    await coll.drop()

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

    pro_laptop = await coll.find_one({"name": "Laptop Pro"})
    print(f"Found: {pro_laptop['name']} — ${pro_laptop['price']}")

    cursor = coll.find({"category": "electronics"}).sort("price", 1)
    electronics = await cursor.to_list(length=10)
    print(f"Electronics ({len(electronics)}): {[e['name'] for e in electronics]}")

    result = await coll.update_one(
        {"name": "Laptop Pro"},
        {"$inc": {"stock": -1}, "$set": {"updated_at": datetime.now(timezone.utc)}},
    )
    print(f"Updated: {result.modified_count} document(s)")

    pipeline = [
        {"$match": {"category": "electronics"}},
        {"$group": {"_id": None, "avg_price": {"$avg": "$price"}, "total_stock": {"$sum": "$stock"}}},
    ]
    cursor = coll.aggregate(pipeline)
    result = await cursor.to_list(length=10)
    if result:
        print(f"Avg price: ${result[0]['avg_price']:.2f}, Total stock: {result[0]['total_stock']}")

    await coll.create_index("price")
    indexes = await coll.index_information()
    print(f"Indexes: {list(indexes.keys())}")

    client.close()
    print("\n✅ Motor demo complete")


if __name__ == "__main__":
    asyncio.run(demo())
