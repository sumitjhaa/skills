# Lesson 05.33: Online Learning

## Learning Objectives
- Understand regret minimization in online convex optimization
- Implement Perceptron, PA, OGD, and FTRL algorithms
- Analyze regret bounds for convex and strongly convex losses
- Apply to streaming CTR prediction and ad placement

## Setup
Data arrives sequentially $(x_t, y_t)$. At each round:
1. Model predicts $\hat{y}_t = f_t(x_t)$
2. True label $y_t$ is revealed
3. Model incurs loss $\ell_t(w_t) = L(y_t, \hat{y}_t)$
4. Update $w_{t+1}$ based on $(x_t, y_t)$

No assumption of i.i.d. data. Goal: minimize cumulative regret.

## Algorithms

### Perceptron
Update only on mistake:

$$w_{t+1} = w_t + \eta \cdot \mathbf{1}[\hat{y}_t \neq y_t] \cdot y_t x_t$$

Mistake bound: at most $(R/\gamma)^2$ mistakes for margin $\gamma$ separable data.

### Passive-Aggressive (PA)
Solve constrained optimization at each step:

$$w_{t+1} = \arg\min_w \frac12 \|w - w_t\|^2 \quad \text{s.t.} \quad \ell(w; (x_t, y_t)) = 0$$

Closed form: $w_{t+1} = w_t + \tau_t y_t x_t$

- **PA-I**: $\tau_t = \min\{C, \ell_t / \|x_t\|^2\}$ (soft margin)
- **PA-II**: $\tau_t = \ell_t / (\|x_t\|^2 + 1/(2C))$ (different tradeoff)

### Online Gradient Descent (OGD)
$$w_{t+1} = w_t - \eta_t \nabla \ell_t(w_t)$$

- $\eta_t = 1/\sqrt{t}$: $O(\sqrt{T})$ regret for convex losses
- $\eta_t = 1/(\mu t)$: $O(\log T)$ regret for $\mu$-strongly convex losses

### Follow the Regularized Leader (FTRL)
$$w_{t+1} = \arg\min_w \sum_{s=1}^t \ell_s(w) + \lambda \|w\|_1 + \frac12 \eta_t \|w\|_2^2$$

- L1 penalty induces sparsity (important for large-scale models)
- Used by Google for ad CTR prediction
- Per-coordinate learning rates: $\eta_{t,i} = \alpha / (\beta + \sqrt{\sum_{s=1}^t g_{s,i}^2})$

## Regret Analysis

$$\text{Regret}_T = \sum_{t=1}^T \ell_t(w_t) - \min_{w^*} \sum_{t=1}^T \ell_t(w^*)$$

| Setting | Condition | Regret Bound | Algorithm |
|---------|-----------|-------------|-----------|
| Convex | $\|g_t\| \leq G$, $\|w\| \leq R$ | $O(GR\sqrt{T})$ | OGD |
| Strongly convex | $\mu$-strongly convex | $O(\frac{G^2}{\mu} \log T)$ | OGD |
| Exp-concave | $\eta \exp(-\eta \ell_t)$ | $O(d \log T)$ | Online Newton Step |
| Adversarial | No assumptions | $O(\sqrt{T})$ | FTRL / Hedge |

## Code: FTRL-Proximal

```python
import numpy as np

class FTRLProximal:
    def __init__(self, alpha=0.1, beta=1.0, L1=1.0, L2=1.0, n_features=2**20):
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2
        self.n = np.zeros(n_features)
        self.z = np.zeros(n_features)
        self.w = np.zeros(n_features)

    def predict(self, x):
        # Weight prediction with L1 proximal operator
        self.w = np.where(np.abs(self.z) <= self.L1, 0,
                          -(np.sign(self.z) * (np.abs(self.z) - self.L1) / (self.L2 + (self.beta + np.sqrt(self.n)) / self.alpha)))
        return 1 / (1 + np.exp(-x @ self.w))

    def update(self, x, y):
        p = self.predict(x)
        g = (p - y) * x  # gradient of log-loss
        sigma = (np.sqrt(self.n + g**2) - np.sqrt(self.n)) / self.alpha
        self.z += g - sigma * self.w
        self.n += g**2
```

## Practical Considerations
- **Feature hashing**: Map features to fixed-size vector to limit memory ($2^{24}$ common)
- **Per-coordinate rates**: Each feature gets its own learning rate (based on gradient history)
- **Proximal operators**: L1 regularization via soft-thresholding
- **Importance sampling**: Weight updates by prediction uncertainty
- **Evaluation**: Use progressive validation (test on current instance before update)
- **Batching**: Micro-batching improves throughput without sacrificing online nature

## Applications
- CTR prediction (Google, Facebook ad systems)
- Real-time bidding for display ads
- Recommendation systems (news, videos)
- Fraud detection (transaction streams)
- Adaptive filtering (spam, content moderation)

## Key Properties
- Constant memory (independent of $n$)
- $O(d)$ update per example
- No assumption of i.i.d. data
- Adversarial robustness via regret bounds
- FTRL with L1 produces sparse models matching Lasso quality

## References
- McMahan et al., "Ad Click Prediction: a View from the Trenches" (KDD 2013)
- McMahan, "Follow-the-Regularized-Leader and Mirror Descent" (2011)
- Crammer et al., "Online Passive-Aggressive Algorithms" (JMLR, 2006)
- Zinkevich, "Online Convex Programming and Generalized Infinitesimal Gradient Ascent" (ICML 2003)
- Shalev-Shwartz, "Online Learning and Online Convex Optimization" (Foundations and Trends in ML, 2011)
