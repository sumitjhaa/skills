# Lesson 05.30: Maximum Entropy Models

## Learning Objectives
- Understand the maximum entropy principle
- Derive exponential family form from moment constraints
- Implement GIS and IIS training algorithms
- Apply to NLP tasks (POS tagging, text classification)

## MaxEnt Principle
Among all distributions consistent with observed constraints, choose the one with **maximum entropy**:

$$H(p) = -\sum_x p(x) \log p(x)$$

This is the least informative (most uncertain) distribution that still respects the constraints.

## Constraints
We require model expectations to match empirical expectations (from training data):

$$\mathbb{E}_p[f_j] = \mathbb{E}_{\tilde{p}}[f_j]$$

where $\mathbb{E}_{\tilde{p}}[f_j] = \frac{1}{n} \sum_i f_j(x_i, y_i)$ is the empirical expectation.

Feature functions $f_j$ are typically binary indicator functions capturing relevant properties of $(x, y)$ pairs.

## Resulting Distribution
Solving the constrained optimization (maximize entropy subject to moment constraints) via Lagrange multipliers yields:

$$p(y|x) = \frac{1}{Z(x)} \exp\left( \sum_{j=1}^m \lambda_j f_j(x, y) \right)$$

This is exactly the **log-linear** (or exponential family) form — equivalent to multinomial logistic regression with feature functions.

The Lagrange multipliers $\lambda_j$ are learned from data to maximize log-likelihood.

## Training Algorithms

### GIS (Generalized Iterative Scaling)
Requires a "correction feature" $C = \max_{x,y} \sum_j f_j(x,y)$:

$$\lambda_j^{(t+1)} = \lambda_j^{(t)} + \frac{1}{C} \log \frac{\mathbb{E}_{\tilde{p}}[f_j]}{\mathbb{E}_{p^{(t)}}[f_j]}$$

- Simple, monotonic convergence
- Slow (linear convergence)
- Requires $C$ to be constant across all $x, y$

### IIS (Improved Iterative Scaling)
Update $\lambda_j \to \lambda_j + \delta_j$ where $\delta_j$ satisfies:

$$\sum_{x,y} \tilde{p}(x) p(y|x) f_j(x,y) e^{\delta_j f^\#(x,y)} = \mathbb{E}_{\tilde{p}}[f_j]$$

where $f^\#(x,y) = \sum_j f_j(x,y)$.

Solved numerically (Newton's method) per feature.

### L-BFGS
Modern approach: directly optimize log-likelihood with L-BFGS (quasi-Newton). Faster convergence than GIS/IIS.

## Feature Functions
Binary indicator features in NLP:

$$f_j(x,y) = \begin{cases} 1 & \text{if } \phi_j(x) \text{ is true and } y = y_j \\ 0 & \text{otherwise} \end{cases}$$

Examples:
- $f_1(x,y) = [\text{word} = \text{"bank"}] \cdot [y = \text{NOUN}]$
- $f_2(x,y) = [\text{prev\_tag} = \text{DET}] \cdot [y = \text{NOUN}]$
- $f_3(x,y) = [\text{contains\_digit}] \cdot [y = \text{CD}]$

Features can be arbitrary and overlapping — the model handles redundancy automatically.

## Regularization
MaxEnt models overfit with many features. Add L2 regularization:

$$\ell(\lambda) = \sum_i \log p(y_i|x_i) - \frac{1}{2\sigma^2} \sum_j \lambda_j^2$$

Gradient with regularization:

$$\frac{\partial \ell}{\partial \lambda_j} = \mathbb{E}_{\tilde{p}}[f_j] - \mathbb{E}_p[f_j] - \frac{\lambda_j}{\sigma^2}$$

## Code: MaxEnt with GIS

```python
import numpy as np

class MaxEnt:
    def __init__(self, n_features, n_classes):
        self.n_features = n_features
        self.n_classes = n_classes
        self.weights = np.zeros((n_classes, n_features))

    def _log_prob(self, x):
        scores = self.weights @ x
        scores -= np.max(scores)  # numerical stability
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum()

    def fit_gis(self, X, Y, C=None, max_iter=1000, tol=1e-5):
        n = len(X)
        # Empirical expectations
        emp = np.zeros_like(self.weights)
        for x, y in zip(X, Y):
            emp[y] += x
        emp /= n
        if C is None:
            C = max(np.sum(x) for x in X)
        for iteration in range(max_iter):
            # Model expectations
            mod = np.zeros_like(self.weights)
            for x in X:
                probs = self._log_prob(x)
                for c in range(self.n_classes):
                    mod[c] += probs[c] * x
            mod /= n
            # Update
            mask = mod > 0
            new_weights = self.weights.copy()
            new_weights[mask] += (1.0 / C) * np.log(emp[mask] / mod[mask])
            if np.max(np.abs(new_weights - self.weights)) < tol:
                break
            self.weights = new_weights
```

## Practical Considerations
- **Feature sparsity**: Most features are zero for a given $(x, y)$ — use sparse data structures
- **Large feature sets**: $10^5-10^7$ features common in NLP — use L-BFGS with OWL-QN (L1 regularization)
- **Class imbalance**: MaxEnt handles it naturally via feature expectations
- **Feature correlation**: Redundant features don't hurt (weights adjust), but slow training
- **Memory**: Store features sparsely; dense representation is infeasible for large models

## Applications
- **Part-of-speech tagging**: Context words, suffixes, capitalization
- **Named entity recognition**: Word shape, gazetteer features
- **Text classification**: Bag-of-words, n-grams, topic features
- **Sentence boundary detection**: Punctuation, case features
- **Preference learning**: Rank-based features

## Key Points
- Equivalent to multinomial logistic regression with arbitrary feature functions
- No independence assumptions (unlike Naive Bayes)
- Feature engineering is critical for performance
- Regularization essential with many features
- Training scales with number of features and classes
- L-BFGS preferred over GIS/IIS in practice

## References
- Berger, Della Pietra, Della Pietra, "A Maximum Entropy Approach to Natural Language Processing" (Computational Linguistics, 1996)
- Ratnaparkhi, "A Simple Introduction to Maximum Entropy Models for Natural Language Processing" (Technical Report, 1997)
- Malouf, "A Comparison of Algorithms for Maximum Entropy Parameter Estimation" (CoNLL 2002)
- Manning & Schütze, "Foundations of Statistical NLP", Ch. 16
