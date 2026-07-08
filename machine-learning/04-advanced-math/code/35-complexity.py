"""04.35 Computational complexity: P, NP, PAC learning."""
import numpy as np
from itertools import combinations

# VC dimension of axis-aligned rectangles in 2D
def vc_rectangles():
    """Demonstrate that axis-aligned rectangles can shatter 4 points."""
    # 4 points in a diamond pattern
    points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    n = len(points)
    all_labels = 0
    shatterable = 0
    for r in range(2**n):
        labels = [(r >> i) & 1 for i in range(n)]
        # Can we separate with an axis-aligned rectangle?
        pos = points[np.array(labels) == 1]
        neg = points[np.array(labels) == 0]
        if len(pos) == 0 or len(neg) == 0:
            shatterable += 1
        else:
            x_min, y_min = pos.min(axis=0)
            x_max, y_max = pos.max(axis=0)
            if not np.any((neg[:, 0] >= x_min) & (neg[:, 0] <= x_max) &
                          (neg[:, 1] >= y_min) & (neg[:, 1] <= y_max)):
                shatterable += 1
        all_labels += 1
    print(f"VC dimension of rects in R^2: 4 (shattered {shatterable}/{all_labels} labelings)")

vc_rectangles()

# PAC sample complexity bound
def pac_sample_complexity(d, eps=0.1, delta=0.05):
    return (1/eps) * np.log(d / delta)

d = 10
eps_grid = [0.01, 0.05, 0.1, 0.2]
print(f"\nPAC sample complexity (d={d}, delta=0.05):")
for eps in eps_grid:
    m = pac_sample_complexity(d, eps, 0.05)
    print(f"  eps={eps}: m >= {m:.0f}")

# Decision tree complexity: SAT as NP-complete (simplified, checking 3-SAT)
def check_sat(formula, assignment):
    for clause in formula:
        satisfied = False
        for lit in clause:
            var, neg = abs(lit) - 1, lit < 0
            val = bool(assignment[var])
            if neg:
                val = not val
            if val:
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def brute_force_sat(formula, n_vars):
    for i in range(2**n_vars):
        assignment = [(i >> j) & 1 for j in range(n_vars)]
        if check_sat(formula, assignment):
            return assignment
    return None

formula = [(1, 2, -3), (-1, 2, 3), (1, -2, 3)]
assign = brute_force_sat(formula, 3)
print(f"\n3-SAT: formula = {formula}")
print(f"  Satisfiable? {assign is not None}, assignment = {assign}")

# NP-completeness: subset sum (brute force)
def subset_sum(arr, target):
    n = len(arr)
    for r in range(1, n+1):
        for combo in combinations(range(n), r):
            if sum(arr[i] for i in combo) == target:
                return [arr[i] for i in combo]
    return None

arr = [3, 1, 4, 1, 5, 9, 2, 6]
target = 10
ss = subset_sum(arr, target)
print(f"\nSubset sum: target={target}, solution={ss}")
