# 📝 PyTorch — Phase 01 Practice (Tensors & Autograd)

## Exercise 1: Tensor Manipulation

Create a 5×3 tensor of random floats. Slice the first 2 rows and last 2 columns. Reshape to (2, 5). Multiply element-wise by a 1D tensor of [1, 2, 3, 4, 5] using broadcasting.

## Exercise 2: Gradient Computation

Define `f(x, y) = x² + 3y² + 2xy + x - y`. Compute gradients at (2, -1) using autograd. Verify manually.

## Exercise 3: Gradient Descent on a Surface

Minimize `f(x, y) = (x-3)² + (y+2)² + xy` using manual gradient descent. Start at (0, 0), lr=0.1, 50 steps. Print (x, y, f) every 10 steps.

## Exercise 4: Linear Regression DIY

Generate `y = 2.5 * X + 0.8 + noise`. Train with manual w,b and autograd. Compare convergence with lr=0.001, 0.01, 0.1.

## Exercise 5: Learning Rate Effect

Modify the gradient descent lesson to try lr = [1.0, 0.5, 0.1, 0.01]. Plot (or print) the value of f(x) at each step for each LR. Which LR is best?

## Exercise 6: nn.Linear with Multiple Features

Generate data with 3 input features: `y = 2*x1 - 1.5*x2 + 0.5*x3 + noise`. Train with nn.Linear(3, 1). Report learned weights vs true.

## Exercise 7: Loss Function Comparison

Compare MSE, L1, and Huber losses on the same regression problem. Which converges fastest? Which is most robust to outliers? (Add a single outlier at 10× magnitude to test.)

## Exercise 8: Optimizer Comparison

Compare SGD, SGD+Momentum, Adam, and RMSprop on a binary classification problem. Report final loss and accuracy for each after 50 epochs.

## Exercise 9: Binary Classifier from Scratch

Without using nn.Linear, implement binary classification with manually defined weight and bias tensors (requires_grad=True) on synthetic 2D data. Visualize (or describe) the decision boundary.

## Exercise 10: End-to-End Classification

For synthetic 5-feature binary data (n=1000):
- Create an nn.Module class
- Train with BCEWithLogitsLoss + Adam
- Track training accuracy
- Report test accuracy
- Try adding one hidden layer (compare 0 vs 1 hidden layer performance)
