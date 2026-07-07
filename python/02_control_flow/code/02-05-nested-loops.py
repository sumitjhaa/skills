"""Squid Game — tournament brackets and game board"""

print("=== Squid Game Tournament Bracket ===")
players = ["Gi-hun", "Sang-woo", "Ali", "Sae-byeok", "Il-nam",
           "Mi-nyeo", "Jun-ho", "Deok-su"]
round_num = 1
while len(players) > 1:
    print(f"\nRound {round_num}:")
    winners = []
    for i in range(0, len(players) - 1, 2):
        print(f"  Match: {players[i]} vs {players[i+1]}")
        winners.append(players[i])
    players = winners
    round_num += 1
print(f"\nChampion: {players[0]}")

print("\n=== Game Board (3×4 Grid) ===")
for row in range(3):
    for col in range(4):
        print(f"  [{row},{col}]", end="")
    print()

print("\n=== Score Multiplier Table ===")
for base_score in [100, 200, 300]:
    for multiplier in [1, 2, 3]:
        print(f"  {base_score} × {multiplier} = {base_score * multiplier}")
    print()
