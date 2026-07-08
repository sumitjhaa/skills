"""Optimizers — SGD, Adam, RMSprop comparison."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Optimizers ===\n")

torch.manual_seed(42)
true_w, true_b = 3.5, 1.2
X = torch.randn(200, 1)
y = true_w * X + true_b + torch.randn(200, 1) * 0.5

def train_with(opt_name, opt_class, lr, **kwargs):
    model = nn.Linear(1, 1)
    criterion = nn.MSELoss()
    optimizer = opt_class(model.parameters(), lr=lr, **kwargs)

    for epoch in range(100):
        y_pred = model(X)
        loss = criterion(y_pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return loss.item(), model.weight.item(), model.bias.item()

print(f"{'Optimizer':<15} | {'Final Loss':>10} | {'w':>8} | {'b':>8}")
print("-" * 50)

results = []
for name, opt_class, lr, kwargs in [
    ("SGD", optim.SGD, 0.01, {}),
    ("SGD+Momentum", optim.SGD, 0.01, {"momentum": 0.9}),
    ("Adam", optim.Adam, 0.01, {}),
    ("RMSprop", optim.RMSprop, 0.01, {}),
    ("AdamW", optim.AdamW, 0.01, {}),
]:
    loss_val, w, b = train_with(name, opt_class, lr, **kwargs)
    results.append((name, loss_val, w, b))
    print(f"{name:<15} | {loss_val:10.4f} | {w:8.4f} | {b:8.4f}")

print(f"\nTrue: w={true_w}, b={true_b}")
print("\nAdam is usually the best default optimizer.")
