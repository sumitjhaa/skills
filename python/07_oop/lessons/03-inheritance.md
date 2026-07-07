# 🎯 Inheritance
<!-- ⏱️ 15 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Create class hierarchies, override methods, use `super()`, and understand Python's MRO with gaming examples.

> 💡 **TL;DR — The whole point:** Inheritance lets a child class reuse and extend a parent class — write once, customize everywhere.

## 🔗 Why This Matters
Games have many entity types (Player, Enemy, NPC). Without inheritance, you'd duplicate health, damage, and movement code in every class. Inheritance is the DRY principle in action.

## The Concept
A **child class** inherits all attributes and methods from its **parent class**. You can override methods to specialize behavior and use `super()` to call the parent's version.

## Code Example
```python
"""Gaming: Character hierarchy with inheritance and super()."""

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
        bonus = self.damage * (self.level * 0.1)
        return f"{self.name} strikes for {self.damage + int(bonus)} damage! (lvl {self.level})"

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

print(f"Player MRO: {[c.__name__ for c in type(hero).__mro__]}")
print(f"Is Player a Character? {issubclass(Player, Character)}")
```

## 🔍 How It Works
- `class Player(Character):` makes Player inherit from Character
- `super().__init__(...)` calls the parent's constructor — avoids code duplication
- Override methods by redefining them with the same name
- `isinstance(obj, Class)` and `issubclass(Child, Parent)` check the hierarchy
- MRO (Method Resolution Order) determines which method is called in diamond inheritance

## ⚠️ Common Pitfall
Forgetting `super().__init__()` in the child class — the parent's initialization won't run. Always call `super().__init__()` unless you have a good reason not to.

## 🧠 Memory Aid
"Child is-a Parent. Player is-a Character. Inheritance = 'is-a' relationship."

## 🏃 Try It
Create a `Boss` class that inherits from `Enemy`. Add a `rage_mode` attribute and override `attack()` to deal double damage when health is below 30%.

## 🔗 Related
- [Polymorphism & ABCs](04-polymorphism-abc.md) — enforcing interfaces
- [Composition](09-composition.md) — has-a vs is-a

## ➡️ Next
[Polymorphism & ABCs](04-polymorphism-abc.md)
