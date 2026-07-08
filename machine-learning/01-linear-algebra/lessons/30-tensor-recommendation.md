# Lesson 30: Tensor Methods for Recommendation

## Learning Objectives
- Formulate collaborative filtering as a tensor completion problem
- Apply weighted ALS for implicit feedback tensor factorization
- Design time-aware recommendation via dynamic tensor models
- Handle context-aware and multi-view data with tensor methods

## Tensor for Recommendation

Users $U$, items $I$, contexts $C_1, \dots, C_k$ → $(U \times I \times C_1 \times \cdots \times C_k)$ tensor.

Each entry represents interaction (rating, purchase, click) under context.

## CP Decomposition for Recommendation

$$X_{u,i,c} \approx \sum_{r=1}^R a_{ur} \cdot b_{ir} \cdot c_{cr}$$

- $a_{ur}$: user $u$'s preference for latent factor $r$
- $b_{ir}$: item $i$'s relation to factor $r$
- $c_{cr}$: context $c$'s influence on factor $r$

**Optimization**: Minimize weighted squared error with regularization:

$$\min_{A,B,C} \sum_{(u,i,c) \in \Omega} \left(X_{uic} - \sum_r a_{ur} b_{ir} c_{cr}\right)^2 + \lambda(\|A\|_F^2 + \|B\|_F^2 + \|C\|_F^2)$$

## Weighted ALS for Implicit Feedback

For implicit data (clicks, views), use confidence weighting:

$$\min_{A,B,C} \sum_{u,i,c} w_{uic}(X_{uic} - \sum_r a_{ur}b_{ir}c_{cr})^2 + \lambda(\|A\|_F^2 + \|B\|_F^2 + \|C\|_F^2)$$

**Confidence**: $w_{uic} = 1 + \alpha X_{uic}$ (linear scaling) or $w_{uic} = 1 + \alpha \log(1 + X_{uic})$ (diminishing returns).

### ALS Updates

Given $B, C$, update $A$ row by row:

$$a_u = \left(\sum_{i,c} w_{uic} \cdot (b_i \odot c_c)(b_i \odot c_c)^\top + \lambda I\right)^{-1} \sum_{i,c} w_{uic} X_{uic} \cdot (b_i \odot c_c)$$

$\odot$: Hadamard (element-wise) product.

## Time-Aware Recommendation

### Time evolving CF tensor
$$X(t)_{u,i} \approx \sum_{r=1}^R a_{ur}(t) \cdot b_{ir}(t)$$

**Dynamic CP**:
$$a_{ur}(t) = a_{ur}^{(0)} + \sum_{p=1}^P \alpha_{urp} \cdot f_p(t)$$

- $f_p(t)$: temporal basis functions (splines, RBFs, seasonal)
- $\alpha_{urp}$: time coefficient

### Seasonal-Trend Decomposition
Model time as product of: static + trend + seasonal:

$$X_{u,i,t} \approx \sum_r a_{ur} b_{ir} + \sum_r a_{ur}^{\text{(trend)}} b_{ir}^{\text{(trend)}} \cdot t + \sum_r a_{ur}^{\text{(seas)}} b_{ir}^{\text{(seas)}} \cdot \sin(\omega t)$$

## Context-Aware Tensor Completion

### Tucker Decomposition
$$X_{u,i,c} \approx \sum_{p=1}^P \sum_{q=1}^Q \sum_{r=1}^R g_{pqr} \cdot a_{up} \cdot b_{iq} \cdot c_{cr}$$

- $g_{pqr}$: core tensor capturing multi-way interactions
- $P, Q, R$: number of factors per mode (can differ)
- More expressive but less sparse than CP

### TimeLMF (Time-Aware Latent Matrix Factorization)
Tensor of (user, item, time) with:
- Temporal smoothness regularization
- $\|A(t) - A(t-1)\|_F^2 \leq \varepsilon$ (factors change slowly)
- Periodic constraints: $A(t + \tau) \approx A(t)$

## Code: CP-WOPT for Tensor Completion

```python
import numpy as np
from scipy.optimize import minimize

def cp_wopt(entries, indices, shape, R, lambda_reg=0.1, max_iter=100):
    """CP with weighted optimization for tensor completion"""
    n_modes = len(shape)
    factors = [np.random.randn(s, R) for s in shape]
    
    def loss(params):
        # Reshape parameters into factors
        offset = 0
        factors_flat = []
        for s in shape:
            n_vals = s * R
            factors_flat.append(params[offset:offset + n_vals].reshape(s, R))
            offset += n_vals
        
        # Compute predictions and loss
        total_loss = 0
        for (idx, val) in zip(indices, entries):
            pred = 1
            for m in range(n_modes):
                pred *= factors_flat[m][idx[m]]
            pred = np.sum(pred)
            total_loss += (val - pred) ** 2
        
        # Regularization
        for f in factors_flat:
            total_loss += lambda_reg * np.sum(f ** 2)
        
        return total_loss
    
    # Initial params
    init_params = np.concatenate([f.ravel() for f in factors])
    total_params = sum(s * R for s in shape)
    
    result = minimize(loss, init_params, method='L-BFGS-B',
                      options={'maxiter': max_iter})
    
    # Restore factors
    factors_final = []
    offset = 0
    for s in shape:
        n_vals = s * R
        factors_final.append(result.x[offset:offset + n_vals].reshape(s, R))
        offset += n_vals
    
    return factors_final
```

## Evaluation Protocols

| Protocol | Description | Metric |
|----------|-------------|--------|
| Leave-one-out | Hold one interaction per user | HR@k, NDCG@k |
| Temporal split | Train on earlier, test on later | Recall, MAP |
| Context holdout | Remove specific context slice | RMSE |
| Cold-start | Test on unseen users/items | F1, coverage |

## Scalability

| Method | Per iteration | Memory | Parallelizable |
|--------|--------------|--------|---------------|
| CP-ALS | $O(\|\Omega\|R)$ | $O((U+I+C)R)$ | Yes (mode-wise) |
| Tucker-ALS | $O(\|\Omega\|R + (U+I+C)R^2)$ | $O(R^3)$ | Partial |
| SGD for CP | $O(R)$ per sample | $O((U+I+C)R)$ | Yes (async) |
| Distributed CP | $O(\|\Omega\|R / P)$ | $O((U+I+C)R/P)$ | Yes (MPI) |

## Practical Considerations
- **Sparsity**: Tensor CP requires $O(R)$ observations per slice; use side info for very sparse tensors
- **Implicit feedback**: Always use weighted loss; binarize with confidence weights
- **Temporal effects**: Use time decay weighting or sliding windows
- **Interpretability**: Non-negativity constraints ($A, B, C \geq 0$) for interpretable factors
- **Cold start**: Incorporate user/item features as side information

## References
- Rendle, Schmidt-Thieme, "Pairwise Interaction Tensor Factorization for Personalized Tag Recommendation" (WSDM 2010)
- Karatzoglou, Amatriain, Baltrunas, Oliver, "Multiverse Recommendation: N-dimensional Tensor Factorization for Context-aware Collaborative Filtering" (RecSys 2010)
- Hu, Koren, Volinsky, "Collaborative Filtering for Implicit Feedback Datasets" (ICDM 2008)
- Xiong, Chen, Huang, Schneider, Carbonell, "Temporal Collaborative Filtering with Bayesian Probabilistic Tensor Factorization" (SDM 2010)
- Kolda & Bader, "Tensor Decompositions and Applications" (SIAM Review, 2009)
