"""Solutions for Phase 03 practice exercises"""

from collections import defaultdict

print("=" * 50)
print("Exercise 1: DNA Sequence Analysis")
dna = "ATCGGCTAGCTAGCATCG"
print("  First 5:", dna[:5])
print("  Last 4 (reversed):", dna[-4:][::-1])
print("  Every 3rd:", dna[::3])
print("  Reversed:", dna[::-1])

print("\n" + "=" * 50)
print("Exercise 2: Email Cleaner")
raw = "  Miss.JEAN@gmAiL.COm  "
cleaned = raw.strip().lower().replace("gmail.com", "hogwarts.edu")
print(f"  Original: '{raw}'")
print(f"  Cleaned: '{cleaned}'")
print(f"  Has digit: {any(c.isdigit() for c in cleaned)}")

print("\n" + "=" * 50)
print("Exercise 3: Potion Inventory")
potions = ["Polyjuice", "Amortentia", "Felix Felicis", "Polyjuice", "Veritaserum"]
potions.remove("Polyjuice")
potions.append("Draught of Peace")
potions.insert(2, "Skele-Gro")
potions.sort()
last = potions.pop()
print(f"  Final list: {potions}")
print(f"  Popped item: {last}")

print("\n" + "=" * 50)
print("Exercise 4: List Comprehension — OWL Scores")
scores = [65, 82, 45, 91, 73, 58, 96, 70]
results = ["Pass" if s >= 70 else "Fail" for s in scores]
for i, (score, result) in enumerate(zip(scores, results), 1):
    print(f"  Student {i}: {score} → {result}")

print("\n" + "=" * 50)
print("Exercise 5: Spell Unpacking")
spells = [
    ("Lumos", "Charm", 1),
    ("Expelliarmus", "Charm", 1),
    ("Protego", "Defense", 2),
]
for name, cat, lvl in spells:
    print(f"  Spell: {name} | Category: {cat} | Level: {lvl}")

print("\n" + "=" * 50)
print("Exercise 6: House Points Merge")
week1 = {"Gryffindor": 50, "Slytherin": 40, "Ravenclaw": 35}
week2 = {"Gryffindor": 30, "Hufflepuff": 45, "Ravenclaw": 20}
all_houses = set(week1) | set(week2)
merged = {h: week1.get(h, 0) + week2.get(h, 0) for h in all_houses}
print(f"  Merged points: {merged}")

print("\n" + "=" * 50)
print("Exercise 7: Wizarding Set Analysis")
quidditch = {"Harry", "Ron", "Fred", "George", "Ginny", "Draco"}
dueling = {"Harry", "Hermione", "Ron", "Draco", "Luna", "Neville"}
print("  Both activities:", quidditch & dueling)
print("  Quidditch only:", quidditch - dueling)
print("  All students:", quidditch | dueling)
print("  Quidditch superset of Dueling?:", quidditch.issuperset(dueling))

print("\n" + "=" * 50)
print("Exercise 8: Tournament Nested Data")
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
print(f"  Tournament: {tournament['name']} ({tournament['year']})")
task_names = [t["name"] for t in tournament["tasks"]]
print(f"  Tasks: {', '.join(task_names)}")
beauxbatons = [c["name"] for c in tournament["champions"] if c["school"] == "Beauxbatons"]
print(f"  Beauxbatons champion: {beauxbatons[0]}")
harry_total = sum(t["points"] for t in tournament["tasks"] if t["winner"] == "Harry")
print(f"  Harry's total points: {harry_total}")
