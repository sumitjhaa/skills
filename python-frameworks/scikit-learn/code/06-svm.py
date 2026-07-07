"""SVM — linear and RBF kernels, C parameter, scaling."""
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.datasets import make_classification


print("=== SVM ===\n")

X, y = make_classification(n_samples=400, n_features=8, n_informative=5,
                           n_redundant=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

for kernel in ['linear', 'rbf', 'poly']:
    for C in [0.1, 1.0, 10.0]:
        model = SVC(kernel=kernel, C=C, random_state=42)
        model.fit(X_train_scaled, y_train)
        acc = accuracy_score(y_test, model.predict(X_test_scaled))
        print(f"kernel={kernel:6s}, C={C:5.1f}: accuracy={acc:.4f}")

print(f"\nBest model (rbf, C=1.0):")
model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
print(f"Support vectors: {model.n_support_[0]} + {model.n_support_[1]} = {sum(model.n_support_)}")
print(f"Total training samples: {len(X_train)}")
