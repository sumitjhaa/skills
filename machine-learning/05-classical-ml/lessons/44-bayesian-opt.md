# Lesson 05.44: Bayesian Optimization

## Learning Objectives
- Understand GP-based surrogate modeling for black-box optimization
- Implement EI, UCB, and Thompson sampling acquisition functions
- Apply to hyperparameter tuning and experimental design
- Analyze sample efficiency and scaling limitations

## Setup
Find $x^* = \arg\max_{x \in \mathcal{X}} f(x)$ where:
- $f$ is a black-box (no gradient)
- $f$ is expensive to evaluate (minutes/hours)
- Observations may be noisy: $y = f(x) + \varepsilon$, $\varepsilon \sim \mathcal{N}(0, \sigma^2)$
- $\mathcal{X}$ typically low-dimensional ($d < 20$)

## Gaussian Process Surrogate
Model $f$ as GP: $f(x) \sim \mathcal{GP}(m(x), K(x, x'))$

After $t$ observations $\mathcal{D}_t = \{(x_i, y_i)\}_{i=1}^t$:

$$\mu_t(x) = K_{x, X_t} (K_{X_t, X_t} + \sigma^2 I)^{-1} y_t$$

$$\sigma_t^2(x) = K(x, x) - K_{x, X_t} (K_{X_t, X_t} + \sigma^2 I)^{-1} K_{X_t, x}$$

- $\mu_t(x)$: posterior mean (best estimate)
- $\sigma_t^2(x)$: posterior variance (uncertainty)

## Acquisition Functions

### Expected Improvement (EI)
$$\text{EI}(x) = \mathbb{E}[\max(f(x) - f^*, 0)]$$

$$= (f^* - \mu_t(x)) \Phi\left(\frac{f^* - \mu_t(x)}{\sigma_t(x)}\right) + \sigma_t(x) \phi\left(\frac{f^* - \mu_t(x)}{\sigma_t(x)}\right)$$

where $f^* = \max_i y_i$ (best observed), $\Phi$ = normal CDF, $\phi$ = normal PDF.

**If $\sigma_t(x) = 0$**: $\text{EI}(x) = 0$ (no exploration benefit). EI naturally trades off mean vs uncertainty.

### Upper Confidence Bound (UCB)
$$\text{UCB}(x) = \mu_t(x) + \kappa \sigma_t(x)$$

- $\kappa > 0$: exploration parameter
- GP-UCB theory: $\kappa_t = \sqrt{2 \log(t^{d/2+2} \pi^2 / (3\delta))}$ ensures sublinear regret with prob $1-\delta$
- Typical: $\kappa = 2$ or $\kappa = 3$

### Probability of Improvement (PoI)
$$\text{PoI}(x) = \Phi\left(\frac{\mu_t(x) - f^* - \xi}{\sigma_t(x)}\right)$$

- $\xi$ controls exploration (default $\xi = 0.0$, larger = more exploration)
- Pure exploitation when $\xi = 0$ and $\sigma_t(x) \to 0$

### Thompson Sampling
1. Sample a function from GP posterior: $\tilde{f} \sim \mathcal{GP}(\mu_t, k_t)$
2. Evaluate $\tilde{f}$ on candidate points
3. Select $x_t = \arg\max \tilde{f}(x)$

**Advantage**: Naturally handles batch settings (draw multiple samples).

## Algorithm
```
D = initial_sample(n0)  # random or Latin hypercube
for t = 1, ..., T:
    fit GP to D
    x_t = argmax acquisition(x)
    y_t = evaluate(x_t)
    D = D ∪ {(x_t, y_t)}
return best found: x* = argmax_{i} y_i
```

## Code: Expected Improvement

```python
import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

def expected_improvement(X, gp, y_best, xi=0.0):
    mu, sigma = gp.predict(X, return_std=True)
    sigma = np.maximum(sigma, 1e-10)
    imp = mu - y_best - xi
    Z = imp / sigma
    ei = imp * norm.cdf(Z) + sigma * norm.pdf(Z)
    return ei

def bayesian_optimization(f, bounds, n_init=10, n_iter=50, acq='ei'):
    d = len(bounds)
    X = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_init, d))
    y = np.array([f(x) for x in X])
    kernel = ConstantKernel(1.0) * RBF(length_scale=np.ones(d))
    gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, normalize_y=True)
    for _ in range(n_iter):
        gp.fit(X, y)
        y_best = np.max(y)
        # Optimize acquisition (grid + local search)
        X_candidates = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(10000, d))
        ei = expected_improvement(X_candidates, gp, y_best)
        x_next = X_candidates[np.argmax(ei)]
        y_next = f(x_next)
        X = np.vstack([X, x_next])
        y = np.append(y, y_next)
    return X[np.argmax(y)], np.max(y)
```

## Practical Considerations
- **Kernel choice**: RBF is default; Matérn for rougher functions; ARD for varying sensitivity per dimension
- **High dimensions ($d > 20$)**: Random search often beats BO — use trust-region BO or random embedding
- **Categorical/Integer inputs**: Use one-hot encoding with different lengthscales or random embedding
- **Noisy observations**: Include as kernel hyperparameter (white kernel)
- **Parallel evaluations**: Use batched BO (q-EI, q-UCB, Thompson sampling)
- **Constrained optimization**: Use expected constrained improvement or integrated acquisition

## Comparison

| Method | Samples needed | Parallel | Handles noise | When to use |
|--------|---------------|----------|---------------|-------------|
| Grid search | $\prod k_i$ | Yes | No | Very low $d$ |
| Random search | $T$ | Yes | N/A | High $d$, low budget |
| Bayesian opt | $O(d \log T)$ | Sequential | Yes | Moderate $d$, expensive evals |
| Hyperband | $O(\log T)$ | Yes | No | Large budget, cheap evals |

## Key Properties
- Sample-efficient: often 10-100x fewer evaluations than random search
- $O(n^3)$ per iteration from GP fitting (use sparse GPs for $n > 1000$)
- Works well for $d < 20$; degrades for higher dimensions
- Bayesian framework provides uncertainty quantification
- Extends to multi-objective (Pareto optimization) via expected hypervolume improvement

## References
- Mockus, "Bayesian Approach to Global Optimization" (1989)
- Jones, Schonlau, Welch, "Efficient Global Optimization of Expensive Black-Box Functions" (J. Global Optimization, 1998)
- Snoek, Larochelle, Adams, "Practical Bayesian Optimization of Machine Learning Algorithms" (NIPS 2012)
- Shahriari et al., "Taking the Human Out of the Loop: A Review of Bayesian Optimization" (IEEE Proc., 2016)
- Frazier, "A Tutorial on Bayesian Optimization" (arXiv, 2018)
