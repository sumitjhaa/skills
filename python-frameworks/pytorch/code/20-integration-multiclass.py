"""Integration: multi-class classification with full pipeline."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Multi-Class Classification Pipeline ===\n")

torch.manual_seed(42)
n, n_features, n_classes = 1000, 8, 4
X = torch.randn(n, n_features)
w = torch.randn(n_features, n_classes)
y = (X @ w).argmax(1)

train_end, val_end = int(0.7*n), int(0.85*n)
X_train, X_val, X_test = X[:train_end], X[train_end:val_end], X[val_end:]
y_train, y_val, y_test = y[:train_end], y[train_end:val_end], y[val_end:]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32)

model = nn.Sequential(
    nn.Linear(n_features, 64), nn.ReLU(),
    nn.Linear(64, 64), nn.ReLU(),
    nn.Linear(64, n_classes),
)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

best_loss = float('inf')
patience = 8
counter = 0

print(f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>9} | {'Val Acc':>8}")
print("-" * 42)

for epoch in range(100):
    model.train()
    train_loss = 0
    for Xb, yb in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(Xb), yb)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * len(Xb)
    train_loss /= len(train_loader.dataset)

    model.eval()
    val_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        for Xb, yb in val_loader:
            logits = model(Xb)
            val_loss += criterion(logits, yb).item() * len(Xb)
            correct += (logits.argmax(1) == yb).sum().item()
            total += len(Xb)
    val_loss /= total
    val_acc = correct / total

    scheduler.step(val_loss)

    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
    else:
        counter += 1

    if epoch % 10 == 0 or counter == patience:
        print(f"{epoch:6d} | {train_loss:10.4f} | {val_loss:9.4f} | {val_acc:8.4f}")

    if counter >= patience:
        print(f"  (early stopping at epoch {epoch})")
        break

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for Xb, yb in test_loader:
        correct += (model(Xb).argmax(1) == yb).sum().item()
        total += len(Xb)
test_acc = correct / total
print(f"\nTest accuracy: {test_acc:.4f}")
print("Pipeline: split → DataLoader → model → train → validate → early stop → test")
