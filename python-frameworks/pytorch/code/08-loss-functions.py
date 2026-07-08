"""Loss functions — MSELoss, L1Loss, BCEWithLogitsLoss, CrossEntropyLoss."""
import torch
import torch.nn as nn


print("=== Loss Functions ===\n")

print("Regression losses:")
pred = torch.tensor([2.5, 0.0, 2.0, 8.0])
target = torch.tensor([3.0, -0.5, 2.0, 7.0])

mse = nn.MSELoss()
l1 = nn.L1Loss()
print(f"  pred:     {pred}")
print(f"  target:   {target}")
print(f"  MSE:      {mse(pred, target):.4f}")
print(f"  L1 (MAE): {l1(pred, target):.4f}")

print("\nBinary classification (BCEWithLogitsLoss):")
logits = torch.tensor([2.0, -1.5, 0.1, -3.0])
labels = torch.tensor([1.0, 0.0, 1.0, 0.0])
bce = nn.BCEWithLogitsLoss()
print(f"  logits: {logits}")
print(f"  labels: {labels}")
print(f"  BCE loss: {bce(logits, labels):.4f}")

print("\nMulti-class (CrossEntropyLoss):")
logits = torch.tensor([[2.0, 0.5, -1.0], [0.1, 3.0, -0.2]])
targets = torch.tensor([0, 1])
ce = nn.CrossEntropyLoss()
print(f"  logits shape: {logits.shape}")
print(f"  targets: {targets}")
print(f"  CE loss: {ce(logits, targets):.4f}")

print("\nKey: Use WithLogits variants for numerical stability.")
