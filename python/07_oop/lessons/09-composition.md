# 🎯 Composition
<!-- ⏱️ 13 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Build "has-a" relationships by composing objects, and know when composition beats inheritance using a gaming character system.

> 💡 **TL;DR — The whole point:** Composition assembles objects from other objects. "Has-a" is often better than "is-a" because parts can be swapped at runtime.

## 🔗 Why This Matters
A game character might have a weapon, armor, and inventory. If you use inheritance, you'd need `SwordWieldingPlayer`, `BowWieldingPlayer`, etc. — an explosion of classes. Composition says "a Player has a Weapon slot."

## The Concept
**Composition** = one object contains another. **Aggregation** = one object references another (weaker). Favor composition over inheritance when the relationship is "has-a" not "is-a".

## Code Example
```python
"""Gaming: Character with composable equipment — weapon, armor, inventory."""

from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage: int
    speed: float  # attacks per second


@dataclass
class Armor:
    name: str
    defense: int
    weight: float


class Inventory:
    def __init__(self, capacity: int = 10):
        self.items: list[str] = []
        self.capacity = capacity

    def add(self, item: str) -> bool:
        if len(self.items) < capacity:
            return False
        self.items.append(item)
        return True

    def __len__(self) -> int:
        return len(self.items)


class Character:
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
        self.weapon: Weapon | None = None
        self.armor: Armor | None = None
        self.inventory = Inventory(20)  # composition — created inside

    def equip_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon  # aggregation — passed from outside

    def equip_armor(self, armor: Armor) -> None:
        self.armor = armor

    @property
    def attack_power(self) -> int:
        if not self.weapon:
            return 5  # bare hands
        return self.weapon.damage

    @property
    def defense_rating(self) -> int:
        if not self.armor:
            return 1
        return self.armor.defense

    def dps(self) -> float:
        if not self.weapon:
            return 5.0
        return self.weapon.damage * self.weapon.speed


sword = Weapon("Iron Sword", 25, 1.5)
shield = Armor("Steel Shield", 15, 8.0)

hero = Character("Lyra", 100)
hero.equip_weapon(sword)
hero.equip_armor(shield)

print(f"{hero.name}: ATK={hero.attack_power}, DEF={hero.defense_rating}")
print(f"DPS: {hero.dps():.1f}")
print(f"Inventory slots: {len(hero.inventory)}")

# Swap weapon at runtime — flexible!
hero.equip_weapon(Weapon("Legendary Blade", 60, 2.0))
print(f"After upgrade: ATK={hero.attack_power}, DPS={hero.dps():.1f}")
```

## 🔍 How It Works
- `Character` **has-a** `Weapon`, **has-a** `Armor`, **has-a** `Inventory`
- `self.inventory = Inventory(20)` is **composition** — Inventory lives and dies with Character
- `self.weapon = weapon` is **aggregation** — the Weapon object can exist independently
- Parts can be swapped at runtime: `hero.equip_weapon(new_sword)`
- Dependency injection (passing objects in) makes testing easy

## ⚠️ Common Pitfall
Deep chains: `hero.weapon.damage` violates the Law of Demeter. Add helper properties like `hero.attack_power` to hide the chain.

## 🧠 Memory Aid
"Inheritance = 'is-a' (Player *is-a* Character). Composition = 'has-a' (Character *has-a* Weapon)."

## 🏃 Try It
Create a `Mount` class (name, speed, stamina) and add it to `Character`. Add a `travel(distance)` method that reduces stamina and returns time taken.

## 🔗 Related
- [Inheritance](03-inheritance.md) — is-a vs has-a comparison
- [OOP Design](11-oop-design.md) — SOLID principles

## ➡️ Next
[Slots & New](10-slots-new.md)
