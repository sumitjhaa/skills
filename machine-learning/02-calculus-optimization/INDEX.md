# Phase 02 — Calculus & Optimization

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 02 — Calculus & Optimization |
| **Lessons** | 40 |
| **Core topics** | Limits, derivatives, Taylor series, multivariable calculus, Hessians, implicit differentiation, gradient descent, momentum/Nesterov, adaptive methods (Adam), Newton, BFGS, conjugate gradient, constrained optimization, LP, QP, SDP, convex analysis, proximal operators, ADMM, operator splitting, variance-reduced SGD, second-order stochastic, natural gradient, calculus of variations, optimal control, SDEs, Hamiltonian Monte Carlo, Bayesian optimization, multi-objective, zeroth-order, genetic algorithms, relaxation, bilevel, compositional, distributed, optimizer zoo, differentiable optimization, minibatch selection, learn-to-optimize, loss landscape |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (vectors, matrices, eigenvalues)
- **Python frameworks:** None specific

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Limits | Epsilon-delta, continuity, limit laws | [lesson](lessons/01-limits.md) | [code](code/01-limits.py) | Foundation for all calculus |
| 02 | Derivative Rules | Product, chain, quotient, higher-order | [lesson](lessons/02-derivative-rules.md) | [code](code/02-derivative-rules.py) | Used in: Phase 06 (backprop chain rule) |
| 03 | Taylor Series | Approximations, remainder, multivariate Taylor | [lesson](lessons/03-taylor-series.md) | [code](code/03-taylor-series.py) | Used in: Phase 06 (second-order opt), Phase 07 (neural ODEs) |
| 04 | Multivariable Calculus | Partial derivatives, gradient, directional derivative | [lesson](lessons/04-multivariable.md) | [code](code/04-multivariable.py) | Used in: Phase 06 (gradient descent), Phase 10 (policy gradient) |
| 05 | Hessian | Second-order derivatives, curvature, definiteness | [lesson](lessons/05-hessian.md) | [code](code/05-hessian.py) | Used in: Phase 06 (2nd order methods), Phase 01 (eigenvalues) |
| 06 | Implicit Differentiation | Implicit function theorem, differentiating through solvers | [lesson](lessons/06-implicit-differentiation.md) | [code](code/06-implicit-differentiation.py) | Used in: Phase 06 (implicit layers), Phase 07 (DEQs) |
| 07 | Gradient Descent | Learning rates, convergence, GD for ML | [lesson](lessons/07-gradient-descent.md) | [code](code/07-gradient-descent.py) | Used in: Phase 06 (training loop), Phase 10 (policy gradient) |
| 08 | Momentum & Nesterov | Momentum, Nesterov accelerated gradient | [lesson](lessons/08-momentum-nesterov.md) | [code](code/08-momentum-nesterov.py) | Used in: Phase 06 (optimizer zoo), Phase 10 (RL) |
| 09 | Adaptive Methods | AdaGrad, RMSProp, Adam, AMSGrad | [lesson](lessons/09-adaptive-methods.md) | [code](code/09-adaptive-methods.py) | Used in: Phase 06 (optimizers), Phase 10 (RL) |
| 10 | Newton Methods | Newton–Raphson, convergence, line search | [lesson](lessons/10-newton-methods.md) | [code](code/10-newton-methods.py) | Used in: Phase 05 (logistic regression IRLS) |
| 11 | Quasi-Newton BFGS | BFGS, L-BFGS, limited memory | [lesson](lessons/11-quasi-newton-bfgs.md) | [code](code/11-quasi-newton-bfgs.py) | Used in: Phase 06 (L-BFGS optimization) |
| 12 | Conjugate Gradient | CG for linear systems, nonlinear CG | [lesson](lessons/12-conjugate-gradient.md) | [code](code/12-conjugate-gradient.py) | Used in: Phase 01 (Krylov methods) |
| 13 | Constrained Optimization | Lagrange multipliers, KKT conditions | [lesson](lessons/13-constrained-optimization.md) | [code](code/13-constrained-optimization.py) | Used in: Phase 05 (SVM dual), Phase 10 (constrained RL) |
| 14 | Linear Programming | Simplex, duality, interior-point | [lesson](lessons/14-linear-programming.md) | [code](code/14-linear-programming.py) | Used in: Phase 11 (resource allocation) |
| 15 | Quadratic Programming | QP, sequential quadratic programming | [lesson](lessons/15-quadratic-programming.md) | [code](code/15-quadratic-programming.py) | Used in: Phase 05 (SVM) |
| 16 | Semidefinite Programming | SDP, LMIs, relaxations | [lesson](lessons/16-semidefinite-programming.md) | [code](code/16-semidefinite-programming.py) | Used in: Phase 04 (max-cut) |
| 17 | Convex Analysis | Convex sets, functions, subgradients, conjugates | [lesson](lessons/17-convex-analysis.md) | [code](code/17-convex-analysis.py) | Used in: Phase 05 (convex loss), Phase 06 (convexity) |
| 18 | Proximal Operators | Prox mapping, Moreau envelope | [lesson](lessons/18-proximal-operators.md) | [code](code/18-proximal-operators.py) | Used in: Phase 05 (regularized models) |
| 19 | ADMM | Alternating direction method of multipliers | [lesson](lessons/19-admm.md) | [code](code/19-admm.py) | Used in: Phase 05 (distributed LR) |
| 20 | Operator Splitting | Forward-backward, Douglas–Rachford | [lesson](lessons/20-operator-splitting.md) | [code](code/20-operator-splitting.py) | Used in: Phase 05 (sparse models) |
| 21 | Variance-Reduced SGD | SVRG, SAGA, SARAH | [lesson](lessons/21-variance-reduced-sgd.md) | [code](code/21-variance-reduced-sgd.py) | Used in: Phase 06 (efficient training) |
| 22 | Second-Order Stochastic | AdaHessian, stochastic L-BFGS | [lesson](lessons/22-second-order-stochastic.md) | [code](code/22-second-order-stochastic.py) | Used in: Phase 06 (scaling) |
| 23 | Natural Gradient | Fisher information matrix, natural GD | [lesson](lessons/23-natural-gradient.md) | [code](code/23-natural-gradient.py) | Used in: Phase 06 (NGD), Phase 07 (VAEs) |
| 24 | Calculus of Variations | Euler–Lagrange, functional derivatives | [lesson](lessons/24-calculus-of-variations.md) | [code](code/24-calculus-of-variations.py) | Used in: Phase 07 (neural ODEs, PINNs) |
| 25 | Optimal Control | LQR, Pontryagin, HJB | [lesson](lessons/25-optimal-control.md) | [code](code/25-optimal-control.py) | Used in: Phase 10 (RL as control) |
| 26 | SDEs | Ito calculus, diffusion processes | [lesson](lessons/26-sdes.md) | [code](code/26-sdes.py) | Used in: Phase 07 (diffusion models) |
| 27 | Hamiltonian Monte Carlo | HMC, leapfrog, NUTS | [lesson](lessons/27-hamiltonian-monte-carlo.md) | [code](code/27-hamiltonian-monte-carlo.py) | Used in: Phase 03 (Bayesian inference) |
| 28 | Bayesian Optimization | GP-based optimization, acquisition functions | [lesson](lessons/28-bayesian-optimization.md) | [code](code/28-bayesian-optimization.py) | Used in: Phase 05 (AutoML), Phase 11 (hyperparam tuning) |
| 29 | Multi-Objective | Pareto frontier, scalarization, MOEA/D | [lesson](lessons/29-multi-objective.md) | [code](code/29-multi-objective.py) | Used in: Phase 11 (model selection) |
| 30 | Zeroth-Order | Finite-difference, evolution strategies | [lesson](lessons/30-zeroth-order.md) | [code](code/30-zeroth-order.py) | Used in: Phase 10 (ES for RL) |
| 31 | Genetic Algorithms | Selection, crossover, mutation, CMA-ES | [lesson](lessons/31-genetic-algorithms.md) | [code](code/31-genetic-algorithms.py) | Used in: Phase 05 (feature selection) |
| 32 | Relaxation | Lagrangian, convex, semidefinite relaxations | [lesson](lessons/32-relaxation.md) | [code](code/32-relaxation.py) | Used in: Phase 04 (combinatorial problems) |
| 33 | Bilevel Optimization | Hyperparameter optimization, meta-learning | [lesson](lessons/33-bilevel-optimization.md) | [code](code/33-bilevel-optimization.py) | Used in: Phase 06 (meta-learning), Phase 12 (AutoML) |
| 34 | Compositional Optimization | Gradient-free, stochastic compositional | [lesson](lessons/34-compositional-optimization.md) | [code](code/34-compositional-optimization.py) | Used in: Phase 06 (multi-task) |
| 35 | Distributed Optimization | All-reduce, decentralized, federated | [lesson](lessons/35-distributed-optimization.md) | [code](code/35-distributed-optimization.py) | Used in: Phase 11 (distributed training) |
| 36 | Optimizer Zoo | Collection of modern ML optimizers | [lesson](lessons/36-optimizer-zoo.md) | [code](code/36-optimizer-zoo.py) | Used in: Phase 06 (optimizer reference) |
| 37 | Differentiable Optimization | OptNet, differentiable convex layers | [lesson](lessons/37-differentiable-optimization.md) | [code](code/37-differentiable-optimization.py) | Used in: Phase 06 (implicit layers) |
| 38 | Minibatch Selection | Curriculum, importance sampling | [lesson](lessons/38-minibatch-selection.md) | [code](code/38-minibatch-selection.py) | Used in: Phase 06 (training efficiency) |
| 39 | Learn to Optimize | L2O, learned optimizers | [lesson](lessons/39-learn-to-optimize.md) | [code](code/39-learn-to-optimize.py) | Used in: Phase 06 (meta-learning) |
| 40 | Loss Landscape | Sharpness, flat minima, mode connectivity | [lesson](lessons/40-loss-landscape.md) | [code](code/40-loss-landscape.py) | Used in: Phase 06 (generalization) |

## 4. Builds Toward

- **Phase 05** (training classical models: logistic regression, SVM, gradient boosting)
- **Phase 06** (gradient-based neural network training, optimizers)
- **Phase 07** (neural ODEs, PINNs, variational methods)
- **Phase 10** (policy gradients, RL optimization)
- **Phase 12** (capstones: autograd, RLHF, distributed training)

## 5. Quick Start

```bash
python3 code/07-gradient-descent.py
```
