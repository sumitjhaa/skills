# 06.09 Loss Functions

Loss functions quantify the error between predictions and targets, driving gradient-based learning.

## MSE (Mean Squared Error)

L = (1/n) Σ (ŷ - y)²

Used for regression. Sensitive to outliers. ∂L/∂ŷ = (2/n)(ŷ - y).

## MAE (Mean Absolute Error)

L = (1/n) Σ |ŷ - y|

Robust to outliers. Gradient is constant (±1/n), not vanishing.

## Cross-Entropy (Binary)

L = -[y log(ŷ) + (1-y) log(1-ŷ)]

Used for binary classification. Pairs with sigmoid output.

## Cross-Entropy (Categorical)

L = -Σ y_i log(ŷ_i)

Used for multi-class classification. Pairs with softmax output.

## Hinge Loss

L = max(0, 1 - y · ŷ)

Used for SVMs. Max-margin objective.

## Huber Loss

L = 0.5(ŷ-y)² if |ŷ-y| ≤ δ, else δ|ŷ-y| - 0.5δ²

Combines MSE and MAE. Quadratic for small errors, linear for large.

## Focal Loss

L = -(1-ŷ)^γ log(ŷ)

Down-weights well-classified examples. γ ≥ 0. Used in object detection (RetinaNet).

## KL Divergence

D_KL(P||Q) = Σ P(i) log(P(i)/Q(i))

Measures distribution divergence. Used in VAEs, knowledge distillation.

## Contrastive Loss

L = yd² + (1-y)max(0, margin-d)²

Used in siamese networks. Pulls similar pairs together, pushes dissimilar apart.

## Choosing a Loss

| Task | Loss |
|------|------|
| Regression | MSE, MAE, Huber |
| Binary classification | BCE |
| Multi-class classification | Cross-entropy |
| Imbalanced classes | Focal |
| Metric learning | Contrastive, Triplet |
