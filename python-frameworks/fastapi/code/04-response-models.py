"""Response models, status codes, serialization."""
from typing import Any, Optional
from datetime import datetime
import json


# ======================== Response Model ========================

class ResponseModel:
    """Simulates FastAPI response model with filtering."""
    def __init__(self, **fields):
        self._fields = fields

    @classmethod
    def from_orm(cls, obj, include: list[str] = None, exclude: list[str] = None):
        """Build response from a dict/object, filtering fields."""
        data = obj if isinstance(obj, dict) else obj.__dict__
        if include:
            data = {k: v for k, v in data.items() if k in include}
        if exclude:
            data = {k: v for k, v in data.items() if k not in exclude}
        return cls(**data)

    def dict(self) -> dict:
        return {k: v for k, v in self._fields.items() if not k.startswith("_")}


# ======================== Status Codes ========================

class status:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_429_TOO_MANY_REQUESTS = 429
    HTTP_500_INTERNAL_SERVER_ERROR = 500


# ======================== Data Store ========================

POSTS_DB = [
    {"id": 1, "title": "Hello FastAPI", "content": "Getting started", "author": "alice", "is_published": True, "views": 42},
    {"id": 2, "title": "Pydantic Deep Dive", "content": "Data validation", "author": "alice", "is_published": True, "views": 15},
    {"id": 3, "title": "Draft Post", "content": "Not ready", "author": "bob", "is_published": False, "views": 0},
]
PK = 4


# ======================== Response Helpers ========================

def api_response(data: Any = None, status_code: int = 200, message: str = "ok") -> dict:
    """Standardized API response format."""
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
    }


def paginated_response(items: list, total: int, page: int, page_size: int) -> dict:
    """Paginated response format."""
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, -(-total // page_size)),
    }


# ======================== Endpoint Responses ========================

class PostResponse(ResponseModel):
    pass


class PostDetailResponse(PostResponse):
    pass


# ======================== Demo ========================
print("=== Response Models Demo ===\n")

# --- Basic responses ---
print("1. Basic API responses:")
print(f"   Success: {json.dumps(api_response({'id': 1, 'name': 'Test'}, 201))}")
print(f"   Error:   {json.dumps(api_response(None, 404, 'Not found'))}")

# --- Response model filtering ---
print("\n2. Response model field filtering:")
post = POSTS_DB[0]
# Public response (exclude internal fields)
public = ResponseModel.from_orm(post, exclude=["views"])
print(f"   Public: {public.dict()}")

# Detail response (include specific fields)
detail = ResponseModel.from_orm(post, include=["id", "title", "content", "author"])
print(f"   Detail: {detail.dict()}")

# --- Paginated response ---
print("\n3. Paginated response:")
all_posts = POSTS_DB
result = paginated_response(
    [ResponseModel.from_orm(p).dict() for p in all_posts],
    total=len(all_posts),
    page=1,
    page_size=2,
)
print(f"   Page 1: {json.dumps(result, indent=4)}")

# --- Status code usage ---
print("\n4. Status code constants:")
codes = [
    (status.HTTP_200_OK, "OK"),
    (status.HTTP_201_CREATED, "Created"),
    (status.HTTP_204_NO_CONTENT, "No Content"),
    (status.HTTP_400_BAD_REQUEST, "Bad Request"),
    (status.HTTP_401_UNAUTHORIZED, "Unauthorized"),
    (status.HTTP_403_FORBIDDEN, "Forbidden"),
    (status.HTTP_404_NOT_FOUND, "Not Found"),
    (status.HTTP_422_UNPROCESSABLE_ENTITY, "Unprocessable"),
    (status.HTTP_429_TOO_MANY_REQUESTS, "Too Many Requests"),
    (status.HTTP_500_INTERNAL_SERVER_ERROR, "Server Error"),
]
for code, name in codes:
    print(f"   {code}: {name}")

# --- Response patterns ---
print("\n5. Response patterns:")
patterns = [
    ("List", "GET /posts/", 200, [{"id": 1}, {"id": 2}]),
    ("Create", "POST /posts/", 201, {"id": 4, "title": "New"}),
    ("Empty", "DELETE /posts/1/", 204, None),
    ("Error", "GET /posts/999/", 404, {"detail": "Not found"}),
    ("Validation", "POST /posts/", 422, {"detail": [{"loc": ["body", "title"], "msg": "field required"}]}),
]
for name, endpoint, code, data in patterns:
    print(f"   {name:12s} {endpoint:20s} → {code}: {json.dumps(data)}")
