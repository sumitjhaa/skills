"""Custom loss functions — implementing your own loss."""
import torch
import torch.nn as nn
import torch.optim as optim


print("=== Custom Loss Functions ===\n")

torch.manual_seed(42)
X = torch.randn(200, 4)
y = torch.randn(200, 1)

print("1. Custom Huber loss:")
def huber_loss(pred, target, delta=1.0):
    diff = pred - target
    abs_diff = diff.abs()
    quadratic = 0.5 * diff ** 2
    linear = delta * (abs_diff - 0.5 * delta)
    return torch.where(abs_diff <= delta, quadratic, linear).mean()

model = nn.Linear(4, 1)
optimizer = optim.SGD(model.parameters(), lr=0.01)
for epoch in range(50):
    loss = huber_loss(model(X), y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
print(f"  Final loss: {loss.item():.4f}")

print("\n2. Custom loss as nn.Module:")
class FocalLoss(nn.Module):
    def __init__(self, gamma=2.0):
        super().__init__()
        self.gamma = gamma

    def forward(self, logits, targets):
        probs = torch.sigmoid(logits)
        bce = - (targets * torch.log(probs + 1e-8) +
                 (1 - targets) * torch.log(1 - probs + 1e-8))
        p_t = probs * targets + (1 - probs) * (1 - targets)
        return (bce * (1 - p_t) ** self.gamma).mean()

focal = FocalLoss(gamma=2.0)
model2 = nn.Linear(4, 1)
optimizer2 = optim.SGD(model2.parameters(), lr=0.01)
y_binary = (y > 0).float()
for epoch in range(50):
    loss = focal(model2(X), y_binary.squeeze())
    optimizer2.zero_grad()
    loss.backward()
    optimizer2.step()
print(f"  Final focal loss: {loss.item():.4f}")

print("\n3. Weighted loss for imbalanced data:")
weights = torch.tensor([1.0, 5.0])
weighted_ce = nn.CrossEntropyLoss(weight=weights)
logits = torch.randn(10, 2)
targets = torch.randint(0, 2, (10,))
w_loss = weighted_ce(logits, targets)
print(f"  Weighted CE: {w_loss.item():.4f}")
