"""E-commerce product search with flexible filtering and pagination."""


def search_products(query: str, /, *, category: str = "", min_price: float = 0, max_price: float = 1_000_000, sort_by: str = "relevance", page: int = 1, **filters: str) -> dict:
    params = {"query": query, "category": category, "price_range": (min_price, max_price), "sort": sort_by, "page": page}
    params.update(filters)
    return params


def paginate(items: list, page: int = 1, page_size: int = 10) -> dict:
    start = (page - 1) * page_size
    end = start + page_size
    return {"page": page, "page_size": page_size, "total": len(items), "results": items[start:end]}


def tag_product(*tags: str, separator: str = ", ") -> str:
    return separator.join(tags)


def filter_products(*categories: str, min_rating: float = 3.0, max_price: float = 100) -> dict:
    return {"categories": categories, "min_rating": min_rating, "max_price": max_price}


print(search_products("wireless mouse", category="electronics", brand="Logitech"))
print(paginate(list(range(50)), page=3, page_size=10))
print(tag_product("electronics", "mouse", "wireless", separator=" | "))
print(filter_products("electronics", "books", min_rating=4.0))
