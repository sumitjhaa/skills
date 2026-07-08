# 40. Loss Landscape Visualization

## Introduction

Loss landscapes — the geometry of the loss function as a function of parameters — determine optimization difficulty and generalization. Visualizing them provides insights into optimizer behavior and model properties.

## 1D Slices

Plot loss along a line connecting two points in parameter space:

```
f(α) = L((1 - α)θ₀ + αθ₁)
```

```python
import numpy as np
import matplotlib.pyplot as plt

def loss_1d_slice(model, loss_fn, theta_0, theta_1, n_points=100):
    """1D slice of loss landscape between two parameter sets."""
    alphas = np.linspace(-1, 2, n_points)
    losses = []

    for alpha in alphas:
        theta = (1 - alpha) * theta_0 + alpha * theta_1
        losses.append(loss_fn(model, theta))

    return alphas, np.array(losses)
```

## 2D Slices

Use two random directions to create a 2D projection:

```
f(α, β) = L(θ* + αδ₁ + βδ₂)
```

```python
def loss_2d_slice(model, loss_fn, theta_star, n_points=50):
    """2D loss landscape near a minimum."""
    np.random.seed(42)
    d1 = np.random.randn(len(theta_star))
    d1 = d1 / np.linalg.norm(d1)

    d2 = np.random.randn(len(theta_star))
    d2 = d2 / np.linalg.norm(d2)
    d2 = d2 - np.dot(d2, d1) * d1  # orthogonalize
    d2 = d2 / np.linalg.norm(d2)

    alphas = np.linspace(-1, 1, n_points)
    betas = np.linspace(-1, 1, n_points)
    Z = np.zeros((n_points, n_points))

    for i, alpha in enumerate(alphas):
        for j, beta in enumerate(betas):
            theta = theta_star + alpha * d1 + beta * d2
            Z[j, i] = loss_fn(model, theta)

    return alphas, betas, Z
```

## Filter Normalization

Random directions can be misleading due to parameter scale differences. Filter normalization scales directions per layer:

```python
def filter_normalized_direction(theta, seed=0):
    """Generate a direction with per-filter normalization."""
    rng = np.random.RandomState(seed)
    direction = []

    for w in theta:
        d = rng.randn(*w.shape)
        # Normalize each filter to have same norm as original
        if w.ndim >= 2:
            for i in range(w.shape[0]):
                d[i] = d[i] * np.linalg.norm(w[i]) / (np.linalg.norm(d[i]) + 1e-10)
        direction.append(d)

    return direction
```

## Sharp vs. Flat Minima

Sharp minima (high curvature) generalize poorly, while flat minima (low curvature) generalize well:

```python
def curvature_estimate(loss_fn, theta, epsilon=0.01):
    """Estimate curvature via finite differences."""
    d = np.random.randn(len(theta))
    d = d / np.linalg.norm(d)

    f_plus = loss_fn(theta + epsilon * d)
    f_minus = loss_fn(theta - epsilon * d)
    f_center = loss_fn(theta)

    # Second derivative estimate
    hessian_direction = (f_plus - 2*f_center + f_minus) / (epsilon**2)
    return hessian_direction
```

## Visualization Techniques

```python
def plot_loss_landscape(alphas, betas, Z, trajectory=None):
    """Plot 2D loss landscape with contour and optional trajectory."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Contour plot
    levels = np.logspace(-1, 2, 20)  # log-spaced for better visibility
    cs = ax1.contour(alphas, betas, Z, levels=levels, cmap='viridis')
    ax1.set_xlabel('Direction 1')
    ax1.set_ylabel('Direction 2')
    ax1.set_title('Loss Landscape (Contour)')

    if trajectory is not None:
        ax1.plot(trajectory[:, 0], trajectory[:, 1], 'r-', linewidth=2)
        ax1.plot(trajectory[0, 0], trajectory[0, 1], 'go', label='Start')
        ax1.plot(trajectory[-1, 0], trajectory[-1, 1], 'r*', label='End')
        ax1.legend()

    # 3D surface
    from mpl_toolkits.mplot3d import Axes3D
    ax2 = fig.add_subplot(122, projection='3d')
    A, B = np.meshgrid(alphas, betas)
    surf = ax2.plot_surface(A, B, Z, cmap='viridis', alpha=0.8)
    ax2.set_xlabel('α'); ax2.set_ylabel('β'); ax2.set_zlabel('Loss')

    plt.tight_layout()
    plt.show()
```

## Key Insights from Landscape Visualizations

1. **Loss surfaces are highly non-convex** but have connected low-loss regions
2. **SGD finds flat minima** that generalize well
3. **Batch normalization smooths the landscape**, making optimization easier
4. **Wider networks have smoother landscapes**
5. **Sharp minima correlate with poor generalization**
6. **Optimizer path visualization** reveals different exploration strategies

## What You'll Implement

- 1D and 2D loss landscape slices
- Filter-normalized plotting directions
- Contour and 3D surface plots
- Optimizer trajectory overlay
- Curvature estimation at minima
- Comparison of sharp vs. flat minima
