"""Hyperparameter optimization — manual sweep (simulating Optuna)."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from itertools import product


print("=== Hyperparameter Optimization ===\n")

torch.manual_seed(42)
X = torch.randn(400, 8)
y = torch.randint(0, 2, (400,))
X_train, X_val = X[:300], X[100:]
y_train, y_val = y[:300], y[100:]
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)


def train_and_eval(lr, hidden, dropout):
    model = nn.Sequential(
        nn.Linear(8, hidden), nn.ReLU(),
        nn.Dropout(dropout),
        nn.Linear(hidden, hidden // 2), nn.ReLU(),
        nn.Dropout(dropout),
        nn.Linear(hidden // 2, 1),
    )
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(15):
        model.train()
        for Xb, yb in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(Xb).squeeze(), yb.float())
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        val_acc = ((torch.sigmoid(model(X_val).squeeze()) > 0.5) == y_val).float().mean()
    return val_acc.item()


param_grid = {
    'lr': [0.1, 0.01],
    'hidden': [32, 64],
    'dropout': [0.0, 0.2],
}

print(f"{'lr':>6} | {'hidden':>6} | {'dropout':>7} | {'Val Acc':>8}")
print("-" * 35)

best_acc, best_params = 0, {}
for lr, hidden, dropout in product(param_grid['lr'], param_grid['hidden'], param_grid['dropout']):
    acc = train_and_eval(lr, hidden, dropout)
    marker = " ✓" if acc > best_acc else ""
    if acc > best_acc:
        best_acc = acc
        best_params = {'lr': lr, 'hidden': hidden, 'dropout': dropout}
    print(f"{lr:6.2f} | {hidden:6d} | {dropout:7.1f} | {acc:8.4f}{marker}")

print(f"\nBest: lr={best_params['lr']}, hidden={best_params['hidden']}, dropout={best_params['dropout']} → val_acc={best_acc:.4f}")
print("\nFor larger searches, use Optuna (pip install optuna)")
