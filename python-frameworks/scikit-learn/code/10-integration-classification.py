"""Integration: classification pipeline — compare multiple models."""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
import warnings
warnings.filterwarnings("ignore")


print("=== Classification Pipeline Comparison ===\n")

iris = load_iris()
X, y = iris.data, iris.target

# Make it binary for simplicity
binary_mask = y != 2
X, y = X[binary_mask], y[binary_mask]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree":       DecisionTreeClassifier(max_depth=5, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM (RBF)":           SVC(kernel='rbf', random_state=42),
    "KNN (k=5)":           KNeighborsClassifier(n_neighbors=5),
    "SVM (Linear)":        SVC(kernel='linear', random_state=42),
}

results = []
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    results.append({
        "Model": name,
        "Accuracy":  accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, average='weighted'),
        "Recall":    recall_score(y_test, y_pred, average='weighted'),
        "F1-Score":  f1_score(y_test, y_pred, average='weighted'),
    })

print(f"{'Model':<22s} {'Accuracy':>9s} {'Precision':>10s} {'Recall':>8s} {'F1-Score':>9s}")
print("-" * 58)
for r in sorted(results, key=lambda x: -x["F1-Score"]):
    print(f"{r['Model']:<22s} {r['Accuracy']:>9.4f} {r['Precision']:>10.4f} {r['Recall']:>8.4f} {r['F1-Score']:>9.4f}")

best = max(results, key=lambda x: x["F1-Score"])
print(f"\nBest model: {best['Model']} (F1={best['F1-Score']:.4f})")
