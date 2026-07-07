# 📊 Model Evaluation Metrics
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Confusion matrix, precision/recall, ROC-AUC, regression metrics.

## Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix
)

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
roc_auc = roc_auc_score(y_true, y_prob)
```

## Regression Metrics

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score
)

mse = mean_squared_error(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```

## When to Use Which

| Goal | Metric |
|------|--------|
| Balanced classes | Accuracy |
| Rare positives | Precision (minimize false alarms) |
| Catch all positives | Recall (minimize misses) |
| Balance | F1-Score |
| Ranking | ROC-AUC |

<!-- 🤔 For imbalanced datasets, use precision/recall/F1 — not accuracy. -->

## Run the Code

```bash
python code/18-model-evaluation.py
```
