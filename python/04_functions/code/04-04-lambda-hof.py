"""E-commerce — sorting products, filtering users, and order processing."""
from functools import reduce

products = [
    {"name": "Laptop", "price": 1200, "rating": 4.5},
    {"name": "Mouse", "price": 25, "rating": 4.8},
    {"name": "Keyboard", "price": 100, "rating": 4.2},
    {"name": "Monitor", "price": 350, "rating": 4.6},
    {"name": "Headphones", "price": 80, "rating": 4.3},
]

by_price = sorted(products, key=lambda p: p["price"])
by_rating = sorted(products, key=lambda p: p["rating"], reverse=True)
print("Cheapest:", [p["name"] for p in by_price[:3]])
print("Top rated:", by_rating[0]["name"])

affordable = list(filter(lambda p: p["price"] < 200, products))
print(f"Affordable ({len(affordable)}): {[p['name'] for p in affordable]}")

discounted = list(map(lambda p: {**p, "price": round(p["price"] * 0.9, 2)}, products))
print(f"Discounted: {discounted[0]}")

orders = [{"item": "book", "qty": 3, "price": 15}, {"item": "pen", "qty": 10, "price": 2}]
total = reduce(lambda acc, o: acc + o["qty"] * o["price"], orders, 0)
print(f"Total order value: ${total}")
