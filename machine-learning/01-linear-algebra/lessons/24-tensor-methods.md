# 24. Tensor Methods for Machine Learning

## Introduction

Tensor methods extend matrix models to multi-way data. They are used in regression, completion, and recommendation with multi-modal data.

## Tensor Regression

Given a tensor **X** and target y, the tensor regression model is:

y = ⟨**W**, **X**⟩ + b

where **W** is a weight tensor. To avoid overfitting, **W** is constrained to be low-rank (CP or Tucker).

```python
def cp_regression(X_list, y, rank, lr=0.01, max_iter=100):
    I, J, K = X_list[0].shape
    weights = [np.random.randn(rank) for _ in range(3)]
    for _ in range(max_iter):
        y_pred = [np.sum(w * torch.tensordot(X, ...)) for X in X_list]
        loss = np.mean((y - y_pred)**2)
        # gradient step
    return weights
```

## Tensor Completion

Missing entries in a tensor can be filled using low-rank tensor decomposition, generalizing matrix completion.

## Tensor Recommendation

Collaborative filtering with user-item-context tensors uses CP or Tucker to predict ratings.

## Tensorly Integration

```python
import tensorly as tl
from tensorly.decomposition import parafac

# PARAFAC decomposition
factors = parafac(tensor, rank=10)
```

## What You'll Implement

- Tensor regression with CP and Tucker constraints
- Tensor completion via CP/Tucker
- Multi-modal data fusion
- Comparison with matrix methods
- Real data experiment (sensor data or image collections)
