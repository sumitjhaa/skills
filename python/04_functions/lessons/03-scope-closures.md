# 🔭 Scope & Closures
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** How Python resolves variable names (LEGB rule), the `global`/`nonlocal` keywords, and how closures capture state.

> 💡 **TL;DR — The whole point:** A closure is a function that remembers the variables from where it was created, even after the outer function finishes.

## 🔗 Why This Matters
Remember how game characters have persistent scores and health? Closures let you create stateful functions — counters, health bars, timers — without needing classes.

## The Concept
Python resolves names using the **LEGB** rule: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in. When you define a function inside another function, the inner function can access the outer function's variables. A **closure** is when the inner function "closes over" those variables, remembering them even after the outer function has returned.

Think of closures like a backpack the inner function carries around — it has everything it needs from its birthplace.

## Code Example

```python
"""Game state management with closures — health bars and counters."""


def create_health_bar(max_hp: int):
    """Create a health tracker with closure state."""
    current_hp = max_hp

    def take_damage(amount: int) -> int:
        nonlocal current_hp
        current_hp = max(0, current_hp - amount)
        return current_hp

    def heal(amount: int) -> int:
        nonlocal current_hp
        current_hp = min(max_hp, current_hp + amount)
        return current_hp

    def status() -> str:
        bar = "█" * current_hp + "░" * (max_hp - current_hp)
        return f"HP: [{bar}] {current_hp}/{max_hp}"

    # Return multiple closures as a namespace
    return {"damage": take_damage, "heal": heal, "status": status}


def make_counter(start: int = 0):
    """Factory that returns a counter closure."""
    count = start

    def increment(step: int = 1) -> int:
        nonlocal count
        count += step
        return count

    return increment


player = create_health_bar(100)
print(player["status"]())        # HP: [████████████████████████████████████████████████████████] 100/100
player["damage"](30)
print(player["status"]())        # HP: [██████████████████████████████████████░░░░░░░░░░░░░░░░░░░] 70/100
player["heal"](15)
print(player["status"]())        # HP: [█████████████████████████████████████████████░░░░░░░░░░░░] 85/100

score = make_counter(0)
print(score())                   # 1
print(score(5))                  # 6
```

## 🔍 How It Works
- Python resolves names: Local → Enclosing → Global → Built-in
- `global` assigns to the module scope; `nonlocal` assigns to the enclosing scope
- A **closure** bundles a function with its enclosing environment's variables — the backpack model
- Each call to the factory creates a *new* closure with its own state

## ⚠️ Common Pitfall
Forgetting `nonlocal`. If you try `count += 1` inside a nested function without `nonlocal count`, Python creates a *new local* variable instead of modifying the enclosing one.

## 🧠 Memory Aid
**"LEGB"**: Little Elephants Go Big. **Local** (innermost), **Enclosing** (outer function), **Global** (module), **Built-in** (Python's builtins).

## 🏃 Try It
Write a factory `make_player(name)` that returns a dict of closures: `get_name()`, `add_score(points)`, `get_score()`. Each player should have independent state.

## 🔗 Related
- [Parameters & Arguments →](./02-parameters.md)
- [Lambda & Higher-Order Functions →](./04-lambda-hof.md)

## ➡️ Next
[Lambda & Higher-Order Functions](./04-lambda-hof.md)
