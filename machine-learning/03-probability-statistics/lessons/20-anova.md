# Lesson 20: Analysis of Variance (ANOVA)

## Learning Objectives

After completing this lesson, you will be able to:
- Decompose total variance into between-group and within-group components
- Conduct one-way and two-way ANOVA tests
- Check ANOVA assumptions and apply corrections when violated
- Perform post-hoc comparisons with multiple testing corrections
- Compute and interpret effect sizes

## One-Way ANOVA

### Model

$$Y_{ij} = \mu + \alpha_i + \varepsilon_{ij}, \quad \varepsilon_{ij} \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, \sigma^2)$$

where:
- $Y_{ij}$: $j$-th observation in group $i$ ($i = 1, \dots, k$, $j = 1, \dots, n_i$)
- $\mu$: grand mean
- $\alpha_i$: effect of group $i$ (with $\sum n_i \alpha_i = 0$ for identifiability)
- $\varepsilon_{ij}$: random error, normally distributed with constant variance

### Hypotheses

$$H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_k = 0 \quad \text{(all group means equal)}$$
$$H_1: \text{at least one } \alpha_i \neq 0$$

## Sums of Squares Decomposition

### Total Sum of Squares (SST)

$$\text{SST} = \sum_{i=1}^k \sum_{j=1}^{n_i} (Y_{ij} - \bar{Y}_{..})^2$$

Total variability in the data.

### Between-Group Sum of Squares (SSB)

$$\text{SSB} = \sum_{i=1}^k n_i (\bar{Y}_{i.} - \bar{Y}_{..})^2$$

Variability **between** group means — the "signal" we want to detect.

### Within-Group Sum of Squares (SSW)

$$\text{SSW} = \sum_{i=1}^k \sum_{j=1}^{n_i} (Y_{ij} - \bar{Y}_{i.})^2$$

Variability **within** groups — the "noise" or natural variation.

### Fundamental Identity

$$\text{SST} = \text{SSB} + \text{SSW}$$

## ANOVA Table

| Source | SS | df | MS | F |
|--------|----|----|----|----|
| Between groups | SSB | $k-1$ | MSB = SSB/(k-1) | $F = \frac{\text{MSB}}{\text{MSW}}$ |
| Within groups | SSW | $N-k$ | MSW = SSW/(N-k) | |
| Total | SST | $N-1$ | | |

Under $H_0$: $F \sim F_{k-1, N-k}$

## Two-Way ANOVA

### Model with Interaction

$$Y_{ijk} = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \varepsilon_{ijk}$$

- $\alpha_i$: main effect of factor A ($a$ levels)
- $\beta_j$: main effect of factor B ($b$ levels)
- $(\alpha\beta)_{ij}$: interaction effect
- $\varepsilon_{ijk} \sim \mathcal{N}(0, \sigma^2)$

### ANOVA Table (Two-Way)

| Source | SS | df | MS | F |
|--------|----|----|----|----|
| Factor A | SSA | $a-1$ | MSA | $F_A$ |
| Factor B | SSB | $b-1$ | MSB | $F_B$ |
| Interaction | SSAB | $(a-1)(b-1)$ | MSAB | $F_{AB}$ |
| Error | SSE | $N-ab$ | MSE | |
| Total | SST | $N-1$ | | |

### Types of Sums of Squares

- **Type I (Sequential):** Order-dependent, tests each factor after adjusting for previous factors
- **Type II (Hierarchical):** Tests each factor after adjusting for all other factors except interactions containing it
- **Type III (Partial):** Tests each factor after adjusting for all other factors, respecting the marginality principle

## Assumptions

1. **Independence:** Observations are independent within and between groups
2. **Normality:** Residuals $\varepsilon_{ij}$ are normally distributed
3. **Homoscedasticity:** Constant variance $\sigma^2$ across all groups

### Diagnostics

| Assumption | Check | What to Look For |
|------------|-------|------------------|
| Normality | Q-Q plot of residuals | Points follow diagonal |
| Homoscedasticity | Residuals vs fitted plot | Constant spread |
| Independence | Residuals vs order plot | No pattern |

### When Assumptions Are Violated

- **Heteroscedasticity:** Use Welch's ANOVA (does not assume equal variance) or transform data
- **Non-normality:** Use Kruskal-Wallis test (non-parametric), or bootstrap
- **Independence:** Use mixed models with random effects

## Post-Hoc Tests

After a significant overall F-test, determine which groups differ:

| Method | Control |
|--------|---------|
| Tukey's HSD | All pairwise comparisons, controls FWER |
| Bonferroni | Simple correction: $\alpha/m$ for $m$ tests |
| Scheffé | All possible contrasts, very conservative |
| Dunnett | Each group vs control |
| Holm | Sequential Bonferroni, less conservative |
| Benjamini-Hochberg | Controls FDR |

## Effect Size Measures

### Eta-squared ($\eta^2$)

