# 🎯 Property Patterns
<!-- ⏱️ 12 min | 🟡 Difficulty | 🧠 Applied -->

**What You'll Learn:** Use cached, lazy, computed, and validated property patterns in an e-commerce pricing domain.

> 💡 **TL;DR — The whole point:** Properties aren't just getters/setters — you can cache expensive lookups, compute values on the fly, validate on assignment, and clear caches when dependencies change.

## 🔗 Why This Matters
A `Product` has `base_price`, `discount`, `tax_rate`, and `shipping_weight`. Price changes must invalidate cached data; discounts must stay in range; shipping weight might require a DB call. Properties let you wire all this up transparently so callers just do `product.final_price`.

## The Concept
Four property patterns: **validated** setters reject bad data (`base_price` > 0, `discount` 0–100%); **computed** properties derive values from others (`final_price`); **cached** properties use `functools.lru_cache` to avoid repeated DB calls (`shipping_weight_kg`); **cache-busting** clears dependent caches when a source value changes.

## Code Example
```python
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
```

## 🔍 How It Works
- `base_price` setter validates > 0 then clears `_cache` — busts derived/cached values automatically
- `final_price` is a live computed property — always re-reads `_base_price`, `_discount`, `_tax_rate`
- `shipping_weight_kg` uses `@lru_cache` so the simulated DB print only fires once
- `discount` setter clamps range 0–100% but doesn't bust cache (trivial to recalc)
- There's no setter for `final_price` or `shipping_weight_kg` — they're effectively read-only

## ⚠️ Common Pitfall
`@lru_cache` on a property caches on the instance, not the class — but it's still per-instance. If you need cache-busting, manually manage `self._cache` or use a custom `cached_property` (Python 3.8+).

## 🧠 Memory Aid
"Four tools, one `@property`: validate gate, compute bridge, cache vault, bust reset."

## 🏃 Try It
Add a `bulk_discount` property to `Product` that applies an extra 5% off when `quantity > 10`. Use cache-busting to clear `final_price` when quantity changes.

## 🔗 Related
- [Properties](06-properties.md) — the basics of `@property`, setter, deleter

## ➡️ Next
[Dataclass Deep](21-dataclass-deep.md)
