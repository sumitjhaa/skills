"""Hogwarts student profiles — dictionary operations"""

harry = {
    "name": "Harry Potter",
    "house": "Gryffindor",
    "year": 3,
    "patronus": "Stag",
    "wand": "Holly, 11 inches, Phoenix Feather",
}
print("=== Student Profile ===")
print(f"  Harry: {harry}")

print("\n=== Safe Access ===")
print(f"  House: {harry.get('house')}")
print(f"  Grade: {harry.get('grade', 'Not assigned')}")
print(f"  Pet: {harry.get('pet', 'Unknown')}")

print("\n=== Modifications ===")
harry["year"] = 4
harry["pet"] = "Hedwig"
print(f"  After updates: {harry}")

print("\n=== Views ===")
print(f"  Keys: {list(harry.keys())}")
print(f"  Values: {list(harry.values())}")
print(f"  Items: {list(harry.items())}")

print("\n=== Iteration ===")
for key, value in harry.items():
    print(f"  {key}: {value}")

print("\n=== Removal ===")
patronus = harry.pop("patronus")
print(f"  Popped 'patronus': {patronus}")
print(f"  After pop: {harry}")

print("\n=== Dict Comprehension ===")
houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
points = {house: 0 for house in houses}
print(f"  House points: {points}")

new_students = dict.fromkeys(["Luna", "Neville", "Ginny"], "Pending")
print(f"\n  New students: {new_students}")

school = {
    "Gryffindor": {"head": "McGonagall", "ghost": "Nearly Headless Nick"},
    "Slytherin": {"head": "Snape", "ghost": "Bloody Baron"},
}
print(f"\n  Gryffindor head: {school['Gryffindor']['head']}")
