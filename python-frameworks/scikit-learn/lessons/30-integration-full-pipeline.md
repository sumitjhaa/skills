# 🏁 Integration: Full ML Pipeline
<!-- ⏱️ 30 min | 🔴 Advanced -->

**What You'll Learn:** Complete ML project from data to deployment-ready model.

## Project Steps

1. **Load & explore** data
2. **Preprocess** (missing values, scaling, encoding)
3. **Feature engineering & selection**
4. **Model comparison** with CV
5. **Hyperparameter tuning**
6. **Final evaluation** on hold-out test set
7. **Save model + pipeline** for deployment

## The Pipeline

```python
full_pipeline = Pipeline([
    ('preprocessor', ColumnTransformer([...])),
    ('selector', SelectKBest(k=15)),
    ('classifier', RandomForestClassifier(random_state=42)),
])

# Tune with GridSearch
grid = GridSearchCV(full_pipeline, param_grid, cv=5, scoring='f1')
grid.fit(X_train, y_train)

# Save
joblib.dump(grid.best_estimator_, 'final_pipeline.joblib')
```

## Output

| Report | Description |
|--------|-------------|
| Classification report | Precision, recall, F1 per class |
| Confusion matrix | Error breakdown |
| Feature importance | Top features driving predictions |
| CV results | Cross-validation stability |

## Run the Code

```bash
python code/30-integration-full-pipeline.py
```
