# 04.24 Symplectic Geometry and Hamiltonian Mechanics

## Motivation
Symplectic geometry is the geometry of phase space in classical mechanics. Its structures — symplectic forms, Poisson brackets, Hamiltonian flows — underpin Hamiltonian Monte Carlo sampling, symplectic integrators, and physics-informed neural networks. Understanding symplectic structure is essential for building energy-preserving models and for sampling from complex probability distributions via Hamiltonian dynamics.

## Learning Objectives
- Define symplectic forms and Hamiltonian vector fields.
- Derive Hamilton's equations from the symplectic form.
- Understand why symplectic integrators (leapfrog) preserve phase-space volume.
- Apply Hamiltonian mechanics to HMC and symplectic neural networks.

## Math Foundation

### Symplectic Form
A symplectic manifold $(M, \omega)$ is an even-dimensional smooth manifold $M^{2n}$ equipped with a closed ($d\omega = 0$) non-degenerate 2-form $\omega$. The standard symplectic form on $\mathbb{R}^{2n}$ with coordinates $(q_1, \dots, q_n, p_1, \dots, p_n)$ is:

$$\omega = \sum_{i=1}^n dq_i \wedge dp_i$$

Non-degeneracy means $\omega(v, \cdot) = 0$ implies $v = 0$, and closedness means $d\omega = 0$.

### Darboux's Theorem
Every symplectic manifold is locally isomorphic to $(\mathbb{R}^{2n}, \omega_{\text{std}})$. This means there are no local invariants in symplectic geometry — only global ones (unlike Riemannian geometry which has curvature). This is why all Hamiltonian systems look the same locally.

### Hamiltonian Vector Fields
Given a smooth function $H: M \to \mathbb{R}$ (the Hamiltonian), the Hamiltonian vector field $X_H$ is defined by:

$$\omega(X_H, \cdot) = dH$$

In coordinates, $X_H = \sum_i \left( \frac{\partial H}{\partial p_i} \frac{\partial}{\partial q_i} - \frac{\partial H}{\partial q_i} \frac{\partial}{\partial p_i} \right)$.

### Hamilton's Equations
The flow of $X_H$ satisfies Hamilton's equations:

$$\dot{q}_i = \frac{\partial H}{\partial p_i}, \quad \dot{p}_i = -\frac{\partial H}{\partial q_i}$$

These are the equations of motion for any Hamiltonian system.

### Poisson Bracket
The Poisson bracket of two functions $F, G: M \to \mathbb{R}$ is:

$$\{F, G\} = \omega(X_F, X_G) = \sum_{i=1}^n \left( \frac{\partial F}{\partial q_i} \frac{\partial G}{\partial p_i} - \frac{\partial F}{\partial p_i} \frac{\partial G}{\partial q_i} \right)$$

Properties: bilinear, anti-symmetric, satisfies the Jacobi identity, and $\frac{dF}{dt} = \{F, H\}$. In particular, $\{q_i, q_j\} = \{p_i, p_j\} = 0$ and $\{q_i, p_j\} = \delta_{ij}$.

### Liouville's Theorem
The Hamiltonian flow preserves the phase-space volume form $\omega^n = \omega \wedge \dots \wedge \omega$ (the $n$-fold wedge product). Equivalently, the flow is divergence-free:

$$\nabla \cdot X_H = \sum_i \left( \frac{\partial}{\partial q_i} \frac{\partial H}{\partial p_i} + \frac{\partial}{\partial p_i} \left( -\frac{\partial H}{\partial q_i} \right) \right) = 0$$

This is the reason HMC can propose far-away states with high acceptance probability — it is a symplectic integrator that preserves volume.

### Symplectic Integrators
The leapfrog (Stormer–Verlet) integrator is symplectic:

1. $p(t + \epsilon/2) = p(t) - \frac{\epsilon}{2} \nabla_q H(q(t), p(t + \epsilon/2))$
2. $q(t + \epsilon) = q(t) + \epsilon \nabla_p H(q(t), p(t + \epsilon/2))$
3. $p(t + \epsilon) = p(t + \epsilon/2) - \frac{\epsilon}{2} \nabla_q H(q(t + \epsilon), p(t + \epsilon/2))$

This integrator exactly conserves a perturbed Hamiltonian $\tilde{H} = H + O(\epsilon^2)$, ensuring long-term stability.

## Python Implementation

