"""Integration: binary classification with nn.Module."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Binary Classification with nn.Module ===\n")

torch.manual_seed(42)
n, n_features = 500, 4
X = torch.randn(n, n_features)
true_w = torch.tensor([2.0, -1.5, 0.5, 0.0])
logits = X @ true_w + 0.3
probs = torch.sigmoid(logits)
y = (probs > 0.5).float()

split = int(0.8 * n)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]


class BinaryClassifier(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.linear = nn.Linear(n_features, 1)

    def forward(self, x):
        return self.linear(x).squeeze(1)


model = BinaryClassifier(n_features)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.1)

print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(100):
    logits_out = model(X_train)
    loss = criterion(logits_out, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 20 == 0 or epoch == 99:
        with torch.no_grad():
            preds = (torch.sigmoid(logits_out) > 0.5).float()
            acc = (preds == y_train).float().mean()
        print(f"{epoch:6d} | {loss.item():8.4f} | {acc.item():8.4f}")

with torch.no_grad():
    test_logits = model(X_test)
    test_preds = (torch.sigmoid(test_logits) > 0.5).float()
    test_acc = (test_preds == y_test).float().mean()
print(f"\nTest accuracy: {test_acc.item():.4f}")
print(f"Learned weights: {model.linear.weight.data}")
print(f"True weights:    {true_w}")
