"""Quiz game — player registration with input() and print()"""

print("=== QUIZ ARENA ===")
print("=" * 18)

player_name = input("Enter your name: ")
score = input("Enter your starting score: ")

print("\nWelcome", player_name, "!", sep="... ", end="\n\n")
print("Your journey begins with", score, "points.")

print("\nCurrent Leaderboard:")
print("Rank", "Player", "Score", sep=" | ")
print("-" * 25)
print("1st", player_name, score, sep=" | ")
print("2nd", "Bot_Alpha", "850", sep=" | ")
print("3rd", "Bot_Beta", "720", sep=" | ")

print("\nLoading", end="")
print(".", end="")
print(".", end="")
print(".", end="")
print(" Ready!")
