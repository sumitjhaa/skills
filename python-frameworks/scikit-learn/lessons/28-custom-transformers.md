# 🏭 Custom Transformers
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Create custom sklearn transformers, FunctionTransformer, fit/transform pattern.

## FunctionTransformer

```python
from sklearn.preprocessing import FunctionTransformer

def log_transform(X):
    return np.log1p(X)  # log(1 + x)

log_transformer = FunctionTransformer(log_transform)
X_transformed = log_transformer.fit_transform(X)
```

## Custom Transformer Class

```python
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor

    def fit(self, X, y=None):
        self.lower_ = np.percentile(X, 25, axis=0)
        self.upper_ = np.percentile(X, 75, axis=0)
        self.iqr_ = self.upper_ - self.lower_
        return self

    def transform(self, X):
        X = X.copy()
        lower_bound = self.lower_ - self.factor * self.iqr_
        upper_bound = self.upper_ + self.factor * self.iqr_
        return np.clip(X, lower_bound, upper_bound)
```

## Using in Pipeline

```python
pipe = Pipeline([
    ('clipper', OutlierClipper(factor=2.0)),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier()),
])
```

<!-- 🤔 Custom transformers let you encapsulate domain-specific preprocessing into reusable Pipeline components. -->

## Run the Code

```bash
python code/28-custom-transformers.py
```
