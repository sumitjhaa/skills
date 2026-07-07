"""08-08-functools-deep.py — E-commerce: caching, dispatch, partial, reduce."""

from functools import lru_cache, singledispatch, partial, reduce, wraps
import time


@lru_cache(maxsize=128)
def compute_shipping_cost(weight_kg: float, distance_km: int) -> float:
    time.sleep(0.05)
    return weight_kg * 0.5 + distance_km * 0.01


print(f"Shipping: ${compute_shipping_cost(2.5, 1000):.2f}")
print(f"Cached: ${compute_shipping_cost(2.5, 1000):.2f}")
print(f"Cache: {compute_shipping_cost.cache_info()}")


@singledispatch
def format_price(value) -> str:
    return str(value)


@format_price.register(float)
def _(value: float) -> str:
    return f"${value:.2f}"


@format_price.register(int)
def _(value: int) -> str:
    return f"${value}.00"


@format_price.register(list)
def _(value: list) -> str:
    return ", ".join(format_price(v) for v in value)


print(f"\nFloat: {format_price(49.99)}")
print(f"Int: {format_price(50)}")
print(f"List: {format_price([10, 20.5, 30])}")


def apply_discount(price: float, discount_pct: float, tax_rate: float = 0.08) -> float:
    return price * (1 - discount_pct / 100) * (1 + tax_rate)


ten_off = partial(apply_discount, discount_pct=10)
print(f"\n10% off $100: ${ten_off(100):.2f}")

prices = [10, 20, 30, 40]
total = reduce(lambda a, b: a + b, prices)
print(f"Total (reduce): ${total}")
