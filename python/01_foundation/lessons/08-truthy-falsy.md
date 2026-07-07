# 🎯 Truthy & Falsy
<!-- ⏱️ 7 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Determine which values Python treats as `True` or `False` in boolean contexts, and use this to write cleaner conditions.

> 💡 **TL;DR — The whole point:** Every value is truthy or falsy; the falsy values are `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `()`, and `set()` — everything else is truthy.

## 🔗 Why This Matters
Type casting (Lesson 07) showed you `bool()` converts values to boolean. But truthiness affects every `if` statement you'll ever write. Instead of `if len(items) > 0:`, you can write `if items:`. This pattern appears in virtually every Python codebase — understanding it makes you read and write code faster.

## The Concept

In Python, every value is either **truthy** (behaves like `True`) or **falsy** (behaves like `False`) when used in a boolean context (like an `if` condition or `while` loop).

The **falsy values** — the only ones that evaluate to `False`:
- `False` — the boolean itself
- `None` — Python's null/empty value
- `0`, `0.0`, `0j` — zero in any numeric type
- `""` — empty string
- `[]` — empty list
- `{}` — empty dict
- `()` — empty tuple
- `set()` — empty set

**Everything else is truthy.** This includes non-zero numbers, non-empty strings, non-empty collections, and `True` itself.

## Code Example

```python
"""Matrix construct — checking if system components exist"""

print("=== Matrix System Check ===")

# System components (some may be missing)
chosen_one = "Neo"
backup_code = ""
error_log = ["Agent Smith anomaly detected"]
null_ref = None
agent_count = 0
construct_version = 4.2

# Truthy checks — cleaner than explicit comparisons
print(f"Chosen one exists: {bool(chosen_one)}")     # True — non-empty string
print(f"Backup code exists: {bool(backup_code)}")    # False — empty string
print(f"Errors logged: {bool(error_log)}")           # True — non-empty list
print(f"Null reference: {bool(null_ref)}")           # False — None
print(f"Agent count: {bool(agent_count)}")           # False — zero
print(f"Construct version: {bool(construct_version)}")  # True — non-zero

# The idiomatic pattern: use truthiness directly
print("\n--- System Diagnosis ---")

if chosen_one:
    print("✓ Chosen one identified — system online")
else:
    print("✗ No chosen one — system idle")

if error_log:
    print(f"⚠ {len(error_log)} error(s) detected — check needed")
else:
    print("✓ No errors — systems nominal")

if null_ref:
    print("✓ Reference found")
else:
    print("✗ Null reference — check connection")

if agent_count:
    print("⚠ Agents active — defensive mode")
else:
    print("✓ No agents detected — safe")

# Combining with logical operators
if backup_code and chosen_one:
    print("\n→ Full recovery possible")
elif chosen_one or backup_code:
    print("\n→ Partial recovery — one component missing")
else:
    print("\n→ Critical failure — both missing")
```

## 🔍 How It Works

- `bool(chosen_one)` — returns `True` because `"Neo"` is a non-empty string (truthy)
- `bool(backup_code)` — returns `False` because `""` is an empty string (falsy)
- `bool(error_log)` — returns `True` because the list has items
- `bool(null_ref)` — returns `False` because `None` is always falsy
- `bool(agent_count)` — returns `False` because `0` is falsy
- `if chosen_one:` — uses truthiness directly: equivalent to `if len(chosen_one) > 0:` but cleaner
- `if error_log:` — equivalent to `if len(error_log) > 0:`
- The `and`/`or` combination shows how truthiness chains in logical operators

## ⚠️ Common Pitfall

Thinking that `[]` and `""` are "nothing" when they're actually just empty — they're still objects (`bool([])` is `False`, but `[] is not False`). Also, confusing `==` with truthiness: `if items == True` is wrong — use `if items` instead. And remember: `0` and `0.0` are falsy, but `-1` and `0.1` are truthy.

## 🧠 Memory Aid

**"Empty is false, full is true — think of it like a glass of water."** An empty glass (`""`, `[]`, `{}`) is falsy. A glass with anything in it (`"hello"`, `[1]`, `{5}`) is truthy. Zero is the absence of quantity, so it's falsy. `None` is the absence of value entirely.

## 🏃 Try It

Run the code file:
```bash
python code/01-08-truthy-falsy.py
```
Then add a `sentinels_defeated` variable (an empty list) and use an `if` check to print whether any sentinels remain.

## 🔗 Related

- [Data Types](03-data-types.md) — the types these values belong to
- [Operators](04-operators.md) — logical operators use truthiness

## ➡️ Next

You've completed Phase 01! Try the [practice exercises](../practice/exercises.md) or the [integration program](../code/integration-matrix.py).
