# 06.30 Loss Symmetries

Techniques for modifying loss computation to improve training dynamics and model quality.

## Label Smoothing

Replace one-hot targets with smoothed targets:

y_smooth = (1 - ε) · y_onehot + ε / K

where K = number of classes, ε ≈ 0.1.

**Effect**: Prevents overconfidence, improves calibration, helps generalization.

**Gradient effect**: Reduces magnitude of logit gradient, prevents logits from growing indefinitely.

## Margin Losses

Force a margin between correct and incorrect predictions:

L = Σ max(0, Δ + (s_j - s_y))  (Multi-class hinge loss, Crammer-Singer)

where s_j is score for class j, y is correct class, Δ is margin.

## Contrastive Loss

L = y · d² + (1-y) · max(0, m-d)²

- y = 1: similar pairs pulled together
- y = 0: dissimilar pairs pushed apart (if within margin m)

## Triplet Loss

L = max(0, d(a, p)² - d(a, n)² + m)

Anchor (a), positive (p), negative (n). Margin m ensures separation. Used in FaceNet, metric learning.

Mining: hard negative mining selects informative triplets (where d(a, p) > d(a, n)).

## Center Loss

L = L_CE + λ · ||x_i - c_{y_i}||²

Pulls features toward their class center. Used with softmax for face recognition.

## ArcFace / CosFace

Add margin in angular space:

ArcFace: L = -log(e^{s·cos(θ_y+m)} / (e^{s·cos(θ_y+m)} + Σ e^{s·cos(θ_j)}))

Instead of modifying logits, modifies the angle between feature and weight vector.

## InfoNCE (Contrastive Prediction)

L = -log(e^{sim(q,k⁺)/τ} / Σ e^{sim(q,k_i)/τ})

Used in self-supervised learning (SimCLR, MoCo). Temperature τ controls concentration.

## Comparison

| Method | Use Case | Key Hyperparameter |
|--------|----------|-------------------|
| Label Smoothing | Classification | ε = 0.1 |
| Triplet Loss | Metric learning | margin = 1.0 |
| Contrastive Loss | Siamese networks | margin = 1.0 |
| InfoNCE | Self-supervised | τ = 0.1 |
| ArcFace | Face recognition | margin = 0.5 |
