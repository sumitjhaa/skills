# 04.36 Information-Theoretic Feature Selection

## Motivation
Selecting the most informative features is critical for building interpretable, efficient, and generalisable models. Information-theoretic criteria — mutual information, conditional mutual information — provide principled ways to rank and select features, capturing relevance, redundancy, and complementarity in a unified framework.

## Learning Objectives
- Define mutual information and conditional mutual information for feature selection.
- Implement the MRMR criterion and conditional likelihood maximisation.
- Identify the Markov blanket and its role in optimal feature selection.
- Apply information-theoretic feature selection to high-dimensional data.

## Math Foundation

### Relevance, Redundancy, Complementarity
Let $X_i$ be a feature, $X_j$ another feature, and $Y$ the target variable.

- **Relevance**: $I(X_i; Y)$ — how much information $X_i$ provides about $Y$.
- **Redundancy**: $I(X_i; X_j)$ — shared information between features.
- **Complementarity**: $I(X_i; Y | X_j) > I(X_i; Y)$ — $X_j$ makes $X_i$ more predictive. This occurs when $X_i$ provides novel information about $Y$ only in the context of $X_j$.

### Mutual Information
For discrete variables:

$$I(X;Y) = \sum_{x,y} p(x,y) \log \frac{p(x,y)}{p(x)p(y)} = H(Y) - H(Y|X)$$

$I(X;Y) = 0$ iff $X$ and $Y$ are independent.

### Conditional Mutual Information
$$I(X;Y|Z) = H(X|Z) - H(X|Y,Z) = \mathbb{E}_{z \sim Z}[I(X;Y|Z=z)]$$

This measures the additional information $X$ provides about $Y$ given $Z$ is already known.

### MRMR (Minimum Redundancy Maximum Relevance)
Select a set $S$ of features maximising:

$$J_{\text{MRMR}}(S) = \frac{1}{|S|} \sum_{i \in S} I(X_i; Y) - \frac{1}{|S|^2} \sum_{i,j \in S} I(X_i; X_j)$$

The first term encourages relevance; the second penalises redundancy. The greedy algorithm adds one feature at a time:

$$X_j^* = \arg\max_{X_j \notin S} \left[ I(X_j; Y) - \frac{1}{|S|} \sum_{i \in S} I(X_j; X_i) \right]$$

### Conditional Likelihood Maximisation (CMI)
Select the feature maximising the conditional mutual information with the selected set:

$$X_j^* = \arg\max_{X_j \notin S} I(Y; X_j | S)$$

Using the chain rule: $I(Y; X_j | S) = I(Y; X_j, S) - I(Y; S)$. This is equivalent to the conditional log-likelihood of $Y$ given $X_j$ and the already selected features.

### Markov Blanket
The Markov blanket $B(Y)$ of $Y$ in a graphical model is the minimal set of features such that:

$$Y \perp\!\!\!\perp (X \setminus B(Y)) \,|\, B(Y)$$

$B(Y)$ contains the parents, children, and co-parents (parents of children) of $Y$. The Markov blanket is the optimal feature set for predicting $Y$ — no other set yields lower predictive error.

## Python Implementation

