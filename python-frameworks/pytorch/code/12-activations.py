"""Activation functions — ReLU, Sigmoid, Tanh, LeakyReLU, GELU, Softmax."""
import torch
import torch.nn as nn


print("=== Activation Functions ===\n")

x = torch.linspace(-3, 3, 7)
print(f"Input: {x}\n")

activations = {
    "ReLU": nn.ReLU(),
    "LeakyReLU(0.1)": nn.LeakyReLU(0.1),
    "Sigmoid": nn.Sigmoid(),
    "Tanh": nn.Tanh(),
    "GELU": nn.GELU(),
}

for name, act in activations.items():
    y = act(x)
    print(f"{name:<15}: {y}")

print("\nSoftmax (multi-class probabilities):")
logits = torch.tensor([[2.0, 1.0, 0.1], [0.5, 3.0, 0.2]])
probs = nn.Softmax(dim=1)(logits)
print(f"  logits:\n{logits}")
print(f"  probabilities:\n{probs}")
print(f"  sums to 1 per row: {probs.sum(dim=1)}")

print("\nChoosing guide:")
print("  Hidden layers: ReLU (or LeakyReLU if dead neurons)")
print("  Binary output: Sigmoid (with BCEWithLogitsLoss)")
print("  Multi-class:   Softmax (with CrossEntropyLoss)")
print("  RNNs:          Tanh")
