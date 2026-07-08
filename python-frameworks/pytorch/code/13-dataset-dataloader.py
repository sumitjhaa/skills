"""Dataset and DataLoader — batching, shuffling, custom datasets."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, TensorDataset


print("=== Dataset & DataLoader ===\n")

torch.manual_seed(42)
X = torch.randn(100, 4)
y = torch.randn(100, 1)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

print(f"Dataset size: {len(dataset)}")
print(f"Batch size: 16")
print(f"Batches per epoch: {len(loader)}")

for batch_idx, (X_batch, y_batch) in enumerate(loader):
    print(f"  Batch {batch_idx}: X shape {X_batch.shape}, y shape {y_batch.shape}")
    if batch_idx == 2:
        break

print("\nCustom Dataset:")
class CustomDataset(Dataset):
    def __init__(self, n=50):
        self.X = torch.randn(n, 3)
        self.y = torch.randn(n)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

custom = CustomDataset()
custom_loader = DataLoader(custom, batch_size=10, shuffle=True)
Xb, yb = next(iter(custom_loader))
print(f"  Custom dataset batch: X {Xb.shape}, y {yb.shape}")

print(f"\nDataLoader params:")
print(f"  batch_size:  samples per batch")
print(f"  shuffle:     randomize order (train only)")
print(f"  drop_last:   drop incomplete final batch")
