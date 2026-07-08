# Phase 06: Deep Learning Foundations — Practice Exercises

## Prerequisite

```bash
pip install numpy scipy matplotlib
```

## Exercises

### 1. Autograd — Manual Gradient Computation

Given `f(x, y, z) = x² + y² + z² + x*y + y*z + x*z`, compute the gradient at (1, 2, 3) using:
- (a) Analytical derivation
- (b) Finite differences
- (c) Your autograd framework from `code/04.py`

Verify all three match.

### 2. Build a Minimal Autograd Tape

Implement a `Tensor` class supporting `__add__`, `__mul__`, `__pow__`, `relu`, and `backward()`. Test on `y = relu(x)² + x` and verify `dy/dx`.

### 3. MLP on Moons Dataset

Use `sklearn.datasets.make_moons` to generate a 2D binary classification dataset. Train a 3-layer MLP (4→16→8→1) with tanh activations using your autograd framework. Report train/test accuracy.

### 4. Activation Function Comparison

Train identical MLPs (same initialization, same data) varying only the activation function (ReLU, Tanh, GELU, Swish). Plot training curves and compare convergence speed.

### 5. Initialization Sensitivity

For a 10-layer MLP with ReLU, compare Xavier vs He vs random (unscaled) initialization. Track activation variances per layer. What happens with poor initialization?

### 6. Optimizer Comparison on Rosenbrock

Minimize the Rosenbrock function `f(x, y) = (a-x)² + b(y-x²)²` (a=1, b=100) using SGD, Momentum, Adam. Plot optimization trajectories. Which converges fastest?

### 7. Implement BatchNorm from Scratch

Implement BatchNorm1d and verify that its output has mean ~0 and variance ~1 across the batch dimension. Show that running statistics work correctly at inference.

### 8. CNN from Scratch — CIFAR-10 Classifier

Implement a 3-layer ConvNet (32→64→128 channels, 3x3 convs) with max pooling. Train on CIFAR-10 subset (5000 samples). Achieve >45% test accuracy.

### 9. Implement Dropout and Test

Add dropout (p=0.5) to an MLP and compare training vs validation accuracy with and without dropout on a synthetic overfitting task (small data, large model).

### 10. Scaled Dot-Product Attention

Implement attention from scratch and verify:
- Attention weights sum to 1 for each query
- Output is a weighted sum of values
- Causally masked attention zeros out future positions

### 11. Mini-Transformer

Implement a 2-layer transformer encoder with 4 heads, d_model=64. Test on a tiny sequence classification task (random sequences of length 8, classify by sum of elements > threshold).

### 12. BPTT for Character-Level RNN

Train a character-level RNN on a small text corpus (e.g., "hello world"). Unroll for 5 steps. Show that the model can predict the next character after training.

### 13. Gradient Clipping Analysis

Train an RNN with and without gradient clipping (norm=1.0). Plot gradient norms during training. Show that clipping prevents gradient explosion.

### 14. Label Smoothing Effect

Train a classifier with label smoothing ε ∈ {0, 0.05, 0.1, 0.2, 0.5}. Report:
- Training accuracy
- Validation accuracy
- Predicted probabilities (are they less overconfident with smoothing?)

### 15. Full Pipeline Ablation

Starting from `code/32.py`, run ablations:
- Remove BatchNorm → compare accuracy
- Remove dropout → check overfitting
- Double learning rate → observe instability
- Add weight decay 0.01 → compare validation accuracy

Report all results in a table.

## Bonus Challenges

### 16. Hessian-Vector Product

Implement Hessian-vector product for a 2-layer MLP. Verify against finite differences.

### 17. Mixup Training

Implement mixup augmentation and train a classifier with α=1.0. Compare accuracy and calibration vs. standard training.

### 18. Sine Wave Prediction with LSTM

Train an LSTM to predict the next value of a sine wave given 10 previous time steps. Evaluate on held-out frequencies.

## Submission

For each exercise, submit:
- Code (well-commented Python file)
- Output log or plot
- Brief written explanation (2-3 sentences)
