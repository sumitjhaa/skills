"""Hogwarts tournament brackets — navigating nested data structures"""

print("=== 2D List: Room Scores ===")
scoreboard = [
    ["Harry", 85, 92, 78],
    ["Ron", 72, 68, 85],
    ["Hermione", 98, 95, 99],
    ["Draco", 80, 75, 82],
]
for row in scoreboard:
    print(f"  {row[0]:10} | Scores: {row[1:]} | Total: {sum(row[1:])}")

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

print("\n=== List of Dicts: Participants ===")
participants = [
    {"name": "Harry Potter", "house": "Gryffindor", "year": 3, "score": 85},
    {"name": "Cedric Diggory", "house": "Hufflepuff", "year": 4, "score": 92},
    {"name": "Fleur Delacour", "house": "Beauxbatons", "year": 6, "score": 88},
    {"name": "Viktor Krum", "house": "Durmstrang", "year": 5, "score": 90},
]
for p in participants:
    print(f"  {p['name']:<18} | {p['house']:<12} | Score: {p['score']}")

names = [p["name"] for p in participants]
print(f"\n  All names: {names}")

winners = sorted(participants, key=lambda p: p["score"], reverse=True)
print(f"\n  Winner: {winners[0]['name']} with {winners[0]['score']} points")
