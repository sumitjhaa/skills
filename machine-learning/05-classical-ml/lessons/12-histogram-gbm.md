# Lesson 05.12: Histogram-based GBM

## Learning Objectives
- Understand histogram-based split finding for GBM
- Implement discrete binning and gradient accumulation
- Analyze tradeoffs between exact and approximate splits
- Compare implementations across libraries

## Histogram Building
Discretize each continuous feature into $m$ bins (typically $m=256$):

1. **Quantile binning**: Equal-width bins based on quantiles of feature distribution (weighted by $|h_i|$ for XGBoost-style)
2. **Uniform binning**: Equal-width intervals between min and max

For each feature $j$, build gradient histogram:
```
for each instance i:
    bin = bin_map[feature_j][x_i[j]]
    G_bin[bin] += g_i
    H_bin[bin] += h_i
```

### Gradient Statistics per Bin
- $G_b = \sum_{i \in \text{bin}(b)} g_i$ (sum of first-order gradients)
- $H_b = \sum_{i \in \text{bin}(b)} h_i$ (sum of second-order gradients)

At each candidate threshold $t$ between bins $b_t$ and $b_t+1$:
- $G_L = \sum_{b \leq b_t} G_b$, $G_R = \sum_{b > b_t} G_b$
- $H_L = \sum_{b \leq b_t} H_b$, $H_R = \sum_{b > b_t} H_b$

## Split Finding with Histograms
Gain for candidate split at threshold $t$:

$$\text{Gain} = \frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L+G_R)^2}{H_L+H_R+\lambda}$$

Scan $m-1$ candidate positions in $O(m)$ per feature vs $O(n \log n)$ for exact split finding.

### Subtree Histogram Subtraction
To compute histograms for children nodes, use parent histogram minus sibling histogram (already computed):

$$\text{hist}_{\text{right}} = \text{hist}_{\text{parent}} - \text{hist}_{\text{left}}$$

This halves the histogram building cost for each split.

## Memory Optimization
Histogram-based GBM stores:
- Binned feature matrix: $n \times d$ integers (1 byte per value at $m=256$)
- Histograms: $d \times m \times 2$ floats (gradient sum + hessian sum)

Compare to exact GBM:
- Raw feature values: $n \times d$ floats (4-8 bytes each)
- Sorted indices: $n \times d$ integers (for pre-sorted approach)

Memory ratio: approximately $1:8$ for $m=256$ vs exact greedy.

## Comparison of Split Finding Strategies

| Method | Complexity | Memory | Precision | When to use |
|--------|-----------|--------|-----------|-------------|
| Exact | $O(nd \log n)$ | High | Exact | Small data ($n < 10^4$) |
| Histogram | $O(n + md)$ | Low | Approximate | Medium-large data |
| Quantile sketch | $O(n \log(1/\varepsilon))$ | Medium | Approx (bounded) | Very large data |
| Sampling | $O(kd \log k)$ | Low | Approximate | Extremely large data |

The histogram approach with $m=256$ typically loses < 0.1% accuracy vs exact while being 10-100x faster.

## Code: Histogram-Based Split Finding

```python
import numpy as np

def build_histograms(X, g, h, num_bins=256):
    """Build gradient and hessian histograms for all features"""
    n, d = X.shape
    G_hist = np.zeros((d, num_bins))
    H_hist = np.zeros((d, num_bins))
    for feat in range(d):
        col = X[:, feat]
        bins = np.floor((col - col.min()) / (col.max() - col.min() + 1e-10) * (num_bins - 1)).astype(int)
        for b in range(num_bins):
            mask = bins == b
            G_hist[feat, b] = np.sum(g[mask])
            H_hist[feat, b] = np.sum(h[mask])
    return G_hist, H_hist

def find_best_histogram_split(G_hist, H_hist, lam=1.0, gamma=0.0):
    """Find best feature and threshold from histograms"""
    d, num_bins = G_hist.shape
    best_feat, best_bin, best_gain = -1, -1, -float('inf')
    for feat in range(d):
        G_cum, H_cum = 0, 0
        G_total, H_total = np.sum(G_hist[feat]), np.sum(H_hist[feat])
        for b in range(num_bins - 1):
            G_cum += G_hist[feat, b]; H_cum += H_hist[feat, b]
            G_left, H_left = G_cum, H_cum
            G_right = G_total - G_left; H_right = H_total - H_left
            gain = 0.5 * (G_left**2/(H_left+lam) + G_right**2/(H_right+lam) - G_total**2/(H_total+lam)) - gamma
            if gain > best_gain:
                best_gain, best_feat, best_bin = gain, feat, b
    return best_feat, best_bin, best_gain
```

## Practical Considerations

### Number of Bins ($m$)
- $m=256$ is standard (max of 1 byte, sufficient precision)
- $m=64$ for very large data (faster, slight accuracy loss)
- $m=1024$ for high-precision needs (more memory, marginal gains)

### Binning Strategy
- **Quantile bins**: better when data is non-uniformly distributed
- **Uniform bins**: simpler, sufficient for most cases
- **CatBoost**: uses a dynamic binning based on gradient statistics

### Missing Values
- Skip missing values during histogram construction
- Track missing count per bin for learned default direction
- Histograms naturally handle missing-by-bin-skipping approach

## Key Advantages
- Dramatically faster training for large datasets (10-100x)
- Fixed memory budget regardless of data size
- Minor accuracy loss (< 0.1%) when $m$ is 256+
- Enables GPU acceleration (histograms are GPU-friendly)
- Used by LightGBM, CatBoost, HistGradientBoosting, XGBoost (approx mode)

## References
- Ke et al., "LightGBM: A Highly Efficient Gradient Boosting Decision Tree" (NIPS 2017)
- Chen & Guestrin, "XGBoost" (KDD 2016) — quantile sketch section
- scikit-learn "HistGradientBoosting" documentation
- Ben-Haim & Tom-Tov, "A Streaming Parallel Decision Tree Algorithm" (JMLR, 2010)
