"""typing patterns: NewType, cast, Annotated, TYPE_CHECKING — production APIs"""
from typing import NewType, Annotated, cast, TYPE_CHECKING, Final, Literal
from dataclasses import dataclass

# NewType: type-safe distinct integer types (caught by mypy, int at runtime)
UserId = NewType('UserId', int)
def get_user(uid: UserId) -> dict:
    return {"id": uid, "name": f"user_{uid}"}

# Annotated: attach metadata for validation / OpenAPI schema generation (3.9+)
@dataclass
class Config:
    port: Annotated[int, "Must be 1024-65535"] = 8080
    env: Literal["dev", "staging", "production"] = "dev"

# Final: prevent reassignment (mypy catches reassignment errors)
MAX_RETRIES: Final = 3

# cast: tell mypy what you know it can't prove (use sparingly)
def process_item(item: object):
    number = cast(int, item)  # "Trust me, it's an int"
    return number * 2  # Without cast, mypy errors on object.__mul__

# TYPE_CHECKING: avoid circular imports at runtime (only import during type-check)
if TYPE_CHECKING:
    from some_module import SomeType  # Never executed at runtime

# NamedTuple with defaults (Python 3.6.1+)
from typing import NamedTuple
class Point(NamedTuple):
    x: float = 0.0
    y: float = 0.0

# Usage
uid = UserId(42)
print(f"  User: {get_user(uid)}")  # UserId is int at runtime
cfg = Config(env="production")
print(f"  Config: {cfg}")
print(f"  Processed: {process_item(5)}")
print(f"  Point: {Point(3.0, 4.0)}")
