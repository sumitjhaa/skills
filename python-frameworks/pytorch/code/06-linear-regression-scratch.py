"""Linear regression from scratch — manual w, b with autograd."""
import torch


print("=== Linear Regression from Scratch ===\n")

torch.manual_seed(42)
true_w, true_b = 3.5, 1.2
X = torch.randn(200, 1)
y = true_w * X + true_b + torch.randn(200, 1) * 0.5

w = torch.randn(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
lr = 0.01

print(f"True w={true_w}, b={true_b}")
print(f"{'Epoch':>6} | {'Loss':>8} | {'w':>8} | {'b':>8}")
print("-" * 40)

for epoch in range(200):
    y_pred = X @ w + b
    loss = ((y_pred - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    w.grad.zero_()
    b.grad.zero_()

    if epoch % 40 == 0 or epoch == 199:
        print(f"{epoch:6d} | {loss.item():8.4f} | {w.item():8.4f} | {b.item():8.4f}")

print(f"\nLearned: w={w.item():.4f}, b={b.item():.4f}")
print(f"True:    w={true_w}, b={true_b}")
