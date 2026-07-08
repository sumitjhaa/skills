# 🏗️ Gradient Clipping
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Prevent exploding gradients with gradient clipping.

## Why Clip?

- Exploding gradients → NaN loss
- Common in RNNs and deep networks
- Training becomes unstable

## Usage

```python
# Before optimizer.step()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=0.5)
```

## Norm vs Value Clipping

| Method | Behavior | Use Case |
|--------|----------|----------|
| `clip_grad_norm_` | Scales all gradients to max norm | General |
| `clip_grad_value_` | Clips each gradient to value | Simple cap |

## Typical Values

```python
clip_grad_norm_(model.parameters(), max_norm=0.5)   # conservative
clip_grad_norm_(model.parameters(), max_norm=1.0)   # default
clip_grad_norm_(model.parameters(), max_norm=5.0)   # aggressive
```

<!-- 🤔 Always clip when training RNNs or very deep networks. Good default: max_norm=1.0. -->

## Run the Code

```bash
python code/38-gradient-clipping.py
```
