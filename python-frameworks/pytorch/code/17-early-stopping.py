"""Early stopping — stop training when validation loss plateaus."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Early Stopping ===\n")

torch.manual_seed(42)
X = torch.randn(600, 4)
y = torch.randint(0, 2, (600,)).float()

X_train, X_val = X[:400], X[400:]
y_train, y_val = y[:400], y[400:]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)

model = nn.Sequential(
    nn.Linear(4, 64), nn.ReLU(),
    nn.Linear(64, 64), nn.ReLU(),
    nn.Linear(64, 1),
)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)


def validate(model, loader):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for Xb, yb in loader:
            logits = model(Xb).squeeze()
            total_loss += criterion(logits, yb).item() * len(Xb)
    return total_loss / len(loader.dataset)


best_loss = float('inf')
patience = 5
counter = 0
max_epochs = 100

print(f"{'Epoch':>6} | {'Train Loss':>10} | {'Val Loss':>9} | {'Patience':>8}")
print("-" * 45)

for epoch in range(max_epochs):
    model.train()
    train_loss = 0
    for Xb, yb in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(Xb).squeeze(), yb)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * len(Xb)
    train_loss /= len(train_loader.dataset)

    val_loss = validate(model, val_loader)
    status = ""

    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        status = "✓ saved"
    else:
        counter += 1
        status = f"{counter}/{patience}"

    if epoch % 10 == 0 or counter == patience or epoch == max_epochs - 1:
        print(f"{epoch:6d} | {train_loss:10.4f} | {val_loss:9.4f} | {status:>8}")

    if counter >= patience:
        print(f"\nEarly stopping triggered at epoch {epoch}")
        break

print(f"\nBest validation loss: {best_loss:.4f}")
