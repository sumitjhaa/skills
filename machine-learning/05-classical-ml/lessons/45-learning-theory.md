# Lesson 05.45: Learning Theory (VC / PAC)

## Learning Objectives
- Understand PAC learnability and sample complexity
- Derive VC dimension for hypothesis classes
- Apply structural risk minimization for model selection
- Analyze concentration inequalities for generalization bounds

## PAC Learning
Probably Approximately Correct (PAC) learning:

A hypothesis class $H$ is PAC-learnable if there exists algorithm $A$ such that for any $\varepsilon, \delta > 0$, any distribution $D$:

$$P_{S \sim D^n} \left[ R(h_S) - R(h^*) \leq \varepsilon \right] \geq 1 - \delta$$

- $R(h) = P_{(x,y)\sim D}[h(x) \neq y]$: true risk
- $\varepsilon$: accuracy parameter
- $\delta$: confidence parameter
- $h_S$: hypothesis learned from sample $S$
- $h^* = \arg\min_{h \in H} R(h)$: best-in-class

### Sample Complexity (Finite $H$)
$$n \geq \frac{1}{\varepsilon} \log \frac{|H|}{\delta}$$

**Agnostic PAC**: When realizability assumption is removed:

$$n \geq O\left(\frac{\text{VC}(H) + \log(1/\delta)}{\varepsilon^2}\right)$$

## VC Dimension
Maximum number of points that can be shattered (all $2^m$ possible labelings realized):

| Hypothesis Class | VC Dimension |
|-----------------|--------------|
| Linear classifier in $\mathbb{R}^d$ | $d+1$ |
| Decision stumps | $2$ |
| Axis-aligned rectangles in $\mathbb{R}^d$ | $2d$ |
| Decision tree (depth $D$) | $O(2^D d)$ |
| Neural net (1 hidden, $m$ nodes) | $O(m^2 d^2)$ |
| RBF kernel SVM | $\infty$ (for $\gamma > 0$) |

### VC Dimension of Linear Classifiers
For $h(x) = \text{sign}(w^\top x + b)$ in $\mathbb{R}^d$, VC dimension = $d+1$.

Proof for $d=2$: can shatter 3 points (any labeling of triangle vertices possible), but not 4 points (linear separability limit).

## Fundamental Theorem of PAC Learning
For hypothesis class $H$ with VC-dim $d$:

$$n = O\left(\frac{d}{\varepsilon} \log \frac{1}{\varepsilon} + \frac{1}{\varepsilon} \log \frac{1}{\delta}\right)$$

Upper bound on sample complexity. Also a lower bound: $\Omega(d/\varepsilon + \log(1/\delta)/\varepsilon)$.

## Structural Risk Minimization (SRM)
Tradeoff between empirical risk and hypothesis complexity:

$$\hat{h}_n = \arg\min_{h \in H} R_{\text{emp}}(h) + \sqrt{\frac{\text{VC}(H) \log(n/\text{VC}(H)) + \log(1/\delta)}{n}}$$

The penalty term is the generalization gap bound. SRM selects the hypothesis class that minimizes the bound on true risk.

## Concentration Inequalities

### Hoeffding's Inequality
For bounded random variables $X_i \in [a, b]$:

$$P(|\bar{X} - \mu| \geq t) \leq 2 e^{-2n t^2 / (b-a)^2}$$

### McDiarmid's Inequality
For functions of independent variables with bounded differences:

$$P(f(X_1, \dots, X_n) - \mathbb{E}[f] \geq t) \leq e^{-2t^2 / \sum_i c_i^2}$$

Used to derive generalization bounds for VC classes.

## Rademacher Complexity
Another measure of hypothesis class complexity:

$$\mathfrak{R}_n(H) = \mathbb{E}_{S, \sigma} \left[ \sup_{h \in H} \frac{1}{n} \sum_{i=1}^n \sigma_i h(x_i) \right]$$

where $\sigma_i \in \{\pm1\}$ are Rademacher random variables.

Generalization bound: $R(h) \leq R_{\text{emp}}(h) + \mathfrak{R}_n(H) + O(\sqrt{\log(1/\delta)/n})$

## Code: VC Dimension of Linear Classifier

```python
import numpy as np
from itertools import combinations

def vc_linear(d):
    """VC dimension of linear classifiers in R^d is d+1"""
    return d + 1

def check_shatter(points, labels):
    """Check if linear classifier realizes given labeling"""
    n = points.shape[0]
    X = np.hstack([points, np.ones((n, 1))])
    y = 2 * labels - 1  # convert to ±1
    try:
        w = np.linalg.solve(X.T @ X, X.T @ y)
        return all((X @ w) * y > 0)
    except np.linalg.LinAlgError:
        return False
```

## Key Insights
- **Overfitting**: Complex models have high VC-dim → need more data for reliable generalization
- **Uniform convergence**: Training error converges to test error uniformly over $H$
- **Agnostic PAC**: No realizability assumption needed
- **Model selection via SRM**: Theoretical approach; cross-validation is practical equivalent
- **Deep learning**: VC dimension of NNs can be large but NNs generalize well — gap explained by implicit regularization, margin theory

## Limitations of VC Theory
- Often loose for practical models (e.g., NNs have very high VC-dim but generalize)
- Doesn't account for optimization algorithm (only hypothesis class)
- Minimax rates can be pessimistic for well-structured data
- Alternative frameworks: PAC-Bayes, margin bounds, stability

## References
- Valiant, "A Theory of the Learnable" (CACM, 1984)
- Vapnik & Chervonenkis, "On the Uniform Convergence of Relative Frequencies" (Theory of Probability, 1971)
- Vapnik, "The Nature of Statistical Learning Theory" (Springer, 1995)
- Shalev-Shwartz & Ben-David, "Understanding Machine Learning" (Cambridge, 2014)
- Mohri, Rostamizadeh, Talwalkar, "Foundations of Machine Learning" (MIT Press, 2012)
