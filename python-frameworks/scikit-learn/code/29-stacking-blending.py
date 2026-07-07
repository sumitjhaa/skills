"""Stacking & blending — manual stacking, sklearn stacking, comparison."""
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier, StackingClassifier,
    GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification


print("=== Stacking & Blending ===\n")

X, y = make_classification(n_samples=300, n_features=8, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

base_models = {
    "RF": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(probability=True, random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "GB": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

print("Base model performance:")
for name, model in base_models.items():
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"  {name}: {acc:.4f}")

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_acc = accuracy_score(y_test, lr.predict(X_test))
print(f"  LR:  {lr_acc:.4f}")

print(f"\nManual stacking (CV meta-features):")
meta_train = np.column_stack([
    cross_val_predict(model, X_train, y_train, cv=3, method='predict_proba')[:, 1]
    for name, model in base_models.items()
])
meta_model = LogisticRegression()
meta_model.fit(meta_train, y_train)

meta_test = np.column_stack([
    model.predict_proba(X_test)[:, 1]
    for name, model in base_models.items()
])
y_pred_manual = meta_model.predict(meta_test)
print(f"  Manual stacking: {accuracy_score(y_test, y_pred_manual):.4f}")

print(f"\nSklearn StackingClassifier:")
stack = StackingClassifier(
    estimators=[(name, model) for name, model in base_models.items()],
    final_estimator=LogisticRegression(),
    cv=3,
)
stack.fit(X_train, y_train)
print(f"  sklearn stacking: {accuracy_score(y_test, stack.predict(X_test)):4f}")

print(f"\nComparison:")
final = {"LR": lr_acc}
for name, model in base_models.items():
    final[name] = accuracy_score(y_test, model.predict(X_test))
final["Manual Stack"] = accuracy_score(y_test, y_pred_manual)
final["sklearn Stack"] = accuracy_score(y_test, stack.predict(X_test))

for name, acc in sorted(final.items(), key=lambda x: -x[1]):
    print(f"  {name:<15s}: {acc:.4f}")
