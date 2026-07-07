# 🎗️ Ridge & Lasso Regularization
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** L1 vs L2 regularization, alpha tuning, feature selection with Lasso.

## Ridge (L2)

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)  # Larger alpha = stronger regularization
ridge.fit(X_train, y_train)
```

## Lasso (L1)

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
print(lasso.coef_)  # Many coefficients become exactly 0
```

## Alpha Tuning

```python
for alpha in [0.001, 0.01, 0.1, 1.0, 10.0]:
    ridge = Ridge(alpha=alpha)
    scores = cross_val_score(ridge, X, y, cv=5, scoring='r2')
    print(f"alpha={alpha:.4f}: CV R²={scores.mean():.4f}")
```

## ElasticNet (L1 + L2)

```python
from sklearn.linear_model import ElasticNet

en = ElasticNet(alpha=1.0, l1_ratio=0.5)  # Mix of L1 and L2
```

<!-- 🤔 Use Ridge by default. Use Lasso when you suspect only a few features are important. -->

## Run the Code

```bash
python code/22-ridge-lasso.py
```
