"""Autograd — automatic differentiation with backward()."""
import torch


print("=== Autograd ===\n")

x = torch.tensor([2.0, 3.0], requires_grad=True)
print(f"x: {x}")

y = x**2 + 2*x + 1
print(f"y = x^2 + 2x + 1: {y}")
print(f"Sum: {y.sum()}")

y.sum().backward()
print(f"Gradient dy/dx: {x.grad}")  # 2x + 2 = [6, 8]

print("\nMulti-step graph:")
a = torch.tensor([3.0], requires_grad=True)
b = a * 2
c = b ** 2
d = c.mean()
d.backward()
print(f"  a={a.item()}, b={b.item()}, c={c.item()}, d={d.item()}")
print(f"  grad of a: {a.grad.item()}")  # 4*b = 4*6 = 24

print("\nNo-grad context:")
with torch.no_grad():
    z = x * 2
print(f"  z (no grad): {z}, requires_grad: {z.requires_grad}")

print("\nDetach:")
x2 = torch.tensor([4.0], requires_grad=True)
y2 = x2.detach()
print(f"  y2 requires_grad: {y2.requires_grad}")
