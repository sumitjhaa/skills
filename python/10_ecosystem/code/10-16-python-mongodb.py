"""MongoDB with PyMongo — product catalog CRUD + aggregation.
Run: python 10-16-python-mongodb.py
"""
from __future__ import annotations

try:
    from pymongo import MongoClient, DESCENDING
    from bson.objectid import ObjectId
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False
    from uuid import uuid4

    class ObjectId:
        def __init__(self, oid: str | None = None) -> None:
            self.oid = oid or str(uuid4())
        def __str__(self) -> str:
            return self.oid
        def __repr__(self) -> str:
            return f"ObjectId('{self.oid}')"
        def __eq__(self, other: object) -> bool:
            return str(self) == str(other)


class MockCollection:
    """In-memory mock that mimics PyMongo Collection for offline demo."""
    def __init__(self) -> None:
        self._docs: dict[str, dict] = {}

    def insert_one(self, doc: dict) -> type("InsertOneResult", (), {"inserted_id": None}):
        _id = doc.get("_id", ObjectId())
        if "_id" not in doc:
            doc["_id"] = _id
        self._docs[str(_id)] = dict(doc)
        return type("InsertOneResult", (), {"inserted_id": _id})()

    def insert_many(self, docs: list[dict]) -> None:
        for d in docs:
            self.insert_one(d)

    def find_one(self, filter_: dict | None = None) -> dict | None:
        for doc in self._docs.values():
            if filter_ is None or all(doc.get(k) == v for k, v in filter_.items()):
                return dict(doc)
        return None

    def find(self, filter_: dict | None = None) -> list[dict]:
        return [dict(d) for d in self._docs.values()
                if filter_ is None or all(d.get(k) == v for k, v in filter_.items())]

    def update_one(self, filter_: dict, update: dict) -> int:
        doc = self.find_one(filter_)
        if doc is None:
            return 0
        stored = self._docs[str(doc["_id"])]
        if "$set" in update:
            stored.update(update["$set"])
        return 1

    def delete_one(self, filter_: dict) -> int:
        doc = self.find_one(filter_)
        if doc is None:
            return 0
        del self._docs[str(doc["_id"])]
        return 1

    def aggregate(self, pipeline: list[dict]) -> list[dict]:
        data = list(self._docs.values())
        for stage in pipeline:
            if "$match" in stage:
                data = [d for d in data if all(
                    d.get(k) == v for k, v in stage["$match"].items())]
            elif "$group" in stage:
                g = stage["$group"]
                key_field = g["_id"]
                accum_fields = {k: v for k, v in g.items() if k != "_id"}
                groups: dict = {}
                for d in data:
                    field_name = key_field[1:] if isinstance(key_field, str) and key_field.startswith("$") else key_field
                    k = d.get(field_name) if isinstance(field_name, str) else field_name
                    if k not in groups:
                        groups[k] = {"_id": k}
                        for af in accum_fields:
                            groups[k][af] = 0
                    for af, expr in accum_fields.items():
                        val = expr.get("$sum", 0)
                        if isinstance(val, str) and val.startswith("$"):
                            val = d.get(val[1:], 0)
                        groups[k][af] += val
                data = list(groups.values())
            elif "$sort" in stage:
                data.sort(key=lambda d: tuple(
                    d.get(k, 0) * (1 if v > 0 else -1) for k, v in stage["$sort"].items()
                ))
        return data

    def create_index(self, field: str) -> str:
        return f"{field}_1"


def main() -> None:
    USE_MOCK = not HAS_PYMONGO
    if HAS_PYMONGO:
        try:
            client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1000)
            client.admin.command("ping")
            db = client.product_catalog
            coll = db.products
            coll.drop()
        except Exception:
            USE_MOCK = True
    if USE_MOCK:
        print("  [MOCK] No MongoDB — using in-memory mock")
        coll = MockCollection()

    # ── Insert ──
    result = coll.insert_one({
        "name": "Wireless Mouse", "category": "Electronics",
        "price": 29.99, "stock": 150, "tags": ["mouse", "wireless", "2.4GHz"],
    })
    print(f"  Inserted _id: {result.inserted_id}")

    coll.insert_many([
        {"name": "USB-C Hub", "category": "Electronics", "price": 49.99,
         "stock": 80, "tags": ["usb", "hub", "type-c"]},
        {"name": "Notebook A5", "category": "Stationery", "price": 4.99,
         "stock": 500, "tags": ["paper", "notebook"]},
        {"name": "Desk Lamp", "category": "Furniture", "price": 34.99,
         "stock": 40, "tags": ["lighting", "led"]},
    ])

    # ── Find ──
    cheap = coll.find_one({"name": "Notebook A5"})
    print(f"  Cheap item: {cheap['name']} — ${cheap['price']}")

    electronics = coll.find({"category": "Electronics"})
    print(f"  Electronics count: {len(electronics)}")

    # ── Update ──
    modified = coll.update_one({"name": "Desk Lamp"}, {"$set": {"stock": 35}})
    print(f"  Updated: {modified} document(s)")

    # ── Aggregate ──
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1},
                     "total_value": {"$sum": "$price"}}},
        {"$sort": {"total_value": -1}},
    ]
    if HAS_PYMONGO:
        results = list(coll.aggregate(pipeline))
    else:
        results = coll.aggregate(pipeline)
    for r in results:
        print(f"  {r['_id']}: {r['count']} product(s), ${r['total_value']:.2f}")

    # ── Index ──
    idx = coll.create_index("category")
    print(f"  Created index: {idx}")

    # ── Delete ──
    coll.delete_one({"name": "USB-C Hub"})
    remaining = coll.find({})
    print(f"  Products after delete: {len(remaining)}")

    print("All MongoDB examples OK")


if __name__ == "__main__":
    main()
