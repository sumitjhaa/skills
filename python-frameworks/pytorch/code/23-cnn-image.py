"""CNN on image-like data — synthetic 2D data."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== CNN Image Classification ===\n")

torch.manual_seed(42)
n = 500
X = torch.randn(n, 1, 8, 8)
y = (X.mean(dim=[1, 2, 3]) > 0).float()

split = int(0.8 * n)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32)

model = nn.Sequential(
    nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(32 * 2 * 2, 1),
)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(30):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for Xb, yb in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(Xb).squeeze(), yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(Xb)
        preds = (torch.sigmoid(model(Xb).squeeze()) > 0.5).float()
        correct += (preds == yb).sum().item()
        total += len(Xb)

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {total_loss/total:8.4f} | {correct/total:8.4f}")

model.eval()
with torch.no_grad():
    preds = (torch.sigmoid(model(X_test).squeeze()) > 0.5).float()
    test_acc = (preds == y_test).float().mean()
print(f"\nTest accuracy: {test_acc:.4f}")
