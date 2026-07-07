"""08-13-weakref-contextvars.py — weakref cache, contextvars tracing."""

from weakref import WeakValueDictionary
from contextvars import ContextVar
import gc
import asyncio


class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"Product({self.sku}, {self.name})"


class ProductCache:
    def __init__(self):
        self._cache: WeakValueDictionary[str, Product] = WeakValueDictionary()

    def add(self, product: Product) -> None:
        self._cache[product.sku] = product

    def get(self, sku: str) -> Product | None:
        return self._cache.get(sku)

    @property
    def size(self) -> int:
        return len(self._cache)


cache = ProductCache()
p = Product("LAP-001", "Gaming Laptop", 1499.99)
cache.add(p)

print(f"Before delete: size = {cache.size}")
del p
gc.collect()
print(f"After delete: size = {cache.size}")

request_id_var: ContextVar[str] = ContextVar("request_id", default="unknown")


async def handle_request(request_id: str) -> None:
    token = request_id_var.set(request_id)
    print(f"  [Handler] {request_id_var.get()}")
    await process_order()
    print(f"  [Handler done] {request_id_var.get()}")
    request_id_var.reset(token)


async def process_order() -> None:
    print(f"  [Process] Request {request_id_var.get()}")
    await asyncio.sleep(0.05)


async def main() -> None:
    print("\n=== ContextVars ===")
    await asyncio.gather(
        handle_request("REQ-001"),
        handle_request("REQ-002"),
        handle_request("REQ-003"),
    )


asyncio.run(main())
