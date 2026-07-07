"""Hogwarts administration — collections module in action"""

from collections import defaultdict, Counter, deque, OrderedDict, ChainMap

print("=== defaultdict — Auto-group Students by House ===")
students = [
    ("Harry", "Gryffindor"), ("Ron", "Gryffindor"),
    ("Draco", "Slytherin"), ("Luna", "Ravenclaw"),
    ("Hermione", "Gryffindor"), ("Cedric", "Hufflepuff"),
]
houses = defaultdict(list)
for name, house in students:
    houses[house].append(name)
for house, members in sorted(houses.items()):
    print(f"  {house}: {', '.join(members)}")

print("\n=== Counter — Spell Frequency ===")
spells = [
    "Expelliarmus", "Lumos", "Expelliarmus", "Accio",
    "Lumos", "Expelliarmus", "Protego", "Accio", "Lumos",
]
spell_counts = Counter(spells)
print(f"  All counts: {dict(spell_counts)}")
print(f"  Top 3: {spell_counts.most_common(3)}")
print(f"  Total spells cast: {sum(spell_counts.values())}")

print("\n=== deque — Recent Spell History ===")
recent = deque(maxlen=3)
for spell in ["Accio", "Lumos", "Expelliarmus", "Protego", "Stupefy"]:
    recent.append(spell)
    print(f"  Cast {spell:15} | Recent: {list(recent)}")

print("\n=== OrderedDict — Priority Queue ===")
tasks = OrderedDict()
tasks["Find Horcruxes"] = "Critical"
tasks["Practice Occlumency"] = "High"
tasks["Brew Polyjuice"] = "Medium"
tasks["Write Potions Essay"] = "Low"
tasks.move_to_end("Write Potions Essay", last=False)
for task, priority in tasks.items():
    print(f"  [{priority:8}] {task}")

print("\n=== ChainMap — Configuration Layers ===")
defaults = {"theme": "dark", "lang": "en", "font_size": 14}
user_prefs = {"lang": "fr", "font_size": 16}
session = {"lang": "de"}
config = ChainMap(session, user_prefs, defaults)
print(f"  Theme: {config['theme']}")
print(f"  Language: {config['lang']}")
print(f"  Font size: {config['font_size']}")
