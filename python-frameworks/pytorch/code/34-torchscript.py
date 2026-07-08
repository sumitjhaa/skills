"""TorchScript — export and run models without Python dependency."""
import torch
import torch.nn as nn
import tempfile
import os


print("=== TorchScript Export ===\n")

tmpdir = tempfile.mkdtemp()

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1),
        )

    def forward(self, x):
        return self.net(x)

model = SimpleModel()
model.eval()

example = torch.randn(1, 4)
traced = torch.jit.trace(model, example)
scripted = torch.jit.script(model)

script_path = os.path.join(tmpdir, "model_script.pt")
traced_path = os.path.join(tmpdir, "model_trace.pt")
torch.jit.save(traced, traced_path)
torch.jit.save(scripted, script_path)

print(f"Saved torchscript models:")
print(f"  Traced:  {traced_path}")
print(f"  Script:  {script_path}")

loaded = torch.jit.load(traced_path)
loaded.eval()

test_input = torch.randn(3, 4)
original_out = model(test_input)
loaded_out = loaded(test_input)
match = torch.allclose(original_out, loaded_out, atol=1e-6)
print(f"\nOriginal vs loaded output matches: {match}")

print(f"\nGraph visualization:")
print(loaded.graph)

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
print(f"\nCleaned up {tmpdir}")
print("\nTorchScript runs anywhere: C++, mobile, no Python needed.")
