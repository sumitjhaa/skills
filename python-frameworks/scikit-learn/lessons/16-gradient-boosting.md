# 📈 Gradient Boosting
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** GradientBoostingClassifier, learning rate, early stopping.

## Training

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.8,
    random_state=42,
)
model.fit(X_train, y_train)
```

## Early Stopping

```python
model = GradientBoostingClassifier(
    n_estimators=1000,
    validation_fraction=0.2,
    n_iter_no_change=10,
    tol=1e-4,
    random_state=42,
)
model.fit(X_train, y_train)
print(f"Stopped at n_estimators: {model.n_estimators_}")
```

## Key Parameters

| Parameter | Effect |
|-----------|--------|
| `learning_rate` | Lower = better but more trees |
| `n_estimators` | Number of boosting stages |
| `max_depth` | Tree depth (usually 3-5) |
| `subsample` | Fraction of samples per tree |
| `min_samples_leaf` | Min samples per leaf |

<!-- 🤔 Use `n_iter_no_change` for early stopping instead of guessing n_estimators. -->

## Run the Code

```bash
python code/16-gradient-boosting.py
```
