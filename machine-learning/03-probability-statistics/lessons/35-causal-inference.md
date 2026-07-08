# Lesson 35: Causal Inference

## Learning Objectives

After completing this lesson, you will be able to:
- Define causal effects using the potential outcomes framework
- Understand assumptions required for causal identification
- Apply methods for causal estimation in observational studies
- Use instrumental variables for unmeasured confounding
- Construct and interpret causal DAGs

## Potential Outcomes Framework

### Setup

For each unit $i$ and treatment $t \in \{0, 1\}$:
- $Y_i(1)$: potential outcome if treated
- $Y_i(0)$: potential outcome if untreated

### Individual Causal Effect

$$\tau_i = Y_i(1) - Y_i(0)$$

### Fundamental Problem of Causal Inference

We observe $Y_i = T_i Y_i(1) + (1-T_i) Y_i(0)$ — only one potential outcome per unit. The counterfactual is always missing.

### Average Treatment Effect (ATE)

$$\tau_{\text{ATE}} = E[Y(1) - Y(0)]$$

### Average Treatment Effect on the Treated (ATT)

$$\tau_{\text{ATT}} = E[Y(1) - Y(0) \mid T = 1]$$

## Identification Assumptions

### Stable Unit Treatment Value Assumption (SUTVA)

1. **No interference:** Treatment of one unit does not affect outcomes of other units
2. **Consistency:** The observed outcome equals the potential outcome under the observed treatment: $Y_i = Y_i(T_i)$

### Ignorability (Unconfoundedness)

$$Y(1), Y(0) \perp T \mid X$$

Given covariates $X$, treatment assignment is "as good as random." This holds by design in randomized experiments but requires conditioning on all confounders in observational studies.

### Positivity (Overlap)

$$0 < P(T = 1 \mid X = x) < 1 \quad \forall x$$

Every unit has a positive probability of receiving both treatment and control.

## Randomized Experiments

### Gold Standard

Randomization ensures $Y(1), Y(0) \perp T$ (unconfoundedness holds without conditioning).

$$\tau_{\text{ATE}} = E[Y \mid T=1] - E[Y \mid T=0]$$

### Block Randomization

Randomize within strata defined by $X$ to improve precision and ensure balance.

## Observational Study Methods

### Stratification

1. Divide data into strata based on $X$
2. Estimate ATE within each stratum
3. Average with stratum-size weights

**Limitation:** Curse of dimensionality with many covariates.

### Propensity Score Methods

The **propensity score** is $e(X) = P(T=1 \mid X)$.

**Propensity score theorem** (Rosenbaum & Rubin, 1983): If unconfoundedness holds given $X$, it also holds given $e(X)$.

**Inverse Probability of Treatment Weighting (IPTW):**

$$\hat{\tau}_{\text{IPTW}} = \frac{1}{n} \sum_{i=1}^n \left(\frac{T_i Y_i}{\hat{e}(X_i)} - \frac{(1-T_i) Y_i}{1 - \hat{e}(X_i)}\right)$$

**Matching:** Match each treated unit to one or more control units with similar $e(X)$. Estimate ATE as average within-match difference.

### Doubly Robust Estimation

Combine regression and propensity score:
$$\hat{\tau}_{\text{DR}} = \frac{1}{n} \sum_{i=1}^n \left[\hat{\mu}_1(X_i) - \hat{\mu}_0(X_i) + \frac{T_i(Y_i - \hat{\mu}_1(X_i))}{\hat{e}(X_i)} - \frac{(1-T_i)(Y_i - \hat{\mu}_0(X_i))}{1-\hat{e}(X_i)}\right]$$

**Consistent if either the outcome model $\hat{\mu}_t$ or the propensity model $\hat{e}$ is correctly specified.**

## Instrumental Variables

### Setup

When unconfoundedness fails due to unmeasured confounding, an **instrument** $Z$ can identify causal effects.

### Requirements

1. **Relevance:** $Z \not\perp T \mid X$ (instrument affects treatment)
2. **Exclusion:** $Z \perp Y \mid T, X$ (instrument affects outcome only through treatment)
3. **Independence:** $Z \perp \text{confounders}$ (instrument is as good as randomly assigned)

### Wald Estimator (binary instrument, binary treatment)

$$\hat{\tau}_{\text{IV}} = \frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{E[T \mid Z=1] - E[T \mid Z=0]}$$

This estimates the **local average treatment effect (LATE)** — the effect for compliers (units whose treatment is affected by the instrument).

## Causal Directed Acyclic Graphs (DAGs)

### Nodes and Edges

- **Directed edge** $X \to Y$: $X$ causes $Y$
- **Path:** Sequence of connected edges

### Causal Structures

| Structure | Pattern | Implication |
|-----------|---------|-------------|
| Chain | $X \to M \to Y$ | $M$ is a mediator |
| Fork | $X \leftarrow C \to Y$ | $C$ is a confounder |
| Collider | $X \to C \leftarrow Y$ | $C$ is a collider |

### do-Calculus (Pearl)

