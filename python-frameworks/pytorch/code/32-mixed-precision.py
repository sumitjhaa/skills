"""Mixed precision training — torch.cuda.amp for faster training."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== Mixed Precision Training ===\n")

has_amp = torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 7
if not has_amp:
    print("AMP requires CUDA GPU with compute capability 7.0+ (Volta/V100 or newer).")
    print("Demonstrating the pattern without actual acceleration:\n")

torch.manual_seed(42)
X = torch.randn(300, 4)
y = (X.sum(dim=1, keepdim=True) > 0).float()
loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

model = nn.Sequential(nn.Linear(4, 64), nn.ReLU(), nn.Linear(64, 1))
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

scaler = torch.amp.GradScaler('cuda' if has_amp else 'cpu')

print(f"{'Epoch':>6} | {'Loss':>8}")
print("-" * 22)

for epoch in range(20):
    model.train()
    for Xb, yb in loader:
        optimizer.zero_grad()
        with torch.amp.autocast('cuda' if has_amp else 'cpu'):
            loss = criterion(model(Xb).squeeze(), yb.squeeze())
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {loss.item():8.4f}")

print("\nAMP pattern:")
print("  scaler = GradScaler()")
print("  with autocast(): forward + loss")
print("  scaler.scale(loss).backward()")
print("  scaler.step(optimizer)")
print("  scaler.update()")
