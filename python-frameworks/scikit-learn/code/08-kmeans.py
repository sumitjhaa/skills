"""K-Means clustering — elbow method, cluster centers, labels."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs


print("=== K-Means Clustering ===\n")

X, y_true = make_blobs(n_samples=500, centers=4, n_features=2,
                        cluster_std=1.5, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Elbow method (inertia vs K):")
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    print(f"  k={k}: inertia={km.inertia_:.2f}")

print(f"\nBest model (k=4):")
km = KMeans(n_clusters=4, random_state=42, n_init=10)
km.fit(X_scaled)
labels = km.labels_
centers = scaler.inverse_transform(km.cluster_centers_)

print(f"Cluster labels (first 20): {labels[:20]}")
print(f"Cluster counts: {np.bincount(labels)}")
print(f"\nCenters (original scale):\n{centers}")

print(f"\nInertia: {km.inertia_:.2f}")
print(f"Silhouette score (if larger = better):")

from sklearn.metrics import silhouette_score
sil = silhouette_score(X_scaled, labels)
print(f"  K=4: {sil:.4f}")

for k in [2, 3, 5]:
    km_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_temp = km_temp.fit_predict(X_scaled)
    sil_temp = silhouette_score(X_scaled, labels_temp)
    print(f"  K={k}: {sil_temp:.4f}")
