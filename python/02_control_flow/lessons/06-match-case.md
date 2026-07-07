# 🎯 Match/Case — Pattern Matching
<!-- ⏱️ 7 min read | 🟡 Medium | 🧠 Applied (Python 3.10+) -->

**What You'll Learn:** Use structural pattern matching (`match`/`case`) to handle multiple conditions cleanly — Python's version of a `switch` statement.

> 💡 **TL;DR — The whole point:** `match value:` checks value against multiple `case` patterns; use `_` as the default/wildcard; use `|` for OR patterns and `if` guards for extra conditions.

## 🔗 Why This Matters
Long `if`/`elif` chains (Lesson 01) work but get messy fast. Match/case is cleaner for multiple discrete values — like a Squid Game referee classifying game outcomes (win/loss/draw/penalty), handling HTTP status codes, or processing game state machine transitions.

## The Concept

`match`/`case` (Python 3.10+) compares a value against several patterns. It's like a powerful `switch` statement — but it can also unpack values and bind variables.

Key features:
- **Wildcard `_`** — matches anything, like `else` or `default`
- **OR `|`** — match multiple literals: `case 1 | 2 | 3:`
- **Guard `if`** — extra condition after a pattern: `case x if x > 10:`
- **No fall-through** — each case is independent; no `break` needed
- **Pattern matching binds variables** — if a pattern matches, variables in the pattern get assigned

## Code Example

```python
"""Squid Game — game state machine and outcome classification"""

# Game round outcomes
print("=== Squid Game Round Result ===")

def classify_outcome(outcome_code):
    match outcome_code:
        case 1:
            return "Player won the round"
        case 2:
            return "Player eliminated"
        case 3:
            return "Draw — both eliminated"
        case 4:
            return "Medical timeout"
        case _:
            return "Unknown outcome"

for code in [1, 4, 2, 99]:
    print(f"  Code {code}: {classify_outcome(code)}")

# Pattern matching with OR and guards
print("\n=== Performance Evaluation ===")

def evaluate_performance(kills, deaths, assists):
    score = kills * 10 + assists * 5 - deaths * 8
    match score:
        case _ if score > 50:
            return "Dominant performance!"
        case _ if score > 20:
            return "Solid performance"
        case _ if score > 0:
            return "Average performance"
        case _:
            return "Needs improvement"

print(f"  Score 55: {evaluate_performance(5, 0, 2)}")
print(f"  Score 25: {evaluate_performance(3, 2, 1)}")
print(f"  Score -5: {evaluate_performance(1, 4, 0)}")

# Matching tuples — unpacking patterns
print("\n=== Game State Machine ===")

def handle_command(command):
    match command:
        case ("start", level):
            return f"Starting game at level {level}"
        case ("pause",):
            return "Game paused"
        case ("resume",):
            return "Game resumed"
        case ("quit", reason):
            return f"Player quit: {reason}"
        case _:
            return "Unknown command"

print(f"  {handle_command(('start', 3))}")
print(f"  {handle_command(('pause',))}")
print(f"  {handle_command(('quit', 'too hard'))}")
```

## 🔍 How It Works

- `match outcome_code:` — the value being pattern-matched
- `case 1:` — literal pattern: matches exactly the integer 1
- `case _:` — wildcard: matches anything not caught by earlier cases
- `case _ if score > 50:` — guard pattern: `_` matches anything, then `if` adds an extra condition
- `case ("start", level):` — tuple pattern: matches a 2-element tuple where first is `"start"`; second element is bound to variable `level`
- No fall-through means each `case` is independent — no `break` needed between cases (unlike C/Java)

## ⚠️ Common Pitfall

Forgetting the wildcard `_` as default — without it, unmatched values silently do nothing (no error raised). Also, confusing `match`/`case` indent: `match` starts the block, each `case` is at the same indentation level. Guards (`if`) go on the same line as the pattern, not indented below.

## 🧠 Memory Aid

**"Match is the Squid Game referee with a rulebook: 'If the player's card matches case 1, give them the prize. Case 2, eliminate them. Case _, send them to the guard for review.'"**

## 🏃 Try It

Run the code file:
```bash
python code/02-06-match-case.py
```
Then add a case for `("save", filename)` that prints "Saving game to {filename}".

## 🔗 Related

- [Conditionals](01-conditionals.md) — the traditional way to handle multiple conditions
- [Tuples](../03_collections/lessons/06-tuples.md) — pattern matching works great with tuples

## ➡️ Next

→ [Practice Exercises](../practice/exercises.md)
