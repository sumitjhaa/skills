"""07-03-inheritance.py — Gaming: Character hierarchy with inheritance."""

class Character:
    def __init__(self, name: str, health: int, damage: int):
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self) -> str:
        return f"{self.name} attacks for {self.damage} damage!"

    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health <= 0:
            print(f"{self.name} has been defeated!")


class Player(Character):
    def __init__(self, name: str, health: int, damage: int, level: int = 1):
        super().__init__(name, health, damage)
        self.level = level
        self.xp = 0

    def attack(self) -> str:
        bonus = int(self.damage * (self.level * 0.1))
        return f"{self.name} strikes for {self.damage + bonus}! (lvl {self.level})"

    def gain_xp(self, amount: int) -> None:
        self.xp += amount
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            print(f"{self.name} leveled up to {self.level}!")


class Enemy(Character):
    def __init__(self, name: str, health: int, damage: int, enemy_type: str):
        super().__init__(name, health, damage)
        self.enemy_type = enemy_type

    def attack(self) -> str:
        return f"{self.enemy_type} {self.name} lunges for {self.damage}!"


hero = Player("Aragorn", 100, 15, 5)
goblin = Enemy("Snaga", 30, 8, "Goblin")

print(hero.attack())
print(goblin.attack())
goblin.take_damage(hero.damage)

print(f"MRO: {[c.__name__ for c in type(hero).__mro__]}")
print(f"Is Player a Character? {issubclass(Player, Character)}")
