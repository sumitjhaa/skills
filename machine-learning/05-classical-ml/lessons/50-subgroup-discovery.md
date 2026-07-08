# Lesson 05.50: Subgroup Discovery

## Learning Objectives
- Understand subgroup discovery for descriptive rule mining
- Implement quality measures (WRAcc, lift, information gain)
- Apply SD-Map algorithm for exhaustive search
- Distinguish from association rules and classification

## Problem
Find subgroups $S$ described by a conjunction of conditions where distribution of target $y$ differs significantly from overall population:

$$\text{qual}(S) = \text{quality}(D_S, D)$$

- $D_S = \{i : \text{conditions}_S(x_i) \text{ holds}\}$ — instances covered by $S$
- $D$: entire dataset
- Target $y$: binary, nominal, or numeric

## Quality Measures

### Binomial Test
$$q(S) = \sqrt{n_S} \cdot (p_S - p_0)$$

- $n_S$: subgroup size
- $p_S$: target proportion in subgroup
- $p_0$: target proportion overall

### WRAcc (Weighted Relative Accuracy)
$$\text{WRAcc}(S) = \frac{n_S}{n} (p_S - p_0)$$

Balances subgroup size with deviation from overall mean. Simple and interpretable.

### Information Gain
$$\text{IG}(S) = H(p_0) - \frac{n_S}{n} H(p_S) - \frac{n - n_S}{n} H(p_{\neg S})$$

- $H(p) = -p \log p - (1-p)\log(1-p)$: binary entropy
- Measures reduction in uncertainty about target

### Other Measures
- **Lift**: $p_S / p_0$ — relative increase over baseline (biased toward small subgroups)
- **Chi-square**: $\sum \frac{(O - E)^2}{E}$ — statistical significance (interpretable as p-value)
- **Fisher's exact test**: Exact p-value for 2×2 table
- **Cosine**: $\sqrt{\text{supp}(S) \cdot \frac{p_S}{p_0}}$ — balances coverage and lift
- **Odds ratio**: $\frac{p_S/(1-p_S)}{p_0/(1-p_0)}$

## SD-Map Algorithm
Extension of FP-Growth for subgroup discovery:

1. **Frequent pattern enumeration**: Use FP-tree to find all itemsets meeting minimum support
2. **Quality computation**: For each frequent itemset, compute subgroup quality
3. **Top-$k$ selection**: Return $k$ subgroups with highest quality scores

**Optimization**: Prune branches where quality cannot exceed current top-$k$ (bounds based on optimistic estimate).

## Exceptional Model Mining (EMM)
Generalizes SD to complex target types:
- **Regression models**: Subgroup where linear model differs significantly
- **Correlation**: Subgroup where correlation between two variables is exceptional
- **Auto-correlation**: Subgroup with unusual time series structure
- **Graph properties**: Subgroup with unusual network properties

## Descriptive vs Predictive
- **Subgroup discovery** is **descriptive**: Find interesting patterns in data
- **Classification** is **predictive**: Build model for future prediction
- SD can generate hypotheses; classification makes decisions

## Code: WRAcc Computation

```python
import numpy as np

def wracc(cover, target):
    """Weighted Relative Accuracy for subgroup"""
    n = len(target)
    n_S = np.sum(cover)
    if n_S == 0:
        return 0
    p0 = np.mean(target)
    pS = np.mean(target[cover])
    return (n_S / n) * (pS - p0)

def subgroup_quality(p0, pS, n_S, n, measure='wracc'):
    if measure == 'wracc':
        return (n_S / n) * (pS - p0)
    elif measure == 'lift':
        return pS / p0 if p0 > 0 else float('inf')
    elif measure == 'binomial':
        return np.sqrt(n_S) * (pS - p0)
    elif measure == 'information_gain':
        def H(p):
            p = np.clip(p, 1e-10, 1 - 1e-10)
            return -p * np.log2(p) - (1-p) * np.log2(1-p)
        H0 = H(p0)
        HS = H(pS)
        HnS = H((p0 * n - pS * n_S) / max(n - n_S, 1))
        return H0 - n_S/n * HS - (n - n_S)/n * HnS
```

## Practical Considerations
- **Minimum support**: Avoids trivial subgroups with very few instances
- **Multiple hypothesis correction**: Use Bonferroni, Holm-Bonferroni, or FDR correction when testing many subgroups
- **Interpretability**: Limit conditions per subgroup (description length penalty)
- **Overlapping subgroups**: Subgroups may overlap — consider redundancy in results
- **Numerical attributes**: Discretize before search (e.g., entropy-based binning)
- **Beam search**: For large search spaces, use beam search instead of exhaustive SD-Map

## Applications
- **Medical**: Find patient subgroups with unusual treatment response
- **Marketing**: Identify customer segments with high conversion rates
- **Quality control**: Find process parameters leading to defects
- **Social science**: Discover population subgroups with different attitudes

## Key Properties
- Explores space of conjunctive descriptions (like association rules)
- Quality measure guides the search
- Multiple hypothesis testing correction needed
- Subgroups should be interpretable (small description length)
- Can be exhaustive (SD-Map) or heuristic (beam search, genetic algorithms)

## References
- Wrobel, "An Algorithm for Multi-relational Discovery of Subgroups" (PKDD 1997)
- Klösgen, "Explora: A Multipattern and Multistrategy Discovery Assistant" (Advances in KDD, 1996)
- Atzmueller, "Subgroup Discovery" (WIREs Data Mining, 2015)
- Lavrač et al., "Subgroup Discovery with CN2-SD" (JMLR, 2004)
- Duivesteijn et al., "Exceptional Model Mining" (Data Mining and Knowledge Discovery, 2012)
