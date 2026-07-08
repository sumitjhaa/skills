# 04.11 Markov Chains and Stationary Distributions

## Motivation
Markov chains model sequential dependence where the future depends only on the present. They are the backbone of MCMC sampling, reinforcement learning (MDPs), stochastic optimisation, and PageRank. Understanding their convergence properties — ergodicity, mixing times, and spectral gaps — is essential for designing efficient sampling and learning algorithms.

## Learning Objectives
- Define discrete-time and continuous-time Markov chains and their transition kernels.
- Characterise stationary distributions, detailed balance, and reversibility.
- Compute mixing times from the spectral gap.
- Apply Markov chain theory to MCMC, RL, and PageRank.

## Math Foundation

### Discrete-Time Markov Chains
A sequence of random variables $\{X_t\}_{t \ge 0}$ on state space $\Omega$ is a Markov chain if:

$$\Pr(X_{t+1} = y | X_t = x, X_{t-1}, \dots, X_0) = \Pr(X_{t+1} = y | X_t = x)$$

The chain is time-homogeneous if the transition probabilities $P(x,y) = \Pr(X_{t+1} = y | X_t = x)$ do not depend on $t$.

### Transition Matrix and $n$-Step Transitions
For a finite chain of size $m$, $P$ is an $m \times m$ stochastic matrix (rows sum to 1). The $n$-step transition matrix is $P^n$, where $P^n(x,y) = \Pr(X_n = y | X_0 = x)$.

### Stationary Distribution
A distribution $\pi$ over $\Omega$ is stationary if:

$$\pi P = \pi, \quad \text{i.e.,} \quad \pi(y) = \sum_{x \in \Omega} \pi(x) P(x,y) \ \forall y$$

If a chain is irreducible (every state reachable from every other) and aperiodic (gcd of return times = 1), it converges to a unique stationary distribution:

$$\lim_{n \to \infty} P^n(x, \cdot) = \pi(\cdot) \ \text{for any initial state } x$$

### Detailed Balance and Reversibility
A chain is reversible with respect to $\pi$ if it satisfies detailed balance:

$$\pi(x) P(x,y) = \pi(y) P(y,x) \quad \forall x,y$$

Detailed balance is sufficient (but not necessary) for $\pi$ to be stationary. Reversible chains have self-adjoint transition operators in the $\pi$-weighted $L^2$ space, enabling spectral analysis.

## Spectral Analysis and Mixing Time

### Eigenvalues and Spectral Gap
For a reversible chain, the eigenvalues of $P$ satisfy $1 = \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_m \ge -1$. The spectral gap is:

$$\gamma = 1 - \lambda_2$$

The relaxation time is $t_{\text{rel}} = 1/\gamma$. The chain mixes in $O(t_{\text{rel}} \log(1/\pi_{\text{min}}))$ steps, where $\pi_{\text{min}} = \min_x \pi(x)$.

### Mixing Time
The $L^1$ mixing time (total variation) is:

$$t_{\text{mix}}(\epsilon) = \min \{ t : \max_x \|P^t(x,\cdot) - \pi\|_{\text{TV}} \le \epsilon \}$$

For reversible chains:

$$t_{\text{mix}}(\epsilon) \le \frac{1}{\gamma} \log\left( \frac{1}{\epsilon \sqrt{\pi_{\text{min}}}} \right)$$

### Continuous-Time Markov Chains
A continuous-time chain has a generator $L$ where:

$$L f(x) = \sum_{y \ne x} Q(x,y) (f(y) - f(x))$$

and $Q(x,y)$ are transition rates. The transition probabilities evolve via the Kolmogorov forward equation:

$$\frac{d}{dt} P_t = P_t L, \quad P_t = e^{tL}$$

## Python Implementation

