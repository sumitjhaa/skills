"""Cricket player stats — storing and swapping with variables"""

player_name = "Virat Kohli"
runs = 12076
batting_average = 59.07
is_captain = True

print(f"Player: {player_name}")
print(f"Runs: {runs}")
print(f"Average: {batting_average}")
print(f"Captain: {is_captain}")

match1, match2, match3 = 82, 45, 103
print(f"Recent scores: {match1}, {match2}, {match3}")

strike_rate_a = 89.5
strike_rate_b = 142.3
strike_rate_a, strike_rate_b = strike_rate_b, strike_rate_a
print(f"Swapped — A: {strike_rate_a}, B: {strike_rate_b}")
