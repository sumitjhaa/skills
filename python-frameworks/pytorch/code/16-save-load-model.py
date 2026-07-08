"""Saving & loading models — state_dict, checkpoints."""
import torch
import torch.nn as nn
import torch.optim as optim
import tempfile
import os


print("=== Save & Load Models ===\n")

tmpdir = tempfile.mkdtemp()
state_path = os.path.join(tmpdir, "model.pt")
checkpoint_path = os.path.join(tmpdir, "checkpoint.pt")

model = nn.Sequential(
    nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3),
)

print(f"Saving state_dict to {state_path}")
torch.save(model.state_dict(), state_path)

loaded = nn.Sequential(
    nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3),
)
loaded.load_state_dict(torch.load(state_path))
loaded.eval()

x = torch.randn(2, 4)
before = model(x)
after = loaded(x)
print(f"  Predictions match: {torch.allclose(before, after)}")

optimizer = optim.Adam(model.parameters(), lr=0.001)
checkpoint = {
    'epoch': 42,
    'model_state': model.state_dict(),
    'optimizer_state': optimizer.state_dict(),
    'loss': 0.1234,
}
torch.save(checkpoint, checkpoint_path)
print(f"\nCheckpoint saved to {checkpoint_path}")

ckpt = torch.load(checkpoint_path)
model2 = nn.Sequential(
    nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3),
)
optimizer2 = optim.Adam(model2.parameters(), lr=0.001)
model2.load_state_dict(ckpt['model_state'])
optimizer2.load_state_dict(ckpt['optimizer_state'])
print(f"  Resumed from epoch {ckpt['epoch']} with loss {ckpt['loss']}")

for f in os.listdir(tmpdir):
    os.remove(os.path.join(tmpdir, f))
os.rmdir(tmpdir)
print(f"\nCleaned up {tmpdir}")
print("\nPrefer state_dict over full model saves.")
