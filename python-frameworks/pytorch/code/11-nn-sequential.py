"""nn.Sequential — building models with sequential API."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== nn.Sequential ===\n")

model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
)
print(f"Model:\n{model}\n")

x = torch.randn(5, 10)
y = model(x)
print(f"Input shape:  {x.shape}")
print(f"Output shape: {y.shape}")

print("\nLayer access:")
for i, layer in enumerate(model):
    print(f"  [{i}] {layer}")

print("\nCustom nn.Module with Sequential:")
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        return self.net(x)

mlp = MLP()
print(f"MLP output shape: {mlp(x).shape}")
print("\nSequential is great for feed-forward models.")
