"""08-03-iterators.py — E-commerce: custom iterator for paginated API."""

class PaginatedAPI:
    def __init__(self, page_size: int = 3):
        self._all_products = [
            {"id": 1, "name": "Laptop", "price": 1499.99},
            {"id": 2, "name": "Mouse", "price": 29.99},
            {"id": 3, "name": "Keyboard", "price": 89.99},
            {"id": 4, "name": "Monitor", "price": 399.99},
            {"id": 5, "name": "Headphones", "price": 149.99},
            {"id": 6, "name": "Webcam", "price": 79.99},
            {"id": 7, "name": "Microphone", "price": 59.99},
        ]
        self.page_size = page_size

    def __iter__(self):
        return _ProductIterator(self._all_products, self.page_size)


class _ProductIterator:
    def __init__(self, products: list[dict], page_size: int):
        self._products = products
        self._page_size = page_size
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> list[dict]:
        if self._index >= len(self._products):
            raise StopIteration
        page = self._products[self._index:self._index + self._page_size]
        self._index += self._page_size
        return page


class ProductSearch:
    def __init__(self, products: list[dict], query: str):
        self._products = products
        self._query = query.lower()

    def __iter__(self):
        for product in self._products:
            if self._query in product["name"].lower():
                yield product


api = PaginatedAPI(page_size=3)
print("=== Paginated Products ===")
for page in api:
    print(f"  Page: {[p['name'] for p in page]}")

print("\n=== Lazy Search (e) ===")
search = ProductSearch(PaginatedAPI()._all_products, "e")
for product in search:
    print(f"  {product['name']}: ${product['price']}")
