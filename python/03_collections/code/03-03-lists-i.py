"""Hogwarts shopping cart — list operations for wizard supplies"""

cart = []
print(f"Empty cart: {cart}")

cart.append("Wand")
cart.append("Cauldron")
cart.append("Broomstick")
print(f"\nAfter append: {cart}")

cart.insert(1, "Robes")
print(f"After insert(1, 'Robes'): {cart}")

print(f"\nFirst item: {cart[0]}")
print(f"Last item: {cart[-1]}")
cart[0] = "Holly Wand"
print(f"After modifying first item: {cart}")

print(f"\nFirst 3 items: {cart[:3]}")
print(f"Every other item: {cart[::2]}")

more_items = ["Potion Kit", "Crystal Ball", "Dragon Hide Gloves"]
cart.extend(more_items)
print(f"\nAfter extend: {cart}")

mixed = ["Harry", 17, True, 9.75, None]
print(f"\nMixed list: {mixed}")

wizards = [["Harry", "Gryffindor"], ["Draco", "Slytherin"]]
print(f"\nNested list: {wizards}")
print(f"First wizard: {wizards[0]}")
print(f"First wizard's name: {wizards[0][0]}")
