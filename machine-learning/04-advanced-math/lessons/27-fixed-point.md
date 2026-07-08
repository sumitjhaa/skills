# 04.27 Fixed Point Theorems (Banach, Brouwer, Kakutani)

## Motivation
Fixed point theorems guarantee existence of solutions to equations of the form $x = T(x)$. They underpin equilibrium proofs in game theory, convergence of iterative algorithms, and the existence of solutions to differential equations and optimal transport. In ML, fixed point arguments prove convergence of value iteration in RL, EM algorithms, and the existence of equilibria in GAN training.

## Learning Objectives
- State and prove the Banach fixed point theorem with error bounds.
- Understand Brouwer's fixed point theorem and its consequences.
- Apply Kakutani's theorem to existence of Nash equilibria.
- Connect fixed point theory to iterative ML algorithms.

## Math Foundation

### Banach Fixed Point Theorem (Contraction Mapping Principle)
Let $(X, d)$ be a complete metric space and $T: X \to X$ a contraction: there exists $\alpha \in [0,1)$ such that:

$$d(Tx, Ty) \le \alpha \, d(x, y) \quad \forall x, y \in X$$

Then:
1. $T$ has a unique fixed point $x^* = Tx^*$.
2. For any starting point $x_0$, the iterates $x_{n+1} = Tx_n$ converge to $x^*$.
3. Convergence is geometric: $d(x_n, x^*) \le \frac{\alpha^n}{1-\alpha} d(x_1, x_0)$.

### Proof Sketch
1. Show $\{x_n\}$ is Cauchy: $d(x_{n+1}, x_n) \le \alpha^n d(x_1, x_0)$.
2. By completeness, $x_n \to x^*$.
3. Continuity of $T$ gives $x^* = \lim x_{n+1} = \lim Tx_n = Tx^*$.
4. Uniqueness: if $x^*$ and $y^*$ are fixed points, $d(x^*, y^*) = d(Tx^*, Ty^*) \le \alpha d(x^*, y^*)$ so $d = 0$.

### Brouwer Fixed Point Theorem
Every continuous function $f: B^n \to B^n$ (from the closed unit ball in $\mathbb{R}^n$ to itself) has a fixed point.

The theorem is equivalent to:
- The hairy ball theorem: there is no continuous non-vanishing tangent vector field on $S^{2n}$.
- The Borsuk–Ulam theorem: for continuous $f: S^n \to \mathbb{R}^n$, there exists $x$ with $f(x) = f(-x)$.
- No retraction: there is no continuous map $r: B^n \to S^{n-1}$ with $r|_{S^{n-1}} = \text{id}$.

### Kakutani Fixed Point Theorem
Let $C \subseteq \mathbb{R}^n$ be compact and convex. Let $F: C \to 2^C$ be an upper hemicontinuous set-valued map with non-empty compact convex values. Then $F$ has a fixed point: there exists $x \in C$ such that $x \in F(x)$.

Kakutani generalises Brouwer to correspondences (set-valued maps). It is used to prove the existence of Nash equilibria in mixed strategies.

### Schauder Fixed Point Theorem
For a Banach space $X$, let $C \subseteq X$ be compact and convex. Every continuous $T: C \to C$ has a fixed point. This generalises Brouwer to infinite dimensions but requires compactness of $C$ (or compactness of $T$).

## Python Implementation

```python
import numpy as np

def banach_iteration(T, x0, tol=1e-10, max_iter=1000):
    """Find fixed point of contraction T via iteration."""
    x = x0
    for i in range(max_iter):
        x_new = T(x)
        if np.linalg.norm(x_new - x) < tol:
            return x_new, i + 1
        x = x_new
    return x, max_iter

def bellman_operator(V, P, R, gamma=0.9):
    """Bellman operator for a finite MDP: (TV)(s) = max_a [R(s,a) + gamma * sum P(s'|s,a) V(s')]"""
    n_states, n_actions = P.shape[0], P.shape[2] if P.ndim == 3 else 1
    TV = np.zeros(n_states)
    for s in range(n_states):
        q_values = np.zeros(n_actions)
        for a in range(n_actions):
            q_values[a] = R[s, a] + gamma * np.sum(P[s, a, :] * V)
        TV[s] = np.max(q_values)
    return TV

def value_iteration(P, R, gamma=0.9, tol=1e-6):
    """Value iteration via Banach fixed point (Bellman operator is gamma-contraction)."""
    n = P.shape[0]
    V = np.zeros(n)
    for i in range(1000):
        TV = bellman_operator(V, P, R, gamma)
        if np.max(np.abs(TV - V)) < tol:
            return TV, i + 1
        V = TV
    return V, 1000

def brouwer_naive(f, n_grid=20):
    """Approximate Brouwer fixed point via grid search on [0,1]^2.
    Only for 2D — for demonstration."""
    grid = np.linspace(0, 1, n_grid)
    for x in grid:
        for y in grid:
            p = np.array([x, y])
            fp = f(p)
            if np.linalg.norm(fp - p) < 0.05:
                return p, fp
    return None, None

# Example: value iteration for a simple MDP
# 2 states, 2 actions
P = np.zeros((2, 2, 2))  # (state, action, next_state)
P[0, 0] = [0.7, 0.3]
P[0, 1] = [0.4, 0.6]
P[1, 0] = [0.5, 0.5]
P[1, 1] = [0.2, 0.8]
R = np.array([[1.0, 0.5], [0.0, -0.5]])  # (state, action)

V_opt, n_iter = value_iteration(P, R)
print(f"Optimal value function: {V_opt}")
print(f"Converged in {n_iter} iterations")

# Verify: V should satisfy V = TV
TV = bellman_operator(V_opt, P, R)
print(f"Bellman residual: {np.max(np.abs(TV - V_opt)):.2e}")
```

