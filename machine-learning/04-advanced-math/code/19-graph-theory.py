"""04.19 Graph theory: spectra, Laplacian, random walks."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csgraph
from scipy.spatial.distance import pdist, squareform

np.random.seed(42)

n_nodes = 20
p_edge = 0.25
adj = np.random.rand(n_nodes, n_nodes) < p_edge
adj = np.triu(adj, 1)
adj = adj + adj.T

degrees = adj.sum(axis=1)
L = np.diag(degrees) - adj

eigvals, eigvecs = np.linalg.eigh(L)

n_components = np.sum(eigvals < 1e-10)

A_norm = np.diag(1/np.sqrt(degrees + 1e-10)) @ adj @ np.diag(1/np.sqrt(degrees + 1e-10))
L_norm = np.eye(n_nodes) - A_norm

n_steps = 1000
start = 0
walk = [start]
for _ in range(n_steps):
    neighbors = np.where(adj[walk[-1]])[0]
    if len(neighbors) > 0:
        walk.append(np.random.choice(neighbors))
    else:
        walk.append(walk[-1])

walk_2 = [1]
for _ in range(n_steps):
    neighbors = np.where(adj[walk_2[-1]])[0]
    if len(neighbors) > 0:
        walk_2.append(np.random.choice(neighbors))
    else:
        walk_2.append(walk_2[-1])

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

pos = np.random.randn(n_nodes, 2) * 0.5
for i in range(n_nodes):
    for j in range(i+1, n_nodes):
        if adj[i, j]:
            axes[0, 0].plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]],
                           "b-", lw=0.5, alpha=0.5)
axes[0, 0].scatter(pos[:, 0], pos[:, 1], c=degrees, s=degrees*20, cmap="viridis", zorder=5)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")
axes[0, 0].set_title(f"Random Graph G({n_nodes}, {p_edge})\nColors = degree")
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(eigvals, "o-", lw=2)
axes[0, 1].axhline(0, color="gray", ls="--")
axes[0, 1].set_xlabel("Eigenvalue index")
axes[0, 1].set_ylabel("λ")
axes[0, 1].set_title(f"Laplacian Spectrum\n{n_components} connected components")
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(eigvecs[:, 1], eigvecs[:, 2], "o", ms=8)
for i in range(n_nodes):
    axes[0, 2].annotate(str(i), (eigvecs[i, 1], eigvecs[i, 2]), fontsize=8)
axes[0, 2].set_xlabel("Fiedler vector (v₂)")
axes[0, 2].set_ylabel("v₃")
axes[0, 2].set_title("Spectral Embedding\n(Fiedler + 3rd eigenvector)")
axes[0, 2].grid(True, alpha=0.3)
axes[0, 2].axis("equal")

visit_counts = np.zeros(n_nodes)
for node in walk:
    visit_counts[node] += 1
pi_empirical = visit_counts / visit_counts.sum()
pi_theory = degrees / degrees.sum()
axes[1, 0].bar(np.arange(n_nodes) - 0.15, pi_empirical, width=0.3, alpha=0.7,
               label="Empirical")
axes[1, 0].bar(np.arange(n_nodes) + 0.15, pi_theory, width=0.3, alpha=0.7,
               label="π ∝ deg(v)")
axes[1, 0].set_xlabel("Node")
axes[1, 0].set_ylabel("Visit probability")
axes[1, 0].set_title("Random Walk Stationary Dist.")
axes[1, 0].legend()
axes[1, 0].grid(True, axis="y", alpha=0.3)

axes[1, 1].plot(walk[:200], "b-", lw=1, label="Start=0")
axes[1, 1].plot(walk_2[:200], "r-", lw=1, label="Start=1")
axes[1, 1].set_xlabel("Step")
axes[1, 1].set_ylabel("Node")
axes[1, 1].set_title("Random Walks on Graph")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

eigval_ratio = eigvals[1] / eigvals[-1] if eigvals[-1] > 0 else 0
mixing_time_est = int(np.log(0.01) / np.log(1 - eigvals[1]/eigvals[-1] + 1e-10))
axes[1, 2].bar(["λ₂", "λₙ", "λ₂/λₙ", "Mixing τ (est)"],
               [eigvals[1], eigvals[-1], eigval_ratio, mixing_time_est / 100],
               color=["blue", "red", "purple", "orange"])
axes[1, 2].set_ylabel("Value")
axes[1, 2].set_title("Spectral Gap & Mixing")
axes[1, 2].grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/19-graph-theory.png")
plt.close()

print("=" * 60)
print("GRAPH THEORY")
print("=" * 60)
print(f"\nGraph G({n_nodes}, {p_edge}):")
print(f"  Connected components: {n_components}")
print(f"  Degrees: [{np.min(degrees)}–{np.max(degrees)}], mean={np.mean(degrees):.1f}")

print(f"\nLaplacian eigenvalues:")
print(f"  λ₁ = {eigvals[0]:.4f} (always 0)")
print(f"  λ₂ = {eigvals[1]:.4f} (Fiedler value - algebraic connectivity)")
print(f"  λₙ = {eigvals[-1]:.4f} (max eigenvalue)")
print(f"  Spectral gap = λ₂ = {eigvals[1]:.4f}")

print(f"\nRandom walk:")
print(f"  Mixing time estimate (τ₀.₀₁): ~{mixing_time_est} steps")
print(f"  Stationary distribution match (KL): {np.sum(pi_empirical * np.log(pi_empirical / (pi_theory + 1e-10) + 1e-10)):.4f}")

print(f"\nKey results:")
print(f"  • Laplacian L = D - A (positive semi-definite)")
print(f"  • Eigenvectors give spectral clustering")
print(f"  • Random walk stationary π(v) = deg(v)/2|E|")
print(f"  • Spectral gap controls mixing time")
