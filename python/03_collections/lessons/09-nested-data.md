# 🎯 Nested Data
<!-- ⏱️ 9 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Work with lists of lists, dicts of dicts, lists of dicts (tabular data), and navigate nested structures safely.

> 💡 **TL;DR — The whole point:** Collections can contain other collections — `lista[outer][inner]` for 2D lists, `dict["key"]["subkey"]` for nested dicts; chain brackets to drill into nested data.

## 🔗 Why This Matters
Dictionaries (Lesson 07) and sets (Lesson 08) handle single-level data. But real-world data is layered — a JSON API response with nested objects, a tournament bracket with rounds and matches, an organization chart with departments and teams. Nested data is how you model these hierarchies.

## The Concept

Nested data is collections inside collections. Common patterns:

- **2D List (matrix)**: `[[1,2,3], [4,5,6]]` — a list of lists, like a spreadsheet
- **Nested dict**: `{"house": {"points": 500}}` — dict inside a dict, like a JSON response
- **List of dicts (tabular)**: `[{"name": "Harry"}, {"name": "Ron"}]` — like a database table

Accessing nested data means chaining square brackets: `data["students"][0]["name"]`. The key skill is knowing what each level returns. Use `.get()` for dicts and check bounds for lists. A few intermediate variables can save your sanity.

## Code Example

```python
"""Hogwarts tournament brackets — navigating nested data structures"""

# 2D List — tournament scoreboard (rooms × players)
print("=== 2D List: Room Scores ===")
scoreboard = [
    ["Harry", 85, 92, 78],   # Room 1
    ["Ron", 72, 68, 85],      # Room 2
    ["Hermione", 98, 95, 99],  # Room 3
    ["Draco", 80, 75, 82],     # Room 4
]
for row in scoreboard:
    print(f"  {row[0]:10} | Scores: {row[1:]} | Total: {sum(row[1:])}")

# Nested dict — Hogwarts house data
print("\n=== Nested Dict: House Details ===")
hogwarts = {
    "school": "Hogwarts School of Witchcraft and Wizardry",
    "headmaster": "Albus Dumbledore",
    "houses": {
        "Gryffindor": {
            "points": 482,
            "head": "Minerva McGonagall",
            "colors": ("Scarlet", "Gold"),
            "students": ["Harry", "Ron", "Hermione"],
        },
        "Slytherin": {
            "points": 472,
            "head": "Severus Snape",
            "colors": ("Green", "Silver"),
            "students": ["Draco", "Crabbe", "Goyle"],
        },
    },
}
gryffindor_head = hogwarts["houses"]["Gryffindor"]["head"]
print(f"  Gryffindor Head: {gryffindor_head}")
gryffindor_students = hogwarts["houses"]["Gryffindor"]["students"]
print(f"  Gryffindor Students: {', '.join(gryffindor_students)}")

# List of dicts — tournament participants
print("\n=== List of Dicts: Participants ===")
participants = [
    {"name": "Harry Potter", "house": "Gryffindor", "year": 3, "score": 85},
    {"name": "Cedric Diggory", "house": "Hufflepuff", "year": 4, "score": 92},
    {"name": "Fleur Delacour", "house": "Beauxbatons", "year": 6, "score": 88},
    {"name": "Viktor Krum", "house": "Durmstrang", "year": 5, "score": 90},
]
for p in participants:
    print(f"  {p['name']:<18} | {p['house']:<12} | Score: {p['score']}")

# Extract a column
names = [p["name"] for p in participants]
print(f"\n  All names: {names}")

# Sort by score
winners = sorted(participants, key=lambda p: p["score"], reverse=True)
print(f"\n  Winner: {winners[0]['name']} with {winners[0]['score']} points")
```

## 🔍 How It Works

- `scoreboard[row][col]` — first index picks the row (list), second picks the element within that row
- `hogwarts["houses"]["Gryffindor"]["head"]` — chains three key lookups: "houses" → "Gryffindor" → "head"
- `row[1:]` — slice of the row list, getting all elements from index 1 onward (skipping the name)
- `p["name"] for p in participants` — list comprehension extracting a column from tabular data
- `sorted(participants, key=lambda p: p["score"], reverse=True)` — sorts the list of dicts by the "score" key
- Access safely by breaking into steps: `house = hogwarts.get("houses", {}); gryff = house.get("Gryffindor")`

## ⚠️ Common Pitfall

Losing track of what level you're at. `data["students"][0]["name"]` — are you accessing a dict or a list at each step? Use intermediate variables or print the type at each level while debugging. Also, forgetting that `.get()` returns `None` by default for missing keys, then trying to index into `None` causes `AttributeError`.

## 🧠 Memory Aid

**"Nested data is like the Room of Requirement — each door leads to another room. `data['floor']` opens the floor door, `[2]` goes to the third room on that floor, `['name']` reads the nameplate on that door."**

## 🏃 Try It

Run the code file:
```bash
python code/03-09-nested-data.py
```
Then create a nested structure for a Quidditch match with teams, players, and scores, and print the top scorer.

## 🔗 Related

- [List Comprehensions](05-list-comprehensions.md) — extracting fields from nested data
- [Dictionaries](07-dictionaries.md) — dict methods for nested access

## ➡️ Next

→ [10 — Collections Module](10-collections-module.md)
