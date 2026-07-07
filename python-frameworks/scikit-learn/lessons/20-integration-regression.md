# 🏁 Integration: Regression Pipeline
<!-- ⏱️ 25 min | 🔴 Advanced -->

**What You'll Learn:** Build, compare, and tune multiple regression models.

## Pipeline Steps

1. Generate or load a regression dataset
2. Split into train/test
3. Scale features
4. Train multiple regression models
5. Compare with CV
6. Tune the best model
7. Evaluate on held-out test set

## Models to Compare

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR

models = {
    "Linear": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1),
    "Random Forest": RandomForestRegressor(n_estimators=100),
    "Gradient Boost": GradientBoostingRegressor(n_estimators=100),
    "SVR": SVR(kernel='rbf'),
}
```

## Evaluation

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name}: CV R²={scores.mean():.4f}, Test MSE={mean_squared_error(y_test, y_pred):.4f}")
```

## Run the Code

```bash
python code/20-integration-regression.py
```
