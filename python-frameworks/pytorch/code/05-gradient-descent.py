"""Gradient descent — manual optimization loop."""
import torch


print("=== Gradient Descent ===\n")

x = torch.tensor([5.0], requires_grad=True)
lr = 0.1

print(f"Minimizing f(x) = x^2 + 2x + 1, starting at x={x.item()}")
print(f"  True minimum at x=-1\n")

values = []
for step in range(20):
    y = x**2 + 2*x + 1
    y.backward()
    with torch.no_grad():
        x -= lr * x.grad
    x.grad.zero_()
    values.append((step, x.item(), y.item()))

for step, xv, yv in values:
    print(f"  step {step:2d}: x={xv:.6f}, f(x)={yv:.6f}")

print(f"\nFinal x={x.item():.6f} (expected ≈ -1.0)")

print("\nLearning rate comparison:")
print(f"  lr=0.01: converges slowly")
print(f"  lr=0.1:  good convergence (used above)")
print(f"  lr=1.0:  may overshoot/oscillate")
