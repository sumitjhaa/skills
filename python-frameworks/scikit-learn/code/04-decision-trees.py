"""Decision trees — classification, feature importance, depth control."""
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification


print("=== Decision Trees ===\n")

X, y = make_classification(n_samples=500, n_features=10, n_informative=5,
                           n_redundant=2, random_state=42)
feature_names = [f"feature_{i}" for i in range(10)]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

depths = [1, 3, 5, 10, None]
for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"max_depth={str(depth):>5}: train_acc={train_acc:.4f}, test_acc={test_acc:.4f}")

print(f"\nBest model (depth=5):")
model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=4, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.4f}")

importances = model.feature_importances_
print(f"\nFeature importances:")
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"  {name}: {imp:.4f}")

print(f"Tree depth: {model.get_depth()}")
print(f"Number of leaves: {model.get_n_leaves()}")
