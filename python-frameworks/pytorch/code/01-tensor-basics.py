"""Tensor basics — creation, dtypes, device, shape, numel."""
import torch


print("=== Tensor Basics ===\n")

t1 = torch.tensor([1, 2, 3])
print(f"t1: {t1}, dtype={t1.dtype}")

t2 = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
print(f"t2:\n{t2}")

z = torch.zeros(3, 4)
print(f"zeros(3,4): shape={z.shape}, dtype={z.dtype}")

o = torch.ones(2, 3)
print(f"ones(2,3): shape={o.shape}")

e = torch.eye(3)
print(f"eye(3):\n{e}")

r = torch.randn(2, 2)
print(f"randn(2,2):\n{r}")

print(f"\nDevice check: CUDA available = {torch.cuda.is_available()}")
device = "cuda" if torch.cuda.is_available() else "cpu"
t = torch.tensor([1, 2, 3], device=device)
print(f"Tensor on {device}: {t}")

t3 = torch.randn(2, 3, 4)
print(f"\n3D tensor:")
print(f"  ndim={t3.ndim}, shape={t3.shape}, numel={t3.numel()}")
print(f"  total elements = {t3.numel()}")
