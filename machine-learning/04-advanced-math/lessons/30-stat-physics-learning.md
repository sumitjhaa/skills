# 04.30 Statistical Physics of Learning

## Motivation
Statistical physics provides powerful tools to analyse learning in neural networks, including generalisation bounds, phase transitions in learning, and the dynamics of gradient descent in high dimensions. The replica method, cavity approach, and Gaussian equivalence theorem yield precise predictions for the performance of neural networks in the high-dimensional limit.

## Learning Objectives
- Understand the teacher-student paradigm for analysing generalisation.
- Derive generalisation error using the replica method.
- Explain double descent and the interpolation threshold.
- Connect random feature models to the Gaussian equivalence principle.

## Math Foundation

### Teacher–Student Paradigm
A "teacher" network (true data-generating process) produces labels:
$$y = f^*(x) + \epsilon$$

A "student" network $f_\theta$ learns from $n$ i.i.d. samples. The generalisation error (test error) is:

$$E_g = \mathbb{E}_{x, \epsilon}[(f_\theta(x) - f^*(x))^2]$$

Statistical physics computes the average $E_g$ over random training sets, model parameters, and teacher realisations.

### Replica Method
The replica trick computes $\mathbb{E}[\log Z]$, which appears in the free energy and generalisation error:

$$\mathbb{E}[\log Z] = \lim_{n \to 0} \frac{1}{n} \log \mathbb{E}[Z^n]$$

For $Z = \int \exp(-\beta \mathcal{L}(\theta)) d\theta$ (the partition function), the replica approach:
1. Compute $\mathbb{E}[Z^n]$ for integer $n$ — this is an $n$-fold replicated system.
2. Assume replica symmetry (RS): the $n$ replicas are symmetric under permutation.
3. Take the limit $n \to 0$ analytically.

### Gardner's Formula (Perceptron)
For a perceptron with $N$ inputs trained on $P = \alpha N$ random patterns, the capacity is $\alpha_c = 2$. Gardner (1988) computed the volume of coupling space:

$$\mathcal{V} \propto \exp\left( N \int dx \log \int_{-\infty}^x \frac{dt}{\sqrt{2\pi}} e^{-t^2/2} \right)$$

showing a critical $\alpha_c$ beyond which the volume vanishes (the perceptron can no longer classify all patterns).

### Gaussian Equivalence Theorem
For random feature models $f(x) = \frac{1}{\sqrt{N}} \sum_{i=1}^N a_i \phi(w_i^\top x)$ with random $w_i$:

