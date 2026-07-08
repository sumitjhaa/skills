# Lesson 12.01: Autograd from Scratch + Neural Net

## Project Architecture

Build a reverse-mode automatic differentiation engine (a "PyTorch-lite") and use it to train a multi-layer perceptron on MNIST.

```
Tensor (value, grad, backward fn)
  └── Operations: +, -, *, /, pow, exp, log, matmul, reshape
       └── Computational Graph (DAG)
            └── Backward() — reverse-mode traversal
                 └── Optimizers: SGD, Adam
                      └── Modules: Linear, ReLU, Sequential, MSELoss, CrossEntropyLoss
                           └── Training loop
```

## Design Decisions

### Tensor class
- Wraps a numpy ndarray as the data payload
- Stores `grad` (same shape, initialized to zero)
- Stores `_backward` closure for the local gradient contribution
- Stores `_prev` set of parent tensors in the graph
- `requires_grad` flag controls tracking

### Operation nodes
Each operation is a function that:
1. Computes the forward result (new Tensor)
2. Defines a `_backward(grad)` closure that accumulates gradients into parents
3. Links the graph via `_prev`

Examples: `add(t1, t2)`, `mul(t1, t2)`, `matmul(t1, t2)`, `relu(t)`, `exp(t)`, `log(t)`

### Backward pass
- Topologically sort the graph (reverse of execution order)
- Chain rule: `grad += local_grad * upstream_grad`
- Zero gradients between iterations

### Neural network components
- `Linear(in_features, out_features)` — weights and biases as Tensors
- `ReLU()` — element-wise activation
- `Sequential(*layers)` — forward pass composition
- `MSELoss()` / `CrossEntropyLoss()` — loss functions

### Optimizers
- `SGD(params, lr)` — simple gradient descent
- `Adam(params, lr, betas, eps)` — adaptive moment estimation

## Implementation Guide

1. **Implement Tensor** with the graph tracking infrastructure
2. **Implement binary ops** (add, sub, mul, div, pow) with correct local gradients
3. **Implement unary ops** (exp, log, neg, reshape) with correct local gradients
4. **Implement matmul** — the trickiest gradient (matrix product rule)
5. **Implement backward** with topological sort
6. **Implement reduction ops** (sum, mean) that broadcast gradients back
7. **Implement Module base class** and Parameter tracking
8. **Implement Linear, ReLU, Sequential**
9. **Implement losses** (MSE, CrossEntropy)
10. **Implement SGD and Adam**
11. **Build a 2-layer MLP and train on MNIST**
12. **Verify gradients against finite differences**

## Key Insights

- The backward graph is the transpose of the forward graph
- Each op's backward is the Jacobian-vector product
- Topological sort guarantees correct gradient propagation order
- Numpy vectorization makes batch training efficient
