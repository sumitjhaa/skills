# ⚖️ Imbalanced Data
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** Class weights, resampling, SMOTE, threshold tuning.

## Class Weights

```python
model = RandomForestClassifier(class_weight='balanced', random_state=42)

# Or custom weights
model = LogisticRegression(class_weight={0: 1, 1: 10})
```

## Oversampling with SMOTE

```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
```

## Undersampling

```python
from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(X, y)
```

## Threshold Tuning

```python
y_prob = model.predict_proba(X_test)[:, 1]
threshold = 0.3  # Lower threshold to catch more positives
y_pred = (y_prob >= threshold).astype(int)
```

## Combined Approach

```python
from imblearn.pipeline import Pipeline as ImbPipeline

pipe = ImbPipeline([
    ('smote', SMOTE()),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier()),
])
```

<!-- 🤔 Always evaluate with precision/recall, not accuracy, on imbalanced data. -->

## Run the Code

```bash
python code/19-imbalanced-data.py
```
