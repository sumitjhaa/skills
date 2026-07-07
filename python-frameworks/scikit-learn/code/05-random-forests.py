"""Random forests — ensemble, OOB score, feature importance."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification


print("=== Random Forests ===\n")

X, y = make_classification(n_samples=800, n_features=15, n_informative=8,
                           n_redundant=3, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

n_estimators_list = [10, 50, 100, 200]
for n in n_estimators_list:
    model = RandomForestClassifier(n_estimators=n, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"n_estimators={n:3d}: test_acc={acc:.4f}")

print(f"\nBest model (n=200):")
model = RandomForestClassifier(n_estimators=200, max_depth=10,
                                min_samples_leaf=2, oob_score=True, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"OOB score:     {model.oob_score_:.4f}")

importances = model.feature_importances_
top_indices = np.argsort(importances)[-5:][::-1]
print(f"\nTop 5 features: {top_indices}")
print(f"Importances: {importances[top_indices].round(4)}")
