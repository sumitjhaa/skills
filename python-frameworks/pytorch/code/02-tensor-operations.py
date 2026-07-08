"""Tensor operations — indexing, slicing, reshaping, broadcasting, math."""
import torch


print("=== Tensor Operations ===\n")

t = torch.arange(16).reshape(4, 4).float()
print(f"t:\n{t}\n")

print(f"First row: {t[0]}")
print(f"Second column: {t[:, 1]}")
print(f"Submatrix 1:3, 1:3:\n{t[1:3, 1:3]}")
print(f"t > 7: {t[t > 7]}")

print(f"\nReshaping:")
print(f"  view(2, 8):\n{t.view(2, 8)}")
print(f"  flatten: {t.flatten()}")
print(f"  unsqueeze(0) shape: {t.unsqueeze(0).shape}")

print(f"\nBroadcasting:")
a = torch.tensor([[1], [2], [3]], dtype=torch.float32)
b = torch.tensor([[10, 20, 30, 40]], dtype=torch.float32)
print(f"  a shape: {a.shape}, b shape: {b.shape}")
print(f"  a + b:\n{a + b}")

print(f"\nMatmul:")
m1 = torch.randn(3, 4)
m2 = torch.randn(4, 2)
result = m1 @ m2
print(f"  ({m1.shape}) @ ({m2.shape}) = {result.shape}")

print(f"\nReductions:")
print(f"  sum: {t.sum().item():.1f}, mean: {t.mean().item():.2f}")
print(f"  sum over dim 0: {t.sum(dim=0)}")
print(f"  mean over dim 1: {t.mean(dim=1)}")
