"""Hogwarts class rosters — set operations for student analysis"""

potions = {"Harry", "Ron", "Hermione", "Draco", "Neville", "Seamus"}
charms = {"Ron", "Hermione", "Luna", "Neville", "Ginny", "Harry"}
defense = {"Harry", "Hermione", "Ron", "Draco", "Luna", "Cedric"}

print("=== Class Rosters ===")
print(f"Potions ({len(potions)}): {potions}")
print(f"Charms ({len(charms)}): {charms}")
print(f"Defense ({len(defense)}): {defense}")

all_students_list = ["Harry", "Ron", "Harry", "Hermione", "Ron", "Luna"]
unique_students = set(all_students_list)
print(f"\n=== Deduplication ===")
print(f"  List with duplicates: {all_students_list}")
print(f"  Unique students: {unique_students}")

all_enrolled = potions | charms | defense
print(f"\n=== Union (all enrolled) ===")
print(f"  Total unique students: {len(all_enrolled)}")
print(f"  {sorted(all_enrolled)}")

both_potions_charms = potions & charms
print(f"\n=== Intersection (Potions ∩ Charms) ===")
print(f"  Students in both: {both_potions_charms}")

only_potions = potions - defense
print(f"\n=== Difference (Potions − Defense) ===")
print(f"  Only in Potions: {only_potions}")

exclusive = potions ^ charms
print(f"\n=== Symmetric Difference ===")
print(f"  In one class only: {exclusive}")

print("\n=== Membership ===")
print(f"  Is Harry in Defense? {'Harry' in defense}")
print(f"  Is Malfoy in Charms? {'Draco' in charms}")

print("\n=== Frozenset ===")
fs = frozenset(["Harry", "Ron", "Hermione"])
print(f"  Frozenset: {fs}")
print(f"  Hashable: {hash(fs) is not None}")
