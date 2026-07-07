# 🎯 Model Calibration
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Probability calibration, CalibratedClassifierCV, reliability curves.

## Why Calibrate?

Some models (SVM, Naive Bayes) output poorly calibrated probabilities. A well-calibrated model's predicted probability matches actual frequency.

## Calibration

```python
from sklearn.calibration import CalibratedClassifierCV

base_model = SVC(probability=False)  # Don't use native probabilities
calibrated = CalibratedClassifierCV(
    base_model,
    method='sigmoid',  # Platt scaling
    cv=5,
)
calibrated.fit(X_train, y_train)
y_prob = calibrated.predict_proba(X_test)
```

## Calibration Methods

| Method | Best For |
|--------|----------|
| `sigmoid` (Platt) | Small datasets, parametric |
| `isotonic` | Large datasets, non-parametric |

## When to Calibrate

- When you need reliable probability estimates
- After model selection, before deployment
- For cost-sensitive decisions

<!-- 🤔 Always calibrate SVM and Naive Bayes if you need probabilities. Random Forest is usually well-calibrated. -->

## Run the Code

```bash
python code/25-model-calibration.py
```
