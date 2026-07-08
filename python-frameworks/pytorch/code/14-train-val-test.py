"""Train/validation/test split with DataLoaders."""
import torch
from torch.utils.data import TensorDataset, DataLoader


print("=== Train/Val/Test Split ===\n")

torch.manual_seed(42)
X = torch.randn(1000, 4)
y = torch.randint(0, 3, (1000,))

n = len(X)
train_end = int(0.7 * n)
val_end = int(0.85 * n)

X_train, X_val, X_test = X[:train_end], X[train_end:val_end], X[val_end:]
y_train, y_val, y_test = y[:train_end], y[train_end:val_end], y[val_end:]

train_dataset = TensorDataset(X_train, y_train)
val_dataset = TensorDataset(X_val, y_val)
test_dataset = TensorDataset(X_test, y_test)

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

print(f"Total samples: {n}")
print(f"Train: {len(train_dataset)} ({100*len(train_dataset)//n}%)")
print(f"Val:   {len(val_dataset)} ({100*len(val_dataset)//n}%)")
print(f"Test:  {len(test_dataset)} ({100*len(test_dataset)//n}%)")
print(f"Batch size: {batch_size}")
print(f"Train batches/epoch: {len(train_loader)}")
print(f"Val batches/epoch:   {len(val_loader)}")
print(f"Test batches/epoch:  {len(test_loader)}")

print("\nRule: Train=60-80%, Val=10-20%, Test=10-20%")
print("Shuffle: Train only (not val/test)")
