"""Inventory management — tracking potion ingredients at Hogwarts"""

ingredients = ["Dittany", "Bezoar", "Mandrake Root", "Bezoar", "Wolfsbane"]
print(f"Starting inventory: {ingredients}")

ingredients.remove("Bezoar")
print(f"\nAfter remove('Bezoar'): {ingredients}")

last = ingredients.pop()
print(f"Popped last: '{last}' | Remaining: {ingredients}")
second = ingredients.pop(1)
print(f"Popped index 1: '{second}' | Remaining: {ingredients}")

scores = [450, 320, 890, 150, 670]
print(f"\nUnsorted scores: {scores}")
scores.sort()
print(f"Sorted ascending: {scores}")
scores.sort(reverse=True)
print(f"Sorted descending: {scores}")
scores.reverse()
print(f"After reverse: {scores}")

items = ["wand", "robe", "wand", "broom", "wand"]
print(f"\nItems: {items}")
print(f"Index of 'broom': {items.index('broom')}")
print(f"Count of 'wand': {items.count('wand')}")

print("\n=== Reference vs Copy ===")
original = [1, 2, 3, [4, 5]]
ref = original
shallow = original.copy()
original[0] = 99
original[3].append(6)
print(f"Original: {original}")
print(f"Reference (changed!): {ref}")
print(f"Shallow copy (top level safe): {shallow}")

original.clear()
print(f"\nAfter clear: {original}")
