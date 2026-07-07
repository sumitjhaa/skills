# 📥 Parameters & Arguments
<!-- ⏱️ 12 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** How to design flexible functions using positional, keyword, `*args`, `**kwargs`, and parameter ordering rules.

> 💡 **TL;DR — The whole point:** Parameters let one function handle many different inputs — like a search engine filter that works for any category.

## 🔗 Why This Matters
Last lesson you wrote functions with fixed parameters. But real APIs need flexibility — think of Amazon's product search where you can filter by category, price range, brand, rating, and sort order.

## The Concept
Python gives you multiple ways to accept arguments:
- **Positional**: matched left-to-right (`search("laptop", "electronics")`)
- **Keyword**: named explicitly (`search(query="laptop", category="electronics")`)
- **Variable positional** (`*args`): captures extra positional args as a tuple
- **Variable keyword** (`**kwargs`): captures extra keyword args as a dict
- **Positional-only** (`/`): must be positional
- **Keyword-only** (`*`): must be named

Order: `positional-only / *args, keyword-only *, **kwargs`

## Code Example

```python
"""E-commerce product search with flexible filtering and pagination."""


def search_products(
    query: str,
    /,
    *,
    category: str = "",
    min_price: float = 0,
    max_price: float = 1_000_000,
    sort_by: str = "relevance",
    page: int = 1,
    **filters: str,
) -> dict:
    """Search products with flexible filters. query is positional-only."""
    params = {
        "query": query,
        "category": category,
        "price_range": (min_price, max_price),
        "sort": sort_by,
        "page": page,
    }
    params.update(filters)
    return params


def paginate(items: list, page: int = 1, page_size: int = 10) -> dict:
    """Split a list into pages."""
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "page": page,
        "page_size": page_size,
        "total": len(items),
        "results": items[start:end],
    }


def tag_product(*tags: str, separator: str = ", ") -> str:
    """Join product tags with a separator."""
    return separator.join(tags)


print(search_products("wireless mouse", category="electronics", brand="Logitech"))
print(paginate(list(range(50)), page=3, page_size=10))
print(tag_product("electronics", "mouse", "wireless", separator=" | "))
```

## 🔍 How It Works
- Parameters are assigned left to right
- `*args` collects extra positional args into a tuple
- `**kwargs` collects extra keyword args into a dict
- Parameters before `/` are positional-only; after `*` are keyword-only
- The mutable default trap: `def f(x=[])` shares the same list across calls — use `None` instead

## ⚠️ Common Pitfall
**Mutable default trap**: `def add_item(item, basket=[])` — the list is created once and shared. Always use `None` and create a new list inside.

## 🧠 Memory Aid
**"PASS order"**: Positional, Args, Star keyword-only, Star-star kwargs. Think of a funnel — wide at the top, narrow at the bottom.

## 🏃 Try It
Write a function `filter_products(*categories, min_rating=3.0, max_price=100)` that returns a dict with the filters applied. Call it with `filter_products("electronics", "books", min_rating=4.0)`.

## 🔗 Related
- [Defining Functions →](./01-defining-functions.md)
- [Scope & Closures →](./03-scope-closures.md)

## ➡️ Next
[Scope & Closures](./03-scope-closures.md)
