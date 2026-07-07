"""07-07-encapsulation.py — Gaming: Inventory with encapsulated internals."""

class Inventory:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self._items: list[dict] = []
        self.__gold = 0

    def add_item(self, name: str, quantity: int = 1) -> bool:
        if len(self._items) >= self.capacity:
            return False
        self._items.append({"name": name, "qty": quantity})
        return True

    def remove_item(self, name: str) -> bool:
        for i, item in enumerate(self._items):
            if item["name"] == name:
                self._items.pop(i)
                return True
        return False

    @property
    def gold(self) -> int:
        return self.__gold

    def add_gold(self, amount: int) -> None:
        if amount > 0:
            self.__gold += amount

    def spend_gold(self, amount: int) -> bool:
        if 0 < amount <= self.__gold:
            self.__gold -= amount
            return True
        return False

    @property
    def item_count(self) -> int:
        return len(self._items)

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.capacity


inv = Inventory(capacity=5)
inv.add_item("Health Potion", 3)
inv.add_item("Mana Potion", 2)

print(f"Items: {inv.item_count}")
print(f"Gold: {inv.gold}")
inv.add_gold(100)
inv.spend_gold(30)
print(f"Gold after spending: {inv.gold}")

try:
    print(inv.__gold)
except AttributeError:
    print("Cannot access __gold directly")
