"""04.34 Social choice: voting, Arrow's theorem, rank aggregation."""
import numpy as np
from itertools import permutations, combinations
import math

# Preference profiles
n_voters = 5
n_alternatives = 3
# Random preferences
np.random.seed(0)
preferences = np.array([np.random.permutation(n_alternatives) for _ in range(n_voters)])
print("Voter preferences (each row = ranking, lower = better):")
print(preferences)

# Borda count
def borda_count(prefs):
    n, m = prefs.shape
    scores = np.zeros(m)
    for v in range(n):
        for alt in range(m):
            scores[alt] += m - 1 - prefs[v, alt]
    return np.argsort(scores)[::-1]

borda_winner = borda_count(preferences)
print(f"\nBorda winner: {borda_winner[0]} (ranking: {borda_winner})")

# Plurality voting
def plurality(prefs):
    n, m = prefs.shape
    first_choices = prefs[:, 0]
    counts = np.bincount(first_choices, minlength=m)
    return np.argsort(counts)[::-1]

plurality_winner = plurality(preferences)
print(f"Plurality winner: {plurality_winner[0]}")

# Condorcet winner (beats all others pairwise)
def condorcet_winner(prefs):
    n, m = prefs.shape
    for i in range(m):
        is_winner = True
        for j in range(m):
            if i != j:
                beats = np.sum(prefs[:, i] < prefs[:, j])
                if beats <= n / 2:
                    is_winner = False
                    break
        if is_winner:
            return i
    return None

cw = condorcet_winner(preferences)
print(f"Condorcet winner: {cw}")

# Arrow's impossibility: find a dictator
def is_dictatorship(prefs, rule):
    """Check if the social welfare function is a dictatorship."""
    n, m = prefs.shape
    for v in range(n):
        social = rule(prefs)
        voter_pref = prefs[v]
        if np.array_equal(social, voter_pref):
            return v
    return None

# Show that majority rule can cycle (Condorcet paradox)
cyclic_prefs = np.array([[0, 1, 2], [1, 2, 0], [2, 0, 1]])
for i, j in combinations(range(3), 2):
    beats = np.sum(cyclic_prefs[:, i] < cyclic_prefs[:, j])
    print(f"  {i} beats {j}: {beats} of 3 (majority: {beats > 1})")

# Shapley value for fair division
def shapley_value(v, n):
    """Compute Shapley value for a cooperative game v: 2^N -> R."""
    sv = np.zeros(n)
    for i in range(n):
        for perm in permutations(range(n)):
            S = set()
            for j in perm:
                if j == i:
                    sv[i] += v(frozenset(S | {i})) - v(frozenset(S))
                    break
                S.add(j)
    return sv / math.factorial(n)

def example_game(S):
    if len(S) >= 2:
        return 1.0
    return 0.0

sv = shapley_value(example_game, 3)
print(f"\nShapley values for majority game: {np.round(sv, 4)}")