1. The features $\phi(w_i^\top x)$ become jointly Gaussian with the target in the $N \to \infty$ limit.
2. The test error depends only on the second-order statistics: $\mathbb{E}[y \phi(w^\top x)]$ and $\mathbb{E}[\phi(w^\top x) \phi(w^\top x')]$.
3. This allows exact computation of generalisation error for kernel regression and wide neural networks.

### Double Descent
The test error as a function of model complexity $N$ (or parameter count) shows:
- Classical regime ($N < n$): error decreases as $N$ increases (bias-variance trade-off).
- Interpolation threshold ($N = n$): error spikes (model exactly fits training data).
- Modern regime ($N > n$): error decreases again (overparameterised, "benign overfitting").

This is predicted by random matrix theory: the test error has a peak at the point where the sample covariance matrix becomes singular.

## Python Implementation

```python
import numpy as np

def teacher_student_perceptron(n_train=200, d=100, alpha=2.0):
    """Simulate teacher-student perceptron learning.
    Returns generalisation error."""
    N = d  # input dimension
    P = int(alpha * N)  # number of samples
    
    # Teacher weights
    w_star = np.random.randn(N)
    w_star /= np.linalg.norm(w_star)
    
    # Generate data
    X = np.random.randn(P, N)
    y = np.sign(X @ w_star)
    
    # Student: perceptron learning (online)
    w = np.zeros(N)
    for _ in range(100):
        for i in range(P):
            if y[i] * (X[i] @ w) <= 0:
                w += y[i] * X[i] / N
    
    w /= np.linalg.norm(w)
    
    # Generalisation error (angle between w and w*)
    Eg = 1 - (w @ w_star)
    return Eg

def double_descent_simulation(n=100, max_d=300, n_trials=20, noise=0.1):
    """Simulate double descent for linear regression."""
    np.random.seed(42)
    errors = np.zeros((n_trials, max_d // 10))
    dims = np.arange(10, max_d + 1, 10)
    
    for t in range(n_trials):
        X = np.random.randn(n, max_d)
        w_star = np.random.randn(max_d) / np.sqrt(max_d)
        y = X @ w_star + noise * np.random.randn(n)
        
        for i, d in enumerate(dims):
            if d <= n:
                # OLS
                w = np.linalg.lstsq(X[:, :d], y, rcond=None)[0]
                bias = 0.0
            else:
                # Min-norm interpolator
                w = X[:, :d].T @ np.linalg.solve(X[:, :d] @ X[:, :d].T, y)
                bias = 0.0
            
            # Test error (infinite test set -> expectation over new data)
            test_err = noise**2 + np.linalg.norm(w - w_star[:d])**2
            errors[t, i] = test_err
    
    return dims, np.mean(errors, axis=0), np.std(errors, axis=0)

def random_feature_model(n_train=500, n_features=100, d_input=50):
    """Random feature regression and its Gaussian equivalent."""
    # Generate data
    X = np.random.randn(n_train, d_input)
    w_star = np.random.randn(d_input) / np.sqrt(d_input)
    y = X @ w_star + 0.1 * np.random.randn(n_train)
    
    # Random features
    W = np.random.randn(d_input, n_features) / np.sqrt(d_input)
    Phi = np.tanh(X @ W)  # nonlinear features
    
    # Feature covariance and target covariance
    C_phi = Phi.T @ Phi / n_train
    c_target = Phi.T @ y / n_train
    
    # Ridge regression
    lam = 0.01
    w_phi = np.linalg.solve(C_phi + lam * np.eye(n_features), c_target)
    train_pred = Phi @ w_phi
    
    train_error = np.mean((train_pred - y)**2)
    print(f"Random feature regression train MSE: {train_error:.4f}")
    
    # Gaussian equivalent kernel
    K = Phi @ Phi.T / n_features
    K_ge = np.tanh(X @ X.T / d_input)  # limiting kernel in infinite-width limit
    print(f"Kernel alignment: {np.corrcoef(K.flatten(), K_ge.flatten())[0,1]:.4f}")
    
    return train_error

# Run perceptron experiment
Eg = teacher_student_perceptron(alpha=2.0)
print(f"Perceptron generalisation error: {Eg:.4f}")
```

## Visualization
Plot the double descent curve: test error vs model complexity $d/n$. The peak at $d = n$ (interpolation threshold) and the decrease for $d > n$ illustrate the modern overparameterised regime. A second panel shows the phase diagram of the perceptron: capacity $\alpha_c$ as a function of the fraction of mislabelled patterns, showing the Gardner-Derrida phase transition. A third panel shows the eigenvalue spectrum of the feature covariance matrix (Marchenko-Pastur) and how it controls the test error.

## Key Results in Statistical Physics of Learning

### Perceptron Capacity
The maximal number of random binary patterns a perceptron can store is $P_{\max} = 2N$. Beyond this capacity, the volume of coupling vectors vanishes — the problem transitions from SAT to UNSAT (a first-order phase transition).

### Generalisation Error of Ridge Regression
For Gaussian data with covariance $\Sigma$ and teacher $w^*$, the test error of ridge regression with regularisation $\lambda$ is:

$$E_g = \frac{1}{N} \sum_{i=1}^N \frac{\lambda^2}{(\hat{\lambda}_i + \lambda)^2} + \text{bias}^2$$

where $\hat{\lambda}_i$ are the eigenvalues of the empirical covariance. In the proportional limit $n/N \to \alpha$, this can be computed exactly using random matrix theory (the Stieltjes transform of the spectral distribution).

### Neural Tangent Kernel Limit
For a wide neural network ($\text{width} \to \infty$) trained with gradient flow, the network function evolves as kernel regression with the NTK. The test error is:

$$E_g(\infty) = \text{noise}^2 + \|(I - K_\infty(K_\infty + \lambda I)^{-1}) w^*\|^2$$

where $K_\infty$ is the NTK matrix on the training data.

## Practical Implications

### When Is Overparameterisation Beneficial?
- **Low noise**: overparameterisation helps (benign overfitting, double descent descent).
- **High noise**: overparameterisation hurts (the test error increases after interpolation).
- **Structure**: if the target function is low-rank, overparameterisation is always beneficial.

### Designing Architectures
- The Gaussian equivalence theorem suggests that wide networks with random features behave like kernel methods.
- Adding depth changes the kernel but the limiting behaviour is still described by a kernel (the deep NTK).
- The replica method can predict which architectures generalise best for given data distributions.

## References
- Engel & Van den Broeck, *Statistical Mechanics of Learning*, Cambridge 2001
- Mezard & Montanari, *Information, Physics, and Computation*, Oxford 2009
- Gardner, "The Space of Interactions in Neural Network Models," *J. Phys. A*, 1988
- Bahri et al., "Statistical Mechanics of Deep Learning," *Annual Review of Condensed Matter Physics*, 2020
- Advani, Saxe, Sompolinsky, "High-Dimensional Dynamics of Generalization Error in Neural Networks," *Neural Networks*, 2020
- Hastie et al., "Surprises in High-Dimensional Ridgeless Least Squares Interpolation," *Annals of Statistics*, 2022
