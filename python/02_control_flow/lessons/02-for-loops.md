# 🎯 For Loops
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Iterate over sequences efficiently using `for` loops with `range()`, strings, lists, and `enumerate()`.

> 💡 **TL;DR — The whole point:** `for item in sequence:` repeats code for each item; `range(n)` generates numbers 0 to n-1; `enumerate()` gives you both index and value.

## 🔗 Why This Matters
Conditionals (Lesson 01) let you make one decision. For loops let you make *thousands* of decisions — like a Squid Game tallying every player's score, or iterating through every item in your gaming inventory. Without loops, you'd have to copy-paste code for every single item.

## The Concept

A `for` loop in Python iterates over any **iterable** — a range of numbers, a string (character by character), a list, or a tuple. The variable after `for` takes each value in turn.

`range()` generates number sequences: `range(stop)` starts at 0, `range(start, stop)` sets the lower bound, `range(start, stop, step)` controls the increment. Remember: `range(n)` gives 0 through `n-1` — off-by-one is the classic beginner trap.

When you need both the index and the value, use `enumerate()`. It returns tuples of `(index, value)` — perfect for scoreboards with position numbers.

## Code Example

```python
"""Squid Game — player score tally and inventory check"""

# Tally scores for 5 players using range
print("=== Player Score Tally ===")
total_score = 0
for player_num in range(1, 6):
    score = player_num * 100  # simulated score
    total_score += score
    print(f"  Player {player_num}: {score} points")
print(f"  Total prize pool: {total_score}")

# Iterate over a list of player names
print("\n=== Current Players ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam"]
for player in players:
    print(f"  {player} is still in the game")

# Iterating a string (character by character)
print("\n=== Game Title ===")
for char in "SQUID":
    print(f"  [{char}]", end=" ")
print()

# Enumerate — index and value together
print("\n=== Leaderboard ===")
scores = [450, 320, 890, 150, 670]
for rank, player_score in enumerate(scores, start=1):
    print(f"  #{rank}: {player_score} points")
```

## 🔍 How It Works

- `for player_num in range(1, 6):` — `range(1, 6)` generates numbers 1, 2, 3, 4, 5 (6 is exclusive)
- `total_score += score` — augmented assignment: adds current score to running total
- `for player in players:` — iterates over each string in the list; `player` becomes "Gi-hun", then "Sang-woo", etc.
- `for char in "SQUID":` — strings are iterable; each character becomes the loop variable
- `for rank, player_score in enumerate(scores, start=1):` — `enumerate()` returns `(index, value)` pairs; `start=1` makes the index begin at 1 instead of 0

## ⚠️ Common Pitfall

Off-by-one errors: `range(5)` gives 0, 1, 2, 3, 4 (not 1, 2, 3, 4, 5). If you want 1-5, use `range(1, 6)`. Also, modifying a list while iterating over it causes skipped or double-processed items — make a copy first with `my_list[:]`.

## 🧠 Memory Aid

**"For each item in the collection, do something — like checking every player's ID card at the Squid Game entrance."** The `for` loop pulls each item from the sequence, hands it to you, and says "process this one."

## 🏃 Try It

Run the code file:
```bash
python code/02-02-for-loops.py
```
Then add a list of game rounds and loop through them with `for round_name in rounds:` printing a message for each.

## 🔗 Related

- [While Loops](03-while-loops.md) — when you don't know how many iterations you need
- [Loop Control](04-loop-control.md) — break, continue, and else in loops

## ➡️ Next

→ [03 — While Loops](03-while-loops.md)
