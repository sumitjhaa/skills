"""08-11-typing-deep-ii.py — Protocol, TypeGuard, Never, Self, ParamSpec."""

from typing import Protocol, TypeGuard, Never, Self, runtime_checkable
from collections.abc import Callable
from functools import wraps


@runtime_checkable
class Loggable(Protocol):
    def to_log(self) -> str: ...


class Order:
    def __init__(self, id: str, total: float):
        self.id = id
        self.total = total

    def to_log(self) -> str:
        return f"Order {self.id}: ${self.total:.2f}"


class User:
    def __init__(self, name: str):
        self.name = name

    def to_log(self) -> str:
        return f"User: {self.name}"


def log_activity(item: Loggable) -> None:
    print(f"[LOG] {item.to_log()}")


log_activity(Order("ORD-1", 150.0))
log_activity(User("Alice"))
print(f"Is loggable? {isinstance(Order('x', 1), Loggable)}")


class Success:
    def __init__(self, data: str):
        self.data = data


class Failure:
    def __init__(self, error: str):
        self.error = error


Result = Success | Failure


class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._where_clauses: list[str] = []
        self._limit_val: int | None = None

    def where(self, condition: str) -> Self:
        self._where_clauses.append(condition)
        return self

    def limit(self, n: int) -> Self:
        self._limit_val = n
        return self

    def build(self) -> str:
        query = f"SELECT * FROM {self._table}"
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        if self._limit_val:
            query += f" LIMIT {self._limit_val}"
        return query


query = QueryBuilder("products").where("price > 100").where("stock > 0").limit(10).build()
print(f"Query: {query}")
