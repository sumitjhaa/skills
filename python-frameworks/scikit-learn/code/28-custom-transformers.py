"""Custom transformers — FunctionTransformer, custom class, Pipeline integration."""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import make_classification


print("=== Custom Transformers ===\n")


class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor

    def fit(self, X, y=None):
        q1 = np.percentile(X, 25, axis=0)
        q3 = np.percentile(X, 75, axis=0)
        self.lower_ = q1 - self.factor * (q3 - q1)
        self.upper_ = q3 + self.factor * (q3 - q1)
        return self

    def transform(self, X):
        return np.clip(X, self.lower_, self.upper_)


class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log1p(np.abs(X))


X, y = make_classification(n_samples=500, n_features=10, random_state=42)

print("Custom transformer in Pipeline:")
pipe = Pipeline([
    ('clipper', OutlierClipper(factor=2.0)),
    ('log', LogTransformer()),
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42)),
])

scores = cross_val_score(pipe, X, y, cv=3, scoring='accuracy')
print(f"  CV accuracy: {scores.mean():.4f}")

print(f"\nOutlierClipper effect:")
clipper = OutlierClipper(factor=1.5)
X_with_outliers = np.concatenate([X, np.array([[100, 200, -50, 0, 0, 0, 0, 0, 0, 0]])])
clipper.fit(X_with_outliers)
X_clipped = clipper.transform(X_with_outliers)
print(f"  Before clip max: {X_with_outliers.max():.1f}")
print(f"  After clip max:  {X_clipped.max():.1f}")

print(f"\nFunctionTransformer:")
ft = FunctionTransformer(lambda x: np.log1p(np.abs(x)))
X_log = ft.fit_transform(X[:5, :2])
print(f"  Original: {X[0, :2]}")
print(f"  Log(1+x): {X_log[0]}")
