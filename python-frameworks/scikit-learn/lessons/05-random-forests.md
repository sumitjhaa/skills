# 🌲 Random Forests
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Ensemble of trees, bagging, out-of-bag score.

## Training

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)
```

## Key Parameters

| Parameter | Effect |
|-----------|--------|
| `n_estimators` | Number of trees (more = better, diminishing returns) |
| `max_depth` | Tree depth |
| `min_samples_leaf` | Min samples per leaf |
| `max_features` | Features per split (sqrt for classification) |
| `bootstrap` | Whether to use bootstrap samples |

## Out-of-Bag Score

```python
model = RandomForestClassifier(oob_score=True, random_state=42)
model.fit(X_train, y_train)
print(model.oob_score_)  # Unbiased estimate without CV
```

## Feature Importance

```python
importances = pd.Series(model.feature_importances_, index=feature_names)
importances.sort_values(ascending=False).plot(kind='bar')
```

<!-- 🤔 Random forests are robust and rarely need hyperparameter tuning for good results. -->

## Run the Code

```bash
python code/05-random-forests.py
```
