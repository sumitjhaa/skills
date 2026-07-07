"""Model calibration — CalibratedClassifierCV, sigmoid vs isotonic."""
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, brier_score_loss
from sklearn.datasets import make_classification


print("=== Model Calibration ===\n")

X, y = make_classification(n_samples=800, n_features=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

svm_uncal = SVC(probability=True, random_state=42)
svm_uncal.fit(X_train, y_train)
prob_uncal = svm_uncal.predict_proba(X_test)[:, 1]

brier_uncal = brier_score_loss(y_test, prob_uncal)
acc_uncal = accuracy_score(y_test, svm_uncal.predict(X_test))
print(f"SVM (uncalibrated):")
print(f"  Accuracy: {acc_uncal:.4f}")
print(f"  Brier score: {brier_uncal:.4f} (lower = better calibrated)")

for method in ['sigmoid', 'isotonic']:
    svm_base = SVC(probability=False, random_state=42)
    calibrated = CalibratedClassifierCV(svm_base, method=method, cv=5)
    calibrated.fit(X_train, y_train)
    prob_cal = calibrated.predict_proba(X_test)[:, 1]
    brier_cal = brier_score_loss(y_test, prob_cal)
    acc_cal = accuracy_score(y_test, calibrated.predict(X_test))
    print(f"\nCalibrated ({method}):")
    print(f"  Accuracy: {acc_cal:.4f}")
    print(f"  Brier score: {brier_cal:.4f}")

print(f"\nProbability distribution (uncalibrated vs calibrated):")
print(f"  Uncalibrated mean prob: {prob_uncal.mean():.4f}")
for method in ['sigmoid', 'isotonic']:
    svm_base = SVC(probability=False, random_state=42)
    calibrated = CalibratedClassifierCV(svm_base, method=method, cv=3)
    calibrated.fit(X_train, y_train)
    prob_cal = calibrated.predict_proba(X_test)[:, 1]
    print(f"  Calibrated ({method:8s}) mean prob: {prob_cal.mean():.4f}")
