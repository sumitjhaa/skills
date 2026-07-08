# 12. Perturbation Theory and Condition Numbers

## Introduction

Perturbation theory studies how the solution of a problem changes when the input data is slightly perturbed. The **condition number** quantifies this sensitivity.

## Condition Number

For solving A**x** = **b**:

κ(A) = ||A|| · ||A⁻¹|| = σₘₐₓ / σₘᵢₙ

A problem with large κ is *ill-conditioned*. The relative error in **x** is bounded by:

||Δ**x**|| / ||**x**|| ≤ κ(A) · (||ΔA||/||A|| + ||Δ**b**||/||**b**||)

```python
import numpy as np

A = np.array([[1, 1], [1, 1.0001]])
cond = np.linalg.cond(A)
print(f"Condition number: {cond:.2f}")
```

## Backward Error

The backward error measures how much we need to perturb the data to explain the computed solution:

η(**x̂**) = min {ε : (A + ΔA)**x̂** = **b** + Δ**b**, ||ΔA|| ≤ ε||A||, ||Δ**b**|| ≤ ε||**b**||}

## Forward Error

The forward error is the actual error in the solution:

forward_error = ||**x̂** − **x**|| / ||**x**||

## Stability Experiments

```python
def perturbation_experiment(A, x_true):
    b = A @ x_true
    x_computed = np.linalg.solve(A, b)
    forward_error = np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)
    residual = np.linalg.norm(A @ x_computed - b) / (np.linalg.norm(A) * np.linalg.norm(x_computed))
    return forward_error, residual
```

## What You'll Implement

- Condition number estimation via SVD
- Forward/backward error analysis
- Perturbation experiments (add noise and measure error)
- Compare theoretical error bounds with actual errors
- Visualize the relationship between condition number and accuracy
