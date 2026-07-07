"""Integration: regression pipeline — compare, tune, evaluate."""
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_regression
import warnings
warnings.filterwarnings("ignore")


print("=== Regression Pipeline Comparison ===\n")

X, y = make_regression(n_samples=500, n_features=10, noise=15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Ridge (alpha=1)":   Ridge(alpha=1.0),
    "Ridge (alpha=10)":  Ridge(alpha=10.0),
    "Lasso (alpha=0.1)": Lasso(alpha=0.1),
    "Lasso (alpha=1)":   Lasso(alpha=1.0),
    "Random Forest":     RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boost":    GradientBoostingRegressor(n_estimators=100, random_state=42),
    "SVR (RBF)":         SVR(kernel='rbf'),
}

print(f"{'Model':<25s} {'CV R²':>8s} {'Test R²':>8s} {'Test RMSE':>10s}")
print("-" * 51)
results = []
for name, model in models.items():
    if name in ["SVR (RBF)"]:
        pipe = Pipeline([('scaler', StandardScaler()), ('model', model)])
        cv_scores = cross_val_score(pipe, X_train, y_train, cv=3, scoring='r2')
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='r2')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    test_r2 = r2_score(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    results.append((name, cv_scores.mean(), test_r2, test_rmse))
    print(f"{name:<25s} {cv_scores.mean():>8.4f} {test_r2:>8.4f} {test_rmse:>10.2f}")

best_r2 = max(results, key=lambda x: x[2])
print(f"\nBest model: {best_r2[0]} (R²={best_r2[2]:.4f}, RMSE={best_r2[3]:.2f})")

print(f"\nTuning best model:")
best_model_name = best_r2[0]
if "Forest" in best_model_name:
    param_grid = {'n_estimators': [50, 200], 'max_depth': [5, 15]}
    base = RandomForestRegressor(random_state=42)
elif "Boost" in best_model_name:
    param_grid = {'n_estimators': [50, 200], 'learning_rate': [0.05, 0.2]}
    base = GradientBoostingRegressor(random_state=42)
else:
    param_grid = {'alpha': [0.01, 0.1, 1.0, 10.0]}
    base = Ridge()

grid = GridSearchCV(base, param_grid, cv=3, scoring='r2')
grid.fit(X_train, y_train)
print(f"  Best params: {grid.best_params_}")
print(f"  Tuned CV R²: {grid.best_score_:.4f}")
print(f"  Tuned Test R²: {r2_score(y_test, grid.predict(X_test)):.4f}")
