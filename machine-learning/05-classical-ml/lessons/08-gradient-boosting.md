# Lesson 05.08: Gradient Boosting

## Learning Objectives
- Understand additive modeling and stagewise additive expansion
- Derive pseudo-residuals from arbitrary loss functions
- Implement gradient boosting with multiple loss functions
- Apply regularization via shrinkage, subsampling, and early stopping

## Mathematical Foundation

### Additive Model
Gradient boosting builds an ensemble additively:

$$F_M(x) = \sum_{m=0}^M \beta_m h(x; a_m)$$

where $h$ is a weak learner (typically a shallow decision tree). $F_0(x) = \arg\min_\gamma \sum_i L(y_i, \gamma)$ — typically the mean (L2) or log-odds (classification).

### Stagewise Additive Modeling
At each iteration $m$, we add the base learner that most reduces the loss:

$$(\beta_m, a_m) = \arg\min_{\beta, a} \sum_{i=1}^n L(y_i, F_{m-1}(x_i) + \beta h(x_i; a))$$

## Algorithm: Gradient Boosting
1. Initialize $F_0(x) = \arg\min_\gamma \sum_i L(y_i, \gamma)$
2. For $m = 1$ to $M$:
   - Compute **pseudo-residuals**: $r_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}}$
   - Fit base learner $h_m$ to $\{(x_i, r_{im})\}_{i=1}^n$
   - Solve line search: $\gamma_m = \arg\min_\gamma \sum_i L(y_i, F_{m-1}(x_i) + \gamma h_m(x_i))$
   - Update: $F_m(x) = F_{m-1}(x) + \nu \gamma_m h_m(x)$

### Why Pseudo-Residuals?
For L2 loss $L(y,F) = \frac{1}{2}(y-F)^2$, the pseudo-residual is $r_i = y_i - F_{m-1}(x_i)$ — the standard residual. For general losses, we fit the base learner to the negative gradient direction, performing gradient descent in function space.

## Common Loss Functions

| Problem | Loss $L(y,F)$ | Pseudo-residual $-\partial L/\partial F$ |
|---------|---------------|------------------------------------------|
| Regression L2 | $\frac{1}{2}(y-F)^2$ | $y - F$ |
| Regression L1 | $|y-F|$ | $\text{sign}(y-F)$ |
| Huber | Mixed L1/L2 | Huberized residual |
| Binary | $\log(1+e^{-2yF})$ | $2y/(1+e^{2yF})$ |
| Multinomial | $-\sum_k [y=k]\log p_k$ | $[y=k] - p_k$ |
| Poisson | $e^F - yF$ | $y - e^F$ |

### Huber Loss
Combines L2 (near zero) with L1 (far from zero):

$$L_\delta(y, F) = \begin{cases} \frac{1}{2}(y-F)^2 & |y-F| \leq \delta \\ \delta(|y-F| - \delta/2) & |y-F| > \delta \end{cases}$$

Pseudo-residual: $r_i = \begin{cases} y_i - F_{m-1}(x_i) & |r_i| \leq \delta \\ \delta \cdot \text{sign}(r_i) & |r_i| > \delta \end{cases}$

Robust to outliers compared to L2, differentiable compared to L1.

## Regularization

### Shrinkage (Learning Rate)
Scale each tree's contribution: $F_m(x) = F_{m-1}(x) + \nu \cdot \gamma_m h_m(x)$

- $\nu \in (0, 1]$, typically $\nu = 0.01-0.1$
- Smaller $\nu$ requires more trees but generalizes better
- Tradeoff: number of trees $M \propto 1/\nu$

### Stochastic Gradient Boosting
Use random subsample (~50%) at each iteration:
- Reduces correlation between trees
- Speeds computation
- Allows out-of-bag estimates

### Other Regularization
- **Tree constraints**: max depth (3-6), min samples per leaf, min impurity decrease
- **Early stopping**: monitor validation loss, stop when no improvement for $n$ rounds
- **Penalized splits**: add complexity penalty to split gain

## Code: Gradient Boosting Regressor

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

class GradientBoosting:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3, subsample=1.0):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.subsample = subsample
        self.trees = []

    def fit(self, X, y):
        n = X.shape[0]
        self.F0 = np.mean(y)
        F = np.full(n, self.F0)
        self.trees = []
        for _ in range(self.n_estimators):
            residuals = y - F  # pseudo-residuals for L2
            if self.subsample < 1.0:
                idx = np.random.choice(n, int(n * self.subsample), replace=False)
                tree = DecisionTreeRegressor(max_depth=self.max_depth)
                tree.fit(X[idx], residuals[idx])
            else:
                tree = DecisionTreeRegressor(max_depth=self.max_depth)
                tree.fit(X, residuals)
            h = tree.predict(X)
            F += self.learning_rate * h
            self.trees.append(tree)

    def predict(self, X):
        pred = np.full(X.shape[0], self.F0)
        for tree in self.trees:
            pred += self.learning_rate * tree.predict(X)
        return pred
```

## Comparison with Random Forest

| Aspect | Gradient Boosting | Random Forest |
|--------|------------------|---------------|
| Training | Sequential (slow) | Parallel (fast) |
| Trees | Shallow (depth 3-6) | Deep (full grown) |
| Bias | Low (focuses on errors) | Low (averaging reduces variance) |
| Variance | High (needs regularization) | Low |
| Parameters | Learning rate, n_estimators, depth | n_estimators, max_features |
| Overfitting | Easy (needs careful tuning) | Harder (more robust) |

## References
- Friedman, "Greedy Function Approximation: A Gradient Boosting Machine" (Ann. Statistics, 2001)
- Friedman, "Stochastic Gradient Boosting" (Computational Statistics, 2002)
- Hastie et al., "ESL", Ch. 10
- Natekin & Knoll, "Gradient Boosting Machines, A Tutorial" (Frontiers in Neurorobotics, 2013)
