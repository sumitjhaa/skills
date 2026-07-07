"""Enum patterns: Flag, StrEnum, auto — HTTP status, permissions, orders"""
from enum import Enum, Flag, auto

class Permission(Flag):
    NONE = 0
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    ALL = READ | WRITE | EXECUTE

class HTTPStatus(Enum):
    OK = (200, "Success")
    CREATED = (201, "Created")
    BAD_REQUEST = (400, "Bad request")
    NOT_FOUND = (404, "Not found")
    SERVER_ERROR = (500, "Server error")

    def __new__(cls, code: int, message: str):
        obj = object.__new__(cls)
        obj.code = code
        obj.message = message
        return obj

    @property
    def is_success(self):
        return 200 <= self.code < 300

p = Permission.READ | Permission.WRITE
print(f"Can execute: {bool(p & Permission.EXECUTE)}")
print(f"Has read: {bool(p & Permission.READ)}")

status = HTTPStatus.OK
print(f"{status.name}: {status.code} {status.message}, success={status.is_success}")
status404 = HTTPStatus.NOT_FOUND
print(f"{status404.name}: {status404.code} {status404.message}, success={status404.is_success}")
