"""Learning rate scheduling — StepLR, CosineAnnealing, ReduceLROnPlateau."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


print("=== LR Scheduling ===\n")

torch.manual_seed(42)
X = torch.randn(300, 4)
y = torch.randint(0, 2, (300,))
loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
criterion = nn.BCEWithLogitsLoss()

schedulers = {
    "StepLR (step=10, gamma=0.5)": optim.lr_scheduler.StepLR,
    "CosineAnnealingLR (T_max=30)": optim.lr_scheduler.CosineAnnealingLR,
}

for name, sched_class in schedulers.items():
    optimizer = optim.Adam(model.parameters(), lr=0.1)
    if "StepLR" in name:
        scheduler = sched_class(optimizer, step_size=10, gamma=0.5)
    else:
        scheduler = sched_class(optimizer, T_max=30)

    lrs = []
    for epoch in range(30):
        for Xb, yb in loader:
            optimizer.zero_grad()
            loss = criterion(model(Xb).squeeze(), yb.float())
            loss.backward()
            optimizer.step()
        lrs.append(optimizer.param_groups[0]['lr'])
        scheduler.step()

    print(f"\n{name}:")
    for i, lr in enumerate(lrs):
        marker = " *" if lr < lrs[i-1] and i > 0 else ""
        print(f"  epoch {i:2d}: lr = {lr:.6f}{marker}")

print("\n\nReduceLROnPlateau (on validation loss):")
optimizer = optim.Adam(model.parameters(), lr=0.1)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, factor=0.5)

lrs = []
for epoch in range(30):
    for Xb, yb in loader:
        optimizer.zero_grad()
        loss = criterion(model(Xb).squeeze(), yb.float())
        loss.backward()
        optimizer.step()
    lrs.append(optimizer.param_groups[0]['lr'])
    scheduler.step(loss)

for i, lr in enumerate(lrs):
    marker = " *" if i > 0 and lr < lrs[i-1] else ""
    print(f"  epoch {i:2d}: lr = {lr:.6f}{marker}")
