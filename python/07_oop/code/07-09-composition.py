"""07-09-composition.py — Gaming: Character with composable equipment."""

from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage: int
    speed: float


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
        if len(self.items) >= self.capacity:
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
        self.inventory = Inventory(20)

    def equip_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def equip_armor(self, armor: Armor) -> None:
        self.armor = armor

    @property
    def attack_power(self) -> int:
        return self.weapon.damage if self.weapon else 5

    @property
    def defense_rating(self) -> int:
        return self.armor.defense if self.armor else 1

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

hero.equip_weapon(Weapon("Legendary Blade", 60, 2.0))
print(f"After upgrade: ATK={hero.attack_power}, DPS={hero.dps():.1f}")
