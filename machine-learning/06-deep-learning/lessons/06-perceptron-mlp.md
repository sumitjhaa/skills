# 06.06 Perceptron / MLP

The Perceptron is the simplest neural unit. The Multi-Layer Perceptron (MLP) stacks them into a universal function approximator.

## Perceptron

y = σ(w · x + b)

- w: weight vector
- b: bias
- σ: activation function (originally step function, now smooth)

## Limitations of Single Perceptron

- Only linearly separable problems
- Cannot solve XOR (Minsky & Papert, 1969)

## MLP Architecture

Hidden layers between input and output:

```
Input → Linear → Activation → Linear → Activation → ... → Linear → Output
```

Each layer: h = σ(W · x + b)

## Universal Approximation Theorem

A feedforward network with a single hidden layer containing enough neurons can approximate any continuous function on a compact domain, given a non-polynomial activation function.

## Forward Pass

```python
def forward(x):
    for W, b in zip(self.weights, self.biases):
        x = np.dot(x, W) + b
        x = activation(x)
    return x
```

## Backward Pass

Error backpropagates through each layer. The gradient w.r.t. weights uses the chain rule:

∂L/∂W^l = (δ^l) · (h^{l-1})^T

where δ^l is the error signal at layer l.

## Design Choices

- Depth vs. width tradeoff
- Activation choice (ReLU family preferred for deep nets)
- Weight initialization (Xavier/He)
- Regularization between layers

## Code Reference

`code/06.py`: Full MLP implementation with numpy, trainable via autograd.
