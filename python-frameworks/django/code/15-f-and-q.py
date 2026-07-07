"""F expressions & Q expressions for complex queries."""
from dataclasses import dataclass, field
from typing import Any, Optional


class F:
    """Reference a model field for updates and comparisons."""
    def __init__(self, name: str):
        self.name = name

    def __add__(self, other):
        return FExpr(self, "+", other)

    def __radd__(self, other):
        return FExpr(other, "+", self)

    def __sub__(self, other):
        return FExpr(self, "-", other)

    def __gt__(self, other):
        return FCondition(self, ">", other)

    def __lt__(self, other):
        return FCondition(self, "<", other)


class FExpr:
    """Expression like F('likes') + 1."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self, row: dict) -> int:
        lval = row.get(self.left.name, 0) if isinstance(self.left, F) else self.left
        rval = row.get(self.right.name, 0) if isinstance(self.right, F) else self.right
        if self.op == "+":
            return lval + rval
        if self.op == "-":
            return lval - rval
        return rval


class FCondition:
    """Condition like F('likes') > 10."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def eval(self, row: dict) -> bool:
        lval = row.get(self.left.name) if isinstance(self.left, F) else self.left
        rval = self.right
        if self.op == ">":
            return lval is not None and lval > rval
        if self.op == "<":
            return lval is not None and lval < rval
        return False


class Q:
    """Encapsulate query conditions with AND/OR/NOT."""
    def __init__(self, **conditions):
        self.conditions = conditions
        self.connector = "AND"
        self.children: list["Q"] = []
        self.negated = False

    @staticmethod
    def _or(*children: "Q") -> "Q":
        q = Q()
        q.connector = "OR"
        q.children = list(children)
        return q

    @staticmethod
    def _and(*children: "Q") -> "Q":
        q = Q()
        q.connector = "AND"
        q.children = list(children)
        return q

    @staticmethod
    def _not(child: "Q") -> "Q":
        q = Q()
        q.negated = True
        q.children = [child]
        return q

    def _eval(self, item: dict) -> bool:
        if self.children:
            results = [c._eval(item) for c in self.children]
            r = all(results) if self.connector == "AND" else any(results)
            return not r if self.negated else r
        results = []
        for key, value in self.conditions.items():
            actual = item.get(key)
            if isinstance(value, F):
                results.append(actual == item.get(value.name))
            elif isinstance(value, (list, tuple)):
                results.append(actual in value)
            else:
                results.append(actual == value)
        return all(results)


class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = list(results) if results is not None else list(table)

    def filter(self, *args, **kwargs) -> "QuerySet":
        results = list(self._results)
        if args and isinstance(args[0], Q):
            q = args[0]
            results = [r for r in results if q._eval(r)]
        if kwargs:
            for key, value in kwargs.items():
                if isinstance(value, F):
                    results = [r for r in results if r.get(key) == r.get(value.name)]
                elif isinstance(value, (list, tuple)):
                    results = [r for r in results if r.get(key) in value]
                elif isinstance(value, FCondition):
                    results = [r for r in results if value.eval(r)]
                else:
                    results = [r for r in results if r.get(key) == value]
        return QuerySet(self.table, results)

    def update(self, **kwargs) -> int:
        count = 0
        for r in self._results:
            for key, value in kwargs.items():
                if isinstance(value, F):
                    r[key] = r.get(value.name, 0)
                elif isinstance(value, FExpr):
                    r[key] = value.eval(r)
                else:
                    r[key] = value
            count += 1
        return count

    def count(self) -> int:
        return len(self._results)


POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "draft": False},
    {"id": 2, "title": "Django Models", "author": "bob", "likes": 5, "draft": False},
    {"id": 3, "title": "Advanced ORM", "author": "alice", "likes": 8, "draft": True},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "draft": False},
    {"id": 5, "title": "Django REST", "author": "dave", "likes": 15, "draft": False},
    {"id": 6, "title": "Testing Django", "author": "alice", "likes": 7, "draft": True},
]

qs = QuerySet(POSTS)

print("--- Q expressions ---")
q_or = Q._or(Q(author="alice"), Q(author="bob"))
or_result = qs.filter(q_or)
print(f"OR(author='alice', author='bob'): {or_result.count()} posts")

q_and = Q._and(Q(author="alice"), Q(draft=True))
and_result = qs.filter(q_and)
print(f"AND(author='alice', draft=True): {and_result.count()} posts")

q_not = Q._not(Q(author="alice"))
not_result = qs.filter(q_not)
print(f"NOT(author='alice'): {not_result.count()} posts")

q_complex = Q._or(
    Q._and(Q(author="alice"), Q(draft=False)),
    Q(likes__gt=10),
)
complex_result = qs.filter(q_complex)
print(f"Complex: {complex_result.count()} posts")

print("\n--- F expressions ---")
print("Before update:", [p["likes"] for p in POSTS[:3]])
updated = qs.filter(draft=False).update(likes=F("likes") + 1)
print(f"Updated {updated} posts (likes += 1)")
print("After update: ", [p["likes"] for p in POSTS[:3]])

print("\n--- filter with F ---")
matched = qs.filter(likes=F("id"))
print(f"likes == id: {[p['title'] for p in matched._results]}")

print("\n--- filter with list ---")
in_list = qs.filter(author=["alice", "charlie"])
print(f"author in [alice, charlie]: {in_list.count()} posts")
