"""Squid Game — soldier patrol and player search"""

import random

print("=== Patrol: Find Eliminated Players ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam"]
for player in players:
    eliminated = random.choice([True, False])
    if eliminated:
        print(f"  Found {player} — eliminated! Stopping patrol.")
        break
    print(f"  {player} is still alive. Continuing patrol...")
print("  Patrol complete.")

print("\n=== Prize Distribution ===")
for player in players:
    if random.choice([True, False]):
        print(f"  {player} is eliminated — skipping prize.")
        continue
    prize = random.randint(100, 500)
    print(f"  {player} gets ${prize} prize!")

print("\n=== Search for Ali ===")
searching_for = "Ali"
for player in players:
    if player == searching_for:
        print(f"  Found {searching_for}!")
        break
else:
    print(f"  {searching_for} not found — must be eliminated.")

print("\n=== Coming in Season 2 ===")
for new_game in ["Glass Bridge", "Squid Game"]:
    pass
