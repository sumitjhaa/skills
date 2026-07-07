"""Pagination, filtering, ordering in DRF."""
from typing import Any, Optional
import json


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", query_params=None, user=None):
        self.method = method
        self.query_params = query_params or {}
        self.user = user or type("Anon", (), {"is_authenticated": False})()


class Response:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    def render(self):
        return json.dumps(self.data, indent=2)


class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True


# ======================== Pagination ========================

class PageNumberPagination:
    """Simulates DRF's PageNumberPagination."""
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"

    def paginate(self, queryset: list, request: Request) -> dict:
        page = int(request.query_params.get(self.page_query_param, 1))
        page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))

        total = len(queryset)
        total_pages = max(1, -(-total // page_size))  # ceil division
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]

        return {
            "count": total,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "next": page + 1 if page < total_pages else None,
            "previous": page - 1 if page > 1 else None,
            "results": results,
        }


class LimitOffsetPagination:
    """Simulates DRF's LimitOffsetPagination."""
    default_limit = 3
    limit_query_param = "limit"
    offset_query_param = "offset"

    def paginate(self, queryset: list, request: Request) -> dict:
        limit = int(request.query_params.get(self.limit_query_param, self.default_limit))
        offset = int(request.query_params.get(self.offset_query_param, 0))

        total = len(queryset)
        results = queryset[offset:offset + limit]

        return {
            "count": total,
            "limit": limit,
            "offset": offset,
            "next": offset + limit if offset + limit < total else None,
            "previous": offset - limit if offset >= limit else None,
            "results": results,
        }


# ======================== Filtering & Ordering ========================

class SearchFilter:
    """Simulates DRF's SearchFilter (icontains across search_fields)."""
    search_param = "search"

    def filter(self, queryset: list, request: Request, search_fields: list[str] = None) -> list:
        search_value = request.query_params.get(self.search_param, "").strip().lower()
        if not search_value or not search_fields:
            return queryset
        results = []
        for item in queryset:
            for field in search_fields:
                val = str(item.get(field, "")).lower()
                if search_value in val:
                    results.append(item)
                    break
        return results


class OrderingFilter:
    """Simulates DRF's OrderingFilter."""
    ordering_param = "ordering"

    def filter(self, queryset: list, request: Request, ordering_fields: list[str] = None) -> list:
        ordering = request.query_params.get(self.ordering_param, "")
        if not ordering or not ordering_fields:
            return queryset
        desc = ordering.startswith("-")
        field = ordering[1:] if desc else ordering
        if field not in ordering_fields:
            return queryset
        return sorted(queryset, key=lambda x: x.get(field, ""), reverse=desc)


# ======================== Data ========================
POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "created": "2024-01-15"},
    {"id": 2, "title": "Django Models", "author": "bob", "likes": 5, "created": "2024-03-20"},
    {"id": 3, "title": "Advanced ORM", "author": "alice", "likes": 8, "created": "2024-06-10"},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "created": "2024-02-01"},
    {"id": 5, "title": "DRF Guide", "author": "dave", "likes": 15, "created": "2024-04-05"},
    {"id": 6, "title": "Testing Django", "author": "alice", "likes": 7, "created": "2024-05-12"},
    {"id": 7, "title": "Django Forms", "author": "bob", "likes": 9, "created": "2024-07-01"},
    {"id": 8, "title": "Docker for Django", "author": "dave", "likes": 11, "created": "2024-04-20"},
    {"id": 9, "title": "REST APIs", "author": "charlie", "likes": 6, "created": "2024-08-15"},
    {"id": 10, "title": "Django Security", "author": "alice", "likes": 14, "created": "2024-09-01"},
]


# ======================== API View with Pagination ========================

class PaginatedListView:
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["likes", "created", "title"]

    def __init__(self, queryset):
        self.queryset = queryset

    def get(self, request: Request) -> dict:
        queryset = list(self.queryset)
        for backend in self.filter_backends:
            inst = backend()
            if isinstance(inst, SearchFilter):
                queryset = inst.filter(queryset, request, self.search_fields)
            elif isinstance(inst, OrderingFilter):
                queryset = inst.filter(queryset, request, self.ordering_fields)
        paginator = self.pagination_class()
        return paginator.paginate(queryset, request)


# ======================== Demo ========================
print("=== Pagination, Filtering & Ordering Demo ===\n")

view = PaginatedListView(POSTS)

# Basic pagination
req = Request("GET", query_params={"page": 1, "page_size": 3})
result = view.get(req)
print(f"Page 1: {len(result['results'])} items of {result['count']} total")
print(f"  Next: {result['next']}")

req2 = Request("GET", query_params={"page": 2, "page_size": 3})
result2 = view.get(req2)
print(f"Page 2: {len(result2['results'])} items")
print(f"  Titles: {[p['title'] for p in result2['results']]}")

# LimitOffset
view.pagination_class = LimitOffsetPagination
req3 = Request("GET", query_params={"limit": 4, "offset": 2})
result3 = view.get(req3)
print(f"\nLimitOffset (limit=4, offset=2): {len(result3['results'])} items")
print(f"  First: {result3['results'][0]['title']}")

# Search
view.pagination_class = PageNumberPagination
req4 = Request("GET", query_params={"search": "django"})
result4 = view.get(req4)
print(f"\nSearch 'django': {result4['count']} results")
print(f"  {[p['title'] for p in result4['results']]}")

# Ordering
req5 = Request("GET", query_params={"ordering": "-likes", "page_size": 5})
result5 = view.get(req5)
print(f"\nOrder by -likes (top 5):")
for p in result5["results"]:
    print(f"  ❤ {p['likes']:2d}  {p['title']}")

# Combined: search + ordering
req6 = Request("GET", query_params={"search": "django", "ordering": "-likes"})
result6 = view.get(req6)
print(f"\nSearch 'django' + order by -likes: {result6['count']} results")
for p in result6["results"]:
    print(f"  ❤ {p['likes']:2d}  {p['title']}")
