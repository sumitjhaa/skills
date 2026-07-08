"""Weight initialization — impact of different init strategies."""
import torch
import torch.nn as nn


print("=== Weight Initialization ===\n")

def init_weights(model, method):
    for m in model.modules():
        if isinstance(m, nn.Linear):
            if method == 'xavier':
                nn.init.xavier_uniform_(m.weight)
            elif method == 'kaiming':
                nn.init.kaiming_uniform_(m.weight, nonlinearity='relu')
            elif method == 'normal':
                nn.init.normal_(m.weight, mean=0, std=0.01)
            elif method == 'zeros':
                nn.init.zeros_(m.weight)
            if m.bias is not None:
                nn.init.zeros_(m.bias)

model = nn.Sequential(
    nn.Linear(10, 64), nn.ReLU(),
    nn.Linear(64, 32), nn.ReLU(),
    nn.Linear(32, 1),
)

methods = ['xavier', 'kaiming', 'normal', 'zeros']
x = torch.randn(50, 10)

print(f"{'Method':<10} | {'Mean':>8} | {'Std':>8} | {'Min':>8} | {'Max':>8}")
print("-" * 50)

for method in methods:
    init_weights(model, method)
    with torch.no_grad():
        out = model(x)
    print(f"{method:<10} | {out.mean():8.4f} | {out.std():8.4f} | {out.min():8.4f} | {out.max():8.4f}")

print("\nGuidelines:")
print("  ReLU:     Kaiming uniform (default)")
print("  Tanh:     Xavier uniform")
print("  Deep:     Kaiming or Xavier")
print("\nPyTorch uses Kaiming uniform by default for Linear layers.")
