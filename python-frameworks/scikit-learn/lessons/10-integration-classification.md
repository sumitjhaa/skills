# 🏁 Integration: Classification Pipeline
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Build, compare, and evaluate multiple classifiers on a real dataset.

## Pipeline Steps

1. Load dataset (Iris or Wine from sklearn)
2. Split into train/test
3. Scale features
4. Train multiple models
5. Compare performance
6. Select best model

## Models to Compare

```python
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "SVM": SVC(kernel='rbf'),
    "KNN": KNeighborsClassifier(n_neighbors=5),
}
```

## Evaluation

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred, average='weighted'),
    })
```

<!-- 🤔 Always compare multiple models — the best theoretical choice isn't always best in practice. -->

## Run the Code

```bash
python code/10-integration-classification.py
```
