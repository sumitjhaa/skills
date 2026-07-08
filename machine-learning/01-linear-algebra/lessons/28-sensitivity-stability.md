# 28. Sensitivity and Stability in Machine Learning

## Introduction

The sensitivity of neural networks to input perturbations is crucial for robustness, generalization, and adversarial examples. The condition number of a neural network's Jacobian measures amplification.

## Lipschitz Constant of Neural Networks

The Lipschitz constant L of a function f satisfies ||f(**x**) − f(**y**)|| ≤ L ||**x** − **y**||. For a neural network with ReLU activations:

```python
def lipschitz_estimate(model, X, n_samples=100):
    max_ratio = 0
    for _ in range(n_samples):
        i, j = np.random.randint(len(X), size=2)
        ratio = np.linalg.norm(model(X[i]) - model(X[j])) / \
                np.linalg.norm(X[i] - X[j])
        max_ratio = max(max_ratio, ratio)
    return max_ratio
```

## Condition Number of Neural Networks

The condition number of a network at input **x** is the ratio of largest to smallest singular values of the Jacobian J(**x**) = ∂f/∂**x**:

κ(J(**x**)) = σₘₐₓ(J) / σₘᵢₙ(J)

```python
def nn_condition_number(model, x, eps=1e-5):
    J = compute_jacobian(model, x)
    s = np.linalg.svd(J, compute_uv=False)
    return s[0] / s[-1], s
```

## Adversarial Robustness

Networks with high Lipschitz constants are more vulnerable to adversarial examples — small perturbations that change the output dramatically:

**x'** = **x** + ε · sign(∇_x L(f(**x**), y))

## Spectral Normalization

A popular technique to control the Lipschitz constant is spectral normalization, which divides each weight matrix by its spectral norm after each update:

```python
def spectral_normalize(W):
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    return W / s[0]
```

## What You'll Implement

- Lipschitz constant estimation via random sampling
- Jacobian computation for neural networks
- Condition number analysis of network layers
- Adversarial example generation (FGSM)
- Spectral normalization
- Compare sensitivity across architectures
