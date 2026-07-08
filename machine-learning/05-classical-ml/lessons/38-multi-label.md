# Lesson 05.38: Multi-Label Learning

## Learning Objectives
- Understand problem transformation methods (BR, CC, LP)
- Implement classifier chains for label dependence modeling
- Evaluate with Hamming loss, exact match, and F1
- Apply to text tagging and image annotation

## Problem
Each instance $x$ is associated with multiple labels $Y \subseteq \{1, \dots, L\}$.
- Binary relevance matrix of size $n \times L$
- Labels are not mutually exclusive

## Problem Transformation Methods

### Binary Relevance (BR)
Train $L$ independent binary classifiers:

$$h_j: \mathcal{X} \to \{0, 1\}, \quad j = 1, \dots, L$$

- **Pros**: Simple, parallelizable, $O(L)$ training time
- **Cons**: Ignores label correlations (each classifier blind to others)
- **Baseline**: Surprisingly strong, often hard to beat

### Classifier Chains (CC)
Train $L$ classifiers in chain, each using previous predictions as features:

$$h_j: \mathcal{X} \times \{0, 1\}^{j-1} \to \{0, 1\}$$

- **Pros**: Captures label dependencies (causal chain assumption)
- **Cons**: Order matters — use ensemble of random orders (ECC)
- **Complexity**: $O(L^2)$ training, $O(L^2)$ inference

### Label Powerset (LP)
Treat each label subset as a unique class:

$$|Y| = 2^L \text{ possible classes}$$

- **Pros**: Captures all correlations naturally
- **Cons**: Scales poorly ($2^L$ classes, many with few examples)
- **When to use**: Only when $L$ is small ($L < 10$)

### RAKEL (RAndom k-labELsets)
1. Sample $m$ random subsets of labels, each of size $k$
2. Train LP classifier for each subset
3. Combine via voting (or weighted voting)

- Balances correlation capture with complexity
- $k = 3$ and $m = 2L$ are common defaults

## Algorithm Adaptation

### Multi-Label k-NN (MLKNN)
For each test point:
1. Find $k$ nearest neighbors
2. Count neighbors with each label
3. Apply Bayesian posterior: $P(l_j = 1|x) \propto P(\text{prior}_j) \cdot \prod \text{likelihood}$

### Multi-Label Decision Trees
Modified splitting criteria for multi-label impurity:

$$\text{Gini}_{\text{multi}}(S) = \sum_{j=1}^L \text{Gini}(S, j)$$

### Multi-Label Neural Networks
Output layer with $L$ sigmoid units and binary cross-entropy loss per label.

## Evaluation Metrics

### Example-based
- **Hamming loss**: $\frac{1}{L} \sum_{j=1}^L [\hat{y}_j \neq y_j]$ — fraction of misclassified labels
- **Exact match**: $[\hat{Y} = Y]$ — all labels must be correct (strict)
- **F1 example**: $F_1(\hat{Y}, Y)$ — per-instance F1

### Label-based
- **Macro-averaged**: Compute metric per label, average — each label equal weight
- **Micro-averaged**: Aggregate TP/FP/FN across all labels — each instance-label pair equal weight

### Ranking-based
- **Coverage**: How far down the ranked list needed to cover all true labels
- **One-error**: How often top-ranked label is not relevant
- **Average precision**: Multi-label extension of AP

## Code: Classifier Chains

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

class ClassifierChain:
    def __init__(self, base_estimator=None):
        self.base_estimator = base_estimator or LogisticRegression()
        self.chains_ = []

    def fit(self, X, Y):
        n, L = Y.shape
        Y_aug = Y.copy()
        for j in range(L):
            clf = self.base_estimator.__class__()
            X_aug = np.hstack([X, Y_aug[:, :j]])
            clf.fit(X_aug, Y[:, j])
            self.chains_.append(clf)

    def predict(self, X):
        n = X.shape[0]
        L = len(self.chains_)
        Y_pred = np.zeros((n, L))
        for j, clf in enumerate(self.chains_):
            X_aug = np.hstack([X, Y_pred[:, :j]])
            Y_pred[:, j] = clf.predict(X_aug)
        return Y_pred
```

## Dataset Characteristics
- **Label cardinality**: Average number of labels per instance (gives sense of density)
- **Label density**: Cardinality divided by $L$
- **Distinct label sets**: Number of unique label combinations (indicates correlation structure)
- **Label imbalance**: Some labels are much rarer than others

## Practical Considerations
- **BR is the baseline** — compare any method against it
- **Label correlation**: CC helps when labels are strongly correlated
- **Threshold calibration**: Adjust threshold per label (not always 0.5)
- **Large $L$ ($> 100$)**: Use embedding methods (label space dimension reduction)
- **Label hierarchy**: Use hierarchical methods if labels have structure (e.g., taxonomy)
- **Missing labels**: Treat as negative or use positive-unlabeled learning per label

## References
- Tsoumakas & Katakis, "Multi-Label Classification: An Overview" (IJDWM, 2007)
- Read et al., "Classifier Chains for Multi-label Classification" (Machine Learning, 2011)
- Tsoumakas, Katakis, Vlahavas, "Random k-Labelsets for Multi-Label Classification" (IEEE TKDE, 2010)
- Zhang & Zhou, "A Review on Multi-Label Learning Algorithms" (IEEE TKDE, 2014)
- Madjarov et al., "An Extensive Experimental Comparison of Methods for Multi-label Learning" (Pattern Recognition, 2012)
