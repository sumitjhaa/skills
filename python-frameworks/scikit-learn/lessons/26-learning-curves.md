# 📉 Learning Curves
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Diagnose bias vs variance with learning curves.

## Plotting Learning Curves

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='accuracy',
)
```

## Interpreting

- **High bias (underfitting)**: Both curves low, close together
- **High variance (overfitting)**: Large gap between curves
- **Good fit**: Both high, small gap, converging

## Validation Curves

```python
from sklearn.model_selection import validation_curve

param_range = [1, 3, 5, 10, 20]
train_scores, test_scores = validation_curve(
    model, X, y,
    param_name='max_depth',
    param_range=param_range,
    cv=5,
)
```

## Using the Diagnosis

| Problem | Fix |
|---------|-----|
| High bias | More features, more complex model |
| High variance | More data, regularization, simpler model |

<!-- 🤔 Learning curves tell you whether collecting more data will help, or if you need a better model. -->

## Run the Code

```bash
python code/26-learning-curves.py
```
