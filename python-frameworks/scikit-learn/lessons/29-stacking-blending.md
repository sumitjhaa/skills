# 🔀 Model Stacking & Blending
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Advanced ensembling with meta-models, cross-validation stacking.

## Manual Stacking

```python
# Level 1: base models
rf = RandomForestClassifier(n_estimators=100)
svm = SVC(probability=True)
lr = LogisticRegression()

# Generate meta-features via cross-val
meta_train = np.column_stack([
    cross_val_predict(rf, X_train, y_train, cv=5, method='predict_proba')[:, 1],
    cross_val_predict(svm, X_train, y_train, cv=5, method='predict_proba')[:, 1],
])

# Train meta-model
meta_model = LogisticRegression()
meta_model.fit(meta_train, y_train)
```

## Blending

```python
# Hold-out set for meta-model (simpler than CV stacking)
X_train_base, X_meta, y_train_base, y_meta = train_test_split(
    X_train, y_train, test_size=0.2
)

# Train base models on X_train_base
# Predict on X_meta for meta-features
# Train meta-model on meta-features
```

## Sklearn Stacking

```python
from sklearn.ensemble import StackingClassifier

stack = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('svm', SVC(probability=True)),
        ('knn', KNeighborsClassifier(n_neighbors=5)),
    ],
    final_estimator=LogisticRegression(),
    cv=5,
)
```

<!-- 🧠 Stacking with CV prevents the meta-model from overfitting to base model predictions. -->

## Run the Code

```bash
python code/29-stacking-blending.py
```
