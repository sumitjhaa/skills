# 04.29 Statistical Mechanics and the Ising Model

## Motivation
Statistical mechanics explains macroscopic behaviour from microscopic interactions using probability. Its tools — partition functions, free energy, the Ising model — are deeply connected to probabilistic graphical models, Hopfield networks, and Boltzmann machines. Understanding these connections is essential for energy-based models, representation learning, and the theory of neural computation.

## Learning Objectives
- Define the partition function, Boltzmann distribution, and free energy.
- Derive mean-field theory for the Ising model.
- Connect the Ising model to Markov random fields and Hopfield networks.
- Apply Boltzmann machine learning via contrastive divergence.

## Math Foundation

### Boltzmann Distribution
For a system with energy $E(\sigma)$ and inverse temperature $\beta = 1/(k_B T)$, the probability of state $\sigma$ is:

$$p_\beta(\sigma) = \frac{1}{Z(\beta)} e^{-\beta E(\sigma)}$$

where the **partition function** $Z(\beta) = \sum_\sigma e^{-\beta E(\sigma)}$ normalises.

### Free Energy
The Helmholtz free energy is:

$$F = -\frac{1}{\beta} \log Z = \langle E \rangle - TS$$

where $S = -\sum_\sigma p(\sigma) \log p(\sigma)$ is the entropy. The free energy is minimised at equilibrium — it balances energy minimisation against entropy maximisation.

### Ising Model
The Ising model on $N$ spins $\sigma_i \in \{\pm 1\}$ with pairwise interactions:

$$E(\sigma) = -\sum_{i<j} J_{ij} \sigma_i \sigma_j - \sum_i h_i \sigma_i$$

- $J_{ij}$: interaction strength (ferromagnetic if $J_{ij} > 0$, anti-ferromagnetic if $J_{ij} < 0$).
- $h_i$: external magnetic field.
- $\sigma_i$: binary spin variables.

The 2D Ising model with nearest-neighbour interactions on a square lattice was solved exactly by Onsager (1944), showing a phase transition at:

$$T_c = \frac{2J}{k_B \text{asinh}(1)} \approx 2.269 J/k_B$$

### Mean-Field Theory
Replace interactions with an effective mean field:

$$m = \tanh(\beta (J_{\text{eff}} m + h))$$

where $m = \frac{1}{N} \sum_i \langle \sigma_i \rangle$ is the magnetisation. This self-consistent equation predicts a phase transition at $T_c = J_{\text{eff}} / k_B$.

### Variational Free Energy (Gibbs' Inequality)
For any distribution $q(\sigma)$:

$$F \le \mathbb{E}_q[E(\sigma)] - \frac{1}{\beta} H(q)$$

with equality iff $q = p_\beta$. This is the **variational principle** underlying mean-field methods in physics and variational inference in ML.

## Python Implementation

```python
import numpy as np
from scipy.special import expit

def ising_energy(spins, J, h=None):
    """Ising model energy."""
    N = len(spins)
    E = 0.0
    for i in range(N):
        for j in range(i+1, N):
            E -= J[i, j] * spins[i] * spins[j]
    if h is not None:
        E -= np.sum(h * spins)
    return E

def partition_function_ising(J, h, beta=1.0):
    """Exact partition function for small Ising model (enumeration)."""
    N = J.shape[0]
    Z = 0.0
    for config in range(2**N):
        spins = np.array([1 if (config >> i) & 1 else -1 for i in range(N)])
        Z += np.exp(-beta * ising_energy(spins, J, h))
    return Z

def mean_field_solution(J_mean, h=0.0, beta=1.0, tol=1e-8):
    """Solve mean-field equation m = tanh(beta * (J_eff * m + h))."""
    m = 0.0
    for _ in range(1000):
        m_new = np.tanh(beta * (J_mean * m + h))
        if abs(m_new - m) < tol:
            break
        m = m_new
    return m

def metropolis_ising(spins, J, h, beta, n_steps=10000):
    """Metropolis-Hastings for Ising model."""
    N = len(spins)
    for _ in range(n_steps):
        i = np.random.randint(N)
        dE = 2 * spins[i] * (np.sum(J[i] * spins) + h[i])
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            spins[i] *= -1
    return spins

# Example: 2-spin Ising model
N = 2
J = np.array([[0, 1], [1, 0]])
h = np.array([0.0, 0.1])
Z = partition_function_ising(J, h)
print(f"Partition function: {Z:.4f}")

# Mean-field magnetisation
for beta in [0.5, 1.0, 2.0]:
    m = mean_field_solution(1.0, h=0, beta=beta)
    print(f"beta={beta}: m = {m:.4f}")

# Gibbs sampling (conditional updates for Ising)
def gibbs_ising_1d(spins, J, h, beta, n_samples=1000):
    """Gibbs sampling for 1D Ising chain."""
    N = len(spins)
    samples = []
    for _ in range(n_samples):
        for i in range(N):
            # full conditional: p(spin_i | rest)
            neighbor_sum = spins[(i-1) % N] + spins[(i+1) % N]  # 1D ring
            logit = 2 * beta * (J[i, (i-1)%N] * spins[(i-1)%N] + J[i, (i+1)%N] * spins[(i+1)%N] + h[i])
            p_up = expit(logit)
            spins[i] = 1 if np.random.rand() < p_up else -1
        samples.append(spins.copy())
    return np.array(samples)

# 4-spin 1D Ising chain (periodic)
N = 4
J_1d = np.zeros((N, N))
for i in range(N):
    J_1d[i, (i+1)%N] = 1.0
    J_1d[(i+1)%N, i] = 1.0
spins = np.ones(N)
samples = gibbs_ising_1d(spins, J_1d, np.zeros(N), beta=1.0, n_samples=5000)
print(f"Mean magnetisation: {np.mean(samples):.4f}")
```

