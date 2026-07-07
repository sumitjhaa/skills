"""Train/test split, scaling, encoding."""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


print("=== Train/Test Split & Preprocessing ===\n")

rng = np.random.default_rng(42)
X = rng.normal(0, 1, (200, 4))
y = rng.integers(0, 2, 200)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape:  {X_test.shape}")
print(f"y_train: {len(y_train)} samples, y_test: {len(y_test)} samples")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"\nScaled X_train mean: {X_train_scaled.mean(axis=0).round(4)}")
print(f"Scaled X_train std:  {X_train_scaled.std(axis=0).round(4)}")
print(f"Scaled X_test mean:  {X_test_scaled.mean(axis=0).round(4)} (close to 0)")

categories = ["cat", "dog", "bird", "dog", "cat", "fish"]
le = LabelEncoder()
encoded = le.fit_transform(categories)
print(f"\nLabel encoding: {categories} -> {encoded}")
print(f"Classes: {list(le.classes_)}")
print(f"Inverse: {le.inverse_transform(encoded)}")
