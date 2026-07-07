"""Imbalanced data — class weights, SMOTE, threshold tuning."""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report)
from sklearn.datasets import make_classification


print("=== Imbalanced Data ===\n")

X, y = make_classification(n_samples=1000, n_features=10, weights=[0.9, 0.1],
                           random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Class distribution (train): {np.bincount(y_train)}")
print(f"Class distribution (test):  {np.bincount(y_test)}\n")

model_default = RandomForestClassifier(random_state=42)
model_default.fit(X_train, y_train)
y_pred_default = model_default.predict(X_test)
print("Default (no class_weight):")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_default):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred_default):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred_default):.4f}")
print(f"  F1:        {f1_score(y_test, y_pred_default):.4f}")

model_balanced = RandomForestClassifier(class_weight='balanced', random_state=42)
model_balanced.fit(X_train, y_train)
y_pred_balanced = model_balanced.predict(X_test)
print(f"\nBalanced class_weight:")
print(f"  Accuracy: {accuracy_score(y_test, y_pred_balanced):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred_balanced):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred_balanced):.4f}")
print(f"  F1:        {f1_score(y_test, y_pred_balanced):.4f}")

# Threshold tuning
y_prob = model_balanced.predict_proba(X_test)[:, 1]
for threshold in [0.3, 0.5, 0.7]:
    y_pred_thresh = (y_prob >= threshold).astype(int)
    print(f"\nThreshold={threshold}:")
    print(f"  Precision: {precision_score(y_test, y_pred_thresh):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred_thresh):.4f}")
    print(f"  F1:        {f1_score(y_test, y_pred_thresh):.4f}")

try:
    from imblearn.over_sampling import SMOTE
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"\nSMOTE resampled: {np.bincount(y_res)}")
    model_smote = RandomForestClassifier(random_state=42)
    model_smote.fit(X_res, y_res)
    y_pred_smote = model_smote.predict(X_test)
    print(f"  Accuracy: {accuracy_score(y_test, y_pred_smote):.4f}")
    print(f"  F1:        {f1_score(y_test, y_pred_smote):.4f}")
except ImportError:
    print("\nSMOTE not available (install imbalanced-learn)")
