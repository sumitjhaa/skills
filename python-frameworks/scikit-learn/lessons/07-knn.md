# 👥 KNN
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** K-Nearest Neighbors, distance metrics, choosing K.

## Training

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

## Choosing K

```python
# Small K → overfits (noisy). Large K → underfits (smooth).
# Rule of thumb: K = sqrt(n_samples)
```

## Distance Metrics

```python
model = KNeighborsClassifier(metric='euclidean')   # Default
model = KNeighborsClassifier(metric='manhattan')
model = KNeighborsClassifier(metric='cosine')
```

## Regression with KNN

```python
from sklearn.neighbors import KNeighborsRegressor
knn_reg = KNeighborsRegressor(n_neighbors=5)
```

## Scaling Required

KNN uses distance — always scale features.

<!-- 🤔 KNN is non-parametric — no training time, but prediction is O(n). Good for small datasets. -->

## Run the Code

```bash
python code/07-knn.py
```
