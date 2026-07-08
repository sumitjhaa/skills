# 06.10 Optimizer Zoo

Optimizers update parameters to minimize the loss function. Each variant addresses specific challenges in gradient descent.

## SGD (Stochastic Gradient Descent)

θ_{t+1} = θ_t - η · ∇L(θ_t)

Simple, but sensitive to learning rate and slow along ravines.

## SGD with Momentum

v_t = β · v_{t-1} + ∇L(θ_t)
θ_{t+1} = θ_t - η · v_t

Accumulates velocity. Dampens oscillations. β typically 0.9.

## Nesterov Accelerated Gradient (NAG)

v_t = β · v_{t-1} + ∇L(θ_t - β · v_{t-1})
θ_{t+1} = θ_t - η · v_t

"Look ahead" before computing gradient. Faster convergence than standard momentum.

## AdaGrad

G_t = G_{t-1} + ∇L(θ_t)²
θ_{t+1} = θ_t - η · ∇L(θ_t) / √(G_t + ε)

Per-parameter learning rates. Accumulates squared gradients in denominator. Learning rate decays aggressively.

## RMSprop

G_t = β · G_{t-1} + (1-β) · ∇L(θ_t)²
θ_{t+1} = θ_t - η · ∇L(θ_t) / √(G_t + ε)

Exponential moving average of squared gradients. Fixes AdaGrad's aggressive decay.

## Adam (Adaptive Moment Estimation)

m_t = β₁·m_{t-1} + (1-β₁)·∇L(θ_t)
v_t = β₂·v_{t-1} + (1-β₂)·∇L(θ_t)²
m̂_t = m_t / (1-β₁^t), v̂_t = v_t / (1-β₂^t)
θ_{t+1} = θ_t - η · m̂_t / (√v̂_t + ε)

Combines momentum (m) with adaptive learning rates (v). Bias-corrected. Default: β₁=0.9, β₂=0.999, ε=1e-8.

## AdamW

Same as Adam but decouples weight decay from gradient update:

θ_{t+1} = θ_t - η(m̂_t/(√v̂_t+ε) + λ·θ_t)

Often generalizes better than Adam.

## Comparison

| Optimizer | Adaptive | Momentum | Bias Correction | Weight Decay |
|-----------|----------|----------|-----------------|--------------|
| SGD | No | No | No | Manual |
| Momentum | No | Yes | No | Manual |
| AdaGrad | Yes | No | No | Manual |
| RMSprop | Yes | No | No | Manual |
| Adam | Yes | Yes | Yes | Manual |
| AdamW | Yes | Yes | Yes | Decoupled |
