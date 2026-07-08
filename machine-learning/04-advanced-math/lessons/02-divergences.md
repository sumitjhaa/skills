# 04.02 f-Divergences, Jensen–Shannon, and Wasserstein Distance

## Motivation
KL divergence is one member of a broad family of divergences. Understanding the landscape of divergence measures is essential for choosing the right objective in generative modelling, domain adaptation, and robust inference. Different divergences induce different optimal solutions — for example, KL divergence leads to mode-seeking or mean-seeking behavior depending on direction, while Wasserstein distance remains well-behaved even for distributions with disjoint support.

## Learning Objectives
- Define f-divergences, give examples, and prove their key properties (non-negativity, convexity, invariance).
- Derive the Jensen-Shannon divergence and contrast it with KL divergence.
- Understand the Kantorovich-Rubinstein duality for Wasserstein distance and explain why it matters for GAN training.
- Choose the appropriate divergence for a given ML task (GANs, VI, domain adaptation, OT).

## Math Foundation

### f-Divergences
Let $p$ and $q$ be probability distributions over $\mathcal{X}$ with $p \ll q$ (i.e., $p$ is absolutely continuous w.r.t. $q$). For a convex function $f: (0,\infty) \to \mathbb{R}$ with $f(1) = 0$, the f-divergence is:

$$D_f(p \| q) = \int_{\mathcal{X}} q(x) \, f\!\left(\frac{p(x)}{q(x)}\right) dx$$

For discrete distributions, the integral becomes a sum. Key examples:

| $f(t)$ | Divergence | Formula |
|--------|-----------|---------|
| $t \log t$ | KL | $D_{\text{KL}}(p\|q) = \sum p \log(p/q)$ |
| $-\log t$ | Reverse KL | $D_{\text{KL}}(q\|p) = \sum q \log(q/p)$ |
| $(\sqrt{t} - 1)^2$ | Squared Hellinger | $H^2(p,q) = \frac12 \sum (\sqrt{p} - \sqrt{q})^2$ |
| $(t-1)^2$ | $\chi^2$ divergence | $\chi^2(p\|q) = \sum \frac{(p-q)^2}{q}$ |
| $\frac12 |t-1|$ | Total Variation | $\text{TV}(p,q) = \frac12 \sum |p-q|$ |

### Properties of f-Divergences
1. **Non-negativity**: $D_f(p\|q) \ge 0$ with equality iff $p = q$ (by Jensen and strict convexity of $f$).
2. **Convexity**: $D_f(p\|q)$ is jointly convex in $(p,q)$.
3. **Invariance**: f-divergences are invariant under smooth invertible transformations (diffeomorphisms).
4. **Range**: KL is unbounded; Hellinger and TV are bounded ($0 \le H^2 \le 1$, $0 \le \text{TV} \le 1$).

### Relationship Between Divergences
Pinsker's inequality relates TV to KL:

$$\text{TV}(p,q) \le \sqrt{\frac12 D_{\text{KL}}(p\|q)}$$

And the Hellinger distance satisfies:

$$H^2(p,q) \le \text{TV}(p,q) \le \sqrt{2} H(p,q)$$

These inequalities mean convergence in KL implies convergence in TV and Hellinger, but not vice versa.

## Jensen-Shannon Divergence

### Definition
Let $m = (p+q)/2$ be the midpoint distribution. The Jensen-Shannon divergence is:

$$\text{JS}(p \| q) = \frac12 D_{\text{KL}}(p \| m) + \frac12 D_{\text{KL}}(q \| m)$$

### Properties
- **Symmetric**: $\text{JS}(p\|q) = \text{JS}(q\|p)$
- **Bounded**: $0 \le \text{JS} \le \log 2$ (in nats)
- **Square root is a metric**: $\sqrt{\text{JS}}$ satisfies the triangle inequality
- **Continuous**: unlike KL, JS is well-defined even when supports don't fully overlap

### Connection to Mutual Information
For two random variables $X$ and $Y$:

$$I(X;Y) = \text{JS}(p(x,y) \| p(x)p(y))$$

This provides a variational lower bound used in Deep InfoMax and related methods.

## Wasserstein Distance

### Definition
For $p \ge 1$, the $p$-Wasserstein distance between distributions $P$ and $Q$ on a metric space $(\mathcal{M}, d)$ is:

$$W_p(P,Q) = \left( \inf_{\gamma \in \Gamma(P,Q)} \mathbb{E}_{(X,Y) \sim \gamma} [d(X,Y)^p] \right)^{1/p}$$

where $\Gamma(P,Q)$ is the set of all couplings (joint distributions) with marginals $P$ and $Q$. The infimum is over all ways to transport mass from $P$ to $Q$.

### Kantorovich-Rubinstein Duality
For $p=1$, the dual form is computationally tractable:

$$W_1(P,Q) = \sup_{\|f\|_L \le 1} \mathbb{E}_{x \sim P}[f(x)] - \mathbb{E}_{x \sim Q}[f(x)]$$

