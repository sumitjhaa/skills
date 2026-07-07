# 🕳️ Missing Data Strategies
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Advanced imputation, interpolation, missing indicator, patterns.

## Interpolation

```python
df.interpolate(method="linear")     # Linear interpolation
df.interpolate(method="quadratic")  # Quadratic
df.interpolate(method="time")       # Time-based
```

## Forward/Backward Fill

```python
df.ffill(limit=2)   # Forward fill, max 2 consecutive
df.bfill(limit=1)   # Backward fill
```

## Missing Indicator

```python
from sklearn.impute import MissingIndicator  # Or manual
df["income_missing"] = df["income"].isna().astype(int)
```

## Imputation by Group

```python
df["income"] = df.groupby("region")["income"].transform(
    lambda x: x.fillna(x.median())
)
```

## Pattern Detection

```python
# Missing pattern matrix
missing = df.isna()
pattern_counts = missing.value_counts()
```

<!-- 🤔 Always add a missing indicator column when imputing — the fact that a value was missing may be predictive. -->

## Run the Code

```bash
python code/27-missing-data.py
```
