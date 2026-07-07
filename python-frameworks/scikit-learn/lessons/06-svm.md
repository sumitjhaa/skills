# ⚡ SVM
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Support Vector Machines, kernels, margin, C parameter.

## Linear SVM

```python
from sklearn.svm import SVC

model = SVC(kernel='linear', C=1.0, random_state=42)
model.fit(X_train, y_train)
```

## RBF Kernel

```python
model = SVC(kernel='rbf', C=1.0, gamma='scale')
```

## Key Parameters

| Parameter | Effect |
|-----------|--------|
| `C` | Lower = softer margin (better generalization) |
| `gamma` | Influence of single points (rbf/poly kernels) |
| `kernel` | linear, rbf, poly, sigmoid |

## Probability Calibration

```python
model = SVC(probability=True)  # Enables predict_proba (slower)
y_prob = model.predict_proba(X_test)
```

## Scaling Required

SVMs are sensitive to feature scales — always use `StandardScaler` first.

<!-- 🧠 SVMs work well on small-to-medium datasets. For large datasets, consider LinearSVC. -->

## Run the Code

```bash
python code/06-svm.py
```
