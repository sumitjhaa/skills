# Lesson 05.29: Conditional Random Fields

## Learning Objectives
- Understand CRF as a discriminative sequence model
- Implement linear-chain CRF feature functions
- Derive gradient of log-likelihood for training
- Compare with HMMs and MEMMs

## Definition
Linear-chain CRF models the conditional distribution $P(Y|X)$ directly:

$$P(Y|X) = \frac{1}{Z(X)} \exp\left( \sum_{t=1}^T \sum_{k=1}^K \theta_k f_k(y_t, y_{t-1}, x_t) \right)$$

- $f_k(y_t, y_{t-1}, x_t)$: feature functions (can overlap, be arbitrary)
- $\theta_k$: learned feature weights
- $Z(X) = \sum_{y'} \exp\left( \sum_t \sum_k \theta_k f_k(y'_t, y'_{t-1}, x_t) \right)$: partition function (normalization)

Unlike HMMs, CRFs do not model $P(X)$ — they focus entirely on the conditional distribution.

## Feature Functions
Features can depend on arbitrary aspects of the input $x$:

### Transition Features
$$f_k(y_t, y_{t-1}, x_t) = [y_t = \text{NOUN}] \cdot [y_{t-1} = \text{ADJ}]$$

### State Features (Observation Features)
$$f_k(y_t, y_{t-1}, x_t) = [y_t = \text{NOUN}] \cdot [x_t \text{ starts with capital}]$$

Binary indicator functions with domain knowledge: word shape, suffix, prefix, capitalization, etc.

## Inference: Viterbi Decoding
Find $Y^* = \arg\max_Y P(Y|X)$. Analogous to HMM Viterbi but using potentials instead of probabilities:

$$\delta_t(j) = \max_i [\delta_{t-1}(i) + \Psi_t(j, i, x_t)]$$

where $\Psi_t(j, i, x) = \sum_k \theta_k f_k(y_t=j, y_{t-1}=i, x_t)$ is the score of transition $i \to j$ at time $t$.

Complexity: $O(T \cdot m^2)$ for $m$ labels.

## Training: Gradient of Log-Likelihood
Log-likelihood: $\ell(\theta) = \log P(Y|X, \theta) = \sum_t \sum_k \theta_k f_k(y_t, y_{t-1}, x_t) - \log Z(X)$

Gradient:

$$\frac{\partial \ell}{\partial \theta_k} = \sum_{t=1}^T \left[ f_k(y_t, y_{t-1}, x_t) - \sum_{y'_t, y'_{t-1}} P(Y'|X) f_k(y'_t, y'_{t-1}, x_t) \right]$$

- First term: empirical feature count from true labels
- Second term: expected feature count under model (via forward-backward)

### Forward-Backward for CRFs
Forward: $\alpha_t(j) = \sum_i \alpha_{t-1}(i) \exp(\Psi_t(j,i,x_t))$
Backward: $\beta_t(i) = \sum_j \exp(\Psi_{t+1}(j,i,x_{t+1})) \beta_{t+1}(j)$

Marginal: $P(y_t=j, y_{t-1}=i | X) \propto \alpha_{t-1}(i) \exp(\Psi_t(j,i,x_t)) \beta_t(j)$

### Regularization
L2 regularization: $\ell(\theta) - \frac{\lambda}{2} \|\theta\|_2^2$ (prevents overfitting)

### Optimization
L-BFGS (quasi-Newton) is standard. SGD for large datasets. Convex optimization (log-likelihood is concave).

## CRF vs HMM vs MEMM

| Property | HMM | MEMM | CRF |
|----------|-----|------|-----|
| Type | Generative | Discriminative | Discriminative |
| Normalization | Global (over $X,Y$) | Per-step (local) | Global ($Z(X)$) |
| Label bias | — | Yes (per-state normalization) | No |
| Feature overlap | No (independence) | Yes | Yes |
| Training | EM (Baum-Welch) | Gradient | Gradient |
| Complexity | $O(T m^2)$ | $O(T m^2)$ | $O(T m^2)$ |

**Label bias**: MEMMs normalize per state, so states with fewer transitions are biased toward those transitions. CRFs normalize globally, avoiding this.

## Code: Simple Linear-Chain CRF

```python
import numpy as np
from scipy.optimize import minimize

class LinearChainCRF:
    def __init__(self, n_labels, n_features):
        self.n_labels = n_labels
        self.n_features = n_features
        self.theta = np.zeros(n_features * n_labels + n_labels * n_labels)

    def _score(self, theta, y_prev, y_curr, x_t):
        """Score for transition from y_prev to y_curr with observation x_t"""
        nf, nl = self.n_features, self.n_labels
        obs_weights = theta[:nf * nl].reshape(nl, nf)
        trans_weights = theta[nf * nl:].reshape(nl, nl)
        return obs_weights[y_curr] @ x_t + trans_weights[y_curr, y_prev]

    def _neg_log_likelihood(self, theta, X, Y):
        n_sentences = len(X)
        total_loss = 0
        for s in range(n_sentences):
            T = len(X[s])
            # Forward pass
            alpha = np.zeros((T, self.n_labels))
            alpha[0] = np.array([self._score(theta, 0, l, X[s][0]) for l in range(self.n_labels)])
            for t in range(1, T):
                for j in range(self.n_labels):
                    alpha[t, j] = np.log(np.sum(np.exp(alpha[t-1] + [self._score(theta, i, j, X[s][t]) for i in range(self.n_labels)])))
            logZ = np.log(np.sum(np.exp(alpha[-1])))
            # True label score
            true_score = sum(self._score(theta, Y[s][t-1] if t > 0 else 0, Y[s][t], X[s][t]) for t in range(T))
            total_loss += -(true_score - logZ)
        return total_loss
```

## Practical Considerations
- **Training cost**: Forward-backward for each training example per gradient step — $O(T m^2)$
- **Large label sets**: $O(m^2)$ becomes expensive — use beam search or constraint-based CRFs
- **Feature engineering**: Feature quality is critical — domain expertise matters
- **Software**: CRFsuite, CRF++ (C++), sklearn-crfsuite (Python)
- **Structured prediction**: CRFs extend to general graphs (not just chains) via junction tree inference

## Key Points
- Avoids label bias problem of MEMMs
- Overlapping features allowed (no independence assumption)
- $O(T m^2)$ inference via Viterbi/forward-backward
- Training requires computing model expectations via inference
- Convex optimization (global optimum guaranteed)

## References
- Lafferty, McCallum, Pereira, "Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data" (ICML 2001)
- Sutton & McCallum, "An Introduction to Conditional Random Fields" (Foundations and Trends in ML, 2012)
- Wallach, "Conditional Random Fields: An Introduction" (Technical Report, 2004)
- Sha & Pereira, "Shallow Parsing with Conditional Random Fields" (NAACL 2003)