## Visualization
Plot the phase diagram of the 2D Ising model: magnetisation $m$ vs temperature $T$, showing the critical temperature $T_c$ where $m$ drops to zero (second-order phase transition). A second panel shows the mean-field prediction vs exact solution for a 1D chain (no phase transition in 1D) and 2D square lattice (phase transition at $T_c$). A third panel shows the free energy landscape $F(m)$ for different temperatures — below $T_c$, the landscape has two minima (spontaneous symmetry breaking).

## Connections to Machine Learning

### Boltzmann Machines
A Boltzmann machine is an Ising model with visible $v$ and hidden $h$ units:

$$E(v, h) = -\sum_{i,j} v_i W_{ij} h_j - \sum_i a_i v_i - \sum_j b_j h_j - \sum_{i<k} v_i U_{ik} v_k - \sum_{j<l} h_j V_{jl} h_l$$

The marginal distribution over visible units $p(v) = \sum_h \exp(-E(v,h))/Z$ is trained by minimising the log-likelihood. The gradient involves:

$$\frac{\partial \log p(v)}{\partial W_{ij}} = \mathbb{E}_{\text{data}}[v_i h_j] - \mathbb{E}_{\text{model}}[v_i h_j]$$

The first term is the "positive phase" (clamped visible), the second is the "negative phase" (free-running). Computing $\mathbb{E}_{\text{model}}$ is intractable; contrastive divergence (CD-k) approximates it via $k$ Gibbs steps.

### Restricted Boltzmann Machines
RBMs remove visible-visible and hidden-hidden connections, making the conditional distributions factorised:

$$p(h|v) = \prod_j p(h_j|v), \quad p(v|h) = \prod_i p(v_i|h)$$

This enables efficient Gibbs sampling and CD-k training. Stacked RBMs form deep belief networks, pre-trained layerwise and fine-tuned with backpropagation.

### Hopfield Networks
A Hopfield network is an Ising model with symmetric couplings $J_{ij}$ learned by Hebbian rule:

$$J_{ij} = \frac{1}{N} \sum_{\mu=1}^M \xi_i^\mu \xi_j^\mu$$

where $\xi^\mu$ are stored patterns. The network dynamics $\sigma_i \leftarrow \text{sign}(\sum_j J_{ij} \sigma_j)$ converges to a local minimum of the energy, retrieving stored patterns. The storage capacity is $M_{\max} \approx 0.14 N$ (Amit, Gutfreund, Sompolinsky 1985).

### Energy-Based Models (EBMs)
EBMs generalise the Boltzmann distribution to arbitrary energy functions $E_\theta(x)$:

$$p_\theta(x) = \frac{\exp(-E_\theta(x))}{Z(\theta)}$$

Training uses maximum likelihood (contrastive divergence, score matching) or noise-contrastive estimation. Modern EBMs use neural network parameterisations of $E_\theta$ and are applied to image generation, anomaly detection, and out-of-distribution detection.

## Practical Considerations

### Computing the Partition Function
- Exact: $O(2^N)$ — only feasible for $N \le 30$.
- Approximate: annealing importance sampling, sequential Monte Carlo, or variational bounds.
- Annealed importance sampling (AIS): slowly transform from a tractable distribution to the target, computing the importance weight as a product of ratios.

### Mean-Field Limitations
- Mean-field assumes independence between variables — it underestimates correlations.
- Structured mean-field (e.g., Bethe approximation) captures pairwise correlations.
- Mean-field predictions are exact in infinite-range (fully connected) models but may be qualitatively wrong for low-dimensional systems.

## References
- Baxter, *Exactly Solved Models in Statistical Mechanics*, Academic Press 1982
- Mezard & Montanari, *Information, Physics, and Computation*, Oxford 2009
- Parisi, *Statistical Field Theory*, Addison-Wesley 1988
- Hinton, "Training Products of Experts by Minimizing Contrastive Divergence," *Neural Computation*, 2002
- Hopfield, "Neural Networks and Physical Systems with Emergent Collective Computational Abilities," *PNAS*, 1982
- Amit, Gutfreund, Sompolinsky, "Storing Infinite Numbers of Patterns in a Spin-Glass Model," *Physical Review Letters*, 1985
