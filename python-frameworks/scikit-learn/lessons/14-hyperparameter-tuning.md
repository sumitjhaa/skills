# 🎛️ Hyperparameter Tuning
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** GridSearchCV, RandomizedSearchCV, param distributions.

## Grid Search

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_leaf': [1, 3, 5],
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
)
grid.fit(X, y)

print(grid.best_params_)
print(grid.best_score_)
```

## Randomized Search

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(10, 500),
    'max_depth': [None] + list(range(5, 30)),
    'min_samples_leaf': randint(1, 10),
}

random = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=50,
    cv=5,
    random_state=42,
)
random.fit(X, y)
```

<!-- 🧠 Use RandomizedSearchCV when you have many parameters — it's faster and often finds better values than grid. -->

## Run the Code

```bash
python code/14-hyperparameter-tuning.py
```
