"""Gradient clipping — prevent exploding gradients."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Gradient Clipping ===\n")

torch.manual_seed(42)
X = torch.randn(200, 4)
y = (X.sum(dim=1, keepdim=True) > 0).float()
loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

model_deep = nn.Sequential(
    nn.Linear(4, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 1),
)
criterion = nn.BCEWithLogitsLoss()

print("Without gradient clipping:")
optimizer = optim.Adam(model_deep.parameters(), lr=0.1)
total_norm = 0
for Xb, yb in loader:
    optimizer.zero_grad()
    loss = criterion(model_deep(Xb).squeeze(), yb.squeeze())
    loss.backward()
    total_norm = torch.nn.utils.clip_grad_norm_(model_deep.parameters(), max_norm=1.0)
    break
print(f"  Gradient norm before clipping: computed")

print("\nWith gradient clipping (max_norm=1.0):")
model_deep2 = nn.Sequential(
    nn.Linear(4, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 256), nn.ReLU(),
    nn.Linear(256, 1),
)
optimizer2 = optim.Adam(model_deep2.parameters(), lr=0.1)

print(f"{'Epoch':>6} | {'Loss (clipped)':>14}")
print("-" * 25)

for epoch in range(20):
    model_deep2.train()
    for Xb, yb in loader:
        optimizer2.zero_grad()
        loss = criterion(model_deep2(Xb).squeeze(), yb.squeeze())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model_deep2.parameters(), max_norm=1.0)
        optimizer2.step()

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {loss.item():14.4f}")

print("\nGradient clipping prevents exploding gradients in deep/RNN models.")
print("Common max_norm values: 0.5, 1.0, 5.0")
