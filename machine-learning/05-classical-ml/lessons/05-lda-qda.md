# Lesson 05.05: LDA / QDA

## Learning Objectives
- Derive LDA and QDA discriminant functions from Bayes' theorem
- Understand shared vs class-specific covariance assumptions
- Implement LDA/QDA from scratch
- Compare with Naive Bayes and logistic regression

## Mathematical Foundation

### Bayes Classifier with Gaussian Class-Conditional Densities
Assume $P(x|y=k) \sim \mathcal{N}(\mu_k, \Sigma_k)$ with prior $\pi_k = P(y=k)$.

The posterior probability via Bayes' rule:

$$P(y=k|x) = \frac{\pi_k \mathcal{N}(x|\mu_k, \Sigma_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(x|\mu_j, \Sigma_j)}$$

### LDA (Linear Discriminant Analysis)
**Assumption**: All classes share the same covariance $\Sigma_k = \Sigma$.

The discriminant function (log-posterior, ignoring constant terms):

$$\delta_k(x) = x^\top \Sigma^{-1} \mu_k - \frac{1}{2} \mu_k^\top \Sigma^{-1} \mu_k + \log \pi_k$$

This is **linear** in $x$ because the quadratic term $x^\top \Sigma^{-1} x$ cancels across classes.

### QDA (Quadratic Discriminant Analysis)
Each class has its own covariance $\Sigma_k$:

$$\delta_k(x) = -\frac{1}{2} \log|\Sigma_k| - \frac{1}{2}(x-\mu_k)^\top \Sigma_k^{-1} (x-\mu_k) + \log \pi_k$$

The decision boundary is **quadratic** in $x$.

### Decision Boundary Between Two Classes
LDA: $\{x : \delta_1(x) = \delta_2(x)\}$ defines a hyperplane.

QDA: $\{x : \delta_1(x) = \delta_2(x)\}$ defines a quadratic surface.

## Parameter Estimation

### Maximum Likelihood Estimates
$$\hat{\pi}_k = \frac{n_k}{n}$$

$$\hat{\mu}_k = \frac{1}{n_k} \sum_{i: y_i=k} x_i$$

### LDA Covariance (Pooled)
$$\hat{\Sigma} = \frac{1}{n-K} \sum_{k=1}^K \sum_{i: y_i=k} (x_i - \hat{\mu}_k)(x_i - \hat{\mu}_k)^\top$$

### QDA Covariance (Class-specific)
$$\hat{\Sigma}_k = \frac{1}{n_k-1} \sum_{i: y_i=k} (x_i - \hat{\mu}_k)(x_i - \hat{\mu}_k)^\top$$

## Regularized Discriminant Analysis (RDA)
Shrinkage between LDA and QDA:

$$\hat{\Sigma}_k(\alpha) = \alpha \hat{\Sigma}_k + (1-\alpha) \hat{\Sigma}$$

- $\alpha = 0$: LDA (shared covariance)
- $\alpha = 1$: QDA (class-specific)
- $0 < \alpha < 1$: Regularized (shrink toward shared)

Further shrinkage toward diagonal:

$$\hat{\Sigma}_k(\alpha, \gamma) = (1-\gamma) \hat{\Sigma}_k(\alpha) + \gamma \cdot \text{diag}(\hat{\Sigma}_k(\alpha))$$

## Dimensionality Reduction View
LDA finds directions maximizing between-class scatter relative to within-class scatter:

$$\max_{v} \frac{v^\top S_B v}{v^\top S_W v}$$

where $S_B$ is between-class scatter and $S_W$ is within-class scatter. This is a generalized eigenvalue problem: $S_B v = \lambda S_W v$, giving at most $K-1$ discriminant directions.

## Code: LDA and QDA from Scratch

```python
import numpy as np
from scipy import linalg

class LDA:
    def fit(self, X, y):
        n, d = X.shape
        self.classes = np.unique(y)
        self.means = {}
        self.priors = {}
        for c in self.classes:
            Xc = X[y == c]
            self.means[c] = Xc.mean(axis=0)
            self.priors[c] = len(Xc) / n
        # Pooled covariance
        S = np.zeros((d, d))
        for c in self.classes:
            Xc = X[y == c] - self.means[c]
            S += Xc.T @ Xc
        self.S_inv = linalg.inv(S / (n - len(self.classes)))

    def discriminant(self, X, c):
        mu = self.means[c]
        score = X @ self.S_inv @ mu - 0.5 * mu @ self.S_inv @ mu + np.log(self.priors[c])
        return score

    def predict(self, X):
        scores = np.array([self.discriminant(X, c) for c in self.classes])
        return self.classes[np.argmax(scores, axis=0)]
```

## Practical Considerations
- **Singular covariance**: When $d > n$, $\hat{\Sigma}$ is singular. Use RDA, diagonal LDA, or PCA preprocessing
- **Non-Gaussian data**: LDA/QDA can still work well if classes are unimodal
- **Outliers**: Covariance estimates are sensitive; consider robust covariance (MCD)
- **Feature scaling**: Unlike SVM/k-means, LDA is scale-aware via covariance
- **Equal covariance assumption**: Test via Box's M-test; if violated, use QDA
- **Computational cost**: LDA $O(nd^2 + d^3)$, QDA $O(Knd^2)$ — expensive for large $d$

## Comparison
| Method | Covariance | Boundary | Parameters | Data needs |
|--------|-----------|----------|------------|------------|
| LDA | Shared | Linear | $O(Kd + d^2)$ | Moderate |
| QDA | Class-specific | Quadratic | $O(Kd + Kd^2)$ | Large per class |
| Diagonal LDA | Diagonal | Linear | $O(Kd)$ | Small |
| RDA | Shrunk | Variable | Tuned $\alpha, \gamma$ | Moderate |

## References
- Fisher, "The Use of Multiple Measurements in Taxonomic Problems" (Annals of Eugenics, 1936)
- Hastie, Tibshirani, Friedman, "ESL", Ch. 4
- Murphy, "Probabilistic Machine Learning", Ch. 8
