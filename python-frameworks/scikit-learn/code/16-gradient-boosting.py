"""Gradient boosting — learning rate, early stopping, staged predictions."""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification


print("=== Gradient Boosting ===\n")

X, y = make_classification(n_samples=600, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for lr in [0.01, 0.05, 0.1, 0.3]:
    model = GradientBoostingClassifier(
        n_estimators=200, learning_rate=lr, max_depth=3, random_state=42
    )
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"lr={lr:5.2f}: train_acc={train_acc:.4f}, test_acc={test_acc:.4f}")

print(f"\nEarly stopping:")
model_es = GradientBoostingClassifier(
    n_estimators=500,
    validation_fraction=0.2,
    n_iter_no_change=10,
    tol=1e-4,
    random_state=42,
)
model_es.fit(X_train, y_train)
print(f"  {model_es.n_estimators_} trees used (out of 500 max)")
print(f"  Test accuracy: {accuracy_score(y_test, model_es.predict(X_test)):.4f}")

print(f"\nPer-stage performance:")
model_staged = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
model_staged.fit(X_train, y_train)

staged_scores = []
for i, y_pred in enumerate(model_staged.staged_predict(X_test)):
    if i % 20 == 0 or i == 199:
        acc = accuracy_score(y_test, y_pred)
        staged_scores.append((i + 1, acc))

for n, acc in staged_scores:
    print(f"  {n:3d} trees: {acc:.4f}")