## Visualization
Plot the convergence of Banach iteration for a 1D contraction: show the iterates $x_n$ converging geometrically to $x^*$, with the contraction factor $\alpha$ controlling the slope of $|x_{n+1} - x^*|$ vs $|x_n - x^*|$. A second panel shows the Brouwer fixed point for a function $f: [0,1]^2 \to [0,1]^2$ — the 45-degree line $f(x)=x$ intersects the graph. A third panel shows the Bellman operator as a contraction in sup-norm, with value iteration tracing a path through value function space.

## Connections to Machine Learning

### Value Iteration in Reinforcement Learning
The Bellman optimality operator $T^*$ is a $\gamma$-contraction in the sup-norm:

$$\|T^* V_1 - T^* V_2\|_\infty \le \gamma \|V_1 - V_2\|_\infty$$

By Banach's theorem, value iteration converges geometrically to the unique optimal value function $V^*$, and the error after $k$ iterations is bounded by $\gamma^k / (1-\gamma)$ times the initial Bellman error.

### EM Algorithm as a Fixed Point
The EM algorithm defines a map $M: \theta \mapsto \theta'$ where:

$$\theta' = \arg\max_\theta \mathbb{E}_{q(z|x,\theta)}[\log p(x,z|\theta)]$$

The EM map is monotonic (the ELBO increases at each step) and its fixed points are stationary points of the log-likelihood. Under regularity conditions (compact parameter space, identifiability), EM converges to a local maximum.

### GANs and Game Theory
GAN training is a zero-sum game between generator $G$ and discriminator $D$ with value:

$$\min_G \max_D V(D, G)$$

Kakutani's theorem guarantees the existence of a Nash equilibrium in mixed strategies. In practice, GAN training seeks a fixed point of the gradient descent-ascent dynamics, though convergence is not guaranteed as contraction requires convex-concave structure.

### Neural ODEs and the Picard–Lindelöf Theorem
The initial value problem $\dot{x} = f(x,t)$, $x(0) = x_0$ is equivalent to the fixed point equation:

$$x(t) = x_0 + \int_0^t f(x(s), s) ds$$

The Picard operator $Tx(t) = x_0 + \int_0^t f(x(s), s) ds$ is a contraction on $C([0,T])$ with the sup-norm for sufficiently small $T$, provided $f$ is Lipschitz. This guarantees existence and uniqueness of solutions to neural ODEs.

## Practical Considerations

### Checking Contraction
- A linear map is a contraction if its spectral radius $\rho(T) < 1$.
- The Bellman operator is a contraction with modulus $\gamma$ (discount factor).
- Gradient descent on a strongly convex function is a contraction: the map $x \mapsto x - \eta \nabla f(x)$ has Lipschitz constant $|1 - \eta \mu|$ where $\mu$ is the strong convexity modulus.

### When Fixed Point Theorems Fail
- Non-contractive maps can have chaotic dynamics (e.g., logistic map $x_{n+1} = 4x_n(1-x_n)$).
- Brouwer requires convexity: a rotation of the annulus has no fixed point.
- In infinite dimensions, Schauder requires compactness: the identity map on the unit ball of an infinite-dimensional Hilbert space has no fixed point (Riesz lemma).

## References
- Granas & Dugundji, *Fixed Point Theory*, Springer 2003
- Border, *Fixed Point Theorems with Applications to Economics and Game Theory*, Cambridge 1985
- Agarwal, Meehan, O'Regan, *Fixed Point Theory and Applications*, Cambridge 2001
- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press 2018
- Dempster, Laird, Rubin, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B*, 1977
