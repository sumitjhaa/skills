# 🎯 Loop Control — break, continue, pass
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Control loop execution with `break` (exit), `continue` (skip), `pass` (placeholder), and `else` clauses on loops.

> 💡 **TL;DR — The whole point:** `break` exits the loop immediately; `continue` skips to the next iteration; `pass` does nothing (placeholder); `else` after a loop runs only if no `break` occurred.

## 🔗 Why This Matters
For loops (Lesson 02) and while loops (Lesson 03) run through entire sequences. But what if you find what you're looking for (Squid Game soldier checking ID badges — `break` as soon as the VIP is found)? Or you need to skip invalid players (`continue` past eliminated ones)? Loop control makes your loops smart instead of blind.

## The Concept

**`break`** — exits the **innermost** loop immediately. Execution jumps to the first line after the loop.

**`continue`** — skips the rest of the current iteration and jumps to the next one's condition check.

**`pass`** — does nothing syntactically. Used as a placeholder when you need a block but haven't written the code yet.

**`for/else` and `while/else`** — the `else` block runs only if the loop completed normally (no `break`). This is perfect for search loops: `break` when you find it, `else` if you searched everything and didn't find it.

The **flag pattern** uses a boolean variable (`found = False`) set to `True` when a condition is met — a simpler alternative to `for/else`.

## Code Example

```python
"""Squid Game — soldier patrol and player search"""

import random

# Break — find the first eliminated player
print("=== Patrol: Find Eliminated Players ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam"]
for player in players:
    eliminated = random.choice([True, False])
    if eliminated:
        print(f"  Found {player} — eliminated! Stopping patrol.")
        break
    print(f"  {player} is still alive. Continuing patrol...")
print("  Patrol complete.")

# Continue — process only active players
print("\n=== Prize Distribution ===")
for player in players:
    if random.choice([True, False]):
        print(f"  {player} is eliminated — skipping prize.")
        continue
    prize = random.randint(100, 500)
    print(f"  {player} gets ${prize} prize!")

# For/else — search for a specific player
print("\n=== Search for Ali ===")
searching_for = "Ali"
for player in players:
    if player == searching_for:
        print(f"  Found {searching_for}!")
        break
else:
    print(f"  {searching_for} not found — must be eliminated.")
# The else block runs only if no break happened

# Pass — placeholder for future code
print("\n=== Coming in Season 2 ===")
for new_game in ["Glass Bridge", "Squid Game"]:
    pass  # TODO: implement game rules
```

## 🔍 How It Works

- `break` inside `if eliminated:` — exits the `for` loop immediately when the first eliminated player is found; remaining players are never processed
- `continue` — skips the prize distribution code for eliminated players, jumps to the next player
- `for/else` — if the loop finishes all players without hitting `break`, the `else` block runs (player wasn't found)
- `pass` — a no-op statement; the loop runs but does nothing (placeholder for future implementation)
- Without `break`/`continue` control, every loop runs through every item unconditionally

## ⚠️ Common Pitfall

Using `break` when you meant `continue` (or vice versa). `break` *exits* the loop entirely; `continue` *skips one iteration* but keeps looping. Also, putting `else` at the wrong indentation level — the `else` belongs to the `for`/`while` keyword, not the `if`. And forgetting that `break` only exits the **innermost** loop (relevant for nested loops).

## 🧠 Memory Aid

**"Break = emergency exit (leave the building). Continue = skip this floor (take the stairs to the next one). Pass = empty room (the blueprint says a room goes here, but it's not built yet)."**

## 🏃 Try It

Run the code file:
```bash
python code/02-04-loop-control.py
```
Then modify the search loop to use a flag variable (`found = False`) instead of `for/else`.

## 🔗 Related

- [For Loops](02-for-loops.md) — the loops that break/continue control
- [While Loops](03-while-loops.md) — while/else works the same way

## ➡️ Next

→ [05 — Nested Loops](05-nested-loops.md)
