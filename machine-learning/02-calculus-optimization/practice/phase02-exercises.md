# Phase 02 — Exercises: Calculus, Optimization & Control

## Theory

1. **ε-δ Proof**: Prove that the derivative of `f(x) = x²` is `2x` using the limit definition.

2. **Taylor Series**: Derive the first four terms of the Taylor expansion of `eˣ` around `x=0`. What is the error bound for `|x| < 0.5`?

3. **Hessian & Convexity**: Compute the Hessian of `f(x, y) = x² + 3y² + 2xy`. Is the function convex? Show your reasoning.

4. **KKT Conditions**: Write the KKT conditions for the problem:
   ```
   minimize    f(x) = (x₁ - 1)² + (x₂ - 2)²
   subject to  x₁ + x₂ ≤ 1
               x₁ ≥ 0, x₂ ≥ 0
   ```

5. **Convexity Proof**: Prove that the sum of two convex functions is convex. Prove that the pointwise maximum of convex functions is convex.

6. **ADMM**: Write the ADMM updates for `minimize f(x) + g(z)` subject to `Ax + Bz = c`. Explain the role of the Lagrange multiplier.

7. **Natural Gradient**: Explain why natural gradient descent uses the Fisher information matrix. How does it differ from standard gradient descent?

8. **Calculus of Variations**: Derive the Euler-Lagrange equation for the functional `F[y] = ∫ₐᵇ L(x, y, y') dx`.

9. **Hamiltonian Monte Carlo**: Explain how the Hamiltonian formulation leads to efficient MCMC sampling. What is the role of the leapfrog integrator?

10. **Bayesian Optimization**: Describe the exploration-exploitation trade-off in Bayesian optimization. Compare Expected Improvement and Upper Confidence Bound acquisition functions.

## Coding

11. **Gradient Descent from Scratch**: Implement gradient descent to minimize `f(x) = x⁴ - 3x³ + 2` with learning rate scheduling (step decay, exponential decay). Plot the convergence.

12. **Adam Optimizer**: Implement the Adam optimizer from scratch for logistic regression on synthetic 2D data. Compare convergence with SGD and momentum.

13. **Proximal Gradient**: Implement ISTA (Iterative Shrinkage-Thresholding Algorithm) for L1-regularized least squares (LASSO). Compare with standard gradient descent.

14. **ADMM for Lasso**: Implement ADMM to solve the LASSO problem: `minimize (1/2)‖Ax - b‖² + λ‖x‖₁`. Track the primal and dual residuals.

15. **Optimizer Zoo Comparison**: Implement a benchmark comparing SGD, Momentum, NAG, AdaGrad, RMSprop, Adam, and BFGS on the Rosenbrock function. Plot convergence curves for all methods on the same axes.

16. **Loss Landscape Visualization**: Implement 1D and 2D slice visualizations of a neural network loss landscape near a minimum. Use filter-normalized directions.

17. **CMA-ES**: Implement a Covariance Matrix Adaptation Evolution Strategy from scratch to minimize `f(x) = Σ xᵢ²` in 10 dimensions. Plot the convergence.

18. **Constrained Optimization**: Use scipy.optimize to solve the constrained problem from Exercise 4. Compare SLSQP and trust-constr methods.

19. **Bayesian Optimization**: Implement a simple GP-based Bayesian optimizer for `f(x) = sin(3x) + x²` with noise. Plot the acquisition function and posterior at each iteration.

20. **SGD with Variance Reduction**: Implement SVRG for logistic regression. Compare the variance of gradients with standard SGD over iterations.
