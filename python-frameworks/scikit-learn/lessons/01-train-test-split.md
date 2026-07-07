# 🏗️ Train/Test Split & Preprocessing
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Split data, standardize features, encode categories.

## Train/Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## Standard Scaling

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

## Label Encoding

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_encoded = le.fit_transform(y)
```

## One-Hot Encoding

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(categorical_data)
```

<!-- 🤔 Always fit scalers/encoders on training data only, then transform test data. -->

## Run the Code

```bash
python code/01-train-test-split.py
```
