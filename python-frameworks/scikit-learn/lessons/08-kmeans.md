# 🔵 K-Means Clustering
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Unsupervised clustering, choosing K, cluster centroids.

## Training

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=3, random_state=42, n_init=10)
model.fit(X)
```

## Results

```python
labels = model.labels_         # Cluster assignments
centers = model.cluster_centers_  # Centroid locations
inertia = model.inertia_       # Sum of squared distances
```

## Choosing K (Elbow Method)

```python
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

# Plot: look for the "elbow" where inertia stops dropping sharply
```

## Limitations

- Assumes spherical clusters
- Sensitive to initialization
- Requires feature scaling

<!-- 🤔 Use `n_init=10` (default) to avoid bad local minima. Set `random_state` for reproducibility. -->

## Run the Code

```bash
python code/08-kmeans.py
```
