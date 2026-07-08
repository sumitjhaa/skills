# 06.05 Higher-Order Gradients

## Learning Objectives
- Understand second derivatives and Hessians in deep learning
- Implement Hessian-vector products (HVPs) efficiently
- Apply double backpropagation for regularization and meta-learning

## Second Derivatives

To compute $H(x) = \nabla^2 f(x)$, we differentiate the gradient computation. After one backward pass, the gradient w.r.t. each input is itself a function that can be differentiated again.

### Hessian Matrix
$$H = \begin{bmatrix}
\frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \dots \\
\frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \dots \\
\vdots & \vdots & \ddots
\end{bmatrix}$$

For $n$ parameters: $O(n^2)$ entries, $O(n)$ memory for HVPs.

## create_graph Mode

When `create_graph=True`, the backward pass builds a new computation graph for the gradient computation:

```python
import torch

x = torch.randn(10, requires_grad=True)
y = (x**2).sum()

# First backward: compute gradient (with graph kept)
grad = torch.autograd.grad(y, x, create_graph=True)[0]

# Second backward: compute Hessian-vector product
hvp = torch.autograd.grad(grad.sum(), x, retain_graph=True)[0]
```

Intermediate gradient values become Tensor nodes instead of raw arrays.

## Hessian-Vector Products (HVP)

$$H(x) \cdot v = \nabla(v^\top \cdot \nabla f(x))$$

Compute in $O(n)$ instead of $O(n^2)$:

```python
def hessian_vector_product(f, x, v):
    # f: scalar function of x
    grad = torch.autograd.grad(f, x, create_graph=True)[0]
    hvp = torch.autograd.grad(grad, x, grad_outputs=v)[0]
    return hvp
```

## Applications

### WGAN-GP Gradient Penalty
$$\mathcal{L}_{\text{GP}} = \lambda \mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}} D(\hat{x})\|_2 - 1)^2]$$

Uses gradients of the discriminator w.r.t. inputs — requires second-order gradients.

### MAML Meta-Learning
Inner loop gradient updates are differentiated through in the outer loop:

```python
def maml_inner_update(model, x, y, inner_lr=0.01):
    pred = model(x)
    loss = F.mse_loss(pred, y)
    grads = torch.autograd.grad(loss, model.parameters(), create_graph=True)
    # Update parameters using grads
    new_params = {name: param - inner_lr * g 
                  for (name, param), g in zip(model.named_parameters(), grads)}
    return new_params
```

### PINNs (Physics-Informed Neural Networks)
$$\mathcal{L} = \|u_t + u u_x - \nu u_{xx}\|^2$$

Requires second derivatives for $u_{xx}$.

## Finite Difference Verification

$$\frac{d^2 f}{dx^2} \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$$

Always validate autograd higher-order results against numerical approximation for correctness.

## Memory Considerations

| Method | Memory | Time |
|--------|--------|------|
| Full Hessian | $O(n^2)$ | $O(n)$ backward passes |
| HVP | $O(n)$ | 2 backward passes |
| Finite diff HVP | $O(n)$ | 2 forward + 1 backward |

Second-order methods roughly double or triple memory vs. first-order only.

## References
- Pearlmutter, "Fast Exact Multiplication by the Hessian", Neural Computation 1994
- Finn, Abbeel, Levine, "Model-Agnostic Meta-Learning (MAML)", ICML 2017
- Gulrajani, Ahmed, et al., "Improved Training of Wasserstein GANs (WGAN-GP)", NeurIPS 2017
- Raissi, Perdikaris, Karniadakis, "Physics-Informed Neural Networks (PINNs)", JCP 2019
