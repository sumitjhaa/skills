# 🎯 Data Types
<!-- ⏱️ 8 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Identify Python's core data types — `int`, `float`, `str`, `bool`, and `None` — and inspect values with `type()` and `isinstance()`.

> 💡 **TL;DR — The whole point:** Every value has a type (`int`, `float`, `str`, `bool`, `None`); use `type()` to ask "what is this?" and `isinstance()` to ask "is this a specific type?"

## 🔗 Why This Matters
Variables (Lesson 02) hold values, but those values behave differently depending on their type. You can't multiply a player name by 2 and get something useful, but you can multiply runs by 2. Knowing types is how you avoid "TypeError: can't multiply sequence by non-int of type 'str'" errors.

## The Concept

Every value in Python has a type that determines what you can do with it:

- **`int`** — whole numbers like `hp = 100`, no size limit in Python
- **`float`** — decimal numbers like `mana = 75.5`, watch for floating-point imprecision (`0.1 + 0.2` might give `0.30000000000000004`)
- **`str`** — text like `player_name = "Aragorn"`, enclosed in quotes
- **`bool`** — `True` or `False` like `is_alive = True`, always capital T and F
- **`None`** — represents "no value" like `empty_inventory_slot = None`, Python's version of null

Use `type()` to ask "what type is this value?" and `isinstance()` to check "is this value an instance of this type?" — the latter is preferred in conditionals.

## Code Example

```python
"""Gaming character stats — exploring Python's core data types"""

# RPG character attributes
player_name = "Aragorn"       # str — character name
level = 5                      # int — experience level
hit_points = 100               # int — health points
mana = 75.5                    # float — magic energy
is_alive = True                # bool — living or defeated
ultimate_ability = None        # None — not yet unlocked

print(f"{player_name}'s Stats:")
print(f"  Level: {level} ({type(level)})")
print(f"  HP: {hit_points} ({type(hit_points)})")
print(f"  Mana: {mana} ({type(mana)})")
print(f"  Alive: {is_alive} ({type(is_alive)})")
print(f"  Ultimate: {ultimate_ability} ({type(ultimate_ability)})")

# Checking types with isinstance()
print(f"\nIs level an int? {isinstance(level, int)}")
print(f"Is mana a float? {isinstance(mana, float)}")
```

## 🔍 How It Works

- `player_name = "Aragorn"` — string: any text in quotes, single or double
- `level = 5` — integer: whole numbers, can be negative, arbitrarily large
- `hit_points = 100` — another integer
- `mana = 75.5` — float: decimal numbers with a decimal point
- `is_alive = True` — boolean: only `True` or `False`, case-sensitive
- `ultimate_ability = None` — NoneType: signals absence of a value
- `type(variable)` — returns the type object like `<class 'int'>`
- `isinstance(value, type)` — returns `True` or `False`; safer than `type()` for inheritance

## ⚠️ Common Pitfall

Expecting `0.1 + 0.2 == 0.3` to be `True`. It's `False` because of floating-point precision. Computers can't represent all decimals exactly in binary. Use `round()` for display or compare with a small tolerance: `abs(0.1 + 0.2 - 0.3) < 0.0001`.

Also: `None` is not the same as `0`, `""`, or `False` — it's its own type (`NoneType`) meaning "nothing here."

## 🧠 Memory Aid

**"Think of RPG character classes: int is your Warrior (tough integers), float is your Mage (slippery decimals), str is your Bard (always talking), bool is your Paladin (only two alignments), and None is the empty treasure chest."**

## 🏃 Try It

Run the code file:
```bash
python code/01-03-data-types.py
```
Then add an `inventory_items` variable set to `12` and check its type with `type()`.

## 🔗 Related

- [Type Casting](07-type-casting.md) — converting between types
- [Truthy & Falsy](08-truthy-falsy.md) — how types behave in boolean contexts

## ➡️ Next

→ [04 — Operators](04-operators.md)
