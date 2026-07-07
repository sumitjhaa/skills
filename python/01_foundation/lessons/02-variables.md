# 🎯 Variables & Dynamic Typing
<!-- ⏱️ 7 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Store data in variables using Python's dynamic typing and follow naming conventions.

> 💡 **TL;DR — The whole point:** Variables are named labels for values; use `=` to assign, `snake_case` for names, and remember Python figures out the type automatically.

## 🔗 Why This Matters
Now that you can print output (Lesson 01), you need a way to store and reuse data. Variables are how every program remembers things — a cricket scoreboard can't show runs if nobody tracks them. Without variables, you'd retype every value every time.

## The Concept

A variable is a named container that holds a value. In cricket, you'd track `runs = 42` — the name `runs` holds the value `42`. Python is **dynamically typed**: you don't declare the type upfront. Just assign with `=`, and Python figures it out at runtime. You can even reassign a variable to a different type later (handy but use with care).

Python convention uses `snake_case`: lowercase with underscores (`player_name`, `batting_average`). Names must start with a letter or underscore, then can contain letters, digits, or underscores. Python also supports multiple assignment (`a, b, c = 1, 2, 3`) and a clever swap trick without a temp variable.

## Code Example

```python
"""Cricket player stats — storing and swapping with variables"""

# Player stats
player_name = "Virat Kohli"
runs = 12076
batting_average = 59.07
is_captain = True

print(f"Player: {player_name}")
print(f"Runs: {runs}")
print(f"Average: {batting_average}")
print(f"Captain: {is_captain}")

# Multiple assignment — set match scores at once
match1, match2, match3 = 82, 45, 103
print(f"Recent scores: {match1}, {match2}, {match3}")

# Swapping — no temp variable needed!
strike_rate_a = 89.5
strike_rate_b = 142.3
strike_rate_a, strike_rate_b = strike_rate_b, strike_rate_a
print(f"Swapped — A: {strike_rate_a}, B: {strike_rate_b}")
```

## 🔍 How It Works

- `player_name = "Virat Kohli"` — assigns a string (text) to the variable
- `runs = 12076` — assigns an integer (whole number)
- `batting_average = 59.07` — assigns a float (decimal number)
- `is_captain = True` — assigns a boolean (True/False)
- `match1, match2, match3 = 82, 45, 103` — **tuple unpacking**: assigns each value to the matching variable in order
- `strike_rate_a, strike_rate_b = strike_rate_b, strike_rate_a` — Python evaluates the right side first (packing the old values into a tuple), then unpacks them to the left side. No temp variable needed!

## ⚠️ Common Pitfall

Using `=` when you mean `==` (comparison). `x = 5` assigns; `x == 5` checks equality. In Python, `NameError` appears if you misspell a variable name. Also, don't use Python keywords (`if`, `for`, `while`, `class`, etc.) as variable names — `if = 10` crashes.

## 🧠 Memory Aid

**"Variable on the left, value on the right — the `=` sign points the value to its name."** Think of a cricket scoreboard: the nameplate (`runs`) stays fixed, but the number underneath changes as the match progresses.

## 🏃 Try It

Run the code file:
```bash
python code/01-02-variables.py
```
Then change `runs` to your own imaginary cricket stat and add a `wickets` variable.

## 🔗 Related

- [Data Types](03-data-types.md) — what kinds of values variables can hold
- [Type Casting](07-type-casting.md) — converting between types

## ➡️ Next

→ [03 — Data Types](03-data-types.md)
