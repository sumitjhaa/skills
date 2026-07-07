# 🎯 While Loops
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Use `while` loops to repeat code based on a condition, and avoid infinite loops.

> 💡 **TL;DR — The whole point:** `while condition:` runs as long as the condition is `True`; perfect when you don't know the iteration count in advance (like waiting for valid input).

## 🔗 Why This Matters
For loops (Lesson 02) are great when you know how many items to process. But what about a Squid Game countdown timer counting down from 60 seconds? Or a music playlist that shuffles until the user says "stop"? While loops handle the unknown — keeping the game running until someone wins.

## The Concept

A `while` loop runs as long as its condition is `True`. It's perfect when you don't know the exact number of iterations — waiting for correct input, counting down until a condition changes, or running a game loop until the player quits.

The classic pattern is `while True` with an explicit `break` inside. This makes the exit point obvious and avoids duplicating code before the loop.

**Infinite loops** happen when the condition never becomes `False`. Press Ctrl+C to interrupt a runaway loop. Always ensure something inside the loop changes the condition.

## Code Example

```python
"""Squid Game — countdown timer and game loop"""

import random

# Countdown timer (simulated)
print("=== Red Light, Green Light Countdown ===")
countdown = 5
while countdown > 0:
    print(f"  {countdown}...")
    countdown -= 1  # critical — changes the condition
print("  GO!")

# Input validation — keep asking until correct
print("\n=== Guard Password Check ===")
password = ""
while password != "456":
    password = input("Enter the VIP code: ")
print("  Access granted.")

# Game loop — play until player quits or loses
print("\n=== Marble Game ===")
marbles = 10
while marbles > 0:
    print(f"\n  You have {marbles} marbles.")
    bet = int(input("  Place your bet (1-3 marbles): "))
    if bet > marbles:
        print("  You don't have that many!")
        continue
    if random.choice([True, False]):
        marbles += bet
        print(f"  You won {bet} marbles!")
    else:
        marbles -= bet
        print(f"  You lost {bet} marbles.")

print("\n  Game over! You're out of marbles.")
```

## 🔍 How It Works

- `while countdown > 0:` — checks before each iteration; runs body only when `countdown > 0` is True
- `countdown -= 1` — **crucial**: without this, the condition never changes → infinite loop
- `while password != "456":` — keeps asking until the user enters the exact string "456"
- `while marbles > 0:` — game loop: each iteration the player bets marbles
- `continue` — skips the rest of this iteration (the bet resolution) and jumps back to the condition check
- `marbles -= bet` — modifies the loop condition variable; eventually `marbles` reaches 0 and the loop exits
- `while True:` pattern — alternative to setting a condition: loop forever until `break`

## ⚠️ Common Pitfall

Forgetting to update the condition variable inside the loop → **infinite loop**. If `countdown` never decreases, `countdown > 0` stays True forever. Always ask: "What changes inside this loop that will eventually make the condition False?" Also, using `==` in the condition when you mean `!=` — `while marbles == 0` instead of `while marbles > 0` — won't run at all.

## 🧠 Memory Aid

**"'While the light is green, keep running.'** The Squid Game doll checks the condition (green light = True), players keep moving. When the light turns red (condition = False), everyone freezes (loop stops)."

## 🏃 Try It

Run the code file:
```bash
python code/02-03-while-loops.py
```
Then modify the marble game so the player starts with 20 marbles and the game ends when they reach 0 or have 30+ marbles (win condition).

## 🔗 Related

- [For Loops](02-for-loops.md) — for vs while: when to use which
- [Loop Control](04-loop-control.md) — break, continue for finer control

## ➡️ Next

→ [04 — Loop Control](04-loop-control.md)
