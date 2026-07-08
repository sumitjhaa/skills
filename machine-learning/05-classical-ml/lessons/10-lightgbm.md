# Lesson 05.10: LightGBM

## Learning Objectives
- Understand GOSS, EFB, and leaf-wise tree growth
- Implement histogram-based split finding
- Compare with XGBoost on efficiency and accuracy
- Handle categorical features natively

## Core Innovations

### GOSS (Gradient-based One-Side Sampling)
Standard boosting uses all data points. GOSS intelligently subsamples:
1. Sort instances by absolute gradient $|g_i|$
2. Keep top $a \times 100\%$ high-gradient instances (all)
3. Randomly sample $b \times 100\%$ of low-gradient instances
4. Amplify sampled low-gradient instances by weight $\frac{1-a}{b}$

**Rationale**: High-gradient instances are under-fitted (informative). Low-gradient instances are well-fitted (redundant). GOSS approximates the full gradient sum with lower variance than uniform sampling.

**Theoretical guarantee**: GOSS converges with $O(nd)$ complexity and maintains accuracy bounds relative to full data training.

### EFB (Exclusive Feature Bundling)
Many features are mutually exclusive (rarely non-zero simultaneously), especially in one-hot encoded data.

**Bundle construction** — reduce to graph coloring problem:
- Vertices: features
- Edges: connect features that conflict (both non-zero in same instance)
- Goal: minimal coloring (each color = one bundle)

**Merge bundled features** — for each bundle, define feature ranges to avoid conflicts. For $k$ features in a bundle, assign range $2^k$ to each feature's bins, ensuring no bin collision.

EFB reduces $d$ to $d' \ll d$ for sparse data, dramatically improving training speed.

### Leaf-Wise (Best-First) Tree Growth
Standard level-wise growth splits all nodes at the current depth. LightGBM splits the leaf with the largest loss reduction:

```
while num_leaves < max_leaves:
    leaf = argmax(gain over all leaves)
    split leaf into two children
```

- Produces asymmetric trees
- Converges faster (fewer splits to reach same loss)
- Risk: overfitting (limit with `num_leaves` or `max_depth`)
- More memory efficient (stores only leaf nodes, not full levels)

## Histogram-Based Splitting
Discretize continuous features into $k$ bins (default $k=255$):

1. Build gradient histogram per feature:
   - For each bin $b$: $G_b = \sum_{i \in \text{bin}(b)} g_i$, $H_b = \sum_{i \in \text{bin}(b)} h_i$
2. Scan $k-1$ possible split positions in $O(k)$ per feature
3. Find best split with optimal gain

**Memory**: Store bin counts instead of raw floats — $O(kd)$ vs $O(nd)$
**Speed**: $O(kd)$ per split vs $O(nd)$ for exact greedy

## Categorical Feature Support
No one-hot encoding needed. Uses "max-sum" grouping:

1. For each category, compute $\text{sum_gradients} / \text{sum_hessians}$
2. Sort categories by this statistic
3. Find optimal split point in the sorted list (treating as ordered)

This is $O(\text{categories} \cdot \log(\text{categories}))$ vs $O(2^{\text{categories}})$ for exhaustive search.

## Code: Histogram Split Finding

```python
import numpy as np

def build_histogram(X, g, h, feature, num_bins=256):
    """Build gradient histogram for a feature"""
    bins = np.digitize(X[:, feature], np.linspace(X[:, feature].min(), X[:, feature].max(), num_bins))
    G_bins = np.bincount(bins, weights=g, minlength=num_bins + 1)
    H_bins = np.bincount(bins, weights=h, minlength=num_bins + 1)
    return G_bins, H_bins

def find_best_split_histogram(G_bins, H_bins, lam=1.0, gamma=0.0):
    """Find best split point from histograms"""
    G_total = np.sum(G_bins)
    H_total = np.sum(H_bins)
    best_gain = -float('inf')
    best_bin = 0
    G_left, H_left = 0.0, 0.0
    for b in range(len(G_bins) - 1):
        G_left += G_bins[b]; H_left += H_bins[b]
        G_right = G_total - G_left; H_right = H_total - H_left
        gain = 0.5 * (G_left**2/(H_left+lam) + G_right**2/(H_right+lam) - (G_total**2)/(H_total+lam)) - gamma
        if gain > best_gain:
            best_gain = gain; best_bin = b
    return best_bin, best_gain
```

## Comparison: LightGBM vs XGBoost

| Aspect | LightGBM | XGBoost |
|--------|----------|---------|
| Tree growth | Leaf-wise (best-first) | Level-wise (depth-first) |
| Split finding | Histogram | Pre-sorted (exact) / Histogram (approx) |
| Sampling | GOSS | None (or subsample) |
| Feature bundling | EFB | None |
| Categorical | Native (max-sum grouping) | One-hot or encoding |
| Speed (large data) | Faster | Moderate |
| Memory | Lower ($O(kd)$) | Higher ($O(nd)$) |
| Small data | Overfits easily | More robust |

## Practical Considerations
- **Small datasets** (< 10k rows): Use XGBoost or enable `min_data_in_leaf` (default 20)
- **Overfitting**: Reduce `num_leaves`, increase `min_data_in_leaf`, decrease `learning_rate`
- **Categorical features**: Declare with `categorical_feature` parameter
- **Large data**: GOSS + histogram gives 10-100x speedup over exact methods
- **GPU**: LightGBM has efficient GPU histogram construction
- **Early stopping**: Monitor validation metric; LightGBM's CV is fast

## Key Advantages
- 10-100x faster training than XGBoost on large datasets
- Lower memory usage (fits in GPU memory for larger data)
- Better accuracy with proper tuning (leaf-wise finds better solutions)
- Native categorical feature handling

## Limitations
- Prone to overfitting on small data (leaf-wise growth)
- Less interpretable than level-wise trees
- GOSS can lose information in very sparse data
- EFB overhead for dense data

## References
- Ke et al., "LightGBM: A Highly Efficient Gradient Boosting Decision Tree" (NIPS 2017)
- LightGBM documentation: https://lightgbm.readthedocs.io
- Friedman, "Stochastic Gradient Boosting" (2002)
