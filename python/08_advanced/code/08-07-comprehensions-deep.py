"""08-07-comprehensions-deep.py — E-commerce: comprehensions for product processing."""

products = [
    {"name": "Laptop", "price": 1499.99, "category": "Electronics", "stock": 5},
    {"name": "Mouse", "price": 29.99, "category": "Accessories", "stock": 50},
    {"name": "Keyboard", "price": 89.99, "category": "Accessories", "stock": 0},
    {"name": "Monitor", "price": 399.99, "category": "Electronics", "stock": 10},
    {"name": "Webcam", "price": 79.99, "category": "Electronics", "stock": 0},
    {"name": "Desk", "price": 299.99, "category": "Furniture", "stock": 3},
]

in_stock = [p["name"] for p in products if p["stock"] > 0]
print(f"In stock: {in_stock}")

discounted = [{"name": p["name"], "sale_price": round(p["price"] * 0.9, 2)} for p in products]
print(f"Sale prices: {discounted[:3]}")

price_lookup = {p["name"]: p["price"] for p in products}
print(f"Laptop price: ${price_lookup['Laptop']}")

categories = {p["category"] for p in products}
print(f"Categories: {categories}")

total_value = sum(p["price"] * p["stock"] for p in products)
print(f"Total inventory: ${total_value:.2f}")

order_items = [["Laptop", "Mouse"], ["Keyboard"], ["Monitor", "Webcam", "Cable"]]
all_items = [item for sublist in order_items for item in sublist]
print(f"Flattened: {all_items}")

results = [
    {"name": p["name"], "total": (t := p["price"] * p["stock"]), "status": "high" if t > 1000 else "low"}
    for p in products if p["stock"] > 0
]
print(f"Walrus: {results}")
