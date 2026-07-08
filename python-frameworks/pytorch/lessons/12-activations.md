# 🏗️ Activation Functions
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Common activation functions and when to use them.

## PyTorch Activations

```python
nn.ReLU()          # Most common: max(0, x)
nn.Sigmoid()       # 0..1: output gates, binary probs
nn.Tanh()          # -1..1: RNNs
nn.LeakyReLU(0.01) # Like ReLU but non-zero for x<0
nn.GELU()          # Smoother ReLU (Transformer default)
nn.Softmax(dim=1)  # Multi-class probabilities
```

## Choosing

| Activation | When to Use |
|------------|-------------|
| ReLU | Default for hidden layers |
| LeakyReLU | Dead ReLU problem |
| Sigmoid | Binary output (with BCE) |
| Tanh | RNNs, normalized outputs |
| GELU | Transformers |
| Softmax | Multi-class output |

<!-- 🤔 ReLU is the default — simple, fast, works well. -->

## Run the Code

```bash
python code/12-activations.py
```
