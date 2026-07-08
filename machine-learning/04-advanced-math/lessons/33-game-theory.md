# 04.33 Game Theory: Nash Equilibrium and Minimax

## Motivation
Game theory models strategic interactions between agents. In ML, it is central to generative adversarial networks (GANs), multi-agent reinforcement learning, and mechanism design for online platforms. Understanding Nash equilibria, minimax optimisation, and learning in games is essential for training adversarial models and designing multi-agent systems.

## Learning Objectives
- Define normal-form games and Nash equilibrium.
- Apply the minimax theorem to zero-sum games, including GANs.
- Understand learning dynamics in games (gradient descent-ascent, fictitious play).
- Identify potential games and their convergence guarantees.

## Math Foundation

### Normal-Form Games
A finite normal-form game consists of:
- $N$ players, each with action set $A_i$ (size $n_i$).
- A utility function $u_i: A_1 \times \dots \times A_N \to \mathbb{R}$ for each player.

Each player selects a mixed strategy $\sigma_i \in \Delta(A_i)$ (a probability distribution over actions). The expected utility for player $i$ given joint strategy $\sigma = (\sigma_1, \dots, \sigma_N)$ is:

$$u_i(\sigma) = \mathbb{E}_{a \sim \sigma}[u_i(a_1, \dots, a_N)]$$

### Nash Equilibrium
A joint strategy $\sigma^*$ is a Nash equilibrium if no player can improve by deviating unilaterally:

$$u_i(\sigma_i^*, \sigma_{-i}^*) \ge u_i(\sigma_i, \sigma_{-i}^*) \quad \forall \sigma_i \in \Delta(A_i), \forall i$$

Nash's theorem (1950): every finite game has at least one mixed-strategy Nash equilibrium.

### Zero-Sum Games and Minimax
In a two-player zero-sum game, $u_1(a_1, a_2) = -u_2(a_1, a_2)$. The payoff matrix $A$ gives $u_1$. Von Neumann's minimax theorem:

$$\max_{p \in \Delta_m} \min_{q \in \Delta_n} p^\top A q = \min_{q \in \Delta_n} \max_{p \in \Delta_m} p^\top A q = V$$

where $V$ is the value of the game. The optimal mixed strategies $(p^*, q^*)$ are the maximin and minimax strategies, and $V = p^{*\top} A q^*$.

### Solution via Linear Programming
Zero-sum games are equivalent to linear programmes:

$$\max_{p, v} v \quad \text{s.t.} \quad p^\top A \ge v \mathbf{1}^\top, \quad p \ge 0, \quad \sum p_i = 1$$

### Learning in Games
- **Fictitious play**: each player best-responds to the empirical distribution of opponents' past actions. Converges to Nash in zero-sum and potential games.
- **Gradient descent-ascent (GDA)**: $\theta_{t+1} = \theta_t + \eta \nabla_\theta u_1$, $\phi_{t+1} = \phi_t - \eta \nabla_\phi u_2$ (for zero-sum). Can cycle or diverge without modifications.
- **Optimistic GDA**: $\theta_{t+1} = \theta_t + 2\eta \nabla_\theta u_1(\theta_t, \phi_t) - \eta \nabla_\theta u_1(\theta_{t-1}, \phi_{t-1})$ — provably converges for bilinear games.

### Potential Games
A game is a potential game if there exists a potential function $\Phi: A \to \mathbb{R}$ such that:

$$u_i(a_i', a_{-i}) - u_i(a_i, a_{-i}) = \Phi(a_i', a_{-i}) - \Phi(a_i, a_{-i})$$

for all $i$, $a_i$, $a_i'$, $a_{-i}$. In potential games:
- Nash equilibria correspond to local optima of $\Phi$.
- Gradient dynamics converge to Nash equilibria.
- Many congestion games and network games are potential games.

## Python Implementation

