"""Fine-tuning — unfreeze base layers after initial training."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Fine-Tuning ===\n")

torch.manual_seed(42)
X = torch.randn(300, 1, 8, 8)
y = (X.mean(dim=[1, 2, 3]) > 0).float()
X_train, X_test = X[:240], X[60:]
y_train, y_test = y[:240], y[60:]

base = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(8, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(),
)
classifier = nn.Linear(16 * 2 * 2, 1)
model = nn.Sequential(base, classifier)

for param in base.parameters():
    param.requires_grad = False

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(classifier.parameters(), lr=0.01)

for epoch in range(10):
    model.train()
    loss = criterion(model(X_train).squeeze(), y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("Phase 1 (classifier only) done.")

for param in base.parameters():
    param.requires_grad = True

optimizer = optim.Adam(model.parameters(), lr=0.001)
print("Phase 2: fine-tuning all layers with lower LR...")

for epoch in range(15):
    model.train()
    loss = criterion(model(X_train).squeeze(), y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    test_acc = ((torch.sigmoid(model(X_test).squeeze()) > 0.5) == y_test).float().mean()
print(f"\nTest accuracy after fine-tuning: {test_acc:.4f}")
print("Strategy: freeze → train head → unfreeze → fine-tune all with lower LR")
