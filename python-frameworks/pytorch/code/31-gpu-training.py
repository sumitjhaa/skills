"""GPU training — device-agnostic code for CPU/GPU."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== GPU Training ===\n")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

torch.manual_seed(42)
X = torch.randn(300, 4).to(device)
y = (X.sum(dim=1, keepdim=True) > 0).float()

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1)).to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

print(f"Model on: {next(model.parameters()).device}")
print(f"Data on:  {X.device}")

print(f"\n{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(20):
    model.train()
    optimizer.zero_grad()
    loss = criterion(model(X).squeeze(), y.squeeze())
    loss.backward()
    optimizer.step()

    with torch.no_grad():
        acc = ((torch.sigmoid(model(X).squeeze()) > 0.5) == y.squeeze()).float().mean()

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {loss.item():8.4f} | {acc.item():8.4f}")

print("\nKey patterns:")
print("  1. Create device: device = torch.device('cuda' if available else 'cpu')")
print("  2. Move model:   model.to(device)")
print("  3. Move data:    X.to(device), y.to(device)")
print("  4. Writes happen automatically on the correct device")
