"""04.31 Random graphs: Erdos-Renyi, giant component, percolation."""
import numpy as np

def erdos_renyi(n, p):
    """Generate Erdos-Renyi random graph G(n,p)."""
    A = np.random.rand(n, n) < p
    A = np.triu(A, 1)
    A = A + A.T
    return A

def giant_component_size(A):
    """Compute the size of the largest connected component via BFS."""
    n = A.shape[0]
    visited = np.zeros(n, dtype=bool)
    largest = 0
    for i in range(n):
        if not visited[i]:
            stack = [i]
            visited[i] = True
            size = 0
            while stack:
                v = stack.pop()
                size += 1
                for u in np.where(A[v])[0]:
                    if not visited[u]:
                        visited[u] = True
                        stack.append(u)
            largest = max(largest, size)
    return largest

np.random.seed(0)
n = 200
ps = np.linspace(0.001, 0.04, 20)
gc_sizes = []
for p in ps:
    A = erdos_renyi(n, p)
    gc = giant_component_size(A)
    gc_sizes.append(gc)
print("Giant component size vs p (n=200):")
for p, gc in zip(ps, gc_sizes):
    print(f"  p={p:.4f} (np={n*p:.2f}): GC size = {gc} / {n}")

# Degree distribution
p_fixed = 0.02
A = erdos_renyi(n, p_fixed)
degrees = A.sum(axis=1)
print(f"\nDegree distribution (n={n}, p={p_fixed}):")
print(f"  Mean degree: {degrees.mean():.2f} (expected np={n*p_fixed:.2f})")
print(f"  Var degree:  {degrees.var():.2f} (expected np(1-p)={n*p_fixed*(1-p_fixed):.2f})")

# Percolation on a 2D lattice
def bond_percolation(L, p):
    """Bond percolation on L x L grid."""
    # Horizontal bonds
    h = np.random.rand(L, L-1) < p
    # Vertical bonds
    v = np.random.rand(L-1, L) < p
    return h, v

L = 20
pc = 0.5
for p in [0.3, 0.5, 0.7]:
    h, v = bond_percolation(L, p)
    n_bonds = h.sum() + v.sum()
    total_possible = L*(L-1)*2
    print(f"Bond percolation L={L}, p={p}: {n_bonds}/{total_possible} bonds present")

# Watts-Strogatz small world
def watts_strogatz(n, k, beta):
    """Generate WS small-world graph."""
    A = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(1, k//2 + 1):
            A[i, (i+j) % n] = True
            A[(i+j) % n, i] = True
    # Rewire
    for i in range(n):
        for j in range(n):
            if A[i, j] and j > i and np.random.rand() < beta:
                A[i, j] = False
                A[j, i] = False
                new_j = np.random.randint(n)
                while new_j == i or A[i, new_j]:
                    new_j = np.random.randint(n)
                A[i, new_j] = True
                A[new_j, i] = True
    return A

ws = watts_strogatz(50, 4, 0.1)
print(f"\nWatts-Strogatz (n=50, k=4, beta=0.1):")
print(f"  Edges: {ws.sum() // 2}")
print(f"  Avg degree: {ws.sum() / 50:.2f}")
