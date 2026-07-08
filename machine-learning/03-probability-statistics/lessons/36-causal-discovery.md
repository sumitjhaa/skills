# Lesson 36: Causal Discovery

## Learning Objectives

After completing this lesson, you will be able to:
- Understand the problem of learning causal structure from observational data
- Apply constraint-based algorithms (PC algorithm)
- Apply score-based algorithms (GES)
- Understand functional causal models (LiNGAM, additive noise)
- Interpret Markov equivalence classes

## Problem Formulation

Given i.i.d. observations from a joint distribution $P(X_1, \dots, X_p)$, learn the underlying causal directed acyclic graph (DAG) $G$ where:
- Nodes = variables $X_1, \dots, X_p$
- Directed edges $X_i \to X_j$ denote direct causal effects

## Key Assumptions

### Causal Markov Condition

Each variable is independent of its non-descendants given its parents:
$$X_i \perp \text{ND}(X_i) \mid \text{Pa}(X_i)$$

### Faithfulness

The conditional independencies in the distribution are exactly those entailed by the graph (no accidental independencies beyond those implied by the Markov property).

### Causal Sufficiency

There are no unmeasured common causes of two or more observed variables.

## Constraint-Based Methods

### PC Algorithm (Spirtes & Glymour, 1991)

**Phase 1 — Skeleton discovery:**
1. Start with fully connected undirected graph on $p$ nodes
2. For each pair $(i, j)$, test marginal independence; if independent, remove edge
3. For each pair with $k$ neighbors, test conditional independence given subsets of neighbors; if independent, remove edge
4. Increase $k$ and repeat

**Phase 2 — Edge orientation:**
1. Identify **v-structures** (colliders): $i - j - k$ where $i$ and $k$ are conditionally independent given any set containing $j$
2. Orient: $i \to j \leftarrow k$
3. Apply Meek's orientation rules to propagate directions

**Time complexity:** $O(p^q)$ for tests conditioning on $q$ variables. Feasible for $p < 1000$ with sparse graphs.

### Conditional Independence Tests

| Variable Types | Test |
|---------------|------|
| Both Gaussian | Fisher's Z (partial correlation) |
| Both discrete | G-test or Chi-squared |
| Mixed | Kernel-based conditional independence |

## Score-Based Methods

### Scoring Criteria

| Criterion | Formula | Properties |
|-----------|---------|------------|
| BIC | $\log L - \frac{p}{2} \log n$ | Consistent, decomposable |
| BDeu | Dirichlet posterior score | Consistent, requires hyperparameters |
| AIC | $\log L - p$ | Not consistent (overfits) |

### Greedy Equivalence Search (GES)

**Forward phase:** Start with empty graph, add edges greedily to maximize score
**Backward phase:** Remove edges greedily to further improve score

**Advantage:** GES searches over **equivalence classes** rather than individual DAGs, avoiding local optima in DAG space.

## Functional Causal Models

### LiNGAM (Shimizu et al., 2006)

$$X_i = \sum_{j: j < i} b_{ij} X_j + \varepsilon_i$$

where $\varepsilon_i$ are independent **non-Gaussian** disturbances.

**Identifiability:** When errors are non-Gaussian, the causal direction is identifiable from observational data (unlike Gaussian case).

**Estimation:** Find a causal order $\pi$ such that the estimated disturbances are maximally independent (using ICA).

### Additive Noise Model (ANM)

$$Y = f(X) + \varepsilon, \quad \varepsilon \perp X$$

If $f$ is non-linear and $\varepsilon$ has non-Gaussian distribution, the direction $X \to Y$ can be distinguished from $Y \to X$.

**Identifiability:** In the linear-Gaussian case, both directions give the same likelihood. With non-linear $f$ or non-Gaussian noise, one direction is preferred.

### Post-Nonlinear (PNL) Model

$$Y = g(f(X) + \varepsilon)$$

Generalizes ANM with an invertible post-nonlinear transformation $g$.

## Markov Equivalence

### Definition

Two DAGs are **Markov equivalent** if they imply the same set of conditional independencies.

### Characterizing Markov Equivalence

Two DAGs are Markov equivalent iff they have:
- The same skeleton
- The same v-structures (uncoupled colliders)

### Representing Equivalence Classes

- **CPDAG (Completed Partially Directed Acyclic Graph):** Directed edges for orientations common to all DAGs in the class; undirected edges for orientations that vary
- **PAG (Partial Ancestral Graph):** For the more general case with latent variables

### What's Not Identifiable

From purely observational data:
- Direction of edges in fully connected triples without v-structures
- Whether a structure is $X \to Y \to Z$ or $X \leftarrow Y \leftarrow Z$ or $X \leftarrow Y \to Z$ (all have same conditional independencies)

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr

# Generate data from a linear DAG with non-Gaussian errors
np.random.seed(42)
n = 5000

