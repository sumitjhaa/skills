"""Marauder's Map — coordinates, RGB colors, and named tuples"""

from collections import namedtuple

crimson = (220, 20, 60)
gold = (255, 215, 0)
print(f"Crimson RGB: {crimson}")
print(f"Gold RGB: {gold}")

hogwarts_castle = (51.527, -0.130)
print(f"\nHogwarts coordinates: {hogwarts_castle}")

single = (1,)
print(f"\nSingle-element tuple: {single}")

print("\n=== Unpacking ===")
r, g, b = crimson
print(f"Red: {r}, Green: {g}, Blue: {b}")

lat, _ = hogwarts_castle
print(f"Latitude only: {lat}")

a, b = 1, 2
a, b = b, a
print(f"\nSwapped: a={a}, b={b}")

print("\n=== Tuples as Dict Keys ===")
locations = {
    (51.527, -0.130): "Hogwarts Castle",
    (51.501, -0.142): "Buckingham Palace",
}
for coords, place in locations.items():
    print(f"  {place}: {coords}")

print("\n=== Named Tuples ===")
Wizard = namedtuple("Wizard", ["name", "house", "year"])
harry = Wizard("Harry Potter", "Gryffindor", 3)
print(f"Named tuple: {harry}")
print(f"Name: {harry.name}")
print(f"House: {harry.house}")
print(f"As regular tuple: {tuple(harry)}")
