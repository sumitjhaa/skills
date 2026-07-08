"""Random tensors & seeding — reproducibility."""
import torch


print("=== Random Tensors & Seeding ===\n")

print("Random tensors (different each run):")
print(f"  rand(2,3):\n{torch.rand(2, 3)}")
print(f"  randn(2,3):\n{torch.randn(2, 3)}")
print(f"  randint(0, 10, (5,)): {torch.randint(0, 10, (5,))}")
print(f"  randperm(5): {torch.randperm(5)}")

print("\nWith seed (deterministic):")
torch.manual_seed(42)
t1 = torch.randn(3)
print(f"  First run: {t1}")

torch.manual_seed(42)
t2 = torch.randn(3)
print(f"  Second run: {t2}")
print(f"  Equal: {torch.equal(t1, t2)}")

print("\nDistributions:")
u = torch.empty(3, 3).uniform_(0, 1)
print(f"  Uniform(0,1):\n{u}")

n = torch.normal(mean=5, std=2, size=(5,))
print(f"  Normal(5, 2): {n}")

print(f"\nSeeding ensures reproducible experiments.")
