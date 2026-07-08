"""Regularization — Dropout and weight decay comparison."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Regularization: Dropout & Weight Decay ===\n")

torch.manual_seed(42)
X = torch.randn(400, 10)
y = torch.randint(0, 2, (400,))
X_train, X_val = X[:300], X[100:]
y_train, y_val = y[:300], y[100:]
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)


def make_model(dropout=0.0):
    layers = []
    in_dim = 10
    for hidden in [64, 64]:
        layers.append(nn.Linear(in_dim, hidden))
        layers.append(nn.ReLU())
        if dropout > 0:
            layers.append(nn.Dropout(dropout))
        in_dim = hidden
    layers.append(nn.Linear(in_dim, 1))
    return nn.Sequential(*layers)


def train_and_eval(model, weight_decay=0):
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=weight_decay)

    for epoch in range(30):
        model.train()
        for Xb, yb in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(Xb).squeeze(), yb.float())
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        val_logits = model(X_val).squeeze()
        val_loss = criterion(val_logits, y_val.float())
        val_acc = ((torch.sigmoid(val_logits) > 0.5) == y_val).float().mean()
    return val_loss.item(), val_acc.item()


print(f"{'Config':<30} | {'Val Loss':>9} | {'Val Acc':>8}")
print("-" * 55)

for name, dropout, wd in [
    ("No regularization", 0.0, 0),
    ("Dropout=0.3", 0.3, 0),
    ("Dropout=0.5", 0.5, 0),
    ("Weight decay=1e-4", 0.0, 1e-4),
    ("Dropout=0.3 + WD=1e-4", 0.3, 1e-4),
]:
    torch.manual_seed(42)
    model = make_model(dropout)
    val_loss, val_acc = train_and_eval(model, weight_decay=wd)
    print(f"{name:<30} | {val_loss:9.4f} | {val_acc:8.4f}")

print("\nUse model.train() during training, model.eval() for inference.")
print("Dropout auto-disables in eval mode.")
