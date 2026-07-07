# 💾 Saving & Loading Models
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Serialize models with pickle, joblib, ONNX.

## Pickle

```python
import pickle

# Save
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

## Joblib (Recommended)

```python
import joblib

# Save
joblib.dump(model, 'model.joblib')

# Load
model = joblib.load('model.joblib')
```

## Pipeline with Joblib

```python
joblib.dump(pipeline, 'pipeline.joblib')
loaded_pipeline = joblib.load('pipeline.joblib')
y_pred = loaded_pipeline.predict(X_new)
```

## ONNX Export

```python
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]
onx = convert_sklearn(model, initial_types=initial_type)
```

<!-- 🤔 Use joblib instead of pickle for sklearn models — it's faster and more efficient with numpy arrays. -->

## Run the Code

```bash
python code/27-save-load-model.py
```
