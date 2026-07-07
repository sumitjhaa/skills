"""Squid Game — player score tally and inventory check"""

print("=== Player Score Tally ===")
total_score = 0
for player_num in range(1, 6):
    score = player_num * 100
    total_score += score
    print(f"  Player {player_num}: {score} points")
print(f"  Total prize pool: {total_score}")

print("\n=== Current Players ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam"]
for player in players:
    print(f"  {player} is still in the game")

print("\n=== Game Title ===")
for char in "SQUID":
    print(f"  [{char}]", end=" ")
print()

print("\n=== Leaderboard ===")
scores = [450, 320, 890, 150, 670]
for rank, player_score in enumerate(scores, start=1):
    print(f"  #{rank}: {player_score} points")
