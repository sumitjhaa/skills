# 🎯 Logistic Regression
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Binary classification, probability output, decision boundary.

## Training

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
```

## Predictions

```python
y_pred = model.predict(X_test)          # Class labels
y_prob = model.predict_proba(X_test)    # Probabilities
```

## Evaluation

```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)
```

## Multi-Class

```python
# Use multi_class='multinomial' for multi-class
model = LogisticRegression(max_iter=1000)  # Auto-detects multi-class
```

<!-- 🤔 Logistic regression outputs probabilities via the sigmoid function. Decision threshold defaults to 0.5. -->

## Run the Code

```bash
python code/03-logistic-regression.py
```
