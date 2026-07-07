"""Hyperparameter tuning — GridSearchCV, RandomizedSearchCV."""
import numpy as np
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from scipy.stats import randint


print("=== Hyperparameter Tuning ===\n")

X, y = make_classification(n_samples=300, n_features=8, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Grid Search:")
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10],
}
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring='accuracy',
    n_jobs=1,
)
grid.fit(X_train, y_train)
print(f"  Best params: {grid.best_params_}")
print(f"  Best CV score: {grid.best_score_:.4f}")
print(f"  Test accuracy: {accuracy_score(y_test, grid.predict(X_test)):.4f}")
print(f"  Combinations evaluated: {len(grid.cv_results_['params'])}")

print(f"\nRandomized Search:")
param_dist = {
    'n_estimators': randint(10, 100),
    'max_depth': [None] + list(range(3, 10)),
}
random = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=5,
    cv=3,
    random_state=42,
    n_jobs=1,
)
random.fit(X_train, y_train)
print(f"  Best params: {random.best_params_}")
print(f"  Best CV score: {random.best_score_:.4f}")
print(f"  Test accuracy: {accuracy_score(y_test, random.predict(X_test)):.4f}")

print(f"\nComparison:")
print(f"  Default RF:    {accuracy_score(y_test, RandomForestClassifier(random_state=42).fit(X_train, y_train).predict(X_test)):.4f}")
print(f"  Grid Search:   {accuracy_score(y_test, grid.predict(X_test)):.4f}")
print(f"  Random Search: {accuracy_score(y_test, random.predict(X_test)):.4f}")
