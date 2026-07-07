"""KNN — choosing K, distance metrics, scaling impact."""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification


print("=== KNN ===\n")

X, y = make_classification(n_samples=500, n_features=6, n_informative=4,
                           random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for k in [1, 3, 5, 10, 20, 50]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"k={k:2d}: accuracy={acc:.4f}")

print(f"\nImpact of scaling:")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_unscaled = KNeighborsClassifier(n_neighbors=5)
model_unscaled.fit(X_train, y_train)
acc_unscaled = accuracy_score(y_test, model_unscaled.predict(X_test))

model_scaled = KNeighborsClassifier(n_neighbors=5)
model_scaled.fit(X_train_scaled, y_train)
acc_scaled = accuracy_score(y_test, model_scaled.predict(X_test_scaled))
print(f"  Unscaled: {acc_unscaled:.4f}")
print(f"  Scaled:   {acc_scaled:.4f}")

for metric in ['euclidean', 'manhattan', 'cosine']:
    model = KNeighborsClassifier(n_neighbors=5, metric=metric)
    model.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, model.predict(X_test_scaled))
    print(f"  metric={metric:10s}: accuracy={acc:.4f}")
