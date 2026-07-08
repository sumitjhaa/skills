# Lesson 05.04: Naive Bayes

## Learning Objectives
- Derive Naive Bayes from Bayes' theorem with conditional independence
- Implement Gaussian, Multinomial, and Bernoulli variants
- Understand log-space computation for numerical stability
- Analyze bias from the independence assumption

## Mathematical Foundation

### Bayes Rule
For classification with $K$ classes:

$$P(y|x) = \frac{P(x|y)P(y)}{P(x)} \propto P(y) \prod_{j=1}^d P(x_j|y)$$

The denominator $P(x) = \sum_{c=1}^K P(x|y=c)P(y=c)$ normalizes.

### Naive Assumption
Features are conditionally independent given the class:

$$P(x|y) = \prod_{j=1}^d P(x_j|y)$$

This is **naive** because real-world features are almost never independent. Despite this, Naive Bayes often works well, especially when $d$ is large.

### Why The Assumption Helps
- Reduces parameter count from exponential $O(K \cdot 2^d)$ to linear $O(K \cdot d)$
- Avoids estimating $d$-dimensional joint distributions
- Each $P(x_j|y)$ can be estimated independently using 1D histograms or parametric forms

## Common Distributional Assumptions

### Gaussian Naive Bayes
For continuous features:

$$P(x_j|y=c) = \frac{1}{\sqrt{2\pi\sigma_{jc}^2}} \exp\left(-\frac{(x_j-\mu_{jc})^2}{2\sigma_{jc}^2}\right)$$

Parameters: $\mu_{jc} = \frac{1}{N_c} \sum_{i: y_i=c} x_{ij}$, $\sigma_{jc}^2 = \frac{1}{N_c} \sum_{i: y_i=c} (x_{ij} - \mu_{jc})^2$

### Multinomial Naive Bayes
For count features (e.g., bag-of-words):

$$P(x_j|y=c) = \frac{N_{cj} + \alpha}{N_c + \alpha d}$$

where $N_{cj} = \sum_{i: y_i=c} x_{ij}$ is the sum of counts for feature $j$ in class $c$, $N_c = \sum_j N_{cj}$ is the total count for class $c$, and $\alpha$ is Laplace smoothing.

### Bernoulli Naive Bayes
For binary features:

$$P(x_j|y=c) = p_{cj}^{x_j} (1-p_{cj})^{1-x_j}$$

where $p_{cj} = \frac{N_{cj} + \alpha}{N_c + 2\alpha}$ (smoothed fraction of documents in class $c$ containing feature $j$).

## Log-Space Computation
To avoid underflow when multiplying many probabilities:

$$\log P(y|x) = \log P(y) + \sum_{j=1}^d \log P(x_j|y) + \text{const}$$

The constant $-\log P(x)$ can be ignored for argmax. For probability estimates:

$$P(y|x) = \frac{\exp(\log P(y) + \sum_j \log P(x_j|y))}{\sum_{c=1}^K \exp(\log P(c) + \sum_j \log P(x_j|c))}$$

Use log-sum-exp trick for numerical stability.

## Laplace (Additive) Smoothing
Prevents zero probabilities when a feature value not seen in training appears at test time:

$$P(x_j|y=c) = \frac{N_{cj} + \alpha}{N_c + \alpha d_j}$$

- $\alpha = 1$: Laplace smoothing
- $\alpha < 1$: Lidstone smoothing
- Higher $\alpha$ means stronger prior

## Decision Boundary
For Gaussian NB, the decision boundary is quadratic in general. With equal class covariances (shared $\sigma_j^2$), it becomes linear — equivalent to LDA with diagonal covariance.

## Code: Gaussian Naive Bayes

```python
import numpy as np
from scipy.stats import norm

class GaussianNaiveBayes:
    def fit(self, X, y):
        n, d = X.shape
        self.classes = np.unique(y)
        self.means = {}
        self.stds = {}
        self.priors = {}
        for c in self.classes:
            Xc = X[y == c]
            self.means[c] = Xc.mean(axis=0)
            self.stds[c] = Xc.std(axis=0) + 1e-9
            self.priors[c] = len(Xc) / n

    def predict_log_proba(self, X):
        log_probs = []
        for c in self.classes:
            log_prior = np.log(self.priors[c])
            log_lik = norm.logpdf(X, self.means[c], self.stds[c]).sum(axis=1)
            log_probs.append(log_prior + log_lik)
        log_probs = np.array(log_probs).T
        return log_probs - np.log(np.sum(np.exp(log_probs), axis=1, keepdims=True))

    def predict(self, X):
        return self.classes[np.argmax(self.predict_log_proba(X), axis=1)]
```

## Practical Considerations
- **Feature correlation**: When highly correlated features exist, NB probabilities become overconfident
- **Zero frequency**: Laplace smoothing essential for categorical features
- **Continuous features**: Kernel density estimation can replace Gaussian assumption
- **Semi-supervised**: NB works well with EM for semi-supervised learning
- **Large $d$**: NB shines (text classification with $10^5$ features)
- **Calibration**: NB probabilities tend to be extreme (too close to 0 or 1) — consider Platt scaling

## Key Points
- Very fast: $O(nd)$ training, $O(Kd)$ inference
- Works well even when independence violated (especially text)
- Excellent for high-dimensional sparse data
- Low-variance, high-bias classifier
- Reliable with small training sets

## References
- Russell & Norvig, "Artificial Intelligence: A Modern Approach", Ch. 20
- Manning, Raghavan, Schütze, "Introduction to Information Retrieval", Ch. 13
- Ng & Jordan, "On Discriminative vs. Generative Classifiers" (NIPS 2001)