$$\eta^2 = \frac{\text{SSB}}{\text{SST}} = \text{proportion of variance explained}$$

### Partial Eta-squared ($\eta^2_p$)

$$\eta^2_p = \frac{\text{SS}_{\text{effect}}}{\text{SS}_{\text{effect}} + \text{SS}_{\text{error}}}$$

Used in two-way and higher ANOVA to isolate the effect of each factor.

### Cohen's Guidelines for $\eta^2$

- Small: $\eta^2 = 0.01$
- Medium: $\eta^2 = 0.06$
- Large: $\eta^2 = 0.14$

### Omega-squared ($\omega^2$)

Less biased than $\eta^2$:
$$\hat{\omega}^2 = \frac{\text{SSB} - (k-1)\text{MSW}}{\text{SST} + \text{MSW}}$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Generate data for one-way ANOVA
np.random.seed(42)
k, n_per_group = 4, 30
group_means = [0, 0.5, 1.0, 1.5]
data = []
groups = []
for i, mu in enumerate(group_means):
    vals = np.random.normal(mu, 1.0, n_per_group)
    data.extend(vals)
    groups.extend([f'Group {i+1}'] * n_per_group)

# One-way ANOVA using scipy
f_stat, p_val = stats.f_oneway(*[data[i*n_per_group:(i+1)*n_per_group]
                                   for i in range(k)])
print(f"One-way ANOVA: F = {f_stat:.3f}, p = {p_val:.6f}")

# Using statsmodels
import pandas as pd
df = pd.DataFrame({'value': data, 'group': groups})
model = ols('value ~ C(group)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print("\nANOVA Table:")
print(anova_table)

# Check assumptions
residuals = model.resid
fitted = model.fittedvalues

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Q-Q plot
sm.qqplot(residuals, line='s', ax=axes[0])
axes[0].set_title('Q-Q Plot of Residuals')

# Residuals vs fitted
axes[1].scatter(fitted, residuals, alpha=0.6)
axes[1].axhline(y=0, color='r', linestyle='--')
axes[1].set_xlabel('Fitted values')
axes[1].set_ylabel('Residuals')
axes[1].set_title('Residuals vs Fitted')

# Boxplot by group
axes[2].boxplot([data[i*n_per_group:(i+1)*n_per_group] for i in range(k)],
                labels=[f'G{i+1}' for i in range(k)])
axes[2].set_title('Data by Group')

plt.tight_layout()
plt.show()

# Post-hoc: Tukey HSD
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(data, groups, alpha=0.05)
print("\nTukey HSD Results:")
print(tukey)

# Effect size
ssb = sum(n_per_group * (np.mean(data[i*n_per_group:(i+1)*n_per_group]) - np.mean(data))**2
          for i in range(k))
sst = sum((d - np.mean(data))**2 for d in data)
eta_sq = ssb / sst
print(f"\nEffect size: η² = {eta_sq:.3f}")

# Two-way ANOVA example
a_levels, b_levels = 2, 3
n_rep = 10
data_2way = []
a_factors, b_factors = [], []
for a in range(a_levels):
    for b in range(b_levels):
        effect = a * 0.5 + b * 0.3 + a * b * 0.1  # main + interaction
        vals = np.random.normal(effect, 1.0, n_rep)
        data_2way.extend(vals)
        a_factors.extend([f'A{a+1}'] * n_rep)
        b_factors.extend([f'B{b+1}'] * n_rep)

df2 = pd.DataFrame({'value': data_2way, 'A': a_factors, 'B': b_factors})
model2 = ols('value ~ C(A) * C(B)', data=df2).fit()
anova2 = sm.stats.anova_lm(model2, typ=2)
print("\nTwo-way ANOVA:")
print(anova2)
```

## Visualization

Create an interaction plot for two-way ANOVA: plot mean response for each combination of factors A and B, connecting points of the same level of factor B. Parallel lines suggest no interaction; non-parallel lines indicate interaction. Add a second panel showing boxplots per group, and a third showing the residuals vs fitted plot for assumption checking.

## Practical Considerations

- **Unbalanced designs:** When group sizes differ, use Type II or Type III sums of squares. Type I (sequential) depends on the order of factors.
- **Repeated measures ANOVA:** For within-subject designs, use repeated measures ANOVA or mixed models (which handle sphericity violations better).
- **MANOVA:** For multiple correlated outcome variables, use multivariate ANOVA.
- **ANCOVA:** To control for continuous covariates, use analysis of covariance.
- **Non-parametric alternative:** Kruskal-Wallis test for one-way, Friedman test for repeated measures.

## References

- Fisher, R. A. (1925). *Statistical Methods for Research Workers*
- Scheffé, H. (1959). *The Analysis of Variance*
- Tukey, J. W. (1949). "Comparing individual means in the analysis of variance"
- Maxwell, S. E. & Delaney, H. D. (2004). *Designing Experiments and Analyzing Data*