```python
import numpy as np

def nash_via_lp(A):
    """Solve zero-sum game via linear programming (simplex method).
    Returns optimal mixed strategy for row player and game value."""
    from scipy.optimize import linprog
    m, n = A.shape
    
    # max v s.t. p^T A >= v, p >= 0, sum p = 1
    # Equivalent: min -v s.t. A^T p - v >= 0, sum p = 1
    c = np.zeros(m + 1)
    c[-1] = -1.0  # -v
    
    # Constraints: A^T p - v >= 0
    A_ub = np.zeros((n, m + 1))
    A_ub[:, :m] = -A.T
    A_ub[:, -1] = 1.0  # v term
    b_ub = np.zeros(n)
    
    # Equality: sum p = 1
    A_eq = np.zeros((1, m + 1))
    A_eq[0, :m] = 1.0
    b_eq = np.array([1.0])
    
    # Bounds
    bounds = [(0, 1)] * m + [(None, None)]  # p_i in [0,1], v unbounded
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    p_opt = result.x[:m]
    v_opt = result.x[-1]
    return p_opt, v_opt

def gradient_descent_ascent(A, n_iters=1000, lr=0.01):
    """Gradient descent-ascent for zero-sum game."""
    m, n = A.shape
    p = np.ones(m) / m
    q = np.ones(n) / n
    
    history = []
    for _ in range(n_iters):
        # Row player: max p^T A q
        grad_p = A @ q
        # Column player: min p^T A q  (so gradient is -A^T p for q)
        grad_q = -A.T @ p
        
        p += lr * grad_p
        q += lr * grad_q
        
        # Project to simplex
        p = np.maximum(p, 0)
        p /= p.sum()
        q = np.maximum(q, 0)
        q /= q.sum()
        
        history.append(p @ A @ q)
    
    return p, q, np.array(history)

# Example: rock-paper-scissors (zero-sum)
A_rps = np.array([[0, -1, 1],
                  [1, 0, -1],
                  [-1, 1, 0]])

p_opt, v_opt = nash_via_lp(A_rps)
print(f"RPS Nash: p = {p_opt.round(3)}, value = {v_opt:.3f}")
print(f"Expected: uniform (1/3 each), value = 0")

# GDA convergence
p_gda, q_gda, vals = gradient_descent_ascent(A_rps, n_iters=500)
print(f"GDA final strategies: p = {p_gda.round(3)}, q = {q_gda.round(3)}")
print(f"GDA final value: {vals[-1]:.4f}")

# GAN-style minimax game
def gan_minimax(d_real, d_fake):
    """Discriminator loss for a GAN (value function)."""
    return np.log(d_real) + np.log(1 - d_fake)

def train_gan_minimax(n_iters=100, lr_d=0.1, lr_g=0.1):
    """Toy GAN minimax game (1D)."""
    # True data distribution: N(0, 1)
    # Generator: produces N(mu, 1)
    # Discriminator: logistic regression on x
    mu = 0.0
    theta = 0.0  # discriminator weight
    
    for t in range(n_iters):
        # Sample real and fake
        x_real = np.random.randn(100)
        x_fake = np.random.randn(100) + mu
        
        # Discriminator gradient (maximise log D(x) + log(1-D(G(z))))
        d_real = 1.0 / (1.0 + np.exp(-theta * x_real))
        d_fake = 1.0 / (1.0 + np.exp(-theta * x_fake))
        grad_d = np.mean(x_real * (1 - d_real)) - np.mean(x_fake * d_fake)
        theta += lr_d * grad_d
        
        # Generator gradient (minimise log(1-D(G(z))) -> maximise log D(G(z)))
        grad_g = np.mean(x_fake * (1 - d_fake))
        mu += lr_g * grad_g
    
    return mu, theta

mu_opt, theta_opt = train_gan_minimax()
print(f"GAN toy: mu = {mu_opt:.3f} (expected 0), theta = {theta_opt:.3f}")
```

## Visualization
Plot the value of a zero-sum game as a function of the row player's mixed strategy for a $2 \times 2$ game — the value function is convex in the row strategy and concave in the column strategy, so the saddle point is the Nash equilibrium. A second panel shows the trajectory of GDA dynamics in strategy space, which may cycle without convergence (e.g., rock-paper-scissors). A third panel shows the payoff matrix of a $3 \times 3$ game with the Nash equilibrium mixed strategy highlighted.

## Connections to Machine Learning

### Generative Adversarial Networks
GAN training is a zero-sum game:

$$\min_G \max_D V(D, G) = \mathbb{E}_{x \sim P_{\text{data}}}[\log D(x)] + \mathbb{E}_{z \sim P_z}[\log(1 - D(G(z)))]$$

The optimal discriminator is $D^*(x) = p_{\text{data}}(x) / (p_{\text{data}}(x) + p_g(x))$, and the minimax solution has $p_g = p_{\text{data}}$ with value $-\log 4$. In practice, GAN training uses non-saturating loss (swap the generator's objective from $\min \log(1-D(G(z)))$ to $\max \log D(G(z))$) to avoid vanishing gradients early in training.

### Multi-Agent Reinforcement Learning
In multi-agent RL, agents interact in a shared environment. Key problems:
- **Self-play**: agents learn by playing against themselves (AlphaGo, AlphaZero).
- **Fictitious play**: each agent best-responds to the empirical distribution of opponents' policies.
- **Mean-field games**: limit of many-agent interactions where each agent experiences the average effect of all others.
- **Potential games**: in cooperative MARL settings, gradient-based learning converges.

### Adversarial Robustness
Robust optimisation against adversarial examples is a zero-sum game:

$$\min_\theta \max_{\|x' - x\| \le \epsilon} \ell(f_\theta(x'), y)$$

The inner maximisation finds the worst-case perturbation; the outer minimisation trains the model to be robust. This is solved by adversarial training (PGD attacks for the inner loop).

### Mechanism Design
In auction design, the seller wants to maximise revenue while agents (bidders) strategically report their values. Myerson's optimal auction uses virtual valuations. ML-based mechanisms (e.g., RegretNet) learn auctions that approximately maximise revenue while satisfying incentive compatibility constraints (truthfulness as a Nash equilibrium).

## Practical Considerations

### Computing Nash Equilibria
- Zero-sum games: solve via LP (polynomial time).
- General-sum games: PPAD-complete (no polynomial algorithm known). Use Lemke-Howson or iterated best response for small games.
- Large games: use fictitious play, multiplicative weights update, or potential function methods.

### GAN Training Instability
- Zero-sum GANs can cycle (rock-paper-scissors dynamics).
- Solutions: optimistic GDA, consensus optimisation, gradient penalty (WGAN-GP), or adding noise to discriminator gradients.
- Potential game structure in some GAN variants (e.g., instance noise) improves convergence.

## References
- Nash, "Non-Cooperative Games," *Annals of Mathematics*, 1951
- Von Neumann & Morgenstern, *Theory of Games and Economic Behavior*, 1944
- Fudenberg & Tirole, *Game Theory*, MIT Press 1991
- Goodfellow et al., "Generative Adversarial Nets," *NeurIPS 2014*
- Daskalakis, Goldberg, Papadimitriou, "The Complexity of Computing a Nash Equilibrium," *SICOMP*, 2009
- Mertikopoulos & Zhou, "Learning in Games with Vanishing Regret," *NeurIPS 2019*
