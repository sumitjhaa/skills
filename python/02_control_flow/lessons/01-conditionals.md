# 🎯 Conditionals — if, elif, else
<!-- ⏱️ 8 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** Make decisions in your code using `if`, `elif`, and `else` statements, plus the ternary operator.

> 💡 **TL;DR — The whole point:** `if` checks a condition and runs code only when it's `True`; `elif` adds more checks; `else` catches everything else; the ternary (`x if cond else y`) is a one-liner.

## 🔗 Why This Matters
Variables and operators (Phase 01) let you store and calculate values, but your programs run the same way every time. Conditionals are the first step toward programs that *react* — like a Squid Game referee deciding if a player moves or gets eliminated based on their speed. Every game, every app, every website uses conditionals.

## The Concept

A conditional branches your program based on boolean expressions. The `if` statement evaluates a condition — if `True`, the indented block runs. You can chain extra checks with `elif` (short for "else if") and provide a fallback with `else`.

Python evaluates conditions top-to-bottom. The first `True` condition's block runs, then the entire chain is skipped. If no condition is `True`, the `else` block (if present) runs.

The **ternary operator** (`x if condition else y`) lets you write simple if/else in one line — useful for assigning a value based on a condition.

## Code Example

```python
"""Squid Game — Red Light, Green Light elimination"""

# Player's movement speed (meters per second) and reaction time
speed = 3.2       # m/s
reaction_ms = 450  # milliseconds

# Green Light — players move
if speed > 5.0:
    print("🏃 Sprinting! Fast player.")
elif speed > 3.0:
    print("🚶 Moving at a steady jog.")
elif speed > 1.0:
    print("🐢 Slow walk — risky!")
else:
    print("😰 Barely moving — might not cross in time.")

# Red Light — must freeze
print(f"\nRed Light! Reaction time: {reaction_ms}ms")

if reaction_ms < 200:
    print("✅ Froze instantly — safe!")
elif reaction_ms < 500:
    print("⚠️ Hesitated — almost eliminated!")
else:
    print("💀 Too slow! Eliminated.")

# Ternary — simple condition in one line
status = "Survived" if reaction_ms < 500 else "Eliminated"
print(f"\nResult: {status}")

# Nested conditionals
if speed > 2.0:
    if reaction_ms < 300:
        print("Elite player — fast and quick reflexes!")
    else:
        print("Fast but slow reactions — dangerous combo.")
```

## 🔍 How It Works

- `if speed > 5.0:` — first check: if True, prints sprinting message; entire chain skips
- `elif speed > 3.0:` — only evaluated if the `if` was False; checks next range
- `elif speed > 1.0:` — third check in the chain
- `else:` — catches everything not caught above (speed <= 1.0)
- `status = "Survived" if reaction_ms < 500 else "Eliminated"` — ternary: if condition is True, use the first value; otherwise use the second
- Nested `if` inside another `if` — the inner block only runs if the outer condition is also True

## ⚠️ Common Pitfall

Using `=` instead of `==` in conditions: `if speed = 5.0` is assignment, not comparison — Python will raise a `SyntaxError`. Also, forgetting the colon `:` at the end of the condition line — it's required. And mixing tabs and spaces for indentation — Python enforces consistent indentation (4 spaces is the standard).

## 🧠 Memory Aid

**"if is the bouncer at the club — 'If you're on the list, come in. Elif you're a VIP guest, come in. Else, sorry, you're not getting in.'"** The bouncer checks each condition in order and only lets in the first match.

## 🏃 Try It

Run the code file:
```bash
python code/02-01-conditionals.py
```
Then change the speed and reaction values to test different outcomes. Add a balance check for `>= 5.0`.

## 🔗 Related

- [Truthy & Falsy](../01_foundation/lessons/08-truthy-falsy.md) — how Python evaluates conditions
- [Match/Case](06-match-case.md) — an alternative to long if/elif chains

## ➡️ Next

→ [02 — For Loops](02-for-loops.md)