```python
import numpy as np

def stationary_distribution(P):
    """Compute stationary distribution via eigenvector of P^T."""
    eigenvalues, eigenvectors = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])
    pi = pi / pi.sum()
    return pi

def spectral_gap(P):
    """Spectral gap for a reversible chain."""
    eigenvalues = np.linalg.eigvalsh(P)  # eigenvalues sorted ascending
    eigenvalues = eigenvalues[::-1]  # descending
    if len(eigenvalues) > 1:
        return 1.0 - eigenvalues[1]
    return 0.0

def mixing_time_bound(P, eps=0.05):
    """Upper bound on epsilon-mixing time via spectral gap."""
    pi = stationary_distribution(P)
    gap = spectral_gap(P)
    pi_min = pi.min()
    if gap <= 0:
        return float('inf')
    return int(np.ceil(1.0 / gap * np.log(1.0 / (eps * np.sqrt(pi_min)))))

def metropolis_chain(target, n_states, n_steps=10000):
    """Build a Metropolis-Hastings transition matrix.
    target: array of unnormalized target probabilities."""
    P = np.zeros((n_states, n_states))
    for i in range(n_states):
        # propose neighbor uniformly (wrap around for simplicity)
        neighbors = [(i - 1) % n_states, (i + 1) % n_states]
        for j in neighbors:
            alpha = min(1.0, target[j] / target[i])
            P[i, j] = alpha / 2.0  # 1/2 for choosing each neighbor
        P[i, i] = 1.0 - P[i].sum()
    return P

# Example: 5-state chain with bimodal target distribution
target = np.array([2, 1, 10, 10, 1])
P = metropolis_chain(target, 5)
pi_empirical = stationary_distribution(P)
print("Stationary distribution:", pi_empirical)
print("Normalized target:", target / target.sum())
print(f"Spectral gap: {spectral_gap(P):.4f}")
print(f"Mixing time bound (eps=0.05): {mixing_time_bound(P)} steps")
```

## Visualization
Plot the transition graph of a 5-state chain (directed edges with probabilities). A second panel shows the convergence of $L^1(\mu_t, \pi)$ from a far-away initial distribution (e.g., all mass at state 0) — the exponential decay rate equals the spectral gap. For a larger chain (100 states), plot the eigenvectors corresponding to the top eigenvalues: the second eigenvector shows the slowest-mixing mode (often a bottleneck between two high-probability regions).

## Connections to Machine Learning

### Markov Chain Monte Carlo
MCMC methods rely on the ergodic theorem for Markov chains:

$$\frac{1}{T} \sum_{t=1}^T f(X_t) \xrightarrow{a.s.} \mathbb{E}_\pi[f]$$

The efficiency of MCMC is determined by the mixing time — chains with small spectral gaps require many steps between independent samples. The effective sample size (ESS) is $N / (1 + 2 \sum_{k=1}^\infty \rho_k)$ where $\rho_k$ is the autocorrelation at lag $k$.

### Reinforcement Learning
Markov decision processes extend Markov chains with actions and rewards. The Bellman equation:

$$V^\pi(s) = \mathbb{E}[R + \gamma V^\pi(s') | s, \pi]$$

is a linear system of equations whose solution is the value function. Policy evaluation iterates $V_{k+1} = T^\pi V_k$ where $T^\pi$ is the Bellman operator — a contraction with modulus $\gamma < 1$ (guaranteeing convergence).

### PageRank
PageRank is the stationary distribution of a Markov chain on the web graph:

$$P(i,j) = \alpha \frac{1}{\text{deg}(i)} + (1-\alpha) \frac{1}{n}$$

where $\alpha = 0.85$ is the teleportation probability. The random surfer moves to a random outgoing link with probability $\alpha$ or jumps to a random page with probability $1-\alpha$, ensuring irreducibility and aperiodicity.

### Hidden Markov Models
HMMs are Markov chains on latent states $z_t$ with emissions $x_t \sim p(x_t | z_t)$. The forward-backward algorithm computes marginal posteriors $p(z_t | x_{1:T})$ using dynamic programming on the Markov chain structure.

## Practical Considerations

### Checking Convergence
- **Gelman–Rubin $\hat{R}$**: run multiple chains from overdispersed starting points; $\hat{R} \approx 1$ indicates convergence.
- **Geweke test**: compare the mean of the first 10% and last 50% of the chain; significant differences indicate non-stationarity.
- **Effective sample size**: ESS $< N/10$ suggests poor mixing — consider thinning or reparameterisation.

### Diagnosing Slow Mixing
- High autocorrelation in trace plots suggests a small spectral gap.
- Visualise the second eigenvector of the transition matrix to identify bottlenecks.
- For continuous chains, use the potential scale reduction factor.

### Improving Mixing
- **Reparameterisation**: centre and orthogonalise parameters (e.g., non-centred parameterisation for hierarchical models).
- **Auxiliary variables**: introduce extra variables to break dependencies (e.g., slice sampling, Hamiltonian Monte Carlo).
- **Parallel tempering**: run multiple chains at different temperatures and swap states.

## References
- Levin & Peres, *Markov Chains and Mixing Times*, AMS 2017
- Brémaud, *Markov Chains: Gibbs Fields, Monte Carlo Simulation, and Queues*, Springer 1999
- Gelman et al., *Bayesian Data Analysis*, 3rd ed., CRC Press 2013
- Page et al., "The PageRank Citation Ranking: Bringing Order to the Web," 1999
- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press 2018
