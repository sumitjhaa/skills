"""Linear regression with nn.Linear — using nn module and optim."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Linear Regression with nn.Linear ===\n")

torch.manual_seed(42)
true_w, true_b = 3.5, 1.2
X = torch.randn(200, 1)
y = true_w * X + true_b + torch.randn(200, 1) * 0.5

model = nn.Linear(1, 1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

print(f"True w={true_w}, b={true_b}")
print(f"{'Epoch':>6} | {'Loss':>8} | {'w':>8} | {'b':>8}")
print("-" * 40)

for epoch in range(200):
    y_pred = model(X)
    loss = criterion(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 40 == 0 or epoch == 199:
        w_l, b_l = model.weight.item(), model.bias.item()
        print(f"{epoch:6d} | {loss.item():8.4f} | {w_l:8.4f} | {b_l:8.4f}")

print(f"\nLearned: w={model.weight.item():.4f}, b={model.bias.item():.4f}")
print(f"True:    w={true_w}, b={true_b}")
print(f"\nPattern: optimizer.zero_grad() → loss.backward() → optimizer.step()")
