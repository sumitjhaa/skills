"""Advanced clustering — Agglomerative, DBSCAN, dendrogram concepts."""
import numpy as np
from sklearn.cluster import AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs


print("=== Advanced Clustering ===\n")

X, y = make_blobs(n_samples=500, centers=4, n_features=2,
                   cluster_std=1.2, random_state=42)
# add some noise points
rng = np.random.default_rng(42)
noise = rng.uniform(-10, 10, (50, 2))
X = np.vstack([X, noise])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Agglomerative Clustering:")
for linkage in ['ward', 'complete', 'average']:
    model = AgglomerativeClustering(n_clusters=4, linkage=linkage)
    labels = model.fit_predict(X_scaled)
    n_clusters = len(np.unique(labels))
    n_noise = np.sum(labels == -1) if -1 in labels else 0
    sil = silhouette_score(X_scaled, labels) if n_clusters > 1 and n_clusters < len(X_scaled) else -1
    print(f"  linkage={linkage:8s}: clusters={n_clusters}, noise={n_noise}, silhouette={sil:.4f}")

print(f"\nDBSCAN:")
for eps in [0.2, 0.5, 1.0]:
    model = DBSCAN(eps=eps, min_samples=5)
    labels = model.fit_predict(X_scaled)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = np.sum(labels == -1)
    print(f"  eps={eps:.1f}: clusters={n_clusters}, noise={n_noise}")

model_best = DBSCAN(eps=0.5, min_samples=5)
labels_best = model_best.fit_predict(X_scaled)
print(f"\nDBSCAN (eps=0.5):")
print(f"  Clusters: {len(set(labels_best)) - (1 if -1 in labels_best else 0)}")
print(f"  Noise points: {np.sum(labels_best == -1)}")
print(f"  Cluster sizes: {np.bincount(labels_best[labels_best >= 0])}")
