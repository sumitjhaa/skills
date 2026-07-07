"""@dataclass deep: field options, post_init, InitVar, replace — user profiles"""
from dataclasses import dataclass, field, replace
import re

@dataclass(order=True)
class User:
    sort_index: int = field(init=False, repr=False)
    user_id: str
    name: str
    email: str
    age: int = field(default=18, metadata={"min": 13, "max": 120})
    tags: list[str] = field(default_factory=list, compare=False)
    _internal_note: str = field(default="", repr=False)

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError(f"Invalid email: {self.email}")
        meta = self.__dataclass_fields__["age"].metadata
        if not (meta["min"] <= self.age <= meta["max"]):
            raise ValueError(f"Age {self.age} out of range [{meta['min']}-{meta['max']}]")
        self.sort_index = self.age

users = [
    User("u1", "Alice", "alice@example.com", 30, ["admin"]),
    User("u2", "Bob", "bob@example.com", 25, ["user"]),
    User("u3", "Charlie", "charlie@test.com", 35),
]
for u in sorted(users):
    print(f"  {u.name} ({u.age})")
alice2 = replace(users[0], age=31)
print(f"Alice updated: {alice2.age}, tags same: {alice2.tags == users[0].tags}")
