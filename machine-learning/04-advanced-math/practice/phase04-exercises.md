# Phase 04 — Practice Exercises

> Complete these exercises after working through the lessons. Each exercise links to specific modules.

---

## Exercise 1: Entropy & Mutual Information (04.01–04.02)

Given the joint distribution $P(X,Y)$ below, compute $H(X)$, $H(Y)$, $H(X,Y)$, $H(X|Y)$, $I(X;Y)$.

| X\Y | 0 | 1 |
|-----|---|---|
| 0   | 0.3 | 0.2 |
| 1   | 0.1 | 0.4 |

**Tasks:**
- Compute all quantities by hand, then verify with Python.
- Which pairs show independence? Which show maximal dependence?

---

## Exercise 2: Maximum Entropy (04.03)

Derive and implement the max-entropy distribution given:
- Support $\mathbb{R}$
- $\mathbb{E}[X] = 0$, $\mathbb{E}[X^2] = 1$
- $\mathbb{E}[|X|] = 1$

Compare the resulting distribution to a standard Gaussian via KL divergence.

---

## Exercise 3: Fisher Information & Natural Gradient (04.04, 04.08)

For a Bernoulli model $p(y|\theta) = \theta^y (1-\theta)^{1-y}$:
- Compute the Fisher information $\mathcal{I}(\theta)$.
- Implement one step of natural gradient descent for logistic regression on a synthetic binary classification dataset.
- Compare convergence (in parameter space) with standard gradient descent.

---

## Exercise 4: Rate–Distortion & Channel Capacity (04.05–04.06)

Implement Blahut–Arimoto for:
1. A ternary source with Hamming distortion
2. A binary channel with crossover probability $p=0.15$

Plot the rate–distortion curve $R(D)$ and show the channel capacity convergence.

---

## Exercise 5: MDL for Model Selection (04.07, 04.32)

Generate data from $y = 2x - 0.5x^2 + \epsilon$ with $\epsilon \sim \mathcal{N}(0, 0.1)$.

Fit polynomials of degree 1 through 8. Use the two-part MDL criterion to select the optimal degree. Compare with BIC and cross-validation.

---

## Exercise 6: Optimal Transport & Sinkhorn (04.10)

Given two point clouds $X \sim \mathcal{N}(0, I)$ and $Y \sim \mathcal{N}(\mu, \Sigma)$ in $\mathbb{R}^2$:
- Compute the Wasserstein-2 distance analytically (using the closed form for Gaussians).
- Implement Sinkhorn's algorithm with entropic regularisation.
- Plot the transport plan for $\epsilon \in \{0.01, 0.1, 1.0\}$.

---

## Exercise 7: MCMC & Hamiltonian Monte Carlo (04.11–04.14)

Sample from a strongly correlated bivariate Gaussian $p(x,y) \propto \exp(-(x^2 + y^2 - 1.8xy)/2)$ using:
1. Random-walk Metropolis–Hastings
2. Gibbs sampling
3. HMC with leapfrog integrator

Compare effective sample size and autocorrelation for each method.

---

## Exercise 8: Gaussian Process Regression (04.09, 04.15)

Implement GP regression from scratch:
- Use a Matérn-5/2 kernel
- Fit to $y = \sin(x) + \epsilon$ with $n=20$ training points
- Predict on a dense grid and plot 95% credible intervals
- Optimise kernel hyperparameters via marginal likelihood

---

## Exercise 9: Spectral Clustering (04.19)

Implement spectral clustering on two concentric circles (noisy):
- Construct the similarity graph using an RBF kernel
- Compute the normalised graph Laplacian
- Extract the second eigenvector and threshold for clustering
- Compare with k-means on raw data

---

## Exercise 10: Persistent Homology (04.20)

Generate point clouds from:
- A circle $S^1$ with noise
- Two intertwined rings

Compute the persistence diagram (birth/death scales) for $H_0$ and $H_1$. Interpret the topological features.

---

## Exercise 11: Symplectic Integration & HMC (04.14, 04.24)

For the Hamiltonian $H(q,p) = \frac12 p^2 + \frac12 q^2 + 0.1 q^4$:
- Implement leapfrog (symplectic) and forward Euler integrators.
- Run both for $T=100$ with $\Delta t = 0.1$.
- Plot energy $H(q,p)$ over time and compare drift.
- Verify the symplectic integrator preserves phase-space volume.

---

## Exercise 12: Information-Theoretic Feature Selection (04.36)

On a high-dimensional synthetic dataset (100 features, 10 informative, 200 samples):
- Compute mutual information between each feature and the target.
- Implement MRMR (minimum redundancy maximum relevance).
- Select the top 10 features and evaluate with a classifier.
- Compare with LASSO-based feature selection.

---

## Bonus Exercise: Statistical Physics of Learning (04.30)

Simulate the teacher–student perceptron:
- Generate a random teacher vector $w^* \in \mathbb{R}^{100}$.
- Train a student perceptron on varying sample sizes $n \in \{20, 40, \ldots, 500\}$.
- Compute the generalisation error $E_g = \frac{1}{\pi} \arccos(\frac{w^\top w^*}{\|w\|\|w^*\|})$.
- Plot $E_g$ vs $\alpha = n/d$ and compare with the theoretical curve $E_g \approx 0.5 \, \text{erfc}(\sqrt{\alpha})$.
