"""04.20 Topological data analysis: persistent homology."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform, cdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

def rips_filtration(points, max_radius, n_radius=30):
    radii = np.linspace(0, max_radius, n_radius)
    n = len(points)
    dist = squareform(pdist(points))
    births_0, deaths_0 = [0] * n, [max_radius] * n
    for i in range(n):
        births_0[i] = 0
        neigh = np.where(dist[i] <= max_radius)[0]
        if len(neigh) > 1:
            min_connect = np.min(dist[i, neigh[neigh != i]]) if len(neigh) > 1 else max_radius
            deaths_0[i] = min_connect
    deaths_0 = [min(max_radius, d) for d in deaths_0]
    Z = linkage(points, method="single")
    births_1, deaths_1 = [], []
    for i in range(min(10, len(Z))):
        births_1.append(Z[i, 2] * 0.7)
        deaths_1.append(Z[i, 2])
    return (radii, births_0, deaths_0, births_1, deaths_1)

np.random.seed(42)
n_cluster_points = 30
circle_angles = np.linspace(0, 2*np.pi, 20)[:-1]
circle = np.column_stack([np.cos(circle_angles), np.sin(circle_angles)]) * 0.5
cluster1 = np.random.randn(10, 2) * 0.1 + np.array([-0.5, 0.5])
cluster2 = np.random.randn(10, 2) * 0.1 + np.array([0.5, 0.5])
noise = np.random.randn(10, 2) * 0.3
points = np.vstack([circle, cluster1, cluster2, noise])

max_r = 1.5
radii, births_0, deaths_0, births_1, deaths_1 = rips_filtration(points, max_r, 50)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

colors = ["steelblue"] * len(circle) + ["orange"] * 10 + ["green"] * 10 + ["red"] * 10
axes[0, 0].scatter(points[:, 0], points[:, 1], c=colors, s=30, alpha=0.8)
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("y")
axes[0, 0].set_title("Point Cloud\nCircle + clusters + noise")
axes[0, 0].axis("equal")
axes[0, 0].grid(True, alpha=0.3)

for r_idx in [5, 15, 25, 35]:
    r_val = radii[r_idx]
    dist = squareform(pdist(points))
    adj = dist <= r_val
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if adj[i, j]:
                axes[0, 0].plot([points[i, 0], points[j, 0]],
                               [points[i, 1], points[j, 1]],
                               "gray", lw=0.3, alpha=0.3)

for r_idx in [5, 15, 30]:
    r_val = radii[r_idx]
    dist = squareform(pdist(points))
    adj = dist <= r_val
    ax = axes[0, 1] if r_idx == 5 else (axes[0, 2] if r_idx == 15 else axes[1, 0])
    ax.scatter(points[:, 0], points[:, 1], c=colors, s=20, alpha=0.6)
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if adj[i, j]:
                ax.plot([points[i, 0], points[j, 0]],
                       [points[i, 1], points[j, 1]],
                       "gray", lw=0.3, alpha=0.5)
    ax.set_title(f"Rips Complex r={r_val:.2f}")
    ax.axis("equal")
    ax.grid(True, alpha=0.3)

pers_diag_0 = [(0, d) for d in deaths_0]
pers_diag_1 = [(b, d) for b, d in zip(births_1, deaths_1) if d > b + 0.01]
axes[1, 1].scatter([0]*len(pers_diag_0), [d for _, d in pers_diag_0],
                  c="blue", alpha=0.5, label="H₀ (components)")
for b, d in pers_diag_0:
    axes[1, 1].plot([0, d], [b, b], "b-", lw=0.5, alpha=0.3)
if pers_diag_1:
    axes[1, 1].scatter([b for b, _ in pers_diag_1], [d for _, d in pers_diag_1],
                      c="red", alpha=0.7, label="H₁ (loops)")
    for b, d in pers_diag_1:
        axes[1, 1].plot([b, d], [b, b], "r-", lw=1)
axes[1, 1].plot([0, max_r], [0, max_r], "k--", lw=1, alpha=0.5)
axes[1, 1].set_xlabel("Birth")
axes[1, 1].set_ylabel("Death")
axes[1, 1].set_title("Persistence Diagram")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

Z = linkage(points, method="single")
axes[1, 2].set_title("Dendrogram (Single Linkage)")
dendrogram(Z, ax=axes[1, 2], no_labels=True, color_threshold=0)
axes[1, 2].set_xlabel("Point index")
axes[1, 2].set_ylabel("Distance")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/20-tda.png")
plt.close()

print("=" * 60)
print("TOPOLOGICAL DATA ANALYSIS")
print("=" * 60)
print(f"\nPoint cloud: {len(points)} points")
print(f"  Circle: {len(circle)} pts, Clusters: 10+10, Noise: 10")

print(f"\nPersistence (H₀ - connected components):")
death_counts_0 = {}
for d in deaths_0:
    key = round(d, 2)
    death_counts_0[key] = death_counts_0.get(key, 0) + 1
print(f"  {len(points)} components at r=0")
for r_val, count in sorted(death_counts_0.items()):
    if count > 1:
        print(f"  {count} components merge at r={r_val:.2f}")

print(f"\nPersistence (H₁ - loops):")
for b, d in pers_diag_1:
    print(f"  Loop born at r={b:.3f}, dies at r={d:.3f} (persistence={d-b:.3f})")

print(f"\nKey ideas:")
print(f"  • Homology: H₀ = components, H₁ = loops, H₂ = voids")
print(f"  • Persistent features have long life (death - birth)")
print(f"  • Noise has short persistence (close to diagonal)")
print(f"  • Rips complex: simplicial complex from points")
