# Lesson 07.24: MCMC for Deep Learning

## Learning Objectives
- Understand Markov Chain Monte Carlo for posterior sampling
- Implement Metropolis-Hastings, Gibbs, and HMC
- Apply Stochastic Gradient Langevin Dynamics (SGLD) for Bayesian deep learning
- Use MCMC for energy-based model training and uncertainty quantification

## Theory
MCMC constructs a Markov chain with the target distribution $p(x)$ as its stationary distribution.

### Detailed Balance
$$p(x') T(x \mid x') = p(x) T(x' \mid x)$$

- $T(x' \mid x)$: transition probability from $x$ to $x'$
- Sufficient condition for $p$ being stationary

## Metropolis-Hastings (MH)

### Algorithm
1. Propose $x' \sim q(x' \mid x_k)$
2. Compute acceptance probability:
   $$\alpha = \min\left(1, \frac{p(x') q(x_k \mid x')}{p(x_k) q(x' \mid x_k)}\right)$$
3. Accept $x_{k+1} = x'$ with prob $\alpha$, else $x_{k+1} = x_k$

### Random Walk MH
$q(x' \mid x) = \mathcal{N}(x, \sigma^2 I)$

- $\sigma$ controls step size (tune to achieve ~23% acceptance)
- **Burn-in**: Discard initial samples until chain converges

## Gibbs Sampling

### Algorithm
Sample each variable conditioned on all others:

$$x_i^{(k+1)} \sim p(x_i \mid x_{<i}^{(k+1)}, x_{>i}^{(k)})$$

### When to Use
- Conditional distributions are tractable (e.g., RBMs, Bayesian networks)
- No tuning parameters needed (always accepts)
- **Slower mixing** than HMC for correlated variables

## Hamiltonian Monte Carlo (HMC)

### Augmented System
Introduce momentum $r \sim \mathcal{N}(0, M)$:

$$H(x, r) = -\log p(x) + \frac{1}{2} r^\top M^{-1} r$$

- $-\log p(x)$: potential energy
- $\frac{1}{2} r^\top M^{-1} r$: kinetic energy

### Update
$$(x, r) \to \text{Leapfrog}(x, r, L, \varepsilon) \to \text{Metropolis accept/reject}$$

- Leapfrog integration: $L$ steps with step size $\varepsilon$
- **Advantage**: Uses gradient $\nabla_x \log p(x)$ — efficient exploration

## Stochastic Gradient MCMC

### SGLD (Stochastic Gradient Langevin Dynamics)
$$x_{k+1} = x_k + \frac{\varepsilon_k}{2} \left(\nabla_x \log p(x_k) + \frac{N}{n} \sum_{i \in \mathcal{B}} \nabla_x \log p(x_i \mid x_k) \right) + \eta_k$$
$$\eta_k \sim \mathcal{N}(0, \varepsilon_k I)$$

- Uses mini-batch gradient (scaled by $N/n$)
- Noise $\eta_k$ ensures correct stationary distribution

### SGHMC (Stochastic Gradient Hamiltonian Monte Carlo)
Adds friction term to counter mini-batch noise:

$$r_{k+1} = (1 - \alpha) r_k + \varepsilon \nabla_x \log p(x_k) + \sqrt{2\alpha \varepsilon} \mathcal{N}(0, I)$$

- $\alpha$: friction coefficient
- More efficient than SGLD for high-dimensional posteriors

## Code: HMC for Bayesian Logistic Regression

```python
import torch
import torch.nn as nn

class HMC:
    def __init__(self, log_prob_fn, step_size=0.01, n_leapfrog=10):
        self.log_prob = log_prob_fn
        self.eps = step_size
        self.L = n_leapfrog

    def leapfrog(self, x, r):
        # Half step momentum
        r = r + 0.5 * self.eps * torch.autograd.grad(self.log_prob(x).sum(), x)[0]
        # Full step position
        for _ in range(self.L - 1):
            x = x + self.eps * r
            r = r + self.eps * torch.autograd.grad(self.log_prob(x).sum(), x)[0]
        # Half step momentum
        x = x + self.eps * r
        r = r + 0.5 * self.eps * torch.autograd.grad(self.log_prob(x).sum(), x)[0]
        return x, r

    def sample(self, x0, n_samples=1000):
        x = x0.clone().requires_grad_(True)
        samples = []
        for _ in range(n_samples):
            r0 = torch.randn_like(x)
            x_prop, r_prop = self.leapfrog(x.clone(), r0.clone())
            
            # Metropolis accept
            h_current = -self.log_prob(x).sum() + 0.5 * (r0 ** 2).sum()
            h_proposed = -self.log_prob(x_prop).sum() + 0.5 * (r_prop ** 2).sum()
            if torch.rand(1) < torch.exp(h_current - h_proposed):
                x = x_prop.detach().clone().requires_grad_(True)
            samples.append(x.detach().clone())
        return torch.stack(samples)
```

## Applications in Deep Learning

| Application | Method | Why |
|-------------|--------|-----|
| BNN posterior | SGHMC, SGLD | Scalable to large data |
| EBM training | HMC, SGLD | Negative phase sampling |
| Hyperparameter optimization | MH, Gibbs | Tractable conditionals |
| Uncertainty estimation | All MCMC | Posterior predictive |
| Missing data imputation | Gibbs | Conditional structure |

## Diagnostics

| Metric | What it Measures | Good Value |
|--------|-----------------|------------|
| $\hat{R}$ (Gelman-Rubin) | Convergence (multi-chain) | $< 1.01$ |
| ESS (Effective Sample Size) | Sample quality | $> 100$ |
| Acceptance rate (MH) | Efficiency | 0.23 (RW) |
| Autocorrelation | Mixing speed | Decay quickly |
| Trace plot | Visual convergence | Stationary |

## Practical Considerations
- **Warm-up/burn-in**: Discard first 10-50% of samples
- **Thinning**: Keep every $k$th sample to reduce autocorrelation
- **Multiple chains**: Run 4+ chains from different starting points
- **Step size tuning**: Target 65% acceptance for HMC, 23% for random walk
- **Gradient clipping**: Essential for SGLD/SGHMC with neural networks

## Limitations
- **Scalability**: Full-batch HMC doesn't scale to large datasets
- **Autocorrelation**: MCMC samples are correlated — less efficient than i.i.d.
- **Convergence assessment**: Cannot guarantee convergence in finite time
- **Neural network posteriors**: High-dimensional, multimodal posteriors are hard to sample
- **Tuning**: HMC step size and trajectory length require careful tuning

## References
- Welling & Teh, "Bayesian Learning via Stochastic Gradient Langevin Dynamics", ICML 2011
- Chen, Fox, Guestrin, "Stochastic Gradient Hamiltonian Monte Carlo", ICML 2014
- Neal, "MCMC Using Hamiltonian Dynamics", Handbook of MCMC, 2011
- Betancourt, "A Conceptual Introduction to Hamiltonian Monte Carlo", 2017
- Gelman, Carlin, Stern, Rubin, "Bayesian Data Analysis", 3rd ed., Ch. 11-12
