# 🏗️ nn.Sequential & Model Building
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Build neural networks with `nn.Sequential`.

## Sequential API

```python
model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
)
```

## Custom Module vs Sequential

```python
# Sequential — simple feed-forward
model = nn.Sequential(...)
model(x)  # forward pass

# Custom Module — complex logic
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(...)

    def forward(self, x):
        return self.net(x)
```

## Inspecting Layers

```python
model[0]  # first layer
model.add_module('dropout', nn.Dropout(0.5))
```

<!-- 🤔 Use Sequential for simple stacks. Use custom nn.Module for complex architectures. -->

## Run the Code

```bash
python code/11-nn-sequential.py
```
