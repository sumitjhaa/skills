# 📈 Polynomial & Interaction Regression
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Polynomial regression, interaction terms, overfitting with high degree.

## Polynomial Regression

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

poly = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly.fit_transform(X)

model = LinearRegression()
model.fit(X_poly, y)
```

## Degree Selection

```python
for degree in [1, 2, 3, 5, 10]:
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    scores = cross_val_score(model, X_poly, y, cv=5, scoring='r2')
    print(f"Degree {degree}: CV R²={scores.mean():.4f}")
```

## Overfitting Warning

High-degree polynomials overfit — they fit training data perfectly but fail on test data. Use CV to pick the right degree.

## Interaction Features

```python
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_interact = poly.fit_transform(X)
# Only x1*x2, x1*x3, etc. — no squared terms
```

<!-- 🤔 Start with degree=2. Higher degrees rarely help in practice and often hurt. -->

## Run the Code

```bash
python code/21-polynomial-regression.py
```
