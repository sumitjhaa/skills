"""Functools: caching DB queries, partial URL builders, singledispatch API handlers."""
from functools import partial, lru_cache, singledispatch, reduce
import json


def build_url(base: str, path: str, **params: str) -> str:
    query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    return f"{base}/{path}?{query}" if query else f"{base}/{path}"


api_v1 = partial(build_url, "https://api.example.com/v1")
api_v2 = partial(build_url, "https://api.example.com/v2")
get_user = partial(api_v1, "users")

print(api_v1("users", id="123"))
print(api_v2("orders", status="active", page="1"))
print(get_user(id="42"))


@lru_cache(maxsize=32)
def get_user_by_id(user_id: int) -> dict:
    print(f"  [DB] Fetching user {user_id}...")
    return {"id": user_id, "name": f"User_{user_id}"}


print(get_user_by_id(1))
print(get_user_by_id(1))


@singledispatch
def format_response(data) -> str:
    return f"Unknown type: {type(data).__name__}"


@format_response.register(dict)
def _(data: dict) -> str:
    return json.dumps(data, indent=2)


@format_response.register(list)
def _(data: list) -> str:
    return "\n".join(f"- {item}" for item in data)


print(format_response({"user": "alice", "role": "admin"}))
print(format_response(["laptop", "mouse", "keyboard"]))

orders = [("laptop", 1200), ("mouse", 25), ("keyboard", 100)]
total = reduce(lambda acc, item: acc + item[1], orders, 0)
print(f"Total order value: ${total}")
