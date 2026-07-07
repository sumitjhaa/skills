"""Integration: full ML pipeline — preprocessing, CV, tuning, evaluation, export."""
import numpy as np
import joblib
import tempfile
import os
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix)
from sklearn.datasets import make_classification
import warnings
warnings.filterwarnings("ignore")


print("=" * 60)
print("  FULL ML PIPELINE — End to End")
print("=" * 60, "\n")

print("1. Generating data...")
rng = np.random.default_rng(42)
n = 300
df_numeric = rng.normal(0, 1, (n, 8))
df_cat = rng.choice(["A", "B", "C", "D"], (n, 2))
X = np.hstack([df_numeric, df_cat])
y = (df_numeric[:, 0] + df_numeric[:, 1] + rng.normal(0, 0.5, n) > 0).astype(int)

numeric_cols = list(range(8))
categorical_cols = [8, 9]
all_cols = numeric_cols + categorical_cols

print("2. Building pipeline...")
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
])

pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('selector', SelectKBest(score_func=f_classif, k=8)),
    ('classifier', RandomForestClassifier(random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("3. Cross-validation...")
cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='accuracy')
print(f"  CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

print("\n4. Hyperparameter tuning...")
param_grid = {
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [5, 10],
}
grid = GridSearchCV(pipe, param_grid, cv=3, scoring='accuracy', n_jobs=1)
grid.fit(X_train, y_train)

print(f"  Best params: {grid.best_params_}")
print(f"  Best CV score: {grid.best_score_:.4f}")

print("\n5. Final evaluation...")
y_pred = grid.predict(X_test)
print(f"  Test accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"  Test precision: {precision_score(y_test, y_pred):.4f}")
print(f"  Test recall:    {recall_score(y_test, y_pred):.4f}")
print(f"  Test F1:        {f1_score(y_test, y_pred):.4f}")

cm = confusion_matrix(y_test, y_pred)
print(f"\n  Confusion Matrix:")
print(f"    TN={cm[0,0]:3d}  FP={cm[0,1]:3d}")
print(f"    FN={cm[1,0]:3d}  TP={cm[1,1]:3d}")

print("\n6. Saving model...")
tmpdir = tempfile.mkdtemp()
model_path = os.path.join(tmpdir, "final_pipeline.joblib")
joblib.dump(grid.best_estimator_, model_path)
print(f"  Saved to: {model_path}")

loaded = joblib.load(model_path)
y_pred_loaded = loaded.predict(X_test)
print(f"  Loaded model accuracy: {accuracy_score(y_test, y_pred_loaded):.4f}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)

print("\n7. Pipeline components in best model:")
best_pipe = grid.best_estimator_
print(f"  Selector k: {best_pipe.named_steps['selector'].k}")
print(f"  Classifier: {type(best_pipe.named_steps['classifier']).__name__}")

print("\n" + "=" * 60)
print("  PIPELINE COMPLETE")
print("=" * 60)
