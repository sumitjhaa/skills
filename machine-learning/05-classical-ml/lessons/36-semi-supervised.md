# Lesson 05.36: Semi-Supervised Learning

## Learning Objectives
- Understand semi-supervised assumptions (smoothness, cluster, manifold)
- Implement self-training, co-training, and label propagation
- Analyze TSVM for transductive learning
- Apply to scenarios with limited labeled data

## Self-Training
1. Train classifier on labeled data $L$
2. Predict pseudo-labels on unlabeled $U$
3. Add high-confidence predictions to $L$
4. Repeat

**Risk**: Reinforces model errors — incorrect high-confidence predictions propagate.

**Mitigation**: Use confidence threshold, only add low-noise examples, or use ensemble disagreement.

## Co-Training
Requires two conditionally independent views of features:

1. Train $h_1$ on view 1, $h_2$ on view 2
2. Each labels highest-confidence examples for the other view
3. Add to labeled pool
4. Repeat

**Requirements**: Features naturally splittable (e.g., words from web page body vs anchor text), views conditionally independent given label.

**When views don't split naturally**: Use random feature split (co-training with random splits often works too).

## Label Propagation
Build similarity graph and propagate labels:

$$W_{ij} = \exp(-\|x_i - x_j\|^2 / \sigma^2)$$

**Iterative**:
$$F^{(t+1)} = \alpha S F^{(t)} + (1-\alpha) Y$$

- $S = D^{-1/2} W D^{-1/2}$ (normalized Laplacian)
- $\alpha \in (0, 1)$: clamping factor (how much to trust initial labels)
- $Y$: initial label matrix (one-hot for labeled, 0 for unlabeled)
- $F$: predicted label distributions

**Closed form**: $F = (I - \alpha S)^{-1} Y$

**Convergence** guaranteed when $\alpha < 1 / \lambda_{\max}(S)$.

## TSVM (Transductive SVM)
Find hyperplane maximizing margin on both labeled and unlabeled data:

$$\min_{w, y_U} \frac12 \|w\|^2 + C_L \sum_{i \in L} \xi_i + C_U \sum_{j \in U} \xi_j$$

s.t. $y_i(w^\top x_i + b) \geq 1 - \xi_i$, $y_j \in \{\pm 1\}$, $y_j(w^\top x_j + b) \geq 1 - \xi_j$

**NP-hard** combinatorial problem. Approximations:
- **Convex relaxation**: Replace with hinge-like loss on unlabeled points
- **Graduated optimization**: Start with small $C_U$, gradually increase
- **SVM with manifold regularization** (Laplacian SVM)

## Graph-Based Methods
Construct graph from both labeled and unlabeled points:

**Manifold regularization**: Add graph Laplacian penalty to SVM objective:

$$\min_{f \in H} \frac{1}{l} \sum_{i=1}^l V(y_i, f(x_i)) + \lambda \|f\|_H^2 + \gamma \sum_{i,j} W_{ij} (f(x_i) - f(x_j))^2$$

The last term is $f^\top L f$, where $L$ is the graph Laplacian — encourages smooth predictions on the graph.

## Code: Label Propagation

```python
import numpy as np
from scipy.spatial.distance import cdist

def label_propagation(X, y_labeled, labeled_idx, alpha=0.99, sigma=1.0, max_iter=100):
    n = X.shape[0]
    n_labels = len(np.unique(y_labeled))
    Y = np.zeros((n, n_labels))
    for i, lbl in zip(labeled_idx, y_labeled):
        Y[i, lbl] = 1.0
    # Similarity graph
    W = np.exp(-cdist(X, X, 'sqeuclidean') / (2 * sigma**2))
    np.fill_diagonal(W, 0)
    D_sqrt = np.diag(1.0 / np.sqrt(np.sum(W, axis=1) + 1e-10))
    S = D_sqrt @ W @ D_sqrt
    # Iterate
    F = Y.copy()
    for _ in range(max_iter):
        F = alpha * S @ F + (1 - alpha) * Y
    return F  # soft label distributions
```

## Assumptions
1. **Smoothness**: Nearby points likely share the same label
2. **Cluster assumption**: Data forms clusters; same cluster = same label
3. **Manifold assumption**: Data lies on low-dimensional manifold; learning on manifold is efficient
4. **Low-density separation**: Decision boundary lies in low-density regions

Active learning violates these (selects boundary points). Semi-supervised relies on them.

## Practical Considerations
- **Assumption violation**: SSL can hurt performance if assumptions are violated
- **Small labeled set**: SSL most effective with very few labels (1-10 per class)
- **Large unlabeled set**: More unlabeled data generally helps (until marginal benefit diminishes)
- **Outliers**: Label propagation can be misled by outliers connecting to many other points
- **Scalability**: Graph methods are $O(n^3)$ — use Nyström or nearest-neighbor graphs for large data
- **Neural SSL**: Use consistency regularization (e.g., FixMatch, MixMatch) for deep learning

## Key Points
- SSL fails if smoothness/cluster assumptions violated
- Self-training is simple but risky (reinforces errors)
- Co-training needs natural feature splits
- TSVM is NP-hard — use approximations
- Graph methods scale as $O(n^3)$ naively

## References
- Zhu, "Semi-Supervised Learning Literature Survey" (2005)
- Chapelle, Schölkopf, Zien, "Semi-Supervised Learning" (MIT Press, 2006)
- Zhu & Ghahramani, "Learning from Labeled and Unlabeled Data with Label Propagation" (CMU TR, 2002)
- Blum & Mitchell, "Combining Labeled and Unlabeled Data with Co-Training" (COLT 1998)
- Joachims, "Transductive Inference for Text Classification using Support Vector Machines" (ICML 1999)