$$P(Y \mid do(T=t)) = \sum_z P(Y \mid T=t, Z=z) P(Z=z)$$

For a set $Z$ satisfying the back-door criterion (all confounders).

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Generate data with confounding
np.random.seed(42)
n = 2000
X = np.random.normal(0, 1, (n, 3))

# Treatment depends on X1, X2
logit = X[:, 0] - 0.5 * X[:, 1] + np.random.normal(0, 0.5, n)
T = 1 / (1 + np.exp(-logit)) > np.random.uniform(0, 1, n)

# Outcome depends on treatment + X1, X3
Y = 2.0 + 1.5 * T + 0.8 * X[:, 0] - 0.3 * X[:, 2] + np.random.normal(0, 0.5, n)

print(f"Treatment rate: {T.mean():.2%}")
print(f"Naive ATE: {Y[T==1].mean() - Y[T==0].mean():.3f} (confounded)")
print(f"True ATE: 1.500")

# Propensity score estimation
ps_model = LogisticRegression(C=1e5).fit(X, T)
ps = ps_model.predict_proba(X)[:, 1]

# IPTW
weights = np.where(T, 1/ps, 1/(1-ps))
iptw_ate = np.average(Y[T==1], weights=weights[T==1]) - \
           np.average(Y[T==0], weights=weights[T==0])
print(f"IPTW ATE: {iptw_ate:.3f}")

# Check overlap
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.hist(ps[T==0], bins=40, alpha=0.5, label='Control', density=True)
plt.hist(ps[T==1], bins=40, alpha=0.5, label='Treated', density=True)
plt.xlabel('Propensity score')
plt.legend()
plt.title('Overlap Check')

# Matching (nearest neighbor)
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=1)
nn.fit(ps[T==0].reshape(-1, 1))
dists, indices = nn.kneighbors(ps[T==1].reshape(-1, 1))
matches = np.where(T==0)[0][indices.flatten()]

matched_Y_treated = Y[T==1]
matched_Y_control = Y[matches]
matched_ate = np.mean(matched_Y_treated - matched_Y_control)
print(f"Propensity matching ATE: {matched_ate:.3f}")

# Doubly robust estimation
outcome_model = RandomForestRegressor(n_estimators=100, random_state=42)

# E[Y|T=1, X]
outcome_model.fit(X[T==1], Y[T==1])
mu1 = outcome_model.predict(X)

# E[Y|T=0, X]
outcome_model.fit(X[T==0], Y[T==0])
mu0 = outcome_model.predict(X)

dr_ate = np.mean(mu1 - mu0 +
                  T * (Y - mu1) / ps -
                  (1 - T) * (Y - mu0) / (1 - ps))
print(f"Doubly robust ATE: {dr_ate:.3f}")

# IPTW distribution
weights_clipped = np.clip(weights, 0.01, 20)
plt.subplot(132)
plt.hist(weights_clipped, bins=50)
plt.xlabel('IPTW weight')
plt.title('Weight Distribution')

plt.subplot(133)
methods = ['Naive', 'IPTW', 'Matching', 'Doubly Robust', 'True']
estimates = [Y[T==1].mean() - Y[T==0].mean(), iptw_ate, matched_ate, dr_ate, 1.5]
colors = ['red', 'blue', 'green', 'purple', 'black']
for i, (m, e, c) in enumerate(zip(methods, estimates, colors)):
    plt.bar(i, e, color=c, alpha=0.7)
    plt.axhline(y=1.5, color='k', linestyle='--', lw=0.5)
plt.xticks(range(len(methods)), methods, rotation=45)
plt.ylabel('ATE estimate')
plt.title('Method Comparison')

plt.tight_layout()
plt.show()
```

## Visualization

Create a "balance plot" showing covariate distributions before and after propensity score weighting — standardized mean differences should be near zero after weighting. The overlap histogram of propensity scores for treated and control should show substantial overlap. A forest plot compares ATE estimates across methods.

## Practical Considerations

- **Unmeasured confounding:** The single biggest threat. Sensitivity analysis (E-value, Rosenbaum bounds) quantifies how strong an unmeasured confounder must be to explain away the result.
- **Model misspecification:** Propensity score and outcome models can both be wrong. Doubly robust estimation protects against one being misspecified.
- **Positivity violations:** If $P(T=1 \mid X) \approx 0$ or $\approx 1$ for some $X$, IPTW estimates are unstable. Trim or truncate extreme weights.
- **Multiple treatments:** Generalize to multiple or continuous treatments using generalized propensity scores or dose-response methods.
- **Mediation analysis:** Decompose the total effect into direct and indirect effects (through mediators).

## References

- Rubin, D. B. (1974). "Estimating causal effects of treatments in randomized and nonrandomized studies"
- Rosenbaum, P. R. & Rubin, D. B. (1983). "The central role of the propensity score in observational studies for causal effects"
- Pearl, J. (2009). *Causality*
- Hernán, M. A. & Robins, J. M. (2020). *Causal Inference: What If*
- Angrist, J. D. & Pischke, J. S. (2009). *Mostly Harmless Econometrics*
