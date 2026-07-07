"""Gaming character stats — exploring Python's core data types"""

player_name = "Aragorn"
level = 5
hit_points = 100
mana = 75.5
is_alive = True
ultimate_ability = None

print(f"{player_name}'s Stats:")
print(f"  Level: {level} ({type(level)})")
print(f"  HP: {hit_points} ({type(hit_points)})")
print(f"  Mana: {mana} ({type(mana)})")
print(f"  Alive: {is_alive} ({type(is_alive)})")
print(f"  Ultimate: {ultimate_ability} ({type(ultimate_ability)})")

print(f"\nIs level an int? {isinstance(level, int)}")
print(f"Is mana a float? {isinstance(mana, float)}")