```python
import numpy as np
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.neighbors import KLDivergence

def mrmr(X, y, n_features=10, discrete=True):
    """Minimum Redundancy Maximum Relevance feature selection (greedy)."""
    n = X.shape[1]
    
    # Compute relevance: MI between each feature and target
    if discrete:
        relevance = mutual_info_classif(X, y, random_state=42)
    else:
        relevance = mutual_info_regression(X, y, random_state=42)
    
    # Greedy forward selection
    selected = []
    remaining = list(range(n))
    
    for _ in range(min(n_features, n)):
        best_score = -np.inf
        best_feat = None
        
        for j in remaining:
            # Relevance term
            score = relevance[j]
            
            # Redundancy term: average MI with already selected features
            if selected:
                redundancy = 0
                for i in selected:
                    # Estimate MI between features (discretise if continuous)
                    bins = min(int(np.sqrt(len(X))), 20)
                    c_xy, _, _ = np.histogram2d(X[:, i], X[:, j], bins=bins)
                    c_xy = c_xy / c_xy.sum()
                    c_x = c_xy.sum(axis=1, keepdims=True)
                    c_y = c_xy.sum(axis=0, keepdims=True)
                    mi_ij = np.sum(c_xy * np.log(c_xy / (c_x @ c_y) + 1e-12))
                    redundancy += mi_ij
                score -= redundancy / len(selected)
            
            if score > best_score:
                best_score = score
                best_feat = j
        
        selected.append(best_feat)
        remaining.remove(best_feat)
    
    return selected

def conditional_mi(X, y, feature, selected_set, bins=10):
    """Estimate I(y; X_i | X_selected) via histogram."""
    y_disc = np.digitize(y, np.percentile(y, np.linspace(0, 100, bins+1)[1:-1]))
    
    if len(selected_set) == 0:
        # Just I(y; X_i)
        c_xy, _, _ = np.histogram2d(X[:, feature], y_disc, bins=bins)
        return mutual_info_from_hist(c_xy)
    
    # Multi-dimensional histogram for I(y; X_i, X_S)
    # Simplified: use kernel density estimation or nearest-neighbour MI
    from sklearn.feature_selection import mutual_info_regression
    X_sub = np.column_stack([X[:, feature]] + [X[:, i] for i in selected_set])
    mi_joint = mutual_info_regression(X_sub, y, random_state=42)[0]
    
    # I(y; X_S)
    X_selected = X[:, list(selected_set)]
    mi_selected = mutual_info_regression(X_selected, y, random_state=42)[0] if selected_set else 0
    
    return mi_joint - mi_selected

def mutual_info_from_hist(counts):
    """Compute MI from a 2D histogram count matrix."""
    counts = counts + 1e-12  # smoothing
    joint = counts / counts.sum()
    mi = 0
    for i in range(joint.shape[0]):
        for j in range(joint.shape[1]):
            if joint[i,j] > 0:
                mi += joint[i,j] * np.log(joint[i,j] / (joint[i,:].sum() * joint[:,j].sum()))
    return mi

# Example: feature selection on synthetic data
np.random.seed(42)
n, d = 500, 20

# Generate data: Y depends on a few features
X = np.random.randn(n, d)
relevant_idx = [0, 3, 7]
y = X[:, 0] + 2 * X[:, 3] - 0.5 * X[:, 7] + 0.1 * np.random.randn(n)

selected_mrmr = mrmr(X, y, n_features=5, discrete=False)
print(f"MRMR selected features: {selected_mrmr}")
print(f"Relevant features: {relevant_idx}")
print(f"First 3 selected in relevant: {np.sum([s in relevant_idx for s in selected_mrmr[:3]])}")

# Compare with correlation-based selection
correlations = np.abs(np.corrcoef(X.T, y)[:-1, -1])
corr_selected = np.argsort(correlations)[::-1][:5]
print(f"Correlation-selected: {list(corr_selected)}")
```

## Visualization
Plot the mutual information between each feature and the target as a bar chart, with the selected features highlighted. A second panel shows pairwise MI between features as a heatmap — features in the same cluster have high redundancy. A third panel shows the MRMR score vs. step count, showing how the score decreases as more features are added (diminishing returns).

## Feature Selection Algorithms

### Overview of Information-Theoretic Criteria
| Criterion | Formula | Property |
|-----------|---------|----------|
| Mutual Information Maximisation (MIM) | $I(X_j; Y)$ | Picks only relevance, ignores redundancy |
| MRMR | $I(X_j; Y) - \frac{1}{|S|} \sum_{i\in S} I(X_j; X_i)$ | Relevance minus pairwise redundancy |
| Joint Mutual Information (JMI) | $\sum_{i \in S} I(X_j X_i; Y)$ | Considers pairs of features |
| Conditional Mutual Information (CMI) | $I(X_j; Y | S)$ | Full conditional criterion |
| CMIM (Conditional MI Maximisation) | $\min_i I(X_j; Y | X_i)$ | Worst-case redundancy penalisation |
| Joint MI (JMI) | $I(X_j; Y) - \frac{1}{|S|} \sum_i [I(X_j; X_i) - I(X_j; X_i|Y)]$ | Corrects MRMR for complementarity |

