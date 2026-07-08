"""Distributed training — DataParallel for multi-GPU (simulated)."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Data Parallel (Distributed Training) ===\n")

torch.manual_seed(42)
X = torch.randn(200, 4)
y = (X.sum(dim=1, keepdim=True) > 0).float()

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))

n_gpus = torch.cuda.device_count()
print(f"Available GPUs: {n_gpus}")

if n_gpus >= 2:
    model = nn.DataParallel(model)
    print("Using DataParallel across all GPUs")
else:
    print("Only 1 GPU / CPU — DataParallel pattern shown for reference")

model_single = model.module if hasattr(model, 'module') else model
print(f"Model: {model_single}")

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

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

print("\nDataParallel: model = nn.DataParallel(model)")
print("Access inner model via model.module")
print("For large-scale: use DistributedDataParallel instead")
