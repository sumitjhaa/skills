# 📉 PCA
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Dimensionality reduction, explained variance, visualization.

## Training

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
```

## Explained Variance

```python
pca.explained_variance_ratio_   # Variance per component
pca.explained_variance_ratio_.cumsum()  # Cumulative
```

## Choosing Components

```python
pca = PCA(n_components=0.95)  # Keep 95% of variance
X_reduced = pca.fit_transform(X)
```

## Visualization

```python
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis')
plt.xlabel('PC1')
plt.ylabel('PC2')
```

## Components

```python
# Each component is a linear combination of original features
components = pca.components_
```

<!-- 🤔 PCA is unsupervised — use it before classification to reduce noise and speed up training. -->

## Run the Code

```bash
python code/09-pca.py
```
