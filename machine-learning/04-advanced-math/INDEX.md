# Phase 04 — Advanced Mathematical Foundations

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 04 — Advanced Mathematical Foundations |
| **Lessons** | 36 |
| **Core topics** | Entropy, divergences (KL, JS, f-divergences), maximum entropy, Fisher information, rate distortion, channel capacity, MDL/Kolmogorov complexity, information geometry, RKHS, optimal transport, Markov chains, Monte Carlo, MCMC, Riemannian HMC, stochastic processes, stochastic calculus, Fourier/wavelet, signal processing, graph theory, TDA, differential geometry, Lie groups, representation theory, symplectic geometry, functional analysis, measure theory, fixed-point theory, category theory, statistical mechanics, statistical physics of learning, random graphs, algorithmic information theory, game theory, social choice, complexity theory, feature selection |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (vector spaces, eigenvalues), [Phase 02](../02-calculus-optimization/INDEX.md) (gradients, convexity), [Phase 03](../03-probability-statistics/INDEX.md) (probability, distributions, MLE)
- **Python frameworks:** None specific

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Entropy | Shannon entropy, conditional entropy, mutual information | [lesson](lessons/01-entropy.md) | [code](code/01-entropy.py) | Used in: Phase 09 (information theory), Phase 06 (cross-entropy loss) |
| 02 | Divergences | KL, JS, f-divergences, properties | [lesson](lessons/02-divergences.md) | [code](code/02-divergences.py) | Used in: Phase 07 (VAEs, diffusion), Phase 09 (distillation) |
| 03 | Maximum Entropy | MaxEnt principle, exponential family | [lesson](lessons/03-max-entropy.md) | [code](code/03-max-entropy.py) | Used in: Phase 05 (MaxEnt models) |
| 04 | Fisher Information | Fisher matrix, Cramér–Rao bound | [lesson](lessons/04-fisher-information.md) | [code](code/04-fisher-information.py) | Used in: Phase 02 (natural gradient) |
| 05 | Rate Distortion | Lossy compression, Blahut–Arimoto | [lesson](lessons/05-rate-distortion.md) | [code](code/05-rate-distortion.py) | Used in: Phase 09 (quantization) |
| 06 | Channel Capacity | Channel coding, mutual information maximization | [lesson](lessons/06-channel-capacity.md) | [code](code/06-channel-capacity.py) | Used in: Phase 06 (capacity of NNs) |
| 07 | MDL & Kolmogorov | Minimum description length, algorithmic complexity | [lesson](lessons/07-mdll-kolmogorov.md) | [code](code/07-mdll-kolmogorov.py) | Used in: Phase 05 (model selection) |
| 08 | Information Geometry | Statistical manifolds, Fisher-Rao metric | [lesson](lessons/08-information-geometry.md) | [code](code/08-information-geometry.py) | Used in: Phase 02 (natural gradient) |
| 09 | RKHS | Reproducing kernel Hilbert space, kernel trick | [lesson](lessons/09-rkhs.md) | [code](code/09-rkhs.py) | Used in: Phase 05 (kernel SVM, GP) |
| 10 | Optimal Transport | Wasserstein distance, Earth mover, Sinkhorn | [lesson](lessons/10-optimal-transport.md) | [code](code/10-optimal-transport.py) | Used in: Phase 07 (Wasserstein GANs) |
| 11 | Markov Chains | Transition matrices, stationary distribution, mixing | [lesson](lessons/11-markov-chains.md) | [code](code/11-markov-chains.py) | Used in: Phase 05 (HMM), Phase 10 (MDPs) |
| 12 | Monte Carlo | Importance sampling, rejection, SIR | [lesson](lessons/12-monte-carlo.md) | [code](code/12-monte-carlo.py) | Used in: Phase 10 (MC RL) |
| 13 | MCMC | Metropolis–Hastings, Gibbs, Hamiltonian MC | [lesson](lessons/13-mcmc.md) | [code](code/13-mcmc.py) | Used in: Phase 03 (Bayesian inference) |
| 14 | Riemannian HMC | HMC on manifolds, geodesic motion | [lesson](lessons/14-riemannian-hmc.md) | [code](code/14-riemannian-hmc.py) | Used in: Phase 03 (Bayesian nonparametrics) |
| 15 | Stochastic Processes | Poisson, Wiener, martingales, ergodicity | [lesson](lessons/15-stochastic-processes.md) | [code](code/15-stochastic-processes.py) | Used in: Phase 10 (RL theory) |
| 16 | Stochastic Calculus | Ito integral, Ito's lemma, Girsanov | [lesson](lessons/16-stochastic-calculus.md) | [code](code/16-stochastic-calculus.py) | Used in: Phase 07 (diffusion SDEs) |
| 17 | Fourier & Wavelet | Fourier transform, wavelet, multiresolution | [lesson](lessons/17-fourier-wavelet.md) | [code](code/17-fourier-wavelet.py) | Used in: Phase 08 (image processing) |
| 18 | Signal Processing | Filtering, sampling, convolution theorem | [lesson](lessons/18-signal-processing.md) | [code](code/18-signal-processing.py) | Used in: Phase 08 (convolutions, audio) |
| 19 | Graph Theory | Graph properties, Laplacian, spectral clustering | [lesson](lessons/19-graph-theory.md) | [code](code/19-graph-theory.py) | Used in: Phase 05 (graph-based learning), Phase 01 (graph Laplacians) |
| 20 | TDA | Persistent homology, barcodes, mapper | [lesson](lessons/20-tda.md) | [code](code/20-tda.py) | Used in: Phase 05 (topological features) |
| 21 | Differential Geometry | Manifolds, tangent spaces, curvature | [lesson](lessons/21-differential-geometry.md) | [code](code/21-differential-geometry.py) | Used in: Phase 07 (neural manifolds) |
| 22 | Lie Groups | SO(3), SE(3), Lie algebra, exponential map | [lesson](lessons/22-lie-groups.md) | [code](code/22-lie-groups.py) | Used in: Phase 08 (3D vision, robotics) |
| 23 | Representation Theory | Group representations, characters, irreps | [lesson](lessons/23-representation-theory.md) | [code](code/23-representation-theory.py) | Used in: Phase 06 (equivariant NNs) |
| 24 | Symplectic Geometry | Symplectic manifolds, Hamiltonian mechanics | [lesson](lessons/24-symplectic-geometry.md) | [code](code/24-symplectic-geometry.py) | Used in: Phase 07 (symplectic ODEs) |
| 25 | Functional Analysis | Banach/Hilbert spaces, operators, spectra | [lesson](lessons/25-functional-analysis.md) | [code](code/25-functional-analysis.py) | Used in: Phase 04 (RKHS), Phase 05 (kernel methods) |
| 26 | Measure Theory | Sigma-algebras, measures, Lebesgue integral | [lesson](lessons/26-measure-theory.md) | [code](code/26-measure-theory.py) | Used in: Phase 03 (probability foundations) |
| 27 | Fixed-Point Theory | Banach fixed point, Brouwer, Kakutani | [lesson](lessons/27-fixed-point.md) | [code](code/27-fixed-point.py) | Used in: Phase 06 (neural ODEs, DEQs) |
| 28 | Category Theory | Functors, natural transformations, adjunctions | [lesson](lessons/28-category-theory.md) | [code](code/28-category-theory.py) | Used in: Phase 06 (differentiable programming) |
| 29 | Statistical Mechanics | Boltzmann distribution, partition function | [lesson](lessons/29-stat-mech.md) | [code](code/29-stat-mech.py) | Used in: Phase 07 (EBMs, Hopfield) |
| 30 | Statistical Physics of Learning | Generalization, phase transitions, replica | [lesson](lessons/30-stat-physics-learning.md) | [code](code/30-stat-physics-learning.py) | Used in: Phase 05 (learning theory) |
| 31 | Random Graphs | Erdős–Rényi, small-world, preferential attachment | [lesson](lessons/31-random-graphs.md) | [code](code/31-random-graphs.py) | Used in: Phase 09 (graph NNs) |
| 32 | Algorithmic Information | Kolmogorov complexity, Solomonoff induction | [lesson](lessons/32-algorithmic-information.md) | [code](code/32-algorithmic-information.py) | Used in: Phase 05 (model selection) |
| 33 | Game Theory | Nash equilibrium, zero-sum, potential games | [lesson](lessons/33-game-theory.md) | [code](code/33-game-theory.py) | Used in: Phase 10 (MARL), Phase 07 (GANs) |
| 34 | Social Choice | Voting, Arrow's theorem, mechanism design | [lesson](lessons/34-social-choice.md) | [code](code/34-social-choice.py) | Used in: Phase 11 (fairness) |
| 35 | Complexity Theory | P, NP, hardness, approximation | [lesson](lessons/35-complexity.md) | [code](code/35-complexity.py) | Used in: Phase 05 (learning theory) |
| 36 | Feature Selection | Information-theoretic methods, mutual information | [lesson](lessons/36-feature-selection.md) | [code](code/36-feature-selection.py) | Used in: Phase 05 (feature engineering), Phase 11 (data pipelines) |

## 4. Builds Toward

- **Phase 07** (VAEs, normalizing flows, EBMs, GANs, diffusion — all rely on information theory/geometry)
- **Phase 08** (Fourier/wavelet for image processing, Lie groups for 3D vision)
- **Phase 09** (information theory for language, optimal transport for alignment)
- **Phase 05** (kernel methods via RKHS, spectral methods via graph theory)
- **Phase 10** (game theory for multi-agent RL, MDPs via Markov chains)

## 5. Quick Start

```bash
python3 code/01-entropy.py
```
