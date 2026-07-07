"""Property patterns: cached, lazy, computed, validated — e-commerce pricing"""
import functools

class Product:
    def __init__(self, name: str, base_price: float, tax_rate: float = 0.1):
        self.name = name
        self._base_price = base_price  # private — setter validates
        self._tax_rate = tax_rate
        self._discount = 0.0
        self._cache = {}

    @property
    def base_price(self):
        return self._base_price

    @base_price.setter
    def base_price(self, value: float):
        """Ensures price stays positive — real inventory constraint"""
        if value <= 0:
            raise ValueError(f"Price must be positive, got {value}")
        self._base_price = value
        self._cache.clear()

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError(f"Discount must be 0-100%, got {percent}")
        self._discount = percent

    @property
    def final_price(self):
        """Computed from base_price, discount, and tax_rate — always live"""
        discounted = self._base_price * (1 - self._discount / 100)
        return round(discounted * (1 + self._tax_rate), 2)

    @property
    @functools.lru_cache(maxsize=1)
    def shipping_weight_kg(self):
        """Cached — simulates a DB lookup, computed once then cached"""
        print("  [DB] Fetching shipping weight...")
        return 1.5

laptop = Product("Gaming Laptop", 1499.99, 0.08)
print(f"Base: ${laptop.base_price}, Final: ${laptop.final_price}")
laptop.discount = 15
print(f"After {laptop.discount}% off: ${laptop.final_price}")
try:
    laptop.base_price = -100
except ValueError as e:
    print(f"  Caught: {e}")
print(f"Weight: {laptop.shipping_weight_kg} kg")
print(f"Weight (cached): {laptop.shipping_weight_kg} kg")
