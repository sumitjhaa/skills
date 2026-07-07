"""Saving and loading models with pickle and joblib."""
import numpy as np
import pickle
import joblib
import tempfile
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score


print("=== Saving & Loading Models ===\n")

from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"Original model accuracy: {accuracy_score(y_test, y_pred):.4f}")

tmpdir = tempfile.mkdtemp()

pkl_path = os.path.join(tmpdir, "model.pkl")
with open(pkl_path, 'wb') as f:
    pickle.dump(model, f)
with open(pkl_path, 'rb') as f:
    loaded_pkl = pickle.load(f)
y_pred_pkl = loaded_pkl.predict(X_test)
print(f"\nPickle - acc: {accuracy_score(y_test, y_pred_pkl):.4f}, size: {os.path.getsize(pkl_path)} bytes")

joblib_path = os.path.join(tmpdir, "model.joblib")
joblib.dump(model, joblib_path)
loaded_jl = joblib.load(joblib_path)
y_pred_jl = loaded_jl.predict(X_test)
print(f"Joblib - acc: {accuracy_score(y_test, y_pred_jl):.4f}, size: {os.path.getsize(joblib_path)} bytes")

print(f"\nModel attributes preserved:")
print(f"  n_estimators: {loaded_jl.n_estimators}")
print(f"  feature_importances: {loaded_jl.feature_importances_[:3].round(4)}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
print(f"\nTemp files cleaned up.")
