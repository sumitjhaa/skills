"""Learning curves — bias/variance diagnosis, validation curves."""
import numpy as np
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score


print("=== Learning Curves ===\n")

X, y = make_classification(n_samples=300, n_features=8, random_state=42)

print("Learning curve (train sizes):")
train_sizes, train_scores, test_scores = learning_curve(
    RandomForestClassifier(n_estimators=50, random_state=42),
    X, y,
    train_sizes=np.linspace(0.1, 1.0, 3),
    cv=3,
    scoring='accuracy',
)

for i, size in enumerate(train_sizes):
    train_mean = train_scores[i].mean()
    test_mean = test_scores[i].mean()
    gap = train_mean - test_mean
    print(f"  train_size={size:4.0f}: train={train_mean:.4f}, test={test_mean:.4f}, gap={gap:.4f}")

print(f"\nValidation curve (max_depth):")
param_range = [3, 5, 10, None]
train_scores, test_scores = validation_curve(
    RandomForestClassifier(n_estimators=50, random_state=42),
    X, y,
    param_name='max_depth',
    param_range=param_range,
    cv=3,
    scoring='accuracy',
)

for i, depth in enumerate(param_range):
    train_mean = train_scores[i].mean()
    test_mean = test_scores[i].mean()
    gap = train_mean - test_mean
    print(f"  max_depth={str(depth):>5}: train={train_mean:.4f}, test={test_mean:.4f}, gap={gap:.4f}")

print(f"\nValidation curve (n_estimators):")
param_range = [10, 50, 100]
train_scores, test_scores = validation_curve(
    RandomForestClassifier(max_depth=10, random_state=42),
    X, y,
    param_name='n_estimators',
    param_range=param_range,
    cv=3,
    scoring='accuracy',
)

for i, n in enumerate(param_range):
    train_mean = train_scores[i].mean()
    test_mean = test_scores[i].mean()
    gap = train_mean - test_mean
    print(f"  n_estimators={n:3d}: train={train_mean:.4f}, test={test_mean:.4f}, gap={gap:.4f}")
