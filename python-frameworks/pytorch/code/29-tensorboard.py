"""TensorBoard — logging metrics and model graphs."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
import tempfile
import os


print("=== TensorBoard ===\n")

tmpdir = tempfile.mkdtemp()
log_dir = os.path.join(tmpdir, "runs", "demo")
writer = SummaryWriter(log_dir)
print(f"Logging to: {log_dir}")

torch.manual_seed(42)
X = torch.randn(200, 4)
y = (X.sum(dim=1, keepdim=True) > 0).float()

model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

dummy_input = torch.randn(1, 4)
writer.add_graph(model, dummy_input)

print(f"{'Epoch':>6} | {'Loss':>8} | {'Acc':>8}")
print("-" * 30)

for epoch in range(30):
    model.train()
    optimizer.zero_grad()
    loss = criterion(model(X).squeeze(), y.squeeze())
    loss.backward()
    optimizer.step()

    with torch.no_grad():
        acc = ((torch.sigmoid(model(X).squeeze()) > 0.5) == y.squeeze()).float().mean()

    writer.add_scalar('Loss/train', loss.item(), epoch)
    writer.add_scalar('Accuracy/train', acc.item(), epoch)
    writer.add_scalar('LR', optimizer.param_groups[0]['lr'], epoch)

    if epoch % 5 == 0:
        print(f"{epoch:6d} | {loss.item():8.4f} | {acc.item():8.4f}")

for name, param in model.named_parameters():
    writer.add_histogram(f'parameters/{name}', param, 0)

writer.close()
print(f"\nLogs written to {log_dir}")
print(f"View with: tensorboard --logdir={os.path.join(tmpdir, 'runs')}")

import shutil
shutil.rmtree(tmpdir)
print("Cleaned up temp files.")
