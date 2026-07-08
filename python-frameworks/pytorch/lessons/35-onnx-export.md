# 🏗️ ONNX Export
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Export models to ONNX for cross-framework deployment.

## Export

```python
torch.onnx.export(
    model,
    example_input,
    'model.onnx',
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}},
)
```

## Validation

```python
import onnx
onnx_model = onnx.load('model.onnx')
onnx.checker.check_model(onnx_model)
```

## Inference with ONNX Runtime

```python
import onnxruntime as ort
session = ort.InferenceSession('model.onnx')
output = session.run(['output'], {'input': input_numpy})
```

## Why ONNX?

- Deploy to any framework (TensorFlow, ML.NET, ...)
- Hardware-specific optimizations
- Cloud vendor support (Azure, AWS)

<!-- 🤔 ONNX is the universal interchange format for ML models. -->

## Run the Code

```bash
python code/35-onnx-export.py
```
