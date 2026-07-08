"""Integration: full production pipeline — training, export, reload, inference."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import tempfile
import os


print("=" * 55)
print("  FULL PRODUCTION PIPELINE")
print("=" * 55, "\n")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tmpdir = tempfile.mkdtemp()
model_path = os.path.join(tmpdir, "prod_model.pt")
script_path = os.path.join(tmpdir, "prod_model_script.pt")

torch.manual_seed(42)
X = torch.randn(800, 8)
y = torch.randint(0, 2, (800,))
X_train, X_test = X[:700], X[100:]
y_train, y_test = y[:700], y[100:]
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32)

model = nn.Sequential(
    nn.Linear(8, 32), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(32, 16), nn.ReLU(),
    nn.Linear(16, 1),
).to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

print("Phase 1: Training")
print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(25):
    model.train()
    for Xb, yb in train_loader:
        Xb, yb = Xb.to(device), yb.to(device).float()
        optimizer.zero_grad()
        loss = criterion(model(Xb).squeeze(), yb)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
    if epoch % 5 == 0:
        model.eval()
        with torch.no_grad():
            acc = ((torch.sigmoid(model(X.to(device)).squeeze()) > 0.5) == y.to(device)).float().mean()
        print(f"{epoch:6d} | {loss.item():8.4f} | {acc.item():8.4f}")

model.eval()
test_acc = 0
with torch.no_grad():
    correct = ((torch.sigmoid(model(X_test.to(device)).squeeze()) > 0.5) == y_test.to(device)).sum()
    test_acc = correct.item() / len(y_test)
print(f"\nTest accuracy: {test_acc:.4f}")

print("\nPhase 2: Export (TorchScript)")
example = torch.randn(1, 8).to(device)
traced = torch.jit.trace(model.cpu(), example.cpu())
torch.jit.save(traced, script_path)
print(f"  Saved to {script_path}")

print("\nPhase 3: Load & Inference")
loaded = torch.jit.load(script_path)
loaded.eval()
sample = torch.randn(5, 8)
with torch.no_grad():
    logits = loaded(sample)
    probs = torch.sigmoid(logits)
    preds = (probs > 0.5).int()
print(f"  Sample input:  {sample[:2]}")
print(f"  Probabilities: {probs[:2].squeeze()}")
print(f"  Predictions:   {preds[:2].squeeze()}")

import shutil
shutil.rmtree(tmpdir)
print(f"\nPhase 4: Cleanup — removed {tmpdir}")
print("\n" + "=" * 55)
print("  PIPELINE COMPLETE")
print("=" * 55)
