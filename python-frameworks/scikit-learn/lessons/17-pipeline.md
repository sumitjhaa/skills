# 🔗 Pipeline
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Chain preprocessing + model into one Pipeline, use in CV.

## Basic Pipeline

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('classifier', RandomForestClassifier(random_state=42)),
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
```

## Pipeline with GridSearch

```python
param_grid = {
    'pca__n_components': [5, 10, 15],
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [5, 10],
}

grid = GridSearchCV(pipe, param_grid, cv=5)
grid.fit(X_train, y_train)
print(grid.best_params_)
```

## ColumnTransformer

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(), categorical_cols),
])

pipe = Pipeline([
    ('prep', preprocessor),
    ('clf', RandomForestClassifier()),
])
```

<!-- 🤔 Pipelines ensure preprocessing is applied correctly inside CV folds — no data leakage. -->

## Run the Code

```bash
python code/17-pipeline.py
```
