"""04.27 Fixed-point theory: Banach, Brouwer, Kakutani."""
import numpy as np
import matplotlib.pyplot as plt

def banach_fixed_point(f, x0=0.0, tol=1e-10, max_iter=100):
    x = x0
    trajectory = [x]
    for _ in range(max_iter):
        x_new = f(x)
        trajectory.append(x_new)
        if abs(x_new - x) < tol:
            break
        x = x_new
    return x, trajectory

def contraction_mapping(c, x0=0.0, n_iter=30):
    f = lambda x: c * np.sin(x)
    return banach_fixed_point(f, x0, tol=1e-12, max_iter=n_iter)

def value_iteration(P, R, gamma=0.9, tol=1e-6, max_iter=100):
    n_states = P.shape[0]
    V = np.zeros(n_states)
    history = [V.copy()]
    for _ in range(max_iter):
        V_new = np.zeros(n_states)
        for s in range(n_states):
            V_new[s] = R[s] + gamma * np.max(P @ V)
        history.append(V_new.copy())
        if np.max(np.abs(V_new - V)) < tol:
            break
        V = V_new
    return V, history

np.random.seed(42)

for c in [0.3, 0.8, -0.5]:
    x_fp, traj = contraction_mapping(c, 0.5)
    print(f"c={c}: FP={x_fp:.6f}, iter={len(traj)}")

x_sin_fp, traj_sin = banach_fixed_point(lambda x: 0.5*np.sin(x), 1.0)
x_cos_fp, traj_cos = banach_fixed_point(lambda x: np.cos(x), 0.5)
x_lin_fp, traj_lin = banach_fixed_point(lambda x: 0.5*x + 0.5, 0.0)

P = np.array([[0.6, 0.4], [0.3, 0.7]])
R = np.array([1.0, 0.5])
V_opt, V_history = value_iteration(P, R, gamma=0.95, tol=1e-6)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xs = np.linspace(-2, 2, 200)
for c, color, label in [(0.3, "blue", "c=0.3"), (0.8, "red", "c=0.8"),
                         (-0.5, "green", "c=-0.5")]:
    axes[0, 0].plot(xs, c * np.sin(xs), color=color, lw=2, label=label)
axes[0, 0].plot(xs, xs, "k--", lw=1, label="f(x)=x")
for c in [0.3, 0.8, -0.5]:
    fp, _ = contraction_mapping(c, 0.5)
    axes[0, 0].plot(fp, fp, "o", ms=8, color="k")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("f(x) = c·sin(x)")
axes[0, 0].set_title("Contraction Mappings\n|c| < 1 → unique fixed point")
axes[0, 0].legend(loc="upper left")
axes[0, 0].grid(True, alpha=0.3)

for c, traj in [(0.3, traj_sin), (0.8, traj_cos), (-0.5, traj_lin)]:
    pass
axes[0, 1].plot(range(len(traj_sin)), traj_sin, "o-", lw=2, label=f"0.5·sin(x)")
axes[0, 1].plot(range(len(traj_cos)), traj_cos, "s-", lw=2, label="cos(x)")
axes[0, 1].plot(range(len(traj_lin)), traj_lin, "^-", lw=2, label="0.5x+0.5")
axes[0, 1].axhline(x_sin_fp, color="blue", ls="--", alpha=0.3)
axes[0, 1].axhline(x_cos_fp, color="red", ls="--", alpha=0.3)
axes[0, 1].axhline(x_lin_fp, color="green", ls="--", alpha=0.3)
axes[0, 1].set_xlabel("Iteration")
axes[0, 1].set_ylabel("x_k")
axes[0, 1].set_title("Convergence of Fixed Point Iteration")
axes[0, 1].set_yscale("symlog")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].step(range(len(V_history)), [v[0] for v in V_history], "b-", lw=2, label="V(s₀)")
axes[0, 2].step(range(len(V_history)), [v[1] for v in V_history], "r-", lw=2, label="V(s₁)")
axes[0, 2].axhline(V_opt[0], color="blue", ls="--", alpha=0.5)
axes[0, 2].axhline(V_opt[1], color="red", ls="--", alpha=0.5)
axes[0, 2].set_xlabel("Iteration")
axes[0, 2].set_ylabel("Value V(s)")
axes[0, 2].set_title("Value Iteration (Bellman Op.)\nContraction in L∞")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

n_range = np.arange(1, 30)
rates = []
for n_its in n_range:
    _, traj_n = banach_fixed_point(lambda x: 0.5*np.sin(x), 1.0,
                                    max_iter=n_its)
    rates.append(abs(traj_n[-1] - x_sin_fp))
axes[1, 0].semilogy(n_range, rates, "o-", lw=2)
axes[1, 0].semilogy(n_range, 0.5**n_range, "--", lw=2, label="O(c^k)")
axes[1, 0].set_xlabel("Iteration k")
axes[1, 0].set_ylabel("|x_k - x*|")
axes[1, 0].set_title("Linear Convergence\nfor contraction c=0.5")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

cs = np.linspace(0.1, 0.95, 20)
iter_counts = []
for c in cs:
    _, traj_c = banach_fixed_point(lambda x, cc=c: cc * np.sin(x), 0.5,
                                    tol=1e-8, max_iter=500)
    iter_counts.append(len(traj_c))
axes[1, 1].plot(cs, iter_counts, "o-", lw=2)
axes[1, 1].set_xlabel("Contraction factor c")
axes[1, 1].set_ylabel("Iterations to converge")
axes[1, 1].set_title("Iterations vs Contraction Factor")
axes[1, 1].grid(True, alpha=0.3)

n_states_mdp = R
gamma_range = np.linspace(0.5, 0.99, 20)
iter_mdp = []
for g in gamma_range:
    V, Vh = value_iteration(P, R, gamma=g, tol=1e-6)
    iter_mdp.append(len(Vh))
axes[1, 2].plot(gamma_range, iter_mdp, "o-", lw=2)
axes[1, 2].set_xlabel("Discount factor γ")
axes[1, 2].set_ylabel("Iterations")
axes[1, 2].set_title("Value Iteration: γ → 1\nslower convergence")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/27-fixed-point.png")
plt.close()

print("=" * 60)
print("FIXED POINT THEORY")
print("=" * 60)
print(f"\nBanach fixed point (contraction) examples:")
print(f"  f(x)=0.5·sin(x): x*={x_sin_fp:.6f}")
print(f"  f(x)=cos(x):     x*={x_cos_fp:.6f}")
print(f"  f(x)=0.5x+0.5:   x*={x_lin_fp:.6f}")

print(f"\nValue iteration (2-state MDP, γ=0.95):")
print(f"  V*(s₀) = {V_opt[0]:.6f}")
print(f"  V*(s₁) = {V_opt[1]:.6f}")
print(f"  Converged in {len(V_history)} iterations")

print(f"\nContraction properties:")
print(f"  d(f(x), f(y)) ≤ c·d(x,y) with c < 1")
print(f"  Convergence rate: |x_k - x*| ≤ c^k · |x₀ - x*|")
print(f"  Banach: unique FP, Picard iteration converges")
print(f"  Brouwer: continuous f: K→K in compact K → ∃ FP")
print(f"  Kakutani: set-valued, used in game theory (Nash)")
