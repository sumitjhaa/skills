# 🔗 Hierarchical & DBSCAN Clustering
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Agglomerative clustering, dendrograms, DBSCAN, density-based clustering.

## Agglomerative Clustering

```python
from sklearn.cluster import AgglomerativeClustering

model = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = model.fit_predict(X)
```

## Linkage Criteria

| Linkage | Behavior |
|---------|----------|
| `ward` | Minimize variance (default, works well) |
| `complete` | Maximum distance between clusters |
| `average` | Average distance between clusters |
| `single` | Minimum distance (can chain) |

## DBSCAN

```python
from sklearn.cluster import DBSCAN

model = DBSCAN(eps=0.5, min_samples=5)
labels = model.fit_predict(X)
# labels = -1 means outlier/noise
```

## DBSCAN Parameters

| Parameter | Effect |
|-----------|--------|
| `eps` | Maximum distance between neighbors |
| `min_samples` | Min points to form dense region |

<!-- 🤔 DBSCAN doesn't require you to specify K — it finds clusters by density. eps is the critical parameter. -->

## Run the Code

```bash
python code/24-clustering-advanced.py
```
