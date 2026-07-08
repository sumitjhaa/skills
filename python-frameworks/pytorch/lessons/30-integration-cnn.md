# 🏗️ Integration: CNN Image Classification
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Complete CNN pipeline with training, validation, and evaluation.

## Full Pipeline

```python
1. Generate/load image data
2. Train/val/test split
3. CNN with conv layers → flatten → classifier
4. BCEWithLogitsLoss for binary classification
5. Adam optimizer with ReduceLROnPlateau
6. Per-epoch validation
7. Final test evaluation
```

## CNN Architecture

```
Conv2d(1→16, 3×3) → ReLU → MaxPool(2×2)
Conv2d(16→32, 3×3) → ReLU → MaxPool(2×2)
Flatten
Linear(32*2*2 → 32) → ReLU
Linear(32 → 1)
```

## Tips

- Start with 2-3 conv layers for small images
- Flatten before linear layers
- Use `BCEWithLogitsLoss` (not raw BCE)
- `model.eval()` before validation/testing

<!-- 🤔 This CNN pattern generalizes to real image datasets — just change input channels and image size. -->

## Run the Code

```bash
python code/30-integration-cnn.py
```
