"""Transfer learning — use a pretrained model on synthetic data."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Transfer Learning ===\n")

torch.manual_seed(42)
n = 200
X = torch.randn(n, 1, 8, 8)
y = (X.mean(dim=[1, 2, 3]) > 0).float()
split = int(0.8 * n)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print("Simulating a pretrained feature extractor:")
pretrained_base = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
)
for param in pretrained_base.parameters():
    param.requires_grad = False

classifier = nn.Linear(16 * 2 * 2, 1)
model = nn.Sequential(pretrained_base, classifier)
print(f"Model:\n{model}\n")

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(classifier.parameters(), lr=0.01)

print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(20):
    model.train()
    optimizer.zero_grad()
    loss = criterion(model(X_train).squeeze(), y_train)
    loss.backward()
    optimizer.step()
    with torch.no_grad():
        acc = ((torch.sigmoid(model(X_train).squeeze()) > 0.5) == y_train).float().mean()
    if epoch % 5 == 0:
        print(f"{epoch:6d} | {loss.item():8.4f} | {acc.item():8.4f}")

model.eval()
with torch.no_grad():
    test_acc = ((torch.sigmoid(model(X_test).squeeze()) > 0.5) == y_test).float().mean()
print(f"\nTest accuracy (transfer learning): {test_acc:.4f}")
print("Key: freeze base, only train new classifier layers.")
