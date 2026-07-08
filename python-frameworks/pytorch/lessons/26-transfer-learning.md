# 🏗️ Transfer Learning
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Leverage pretrained models for new tasks.

## Freezing Layers

```python
for param in pretrained_model.parameters():
    param.requires_grad = False

# Replace classifier
num_features = pretrained_model.fc.in_features
pretrained_model.fc = nn.Linear(num_features, n_classes)

# Only classifier will train
optimizer = optim.Adam(pretrained_model.fc.parameters(), lr=0.001)
```

## When to Transfer Learn

| Dataset Size | Similar to Pretrained | Different from Pretrained |
|-------------|----------------------|--------------------------|
| Small | Fine-tune classifier | Harder — may overfit |
| Large | Fine-tune a few layers | Fine-tune whole model |

## Steps

1. Load pretrained model
2. Freeze base layers
3. Replace classifier head
4. Train classifier only (few epochs)
5. Optionally unfreeze and fine-tune entire model

<!-- 🤔 Transfer learning is the reason PyTorch has `torchvision.models` and `huggingface`. -->

## Run the Code

```bash
python code/26-transfer-learning.py
```
