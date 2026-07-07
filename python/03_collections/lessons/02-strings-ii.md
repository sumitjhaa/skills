# 🎯 Strings II: Methods
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Transform, inspect, split, and join strings using Python's built-in string methods.

> 💡 **TL;DR — The whole point:** String methods like `.upper()`, `.split()`, `.strip()`, `.join()` transform or inspect text; they return **new** strings (strings are immutable).

## 🔗 Why This Matters
Indexing and slicing (Lesson 01) let you extract parts of strings. But real data needs *transformation* — cleaning user input (`.strip()`), parsing CSV data (`.split()`), validating emails (`.isdigit()`, `.isalpha()`), or generating reports (`.join()`, `.upper()`). String methods are the tools for every text-processing task.

## The Concept

Python strings come with a toolbox of methods — functions attached to the string that you call with dot notation.

**Case modifiers**: `.upper()`, `.lower()`, `.capitalize()`, `.title()`, `.swapcase()`

**Stripping**: `.strip()` removes whitespace from both ends; `.lstrip()` and `.rstrip()` for specific sides

**Splitting & Joining**: `.split()` breaks a string into a list; `.join()` merges a list into a string

**Searching**: `.find()` returns index or -1; `.count()` counts occurrences; `.startswith()`, `.endswith()` check boundaries

**Validation**: `.isdigit()`, `.isalpha()`, `.isalnum()`, `.isspace()`

**Replacing**: `.replace(old, new)` substitutes text; `.zfill(width)` pads with zeros

## Code Example

```python
"""Email validation and data cleaning — string methods in action"""

# Raw user input (simulated)
raw_email = "  Harry.Potter@HOGWARTS.UK  "
raw_hashtag = "#Python #HarryPotter #100DaysOfCode"
raw_numbers = "  42   "
csv_line = "Harry,Ron,Hermione,Ginny,Neville"

# Cleaning input with strip and case methods
print("=== Input Cleaning ===")
cleaned_email = raw_email.strip().lower()
print(f"  Raw: '{raw_email}'")
print(f"  Cleaned: '{cleaned_email}'")

# Validation checks
print("\n=== Validation ===")
print(f"  Contains '@': {'@' in cleaned_email}")
print(f"  Has digits: {any(c.isdigit() for c in cleaned_email)}")
print(f"  All alphabetic (local part): "
      f"{cleaned_email.split('@')[0].replace('.', '').isalpha()}")

# Split and join — hashtag parsing
print("\n=== Hashtag Parsing ===")
tags = raw_hashtag.split()
print(f"  Raw hashtags: {tags}")
clean_tags = [tag.strip("#").lower() for tag in tags]
print(f"  Clean tags: {clean_tags}")
rejoined = " | ".join(clean_tags)
print(f"  Rejoined: {rejoined}")

# CSV parsing
print("\n=== CSV Parsing ===")
wizard_list = csv_line.split(",")
print(f"  Wizards: {wizard_list}")
for i, wizard in enumerate(wizard_list, 1):
    print(f"    {i}. {wizard.strip()}")

# Replace and find
print("\n=== Search & Replace ===")
message = "You're a wizard, Harry."
print(f"  Find 'wizard': {message.find('wizard')}")  # index where it starts
print(f"  Replace: {message.replace('Harry', 'Hermione')}")

# Padding
print(f"\n  zfill example: {'7'.zfill(3)}")  # "007"
```

## 🔍 How It Works

- `raw_email.strip()` — removes leading/trailing whitespace (spaces, tabs, newlines)
- `.lower()` — converts everything to lowercase for case-insensitive comparison
- `"@".join(parts)` — the opposite of split: joins list elements with "@" between them
- `.split(",")` — breaks the CSV string into a list at each comma
- `.find('wizard')` — returns the index where "wizard" starts, or -1 if not found
- `.replace('Harry', 'Hermione')` — returns a new string with all occurrences replaced
- Methods chain: `"  Hello  ".strip().upper()` — calls `.upper()` on the result of `.strip()`

## ⚠️ Common Pitfall

Forgetting that methods return **new** strings — they don't modify the original. `text.upper()` without assigning the result does nothing visible. Also, `.find()` returns -1 (not an error) when not found, while `.index()` raises `ValueError`. And `.split()` with no arguments splits on any whitespace, but `.split(" ")` splits only on single spaces (different behavior with multiple spaces).

## 🧠 Memory Aid

**"Think of string methods as wand spells — `.upper()` is 'Wingardium Leviosa' (lifts the case), `.strip()` is 'Scourgify' (cleans the edges), `.split()` is 'Diffindo' (splits apart), `.join()` is 'Aparecium' (brings together)."**

## 🏃 Try It

Run the code file:
```bash
python code/03-02-strings-ii.py
```
Then take `"  mishchief_mAnaged!  "` and chain methods to produce `"Mischief Managed"`.

## 🔗 Related

- [Strings I: Indexing & Slicing](01-strings-i.md) — the fundamentals methods build on
- [Lists I](03-lists-i.md) — `.split()` produces a list; `.join()` consumes one

## ➡️ Next

→ [03 — Lists I: Creation, Indexing, Mutability](03-lists-i.md)
