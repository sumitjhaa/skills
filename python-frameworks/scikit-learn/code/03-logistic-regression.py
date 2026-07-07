"""Logistic regression — binary classification, probabilities."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


print("=== Logistic Regression ===\n")

rng = np.random.default_rng(42)
n = 300
X = rng.normal(0, 1, (n, 2))
y = (X[:, 0] + X[:, 1] + rng.normal(0, 0.5, n) > 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"Coefficients: {model.coef_[0]}")
print(f"Intercept: {model.intercept_[0]:.4f}")

cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:\n{cm}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

print(f"Sample probabilities (first 5):")
for i in range(5):
    print(f"  True={y_test[i]}, Pred={y_pred[i]}, Prob0={y_prob[i][0]:.4f}, Prob1={y_prob[i][1]:.4f}")

print(f"\nMulti-class (Iris-like):")
from sklearn.datasets import make_classification
X_mc, y_mc = make_classification(n_samples=200, n_features=5, n_classes=3,
                                  n_informative=3, random_state=42)
X_mc_train, X_mc_test, y_mc_train, y_mc_test = train_test_split(
    X_mc, y_mc, test_size=0.2, random_state=42
)
model_mc = LogisticRegression(max_iter=1000)
model_mc.fit(X_mc_train, y_mc_train)
y_mc_pred = model_mc.predict(X_mc_test)
print(f"Multi-class accuracy: {accuracy_score(y_mc_test, y_mc_pred):.4f}")
