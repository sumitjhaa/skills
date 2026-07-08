# Lesson 05.35: Active Learning

## Learning Objectives
- Understand uncertainty, diversity, and expected model change strategies
- Implement uncertainty sampling and query-by-committee
- Apply batch active learning for efficiency
- Analyze stopping criteria and cold-start strategies

## Setup
Pool-based active learning:
- **Labeled set $L$**: Small set of labeled examples
- **Unlabeled pool $U$**: Large set of unlabeled examples
- **Query**: Select most informative instance(s) from $U$ for labeling
- **Goal**: Maximize model accuracy with minimal labeling budget

## Query Strategies

### Uncertainty Sampling
Pick instance with highest prediction uncertainty:
- **Least confident**: $1 - \max_y P(y|x)$ — simple, widely used
- **Margin**: $P(y_1|x) - P(y_2|x)$ — small margin = uncertain
- **Entropy**: $-\sum_y P(y|x) \log P(y|x)$ — information-theoretic

**Problem**: Focuses on decision boundary but ignores diversity — may query redundant points.

### Query-by-Committee (QBC)
Maintain committee of $C$ models (e.g., bootstrap samples):
- **Vote entropy**: $-\sum_y \frac{V(y)}{|C|} \log \frac{V(y)}{|C|}$ where $V(y)$ = votes for class $y$
- **KL divergence**: $\frac{1}{|C|} \sum_c KL(P_c \| \bar{P})$

**Density weighting**: Multiply uncertainty by similarity to unlabeled pool $U$:

$$x^* = \arg\max_x \text{uncertainty}(x) \cdot \frac{1}{|U|} \sum_{u \in U} \text{sim}(x, u)$$

### Expected Model Change
Query $x$ that would most change the current model:
- **Expected gradient length**: $\mathbb{E}_y[\|\nabla L(y)\|]$ — expensive (requires retraining for each candidate)
- **Estimated using influence functions**: Approximate change without full retraining

### Expected Error Reduction
Query $x$ to minimize expected generalization error:

$$\hat{x} = \arg\min_x \mathbb{E}_{y \sim P(y|x)} \left[ \sum_{u \in U} \text{err}(P(y|u; L \cup \{(x,y)\})) \right]$$

Computationally expensive: requires retraining for each candidate label.

## Batch Active Learning
Select diverse batch to avoid redundancy:

### Determinantal Point Process (DPP)
Probability proportional to determinant of similarity matrix: $P(S) \propto \det(L_S)$
- Balances quality (informative) and diversity (different instances)
- $O(|B|^3)$ for batch size $|B|$

### Core-set Selection
Select examples such that all unlabeled points are close to some selected point:
- Minimize maximum distance from unlabeled points to selected set
- Greedy approximation (furthest-first traversal)

### Diversity + Uncertainty
Score each candidate: $s(x) = \lambda \cdot \text{uncertainty}(x) + (1-\lambda) \cdot \text{diversity\_bonus}(x)$

## Code: Uncertainty Sampling

```python
import numpy as np

def uncertainty_sampling(model, X_pool, strategy='entropy'):
    probs = model.predict_proba(X_pool)
    if strategy == 'least_confident':
        scores = 1 - np.max(probs, axis=1)
    elif strategy == 'margin':
        sorted_probs = np.sort(probs, axis=1)
        scores = sorted_probs[:, -1] - sorted_probs[:, -2]
    elif strategy == 'entropy':
        scores = -np.sum(probs * np.log(probs + 1e-10), axis=1)
    return np.argmax(scores)
```

## Practical Considerations
- **Cold start**: Start with a small random seed set (10-100 examples)
- **Retraining cost**: Re-train model after each query batch — incremental updates help
- **Stopping criteria**: Stop when:
  - Performance plateaus on held-out validation set
  - Budget exhausted
  - Query informativeness drops below threshold
- **Noisy labels**: Include label quality checks in acquisition
- **Imbalanced data**: Use class-balanced acquisition or cost-sensitive strategies
- **Model calibration**: Well-calibrated probabilities improve uncertainty sampling

## Comparison

| Strategy | Computation | Effectiveness | Robustness |
|----------|------------|---------------|------------|
| Random baseline | $O(1)$ | Poor | High |
| Uncertainty sampling | $O(|U|)$ | Good | Low (calibration dependent) |
| QBC | $O(|C| \cdot |U|)$ | Good | Moderate |
| Expected error reduction | $O(|U|^2)$ | Best | High |
| DPP batch | $O(|B|^3 + |U||B|^2)$ | Very good | High |

## References
- Settles, "Active Learning Literature Survey" (Computer Sciences TR, 2009)
- Lewis & Gale, "A Sequential Algorithm for Training Text Classifiers" (SIGIR 1994)
- Seung, Opper, Sompolinsky, "Query by Committee" (COLT 1992)
- Hoi, Jin, Lyu, "Batch Mode Active Learning with Applications to Text Categorization" (JMLR, 2009)
- Ash et al., "Deep Batch Active Learning by Diverse, Uncertain Gradient Lower Bounds" (ICLR 2020)