```python
import numpy as np

def hamiltonian(position, momentum, potential_fn, kinetic_fn=None):
    """Total energy H = K + U."""
    K = kinetic_fn(momentum) if kinetic_fn else 0.5 * np.sum(momentum**2)
    U = potential_fn(position)
    return K + U

def hamiltonian_flow(potential_grad_fn, n_steps=100, dt=0.01, q0=None, p0=None):
    """Integrate Hamiltonian dynamics via leapfrog."""
    dim = len(q0)
    q = q0.copy()
    p = p0.copy()
    trajectory = [q.copy()]
    
    for _ in range(n_steps):
        p -= 0.5 * dt * potential_grad_fn(q)
        q += dt * p
        p -= 0.5 * dt * potential_grad_fn(q)
        trajectory.append(q.copy())
    
    return np.array(trajectory)

def poisson_bracket(F, G, q, p, eps=1e-6):
    """Approximate Poisson bracket via finite differences.
    F, G are functions of (q, p)."""
    dim = len(q)
    bracket = 0.0
    for i in range(dim):
        # partial F / partial q_i
        dq = np.zeros(dim); dq[i] = eps
        dF_dq = (F(q + dq, p) - F(q - dq, p)) / (2 * eps)
        # partial G / partial p_i
        dp = np.zeros(dim); dp[i] = eps
        dG_dp = (G(q, p + dp) - G(q, p - dp)) / (2 * eps)
        bracket += dF_dq * dG_dp
        
        # partial F / partial p_i
        dF_dp = (F(q, p + dp) - F(q, p - dp)) / (2 * eps)
        dG_dq = (G(q + dq, p) - G(q - dq, p)) / (2 * eps)
        bracket -= dF_dp * dG_dq
    
    return bracket

# Example: 1D harmonic oscillator H = p^2/2 + q^2/2
potential = lambda q: 0.5 * q**2
potential_grad = lambda q: q
kinetic = lambda p: 0.5 * p**2

# Integrate
q0, p0 = np.array([1.0]), np.array([0.0])
traj = hamiltonian_flow(potential_grad, n_steps=500, dt=0.05, q0=q0, p0=p0)

# Check energy conservation
energies = [hamiltonian(traj[i], -np.diff(traj[:i+1], axis=0).sum(axis=0), potential, kinetic) 
            for i in range(0, len(traj), 50)]
H0 = hamiltonian(q0, p0, potential, kinetic)
print(f"Initial energy: {H0:.4f}")
print(f"Energy drift over 500 steps: {(energies[-1] - H0) if len(energies) > 1 else 0:.2e}")
```

## Visualization
Plot the phase-space trajectory of the harmonic oscillator — it follows an ellipse (constant energy). The symplectic integrator keeps the trajectory on the ellipse even after thousands of steps, while a non-symplectic Euler method would spiral outward (energy increases). A second panel shows the energy drift explicitly: leapfrog oscillates around the true energy with bounded error; Euler's method has secular drift.

## Connections to Machine Learning

### Hamiltonian Monte Carlo
HMC uses Hamiltonian dynamics to propose new states in MCMC:
1. Sample momentum $p \sim \mathcal{N}(0, M)$.
2. Integrate Hamiltonian dynamics for $L$ leapfrog steps.
3. Accept/reject with Metropolis probability $\min(1, \exp(-H(q',p') + H(q,p)))$.

The symplectic nature of leapfrog ensures high acceptance rates even for large $L$, enabling efficient exploration of high-dimensional posteriors.

### Symplectic Neural Networks
Symplectic ODE-Nets and Hamiltonian Neural Networks (HNNs) learn the Hamiltonian $H_\theta(q,p)$ from trajectory data:

$$\mathcal{L} = \mathbb{E}_{(q,p) \sim \text{data}} \left[ \left\| \frac{\partial H_\theta}{\partial p} - \dot{q} \right\|^2 + \left\| -\frac{\partial H_\theta}{\partial q} - \dot{p} \right\|^2 \right]$$

The learned dynamics are then integrated with a symplectic integrator, guaranteeing long-term energy conservation even for imperfectly learned Hamiltonians. Applications include modelling physical systems (pendula, celestial mechanics, fluid dynamics) from observations.

### Physics-Informed Neural Networks (PINNs)
PINNs can enforce Hamiltonian structure as a PDE constraint:

$$\mathcal{L} = \mathcal{L}_{\text{data}} + \lambda \left\| \frac{\partial u}{\partial t} - \{u, H\} \right\|^2$$

where $u(q,p,t)$ is the solution field. The symplectic constraint ensures the predicted dynamics respect phase-space conservation.

### Lagrangian and Hamiltonian Neural ODEs
- **Lagrangian NODE**: learn the Lagrangian $L(q, \dot{q})$ and derive equations via Euler-Lagrange.
- **Hamiltonian NODE**: learn $H(q,p)$ directly. The Hamiltonian formulation is preferred because it works in first-order form and naturally separates kinetic and potential energies.

## Practical Considerations

### Symplectic Integration in ML
- Use leapfrog (Stormer–Verlet) as the default integrator for any Hamiltonian-like system.
- The choice of step size $\epsilon$ and number of steps $L$ controls the exploration-exploitation trade-off in HMC: large $\epsilon$ reduces acceptance; small $\epsilon$ requires more steps.
- For non-separable Hamiltonians $H(q,p)$ where $\partial H/\partial p$ depends on $q$, use implicit symplectic integrators (e.g., the generalised leapfrog via fixed-point iteration).

### Checking Symplecticity
- Monitor the energy drift $\Delta H / H_0$ over integration time — it should be bounded without secular trend.
- Monitor the volume preservation: the determinant of the Jacobian of the integrator step should be 1 (to machine precision).

## References
- da Silva, *Lectures on Symplectic Geometry*, Springer 2008
- Hairer, Lubich & Wanner, *Geometric Numerical Integration*, 2nd ed., Springer 2006
- Marsden & Ratiu, *Introduction to Mechanics and Symmetry*, 2nd ed., Springer 1999
- Greydanus, Dzamba, Yosinski, "Hamiltonian Neural Networks," *NeurIPS 2019*
- Neal, "MCMC Using Hamiltonian Dynamics," in *Handbook of MCMC*, CRC 2011
- Betancourt, "A Conceptual Introduction to Hamiltonian Monte Carlo," *arXiv:1701.02434*, 2017
