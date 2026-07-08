"""04.24 Symplectic geometry and Hamiltonian mechanics."""
import numpy as np
import matplotlib.pyplot as plt

def symplectic_matrix(n):
    return np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])

def hamiltonian_system(grad_H, q0, p0, T=10.0, dt=0.01):
    n_steps = int(T / dt)
    q, p = np.copy(q0), np.copy(p0)
    traj = np.zeros((n_steps + 1, 2))
    traj[0] = np.array([q.item(), p.item()])
    for i in range(n_steps):
        dq, dp = grad_H(q, p)
        q_half = q + 0.5 * dt * dp
        dq2, dp2 = grad_H(q_half, p)
        p_new = p - dt * dq2
        dq3, dp3 = grad_H(q_half, p_new)
        q_new = q_half + 0.5 * dt * dp3
        q, p = q_new, p_new
        traj[i+1] = np.array([q.item(), p.item()])
    return traj

def simple_pendulum_H(q, p):
    return 0.5 * p**2 - np.cos(q)

def simple_pendulum_grad(q, p):
    return -np.sin(q), p

def harmonic_H(q, p):
    return 0.5 * (p**2 + q**2)

def harmonic_grad(q, p):
    return q, p

np.random.seed(42)
dt = 0.05
T = 20.0
traj_pend = hamiltonian_system(simple_pendulum_grad,
                                np.array([0.5]), np.array([0.0]), T, dt)

traj_harm = hamiltonian_system(harmonic_grad,
                                np.array([1.0]), np.array([0.0]), T, dt)

energies_pend = [simple_pendulum_H(t[0], t[1]) for t in traj_pend]
energies_harm = [harmonic_H(t[0], t[1]) for t in traj_harm]

J = symplectic_matrix(1)

n_grid = 20
Q = np.linspace(-np.pi, np.pi, n_grid)
P = np.linspace(-2, 2, n_grid)
H_grid = np.zeros((n_grid, n_grid))
for i in range(n_grid):
    for j in range(n_grid):
        H_grid[i, j] = simple_pendulum_H(Q[i], P[j])

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

contour = axes[0, 0].contourf(Q, P, H_grid.T, levels=20, cmap="viridis")
plt.colorbar(contour, ax=axes[0, 0])
axes[0, 0].plot(traj_pend[:, 0], traj_pend[:, 1], "r-", lw=1.5, label="Trajectory")
axes[0, 0].set_xlabel("q (position)")
axes[0, 0].set_ylabel("p (momentum)")
axes[0, 0].set_title("Pendulum Phase Space\nH = p²/2 - cos(q)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(traj_pend[:500, 0], "b-", lw=1.5, label="q(t)")
axes[0, 1].plot(traj_pend[:500, 1], "r-", lw=1.5, label="p(t)")
axes[0, 1].set_xlabel("Time step")
axes[0, 1].set_ylabel("State")
axes[0, 1].set_title("Pendulum Evolution")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

rel_energy_error = np.abs(energies_pend - energies_pend[0]) / np.abs(energies_pend[0] + 1e-10)
axes[0, 2].semilogy(rel_energy_error, "b-", lw=1.5)
axes[0, 2].set_xlabel("Time step")
axes[0, 2].set_ylabel("|ΔE/E₀|")
axes[0, 2].set_title("Energy Conservation\n(Störmer-Verlet)")
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(traj_harm[:, 0], traj_harm[:, 1], "g-", lw=1.5, label="Harmonic")
theta = np.linspace(0, 2*np.pi, 100)
axes[1, 0].plot(np.cos(theta), np.sin(theta), "k--", alpha=0.5, label="E=const")
axes[1, 0].set_xlabel("q")
axes[1, 0].set_ylabel("p")
axes[1, 0].set_title("Harmonic Oscillator\nExact symplectic integration")
axes[1, 0].axis("equal")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

dts = np.logspace(-2, 0, 15)
energy_errors = []
for d in dts:
    traj = hamiltonian_system(simple_pendulum_grad,
                               np.array([0.5]), np.array([0.0]), T=5.0, dt=d)
    energies = [simple_pendulum_H(t[0], t[1]) for t in traj]
    max_err = np.max(np.abs(energies - energies[0]) / np.abs(energies[0] + 1e-10))
    energy_errors.append(max_err)
axes[1, 1].loglog(dts, energy_errors, "o-", lw=2, label="Symplectic Euler")
axes[1, 1].loglog(dts, dts**2, "--", lw=2, label="O(dt²)")
axes[1, 1].set_xlabel("dt")
axes[1, 1].set_ylabel("Max |ΔE/E₀|")
axes[1, 1].set_title("Energy Error vs Step Size")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

J_2 = symplectic_matrix(2)
axes[1, 2].imshow(J_2, cmap="RdBu", interpolation="nearest")
for i in range(4):
    for j in range(4):
        val = f"{J_2[i, j]:.0f}"
        if J_2[i, j] != 0:
            axes[1, 2].text(j, i, val, ha="center", va="center", color="white", fontsize=12)
        else:
            axes[1, 2].text(j, i, val, ha="center", va="center", color="gray", fontsize=8)
axes[1, 2].set_xticks(range(4))
axes[1, 2].set_yticks(range(4))
axes[1, 2].set_xticklabels(["q₁", "q₂", "p₁", "p₂"])
axes[1, 2].set_yticklabels(["q₁", "q₂", "p₁", "p₂"])
axes[1, 2].set_title("Symplectic Matrix J\nJᵀ = -J, J² = -I")
plt.colorbar(axes[1, 2].images[0], ax=axes[1, 2])

plt.tight_layout()
plt.savefig("../../assets/phase04/24-symplectic-geometry.png")
plt.close()

print("=" * 60)
print("SYMPLECTIC GEOMETRY")
print("=" * 60)
print(f"\nPendulum (Störmer-Verlet integrator, dt={dt}):")
print(f"  Mean energy: {np.mean(energies_pend):.6f}")
print(f"  Energy drift: {np.max(energies_pend) - np.min(energies_pend):.6f}")

print(f"\nHarmonic Oscillator:")
print(f"  Mean energy: {np.mean(energies_harm):.6f}")
print(f"  Energy drift: {np.max(energies_harm) - np.min(energies_harm):.6f}")

print(f"\nSymplectic properties:")
print(f"  Jᵀ = -J (skew-symmetric)")
print(f"  J² = -I (almost complex structure)")
print(f"  ω(u,v) = uᵀJv (symplectic form)")
print(f"  Phase space volume preserved (Liouville's theorem)")

print(f"\nSymplectic Euler (Störmer-Verlet):")
print(f"  • Second-order accurate (O(dt²) energy error)")
print(f"  • Exactly symplectic (preserves J structure)")
print(f"  • Long-time energy stability")
print(f"  • Time-reversible")
