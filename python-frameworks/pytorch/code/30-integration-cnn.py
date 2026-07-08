"""Integration: CNN for image-like classification with full pipeline."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== CNN Integration: Image Classification ===\n")

torch.manual_seed(42)
n = 800
X = torch.randn(n, 1, 8, 8)
y = (X.mean(dim=[1, 2, 3]) + 0.2 * torch.randn(n) > 0).float()

train_end, val_end = int(0.7*n), int(0.85*n)
X_train, X_val, X_test = X[:train_end], X[train_end:val_end], X[val_end:]
y_train, y_val, y_test = y[:train_end], y[train_end:val_end], y[val_end:]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32)


class CNNClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(32 * 2 * 2, 32), nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        return self.classifier(self.features(x)).squeeze(1)


model = CNNClassifier()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)

print(f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>9} | {'Val Acc':>8}")
print("-" * 40)

for epoch in range(30):
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
            correct += ((torch.sigmoid(logits) > 0.5) == yb).sum().item()
            total += len(Xb)
    val_loss /= total
    val_acc = correct / total
    scheduler.step(val_loss)

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {train_loss:10.4f} | {val_loss:9.4f} | {val_acc:8.4f}")

model.eval()
test_acc = 0
with torch.no_grad():
    correct, total = 0, 0
    for Xb, yb in test_loader:
        correct += ((torch.sigmoid(model(Xb)) > 0.5) == yb).sum().item()
        total += len(Xb)
    test_acc = correct / total
print(f"\nTest accuracy: {test_acc:.4f}")