where $\|f\|_L \le 1$ means $f$ is 1-Lipschitz. This dual form is the basis for Wasserstein GANs, where a critic network approximates the optimal $f$.

### Why Wasserstein Over f-Divergences
When $P$ and $Q$ have disjoint support (common early in GAN training), KL and JS divergences are either infinite or constant (log 2), providing no useful gradient. Wasserstein distance remains continuous and differentiable almost everywhere, giving meaningful gradients even when supports don't overlap.

## Python Implementation

```python
import numpy as np
from scipy.special import rel_entr
from scipy.stats import wasserstein_distance
import ot  # POT library for optimal transport

def f_divergence(p, q, f_type='kl'):
    p = np.asarray(p, dtype=float) + 1e-12
    q = np.asarray(q, dtype=float) + 1e-12
    p /= p.sum()
    q /= q.sum()
    t = p / q
    if f_type == 'kl':
        return np.sum(p * np.log(t))
    elif f_type == 'reverse_kl':
        return np.sum(q * np.log(1/t))
    elif f_type == 'hellinger':
        return 0.5 * np.sum((np.sqrt(p) - np.sqrt(q))**2)
    elif f_type == 'chi2':
        return np.sum((p - q)**2 / q)
    elif f_type == 'tv':
        return 0.5 * np.sum(np.abs(p - q))

def js_divergence(p, q):
    p = np.asarray(p, dtype=float) + 1e-12
    q = np.asarray(q, dtype=float) + 1e-12
    p /= p.sum()
    q /= q.sum()
    m = 0.5 * (p + q)
    return 0.5 * (np.sum(rel_entr(p, m)) + np.sum(rel_entr(q, m)))

def wasserstein_1d(p, q, x_values=None):
    """Wasserstein-1 distance for 1D distributions.
    If x_values given, computes empirical W_1."""
    if x_values is not None:
        return wasserstein_distance(x_values, x_values, p, q)
    # Closed form for 1D: W_1 = int |F_p^{-1} - F_q^{-1}|
    cp = np.cumsum(p)
    cq = np.cumsum(q)
    return np.trapz(np.abs(cp - cq), dx=1.0/len(p))

# Example
p = np.array([0.6, 0.3, 0.1])
q = np.array([0.2, 0.5, 0.3])
print(f"KL(p||q) = {f_divergence(p, q, 'kl'):.4f}")
print(f"Reverse KL = {f_divergence(p, q, 'reverse_kl'):.4f}")
print(f"Hellinger = {f_divergence(p, q, 'hellinger'):.4f}")
print(f"JS(p,q) = {js_divergence(p, q):.4f}")
print(f"W_1(p,q) = {wasserstein_1d(p, q):.4f}")
```

## Visualization
Plot the same two Gaussian mixtures and overlay histograms. Show the transport plan from Wasserstein as a heatmap (the optimal coupling $\gamma^*$). Underneath, display a bar chart comparing KL, reverse KL, JS, Hellinger, and Wasserstein values — note that KL is much larger and asymmetric.

## Practical Considerations

### Choosing a Divergence for Your Task
- **KL divergence**: classification (cross-entropy), where the true distribution is fixed and you want the predictive distribution to cover all modes.
- **Reverse KL**: variational inference, where $D_{\text{KL}}(q\|p)$ encourages $q$ to be zero where $p$ is zero (mode-seeking, potentially underestimating variance).
- **JS divergence**: original GANs; bounded and symmetric but saturates for far-apart distributions.
- **Wasserstein distance**: GANs with disjoint support; provides linear gradients everywhere.
- **$\chi^2$ divergence**: some value function learning algorithms in offline RL; penalizes overestimation of OOD actions.

### Computational Cost
- f-divergences: $O(n)$ for $n$ support points — cheap.
- Wasserstein-1 via Sinkhorn: $O(n^2)$ per iteration but converges in few iterations with entropic regularization.
- Exact Wasserstein: $O(n^3 \log n)$ via network simplex — impractical for large $n$ without approximations.

### Entropic Regularization
Adding entropy to the optimal transport problem gives the Sinkhorn divergence:

$$W_{p,\varepsilon}(P,Q) = \inf_{\gamma} \mathbb{E}[d^p] + \varepsilon H(\gamma)$$

This is differentiable, parallelizable on GPU, and interpolates between Wasserstein ($\varepsilon \to 0$) and MMD ($\varepsilon \to \infty$).

## References
- Amari, *Information Geometry and Its Applications*, Springer 2016
- Villani, *Optimal Transport: Old and New*, Springer 2009
- Arjovsky, Chintala, Bottou, "Wasserstein GAN," *ICML 2017*
- Nowozin, Cseke, Tomioka, "f-GAN: Training Generative Neural Samplers using Variational Divergence Minimization," *NeurIPS 2016*
- Cuturi, "Sinkhorn Distances: Lightspeed Computation of Optimal Transport," *NeurIPS 2013*
