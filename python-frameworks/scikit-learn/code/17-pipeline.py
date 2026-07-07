"""Pipeline — chain preprocessing, feature selection, model."""
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
import pandas as pd


print("=== Pipeline ===\n")

X, y = make_classification(n_samples=500, n_features=15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=10)),
    ('classifier', RandomForestClassifier(random_state=42)),
])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print(f"Pipeline test accuracy: {accuracy_score(y_test, y_pred):.4f}")

print(f"\nPipeline with GridSearch:")
param_grid = {
    'pca__n_components': [5, 10],
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [5, 10],
}

grid = GridSearchCV(pipe, param_grid, cv=3, scoring='accuracy')
grid.fit(X_train, y_train)
print(f"  Best params: {grid.best_params_}")
print(f"  Best CV score: {grid.best_score_:.4f}")
print(f"  Test accuracy: {accuracy_score(y_test, grid.predict(X_test)):.4f}")

print(f"\nColumnTransformer demo:")
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "age": rng.normal(35, 10, 100),
    "income": rng.normal(60000, 20000, 100),
    "city": rng.choice(["NYC", "SF", "LA"], 100),
    "department": rng.choice(["Eng", "Sales", "HR"], 100),
})
y_demo = rng.integers(0, 2, 100)

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['age', 'income']),
    ('cat', OneHotEncoder(sparse_output=False), ['city', 'department']),
])

pipe_demo = Pipeline([
    ('prep', preprocessor),
    ('clf', RandomForestClassifier(random_state=42)),
])
scores = cross_val_score(pipe_demo, df, y_demo, cv=3, scoring='accuracy')
print(f"  CV accuracy: {scores.mean():.4f}")
