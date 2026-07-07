"""07-01-classes-objects.py — E-commerce: Product class with class/instance attributes."""

class Product:
    store_name = "PyMart"

    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price


laptop = Product("TECH-001", "Gaming Laptop", 1499.99)
mouse = Product("ACC-002", "Wireless Mouse", 29.99)

print(f"{laptop.name}: ${laptop.price} @ {laptop.store_name}")
print(f"{mouse.name}: ${mouse.price} @ {mouse.store_name}")
print(f"Type: {type(laptop).__name__}")

Product.store_name = "PyMart Pro"
print(f"After rename: {mouse.store_name}")
