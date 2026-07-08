"""Batch normalization — effect on training convergence."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Batch Normalization ===\n")

torch.manual_seed(42)
X = torch.randn(600, 10)
y = torch.randint(0, 2, (600,)).float()
X_train, X_val = X[:400], X[200:]
y_train, y_val = y[:400], y[200:]
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)


def make_model(use_bn=False):
    layers = []
    in_dim = 10
    for hidden in [64, 64]:
        layers.append(nn.Linear(in_dim, hidden))
        if use_bn:
            layers.append(nn.BatchNorm1d(hidden))
        layers.append(nn.ReLU())
        in_dim = hidden
    layers.append(nn.Linear(in_dim, 1))
    return nn.Sequential(*layers)


def train_and_eval(model):
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(30):
        model.train()
        for Xb, yb in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(Xb).squeeze(), yb)
            loss.backward()
            optimizer.step()
    model.eval()
    with torch.no_grad():
        val_loss = criterion(model(X_val).squeeze(), y_val)
        correct = ((torch.sigmoid(model(X_val).squeeze()) > 0.5) == y_val).sum()
        acc = correct / len(y_val)
    return val_loss.item(), acc.item()


print(f"{'Config':<25} | {'Val Loss':>9} | {'Val Acc':>8}")
print("-" * 48)

for name, use_bn in [("Without BN", False), ("With BatchNorm", True)]:
    torch.manual_seed(42)
    model = make_model(use_bn)
    loss, acc = train_and_eval(model)
    print(f"{name:<25} | {loss:9.4f} | {acc:8.4f}")

print("\nBatchNorm benefits:")
print("  - Faster convergence")
print("  - Allows higher learning rates")
print("  - Reduces sensitivity to initialization")
