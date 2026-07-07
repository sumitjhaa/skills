"""Cross-validation — K-Fold, stratified, cross_validate."""
import numpy as np
from sklearn.model_selection import (cross_val_score, cross_validate,
    KFold, StratifiedKFold, LeaveOneOut)
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification


print("=== Cross-Validation ===\n")

X, y = make_classification(n_samples=300, n_features=10, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"KFold (5): scores={scores.round(4)}")
print(f"  Mean: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

cv_strat = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores_strat = cross_val_score(model, X, y, cv=cv_strat, scoring='accuracy')
print(f"\nStratified (5): scores={scores_strat.round(4)}")
print(f"  Mean: {scores_strat.mean():.4f}")

scoring = ['accuracy', 'precision', 'recall', 'f1']
results = cross_validate(model, X, y, cv=5, scoring=scoring)
print(f"\nMultiple metrics:")
for metric in scoring:
    scores = results[f'test_{metric}']
    print(f"  {metric}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

print(f"\nFit time: {results['fit_time'].mean():.3f}s")
print(f"Score time: {results['score_time'].mean():.3f}s")

cv_folds = [3, 5, 10]
print(f"\nImpact of K:")
for k in cv_folds:
    scores = cross_val_score(model, X, y, cv=k, scoring='accuracy')
    print(f"  k={k}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
