# 🏗️ Weight Initialization
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** How initialization affects training.

## Built-in Initializations

```python
nn.init.xavier_uniform_(tensor)    # Xavier/Glorot
nn.init.xavier_normal_(tensor)
nn.init.kaiming_uniform_(tensor)   # He/Kaiming
nn.init.kaiming_normal_(tensor)
nn.init.normal_(tensor, mean=0, std=0.01)
nn.init.zeros_(tensor)
nn.init.ones_(tensor)
```

## When to Use What

| Activation | Init | Reason |
|------------|------|--------|
| ReLU | Kaiming | Accounts for ReLU's zero half |
| Tanh | Xavier | Balanced for tanh range |
| Sigmoid | Xavier | Balanced for sigmoid range |

## Defaults

PyTorch uses Kaiming uniform by default for `nn.Linear` and `nn.Conv2d`. You rarely need to change it.

```python
# Custom init function
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)

model.apply(init_weights)
```

<!-- 🤔 Modern architectures rarely need manual init — PyTorch's defaults work well. -->

## Run the Code

```bash
python code/39-weight-init.py
```
