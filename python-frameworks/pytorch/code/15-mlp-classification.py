"""Multi-layer perceptron for multi-class classification."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== MLP for Multi-Class Classification ===\n")

torch.manual_seed(42)
n, n_features, n_classes = 500, 4, 3
X = torch.randn(n, n_features)
y = torch.randint(0, n_classes, (n,))

split = int(0.8 * n)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32)


class MLP(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x):
        return self.net(x)


model = MLP(n_features, 32, n_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(50):
    model.train()
    total_loss, correct, total = 0, 0, 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        logits = model(X_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(X_batch)
        correct += (logits.argmax(1) == y_batch).sum().item()
        total += len(X_batch)
    train_loss = total_loss / total
    train_acc = correct / total

    if epoch % 10 == 0 or epoch == 49:
        print(f"{epoch:6d} | {train_loss:8.4f} | {train_acc:8.4f}")

model.eval()
with torch.no_grad():
    correct, total = 0, 0
    for X_batch, y_batch in test_loader:
        logits = model(X_batch)
        correct += (logits.argmax(1) == y_batch).sum().item()
        total += len(X_batch)
    test_acc = correct / total
print(f"\nTest accuracy: {test_acc:.4f}")
