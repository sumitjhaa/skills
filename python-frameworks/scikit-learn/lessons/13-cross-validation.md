# 🔄 Cross-Validation
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** K-Fold, stratified CV, cross_val_score, custom CV.

## K-Fold CV

```python
from sklearn.model_selection import cross_val_score, KFold

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"Scores: {scores}")
print(f"Mean: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
```

## Stratified K-Fold

```python
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='f1_macro')
```

## Custom CV

```python
from sklearn.model_selection import cross_validate

scoring = ['accuracy', 'precision', 'recall', 'f1']
results = cross_validate(model, X, y, cv=5, scoring=scoring)
```

## Leave-One-Out

```python
from sklearn.model_selection import LeaveOneOut

scores = cross_val_score(model, X, y, cv=LeaveOneOut())
```

<!-- 🤔 Always use stratified CV for classification to maintain class proportions. -->

## Run the Code

```bash
python code/13-cross-validation.py
```
