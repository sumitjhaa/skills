"""CNN basics — Conv2d, pooling, and feature maps."""
import torch
import torch.nn as nn


print("=== CNN Basics ===\n")

x = torch.randn(4, 1, 28, 28)  # N, C, H, W
print(f"Input shape: {x.shape}")

conv = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
out = conv(x)
print(f"After Conv2d(1→16, 3x3): {out.shape}")
print(f"  Weight shape: {conv.weight.shape}")
print(f"  Params: {sum(p.numel() for p in conv.parameters())}")

pool = nn.MaxPool2d(kernel_size=2, stride=2)
out = pool(out)
print(f"After MaxPool2d(2x2): {out.shape}")

print("\nTypical CNN block:")
block = nn.Sequential(
    nn.Conv2d(1, 32, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Conv2d(32, 64, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(64 * 7 * 7, 10),
)
out = block(x)
print(f"  Input:  {x.shape}")
print(f"  Output: {out.shape}")

print(f"\nTotal params: {sum(p.numel() for p in block.parameters()):,}")
