"""TorchServe basics — model archiving and serving pattern."""
import torch
import torch.nn as nn
import tempfile
import os


print("=== TorchServe Basics ===\n")

tmpdir = tempfile.mkdtemp()
model_path = os.path.join(tmpdir, "model.pt")
mar_dir = os.path.join(tmpdir, "model_store")
os.makedirs(mar_dir, exist_ok=True)

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3))
example = torch.randn(1, 4)
traced = torch.jit.trace(model, example)
torch.jit.save(traced, model_path)
print(f"Traced model saved to {model_path}")

handler_code = """
import torch
import torch.nn as nn

class ModelHandler:
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def initialize(self, context):
        model_path = context.system_properties.get('model_dir') + '/model.pt'
        self.model = torch.jit.load(model_path).to(self.device)
        self.model.eval()

    def preprocess(self, data):
        import numpy as np
        body = data[0].get('data') or data[0].get('body')
        import json, io
        if isinstance(body, (bytes, bytearray)):
            body = json.loads(body.decode())
        return torch.tensor(body, dtype=torch.float32).to(self.device)

    def inference(self, data):
        with torch.no_grad():
            results = self.model(data)
        return results

    def postprocess(self, data):
        return [data.cpu().tolist()]
"""

handler_path = os.path.join(tmpdir, "handler.py")
with open(handler_path, 'w') as f:
    f.write(handler_code)

print(f"Handler script written to {handler_path}")
print(f"\nTo archive and serve:")
print(f"  torch-model-archiver --model-name my_model --version 1.0 \\")
print(f"    --model-file {model_path} --handler {handler_path} \\")
print(f"    --export-path {mar_dir}")
print(f"  torchserve --start --model-store {mar_dir} --models my_model.mar")

print(f"\nSimulated prediction:")
with torch.no_grad():
    sample = torch.randn(1, 4)
    probs = torch.softmax(model(sample), dim=1)
    print(f"  Input: {sample}")
    print(f"  Output probs: {probs}")
    print(f"  Predicted class: {probs.argmax().item()}")

import shutil
shutil.rmtree(tmpdir)
print(f"\nCleaned up {tmpdir}")
