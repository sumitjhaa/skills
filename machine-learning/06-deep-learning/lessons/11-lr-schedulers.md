# 06.11 LR Schedulers

Learning rate schedules adjust the learning rate during training to balance convergence speed and stability.

## Step Decay

η_t = η_0 · γ^{⌊t/step_size⌋}

Drop LR by factor γ every step_size epochs. Simple and effective.

## Exponential Decay

η_t = η_0 · γ^t

Smooth, continuous decay. γ close to 1 (e.g., 0.95).

## Cosine Annealing

η_t = η_min + 0.5(η_0 - η_min)(1 + cos(tπ/T))

Smooth cosine-shaped decay from η_0 to η_min over T steps. Popular with warmup.

## Cosine with Warm Restarts (SGDR)

Resets LR periodically. Helpful for escaping local minima.

## OneCycleLR

Triangular schedule: warmup from η_0/div to η_0, then anneal to η_0/div. Combines high LR exploration with low LR convergence.

## Warmup

η_t = η_0 · (t / warmup_steps) for t < warmup_steps

Gradually increases LR at the start to prevent early instability (especially for Adam).

## ReduceLROnPlateau

Reduce LR when a metric (e.g., validation loss) stops improving. Adaptive to training dynamics.

## Polynomial Decay

η_t = η_0 · (1 - t/T)^p

p=1: linear, p=2: quadratic. Natural for long training runs.

## Best Practices

- Always warmup for transformer-based models (5-10% of total steps)
- Cosine decay often works better than step decay
- OneCycleLR can train faster with higher peak LR
- Monitor loss curve to detect when LR reduction helps
