# 🎯 Dictionaries
<!-- ⏱️ 9 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Store and look up data by key, handle missing keys safely with `.get()`, iterate over key-value pairs, and write dict comprehensions.

> 💡 **TL;DR — The whole point:** Dictionaries map keys to values (`{"key": "value"}`); use `.get(key, default)` for safe access; iterate with `.items()`; build with `{k: v for ...}` comprehensions.

## 🔗 Why This Matters
Tuples (Lesson 06) are great for fixed sequences, but what if you need to look up a value by name? A wizard's profile — name, house, year, patronus — is a natural dictionary: look up "house" and get "Gryffindor". Dictionaries are everywhere in real code: user profiles, API responses, configuration settings, and database records.

## The Concept

A dictionary maps **keys** to **values** — like a phonebook where you look up a name (key) and get a number (value). Keys must be immutable (strings, numbers, tuples) and unique. Values can be anything.

- **Create** with `{}` or `dict()`
- **Access** with `d[key]` — but raises `KeyError` if missing
- **Safe access** with `.get(key, default)` — returns `None` or your default instead of crashing
- **View methods**: `.keys()`, `.values()`, `.items()` — dynamic views that update when the dict changes
- **Modify**: `d[key] = value`, `.update(other_dict)`, `.pop(key)`, `.setdefault(key, val)`
- **Comprehensions**: `{k: v for k, v in iterable}` builds dicts concisely

## Code Example

```python
"""Hogwarts student profiles — dictionary operations"""

# Create a student profile
harry = {
    "name": "Harry Potter",
    "house": "Gryffindor",
    "year": 3,
    "patronus": "Stag",
    "wand": "Holly, 11 inches, Phoenix Feather",
}
print("=== Student Profile ===")
print(f"  Harry: {harry}")

# Access with safe .get()
print("\n=== Safe Access ===")
print(f"  House: {harry.get('house')}")
print(f"  Grade: {harry.get('grade', 'Not assigned')}")  # default if missing
print(f"  Pet: {harry.get('pet', 'Unknown')}")

# Modify and add
print("\n=== Modifications ===")
harry["year"] = 4  # update existing
harry["pet"] = "Hedwig"  # add new key
print(f"  After updates: {harry}")

# View methods
print("\n=== Views ===")
print(f"  Keys: {list(harry.keys())}")
print(f"  Values: {list(harry.values())}")
print(f"  Items: {list(harry.items())}")

# Iteration
print("\n=== Iteration ===")
for key, value in harry.items():
    print(f"  {key}: {value}")

# Pop and update
print("\n=== Removal ===")
patronus = harry.pop("patronus")
print(f"  Popped 'patronus': {patronus}")
print(f"  After pop: {harry}")

# Dict comprehension
print("\n=== Dict Comprehension ===")
houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
points = {house: 0 for house in houses}
print(f"  House points: {points}")

# fromkeys — initialize with default values
new_students = dict.fromkeys(["Luna", "Neville", "Ginny"], "Pending")
print(f"\n  New students: {new_students}")

# Nested dict
school = {
    "Gryffindor": {"head": "McGonagall", "ghost": "Nearly Headless Nick"},
    "Slytherin": {"head": "Snape", "ghost": "Bloody Baron"},
}
print(f"\n  Gryffindor head: {school['Gryffindor']['head']}")
```

## 🔍 How It Works

- `harry = {"name": "Harry Potter", ...}` — curly braces with key:value pairs separated by commas
- `harry.get("grade", "Not assigned")` — returns `"Not assigned"` instead of raising `KeyError`; without default, returns `None`
- `harry["year"] = 4` — if key exists, updates it; if key doesn't exist, creates it
- `harry.items()` — returns a view of `(key, value)` tuples; use in `for` loops with tuple unpacking
- `.pop("patronus")` — removes the key and returns its value; raises `KeyError` if missing
- `{house: 0 for house in houses}` — dict comprehension: for each house, create a key-value pair
- `.fromkeys(["Luna", "Neville", "Ginny"], "Pending")` — creates a dict with those keys all set to `"Pending"`

## ⚠️ Common Pitfall

Using `d[key]` when the key might not exist — this crashes with `KeyError`. Always use `.get(key, default)` for uncertain access. Also, forgetting that dict keys must be **immutable**: `d[[1, 2]] = "value"` raises `TypeError` because lists are unhashable. Use tuples instead.

## 🧠 Memory Aid

**"A dictionary is like the Hogwarts book of students — you look up a name (key) and find their information (value). If the name isn't in the book, `.get()` says 'Student not found' instead of crashing the library."**

## 🏃 Try It

Run the code file:
```bash
python code/03-07-dictionaries.py
```
Then create a dictionary for `hermione` with keys for name, house, year, and pet, and print each field.

## 🔗 Related

- [Nested Data](09-nested-data.md) — dicts inside dicts, lists of dicts
- [Collections Module](10-collections-module.md) — `defaultdict` and `OrderedDict`

## ➡️ Next

→ [08 — Sets](08-sets.md)
