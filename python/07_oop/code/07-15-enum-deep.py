"""07-15-enum-deep.py — Permissions with IntFlag, HTTP methods, and more."""

from enum import Enum, IntFlag, auto, unique


class Permission(IntFlag):
    NONE = 0
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()


def check_permission(user_perm: Permission, required: Permission) -> bool:
    return (user_perm & required) == required


admin = Permission.READ | Permission.WRITE | Permission.EXECUTE | Permission.DELETE
dev = Permission.READ | Permission.WRITE
viewer = Permission.READ

print(f"Admin can delete: {check_permission(admin, Permission.DELETE)}")
print(f"Dev can execute: {check_permission(dev, Permission.EXECUTE)}")
print(f"Dev perm value: {dev.value}")

@unique
class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


StatusCode = Enum("StatusCode", ["OK", "NOT_FOUND", "ERROR"])
print(f"Functional enum: {StatusCode.OK} = {StatusCode.OK.value}")

for status in OrderStatus:
    print(f"  {status.name} = {status.value}")
