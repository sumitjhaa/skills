# Phase 03 — Practice Exercises

Solve each exercise, then check your answers in [solutions.py](solutions.py).

## Exercise 1: DNA Sequence Analysis
Given `dna = "ATCGGCTAGCTAGCATCG"`, use slicing to extract:
- First 5 bases
- Last 4 bases (as "reverse complement" — just reversed)
- Every 3rd base
- The reverse of the entire sequence (to find a palindrome)

**Hints:** Slicing with `[:5]`, `[-4:]`, `[::3]`, `[::-1]`.

---

## Exercise 2: Email Cleaner
Take the string `"  Miss.JEAN@gmAiL.COm  "` and clean it:
- Strip whitespace
- Lowercase the entire address
- Replace "gmail.com" with "hogwarts.edu"
- Check if it contains a digit

**Hints:** `.strip()`, `.lower()`, `.replace()`, `any(c.isdigit() for c in ...)`.

---

## Exercise 3: Potion Inventory
Start with `potions = ["Polyjuice", "Amortentia", "Felix Felicis", "Polyjuice", "Veritaserum"]` and perform:
- Remove the first `"Polyjuice"` with `.remove()`
- Append `"Draught of Peace"`
- Insert `"Skele-Gro"` at index 2
- Sort the list alphabetically
- Pop and print the last item

**Hints:** `.remove()`, `.append()`, `.insert()`, `.sort()`, `.pop()`.

---

## Exercise 4: List Comprehension — OWL Scores
Given `scores = [65, 82, 45, 91, 73, 58, 96, 70]`, use a list comprehension to:
- Create a new list with "Pass" for scores >= 70 and "Fail" for scores < 70

**Hints:** `"Pass" if score >= 70 else "Fail"`.

---

## Exercise 5: Spell Unpacking
Given `spells = [("Lumos", "Charm", 1), ("Expelliarmus", "Charm", 1), ("Protego", "Defense", 2)]`, unpack each tuple and print `"Spell: {name} | Category: {cat} | Level: {lvl}"`.

**Hints:** `for name, cat, lvl in spells:`.

---

## Exercise 6: House Points Merge
Given these two dicts:
```python
week1 = {"Gryffindor": 50, "Slytherin": 40, "Ravenclaw": 35}
week2 = {"Gryffindor": 30, "Hufflepuff": 45, "Ravenclaw": 20}
```
Merge them so points from both weeks are **added together** for the same house. (Gryffindor should be 80, etc.)

**Hints:** Use a dict comprehension: `{house: week1.get(house, 0) + week2.get(house, 0) for house in all_houses}`.

---

## Exercise 7: Wizarding Set Analysis
```python
quidditch = {"Harry", "Ron", "Fred", "George", "Ginny", "Draco"}
dueling = {"Harry", "Hermione", "Ron", "Draco", "Luna", "Neville"}
```
Find:
- Students in both Quidditch and Dueling Club
- Students who do Quidditch but not Dueling Club
- All unique students across both activities
- Whether `quidditch` is a superset of `dueling`

**Hints:** `&`, `-`, `|`, `.issuperset()`.

---

## Exercise 8: Tournament Nested Data
Given this nested data:
```python
tournament = {
    "name": "Triwizard Tournament",
    "year": 1994,
    "tasks": [
        {"name": "Dragons", "winner": "Harry", "points": 40},
        {"name": "Lake", "winner": "Harry", "points": 40},
        {"name": "Maze", "winner": "Harry", "points": 50},
    ],
    "champions": [
        {"name": "Harry Potter", "school": "Hogwarts", "age": 14},
        {"name": "Cedric Diggory", "school": "Hogwarts", "age": 17},
        {"name": "Fleur Delacour", "school": "Beauxbatons", "age": 17},
    ],
}
```
Write code to:
- Print the tournament name and year
- Print all task names
- Find the champion from Beauxbatons
- Calculate Harry's total points

**Hints:** Nested indexing, list comprehension, `sum()`.