### Greedy Forward Selection
The standard algorithm:
1. Start with $S = \emptyset$.
2. For each candidate $X_j \notin S$, compute the criterion $J(X_j; S)$.
3. Select $X_j^* = \arg\max J(X_j; S)$.
4. Add $X_j^*$ to $S$, repeat until $|S| = k$ or no improvement.
5. Complexity: $O(k d)$ criteria evaluations.

### Estimation of MI
- **Histogram**: simple but biased; requires bin selection.
- **Kernel density estimation**: smoother but parameter-dependent.
- **$k$-nearest neighbours** (Kraskov et al. 2004): consistent and adaptive; the KSG estimator uses distances to $k$th neighbours.
- **Learned MI estimators**: MINE (Belghazi et al. 2018) uses a neural network to estimate the Donsker-Varadhan lower bound.

## Connections to Machine Learning

### High-Dimensional Genomics
In genomics, the number of features (genes) typically far exceeds the number of samples ($p \gg n$). Information-theoretic feature selection:
- Identifies biomarker panels for disease classification.
- Captures non-linear dependencies that correlation-based methods miss.
- The Markov blanket corresponds to the set of genes directly involved in the regulatory network of the target phenotype.

### Interpretable Modelling
Feature selection is essential for interpretability:
- Lasso ($\ell_1$ regularisation) selects features via linear shrinkage but is limited to linear dependencies.
- Information-theoretic methods capture non-linear relationships without assuming a functional form.
- The selected features can be visualised and inspected by domain experts.

### Causal Feature Selection
Under the causal Markov condition, the Markov blanket of $Y$ equals its direct causes and direct effects. Algorithms like MBOR (Markov Blanket Oracle) and IAMB (Incremental Association Markov Blanket) use conditional independence tests to discover the Markov blanket, providing causally interpretable feature sets.

### Feature Selection for Deep Learning
While deep networks learn representations end-to-end, feature selection is still useful:
- **Input pruning**: remove irrelevant features to improve efficiency and reduce overfitting.
- **Attention-based selection**: attention weights can be interpreted as feature relevance.
- **Neural feature selection**: learn binary gates (concrete relaxation) that select features during training.

## Practical Considerations

### Estimating MI in Practice
- **Small samples**: histogram-based MI is heavily biased. Use KSG estimator which has lower bias.
- **Continuous features**: discretise or use kernel-based estimation with careful bandwidth selection.
- **High dimensions**: conditional MI with many features is hard to estimate — use pairwise approximations (JMI, MRMR).

### Choosing the Number of Features
- Use cross-validation: add features incrementally and stop when test performance saturates.
- Use the "elbow" in the MI cumulative relevance curve.
- For the Markov blanket, test conditional independence: feature $X_i$ is in the blanket iff $I(X_i; Y | X \setminus \{X_i\}) > 0$.

## References
- Cover & Thomas, *Elements of Information Theory*, 2nd ed., Wiley 2006
- Brown et al., "Conditional Likelihood Maximisation: A Unifying Framework for Information Theoretic Feature Selection," *JMLR*, 2012
- Peng, Long, Ding, "Feature Selection Based on Mutual Information: Criteria of Max-Dependency, Max-Relevance, and Min-Redundancy," *IEEE TPAMI*, 2005
- Kraskov, Stögbauer, Grassberger, "Estimating Mutual Information," *Physical Review E*, 2004
- Guyon & Elisseeff, "An Introduction to Variable and Feature Selection," *JMLR*, 2003
- Tsamardinos, Aliferis, Statnikov, "Algorithms for Large Scale Markov Blanket Discovery," *FLAIRS*, 2003