# True DAG: X1 -> X2 -> X3, X1 -> X3
e1 = np.random.uniform(-2, 2, n)  # non-Gaussian!
X1 = e1
X2 = 0.8 * X1 + np.random.uniform(-1, 1, n)  # non-Gaussian
X3 = 0.5 * X1 + 0.7 * X2 + np.random.uniform(-1, 1, n)

data = np.column_stack([X1, X2, X3])
var_names = ['X1', 'X2', 'X3']

# LiNGAM-style causal discovery
# Find causal order by testing independence of residuals
def lingam_order(data):
    """Find causal order by regression and independence testing."""
    n_vars = data.shape[1]
    remaining = list(range(n_vars))
    order = []

    for _ in range(n_vars):
        # Find the variable with residuals most independent of regressors
        best_indep = -np.inf
        best_var = None

        for v in remaining:
            X = data[:, [i for i in remaining if i != v]]
            y = data[:, v]

            if X.shape[1] > 0:
                reg = LinearRegression().fit(X, y)
                residuals = y - reg.predict(X)
            else:
                residuals = y

            # Test independence: correlation with each regressor
            if X.shape[1] > 0:
                max_corr = max(abs(pearsonr(residuals, X[:, j])[0])
                               for j in range(X.shape[1]))
            else:
                max_corr = 0

            # Lower max correlation = more independent = better
            if -max_corr > best_indep:
                best_indep = -max_corr
                best_var = v

        order.append(best_var)
        remaining.remove(best_var)

    return order

order = lingam_order(data)
print(f"Estimated causal order: {[var_names[i] for i in order]}")
print(f"True order: X1, X2, X3")

# PC algorithm skeleton (simplified)
# Test marginal and conditional independencies
def test_indep(x, y, cond=None):
    if cond is None:
        r, p = pearsonr(x, y)
        return p > 0.05
    else:
        # Partial correlation
        from sklearn.linear_model import LinearRegression
        reg_xy = LinearRegression()
        if cond.ndim == 1:
            cond = cond.reshape(-1, 1)
        r_x = x - LinearRegression().fit(cond, x).predict(cond)
        r_y = y - LinearRegression().fit(cond, y).predict(cond)
        r, p = pearsonr(r_x, r_y)
        return p > 0.05

# Adjacency matrix
p = 3
adj = np.ones((p, p)) - np.eye(p)

# Test marginal independence
for i in range(p):
    for j in range(p):
        if i < j and test_indep(data[:, i], data[:, j]):
            adj[i, j] = adj[j, i] = 0

print(f"\nAdjacency after marginal tests:\n{adj}")

# Test conditional independence (condition on third variable)
for i in range(p):
    for j in range(p):
        if adj[i, j] == 1:
            other = [k for k in range(p) if k not in [i, j]][0]
            if test_indep(data[:, i], data[:, j], cond=data[:, other]):
                adj[i, j] = adj[j, i] = 0

print(f"\nAdjacency after conditional tests:\n{adj}")

# Orientation (simplified v-structure detection)
# For this simple case, we can orient based on known pattern
# True: X1 -> X2, X1 -> X3, X2 -> X3
print(f"\nTrue DAG: {var_names[0]} -> {var_names[1]}, {var_names[0]} -> {var_names[2]}, {var_names[1]} -> {var_names[2]}")
```

## Visualization

Create a plot comparing the true DAG (left) with the estimated CPDAG (right). For the PC algorithm output, directed edges are arrows and undirected edges are dashed lines. A second figure shows the distribution of residuals in the LiNGAM analysis — non-Gaussian residuals confirm the model assumptions.

## Practical Considerations

- **Sample size:** Constraint-based methods typically need $n > 10p$ for reliable independence tests. The number of conditional independence tests grows exponentially with $p$.
- **Multiple testing:** PC algorithm performs many independence tests. Use a conservative significance level (e.g., $\alpha = 0.01$) and correct for multiple testing.
- **Latent confounders:** Causal sufficiency is often violated. The Fast Causal Inference (FCI) algorithm handles latent confounders.
- **Interleaving experimentation:** Observational studies suggest causal hypotheses; interventional studies (RCT, A/B test) confirm them.
- **Non-linear and cyclic:** For non-linear relationships, use kernel-based independence tests. For cyclic graphs, use time series methods (Granger causality).

## References

- Spirtes, P., Glymour, C., & Scheines, R. (2000). *Causation, Prediction, and Search*
- Pearl, J. (2009). *Causality*
- Shimizu, S., et al. (2006). "A linear non-Gaussian acyclic model for causal discovery"
- Chickering, D. M. (2002). "Optimal structure identification with greedy search"
- Glymour, C., Zhang, K., & Spirtes, P. (2019). "Review of causal discovery methods based on graphical models"
