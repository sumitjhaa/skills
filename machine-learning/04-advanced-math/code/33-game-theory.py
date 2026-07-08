"""04.33 Game theory: Nash equilibrium, minimax, fictitious play."""
import numpy as np

# Zero-sum game: payoff matrix
A = np.array([[3, -1, 2],
              [-2, 1, 0],
              [1, 0, -1]])

# Solve via linear programming (simplified: dominance)
def nash_2player(A):
    """Compute mixed-strategy Nash for zero-sum via LP duality (brute force grid)."""
    n, m = A.shape
    best_val = -np.inf
    best_p = None
    for p1 in np.linspace(0, 1, 101):
        for p2 in np.linspace(0, 1, 101 - int(round(p1*100))):
            p = np.array([p1, p2, 1 - p1 - p2])
            if np.any(p < -1e-10):
                continue
            val = np.min(p @ A)
            if val > best_val:
                best_val = val
                best_p = p.copy()
    return best_p, best_val

p, v = nash_2player(A)
print(f"Zero-sum game Nash equilibrium:")
print(f"  Player 1 strategy: {np.round(p, 4)}")
print(f"  Game value: {v:.4f}")
print(f"  Check: p @ A = {np.round(p @ A, 4)}")

# Minimax theorem verification
minimax_val = np.min(np.max(A, axis=0))
maximin_val = np.max(np.min(A, axis=1))
print(f"\nMinimax: {minimax_val}")
print(f"Maximin: {maximin_val}")
print(f"Equal? {np.isclose(minimax_val, maximain_val)}")

# Fictitious play: learning in zero-sum games
def fictitious_play(A, n_rounds=10000):
    n, m = A.shape
    p_counts = np.ones(n)
    q_counts = np.ones(m)
    for t in range(n_rounds):
        p = p_counts / p_counts.sum()
        q = q_counts / q_counts.sum()
        # Best response
        br_p = np.argmin(A @ q)  # P1 minimizes since zero-sum
        br_q = np.argmax(p @ A)  # P2 maximizes
        p_counts[br_p] += 1
        q_counts[br_q] += 1
    return p_counts / p_counts.sum(), q_counts / q_counts.sum()

p_fp, q_fp = fictitious_play(A, 5000)
print(f"\nFictitious play equilibrium:")
print(f"  P1: {np.round(p_fp, 4)}")
print(f"  P2: {np.round(q_fp, 4)}")

# Prisoner's dilemma
PD = np.array([[(-1, -1), (-3, 0)],
               [(0, -3), (-2, -2)]])
print(f"\nPrisoner's dilemma payoffs:")
print(f"  (C,C): {-1}, {-1}")
print(f"  (D,D): {-2}, {-2} (dominant strategy equilibrium)")
