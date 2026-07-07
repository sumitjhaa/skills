# 🔧 Feature Engineering
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Create features from existing data, polynomial features, binning, date features.

## Polynomial Features

```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
```

## Interaction Features

```python
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_interact = poly.fit_transform(X)
```

## Binning

```python
from sklearn.preprocessing import KBinsDiscretizer

kbd = KBinsDiscretizer(n_bins=5, encode='onehot-dense')
X_binned = kbd.fit_transform(X)
```

## Date Features

```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

<!-- 🤔 Good features matter more than the model. Feature engineering is where domain expertise shines. -->

## Run the Code

```bash
python code/11-feature-engineering.py
```
