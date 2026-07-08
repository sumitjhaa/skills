"""ONNX export — interoperability with other frameworks."""
import torch
import torch.nn as nn
import tempfile
import os


print("=== ONNX Export ===\n")

try:
    import onnx
    import onnxruntime as ort
    has_onnx = True
except ImportError:
    has_onnx = False

tmpdir = tempfile.mkdtemp()
onnx_path = os.path.join(tmpdir, "model.onnx")

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
model.eval()

example = torch.randn(1, 4)
torch.onnx.export(
    model,
    example,
    onnx_path,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
)
print(f"ONNX model saved to: {onnx_path}")

if has_onnx:
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX model validated ✓")

    session = ort.InferenceSession(onnx_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    test_input = torch.randn(3, 4).numpy()
    onnx_output = session.run([output_name], {input_name: test_input})[0]
    torch_output = model(torch.from_numpy(test_input)).detach().numpy()
    match = torch.allclose(torch.from_numpy(torch_output), torch.from_numpy(onnx_output), atol=1e-6)
    print(f"PyTorch vs ONNX output matches: {match}")
else:
    print("\nInstall onnx + onnxruntime to verify:")
    print("  pip install onnx onnxruntime")

import shutil
shutil.rmtree(tmpdir)
print(f"\nCleaned up {tmpdir}")
