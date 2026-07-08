# Lesson 25: INDSCAL and PARAFAC2

## Learning Objectives
- Understand INDSCAL for individual differences scaling
- Apply PARAFAC2 for flexible tensor decomposition
- Compare with standard CP/PARAFAC decomposition
- Analyze multi-way data with varying modes

## INDSCAL (INdividual Differences SCALing)
**Goal**: Model individual differences in similarity judgments across subjects.

**Data**: Three-way array $X_{ijk}$ — similarity between stimulus $i$ and $j$ as rated by subject $k$.

**Model**:

$$X_{ijk} = \sum_{r=1}^R w_{kr} \cdot a_{ir} \cdot a_{jr} + e_{ijk}$$

- $a_{ir}$: coordinate of stimulus $i$ on dimension $r$ (common space)
- $w_{kr}$: salience weight of dimension $r$ for subject $k$
- $e_{ijk}$: residual

### Key Properties
- **Common stimulus space**: All subjects share the same $A$ matrix
- **Dimension weights**: Subjects differ only in how much they emphasize each dimension
- **Symmetry**: $X_{ij} = X_{ji}$ for each subject
- **Identifiability**: Dimensions are unique (up to permutation) — no rotation ambiguity

### Matrix Form
For subject $k$:
$$X_k = A \, \text{diag}(w_{k}) \, A^\top + E_k$$

- $X_k$: $n \times n$ symmetric similarity matrix
- $A$: $n \times R$ common configuration
- $w_k \in \mathbb{R}^R$: subject weights

## Algorithm: INDSCAL via ALS

1. Initialize $A$ (e.g., via PCA of stacked $X_k$)
2. Iterate until convergence:
   - **Update $w_k$** for each $k$: regress vec($X_k$) on columns of $(A \odot A)$
   - **Update $A$**: Given $W = [w_1 | \dots | w_K]$, solve $X_k = A \, \text{diag}(w_k) \, A^\top$ by fixed-point or gradient
3. Optionally normalize $A$ columns to unit norm

## PARAFAC2
**Motivation**: CP decomposition requires all slices to have same structure. PARAFAC2 relaxes this — allows one mode to vary across slices.

**Model**:

$$X_k = A \, \text{diag}(b_k) \, C_k^\top + E_k$$

- $X_k$: $I \times J_k$ matrix (note: $J_k$ can vary by $k$)
- $A$: $I \times R$ — common loading (mode 1)
- $b_k \in \mathbb{R}^R$ — weights for $k$th slice (mode 2)
- $C_k$: $J_k \times R$ — varying mode loadings, with constraint:
  $$C_k^\top C_k = \Phi \quad (\text{same cross-product for all } k)$$

### Constraint
$C_i^\top C_i = C_j^\top C_j = \Phi$ for all $i, j$. This ensures that the cross-product of the varying mode is identical across slices, while allowing individual $C_k$ to differ.

**Why this constraint**: Preserves uniqueness while providing flexibility for varying length ($J_k$).

## Algorithm: PARAFAC2 via ALS

1. **Reformulate**: $Y_k = X_k^\top A$
2. **Constrain**: $Y_k^\top Y_k = \Phi$ — enforce via SVD of stacked $Y_k$
3. **Update $A$**: $A = \left(\sum_k X_k C_k \, \text{diag}(b_k)\right) \left(\sum_k \text{diag}(b_k) C_k^\top C_k \, \text{diag}(b_k)\right)^\dagger$
4. **Update $b_k$**: $b_k = \text{diag}(C_k^\top X_k^\top A \, (A^\top A)^{-1})$
5. **Update $\Phi$**: from $C_k^\top C_k$ averaged across $k$
6. Repeat until convergence

### Identifiability
PARAFAC2 is unique under mild conditions (weaker than CP), making it suitable for:
- Time-warped signals (e.g., EEG across trials)
- Varying-length sequences (e.g., sensor readings)
- Aligned factor analysis

## Comparison: CP vs INDSCAL vs PARAFAC2

| Aspect | CP/PARAFAC | INDSCAL | PARAFAC2 |
|--------|-----------|---------|----------|
| Data | $I \times J \times K$ | $I \times I \times K$ (symmetric) | $I \times J_k \times K$ |
| Constraints | None | $X_k$ symmetric, $w_{kr} \geq 0$ | $C_k^\top C_k = \Phi$ |
| Uniqueness | Up to permutation+scaling | Permutation only | Permutation+scaling |
| Varying mode | Fixed | Fixed mode 2 = mode 1 | Allowed |
| Application | General 3-way | Similarity ratings | Time series, sequences |

## Code: PARAFAC2 Simulation

```python
import numpy as np

def parafac2_als(X_list, R, max_iter=100, tol=1e-6):
    K = len(X_list)
    I = X_list[0].shape[0]
    
    A = np.random.randn(I, R)
    B = np.random.randn(K, R)
    C_list = [np.random.randn(X.shape[1], R) for X in X_list]
    
    for it in range(max_iter):
        # Update B and C_k given A
        for k in range(K):
            Ak = X_list[k].T @ A
            Bk = B[k]  # diagonal weights
            # Update C_k with cross-product constraint
            U, S, Vt = np.linalg.svd(Ak, full_matrices=False)
            C_list[k] = U @ Vt
            B[k] = np.diag(C_list[k].T @ X_list[k].T @ A @ np.linalg.inv(A.T @ A))
        
        # Update A given B, C_k
        numerator = 0
        denominator = 0
        for k in range(K):
            bk = np.diag(B[k])
            numerator += X_list[k] @ C_list[k] @ bk
            denominator += bk @ C_list[k].T @ C_list[k] @ bk
        A_new = numerator @ np.linalg.inv(denominator)
        
        if np.linalg.norm(A_new - A) < tol:
            break
        A = A_new
    
    return A, B, C_list
```

## Applications

### EEG Analysis
- Each trial $k$ has different time length $J_k$
- PARAFAC2 extracts spatial factors $A$ (channels $\times$ components) with time-varying loadings $C_k$
- Cross-trial consistency via $\Phi$ constraint

### Chemometrics (GC-MS)
- Elution profiles vary across runs (retention time shifts)
- Mass spectra $A$ are common across runs
- PARAFAC2 handles retention time misalignment

### Longitudinal MDS
- Subjects rate similarity at multiple time points
- INDSCAL captures stable dimensions with time-varying salience

## Limitations
- **Local minima**: ALS is sensitive to initialization; run multiple random starts
- **Non-negativity**: Standard formulation allows negative loadings; extend to NTF
- **Missing data**: Requires imputation or weighted loss variants
- **Scalability**: $O(IKR^2)$ per iteration — challenging for large $I, K$
- **Order selection**: $R$ must be chosen via cross-validation or DIFFIT

## References
- Carroll & Chang, "Analysis of Individual Differences in Multidimensional Scaling" (Psychometrika, 1970)
- Harshman, "Foundations of the PARAFAC Procedure" (UCLA Working Papers in Phonetics, 1970)
- Kiers, Ten Berge, Bro, "PARAFAC2 — Part I. A direct fitting algorithm" (J. Chemometrics, 1999)
- Bro, "Multiway Analysis in the Food Industry" (Ph.D. Thesis, 1998)
- Kolda & Bader, "Tensor Decompositions and Applications" (SIAM Review, 2009)
