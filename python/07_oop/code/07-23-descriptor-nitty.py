"""Descriptor patterns: validation, unit conversion, access logging"""
import logging

logger = logging.getLogger(__name__)

class PositiveNumber:
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._name, 0.0)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name[1:]} must be numeric, got {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"{self._name[1:]} must be positive, got {value}")
        logger.info(f"Setting {self._name[1:]} to {value}")
        setattr(obj, self._name, value)

class InventoryItem:
    quantity = PositiveNumber()
    price = PositiveNumber()

    def __init__(self, sku: str, quantity: int, price: float):
        self.sku = sku
        self.quantity = quantity
        self.price = price

item = InventoryItem("LAP-001", 10, 1499.99)
print(f"Qty: {item.quantity}, Price: ${item.price}")
try:
    item.quantity = -5
except ValueError as e:
    print(f"  Caught: {e}")
try:
    item.price = "free"
except TypeError as e:
    print(f"  Caught: {e}")
