"""10.01 Markov decision processes and Bellman equations."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 5
n_actions = 2
P = np.random.dirichlet(np.ones(n_states), (n_states, n_actions))
R = np.random.randn(n_states, n_actions)
gamma = 0.9

V = np.zeros(n_states)
for _ in range(100):
    V_new = np.zeros(n_states)
    for s in range(n_states):
        V_new[s] = max(R[s, a] + gamma * P[s, a] @ V for a in range(n_actions))
    if np.max(np.abs(V_new - V)) < 1e-6:
        break
    V = V_new

Q = np.zeros((n_states, n_actions))
for s in range(n_states):
    for a in range(n_actions):
        Q[s, a] = R[s, a] + gamma * P[s, a] @ V

policy = np.argmax(Q, axis=1)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(range(n_states), V, color="steelblue", alpha=0.7)
axes[0, 0].set_xlabel("State")
axes[0, 0].set_ylabel("V*(s)")
axes[0, 0].set_title("Optimal Value Function\n(Bellman optimality)")
axes[0, 0].grid(True, axis="y", alpha=0.3)

im = axes[0, 1].imshow(Q, cmap="coolwarm", interpolation="nearest")
for s in range(n_states):
    for a in range(n_actions):
        axes[0, 1].text(a, s, f"{Q[s, a]:.2f}", ha="center", va="center")
axes[0, 1].set_xlabel("Action")
axes[0, 1].set_ylabel("State")
axes[0, 1].set_title("Q*(s,a) Matrix")
plt.colorbar(im, ax=axes[0, 1])

axes[0, 2].bar(range(n_states), policy, color=["red", "blue"], alpha=0.7)
axes[0, 2].set_xlabel("State")
axes[0, 2].set_ylabel("Optimal action")
axes[0, 2].set_yticks([0, 1])
axes[0, 2].set_yticklabels(["a₀", "a₁"])
axes[0, 2].set_title("Optimal Policy π*(s)")
axes[0, 2].grid(True, axis="y", alpha=0.3)

gammas = np.linspace(0, 0.99, 20)
V_s0 = []
for g in gammas:
    V_g = np.zeros(n_states)
    P_g = P.copy()
    for _ in range(50):
        V_new_g = np.zeros(n_states)
        for s in range(n_states):
            V_new_g[s] = max(R[s, a] + g * P_g[s, a] @ V_g for a in range(n_actions))
        V_g = V_new_g
    V_s0.append(V_g[0])
axes[1, 0].plot(gammas, V_s0, "o-", lw=2)
axes[1, 0].axvline(1, color="r", ls="--", alpha=0.5)
axes[1, 0].set_xlabel("Discount factor γ")
axes[1, 0].set_ylabel("V*(s₀)")
axes[1, 0].set_title("Value vs Discount Factor\n(γ→1: harder convergence)")
axes[1, 0].grid(True, alpha=0.3)

n_iterations = np.arange(1, 30)
V_conv = np.zeros(n_states)
conv_traj = [V_conv.copy()]
for _ in range(30):
    V_new = np.zeros(n_states)
    for s in range(n_states):
        V_new[s] = max(R[s, a] + gamma * P[s, a] @ V_conv for a in range(n_actions))
    V_conv = V_new
    conv_traj.append(V_conv.copy())
conv_arr = np.array(conv_traj)
for s in range(n_states):
    axes[1, 1].plot(range(len(conv_arr)), conv_arr[:, s], lw=2, label=f"S{s}")
axes[1, 1].set_xlabel("Iteration")
axes[1, 1].set_ylabel("V(s)")
axes[1, 1].set_title("Value Iteration Convergence")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

reward_sparsity = [0, 0.2, 0.5, 0.8, 1.0]
iters_needed = []
for sp in reward_sparsity:
    R_sp = R.copy()
    mask = np.random.rand(*R.shape) < sp
    R_sp[mask] = 0
    V_sp = np.zeros(n_states)
    for it in range(500):
        V_new_sp = np.zeros(n_states)
        for s in range(n_states):
            V_new_sp[s] = max(R_sp[s, a] + gamma * P[s, a] @ V_sp for a in range(n_actions))
        if np.max(np.abs(V_new_sp - V_sp)) < 1e-4:
            iters_needed.append(it)
            break
        V_sp = V_new_sp
    else:
        iters_needed.append(500)
axes[1, 2].plot(reward_sparsity, iters_needed, "o-", lw=2)
axes[1, 2].set_xlabel("Reward sparsity")
axes[1, 2].set_ylabel("Iterations to converge")
axes[1, 2].set_title("Effect of Reward Sparsity\non Convergence")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/01-mdp.png")
plt.close()

print("=" * 60)
print("MARKOV DECISION PROCESSES")
print("=" * 60)
print(f"\nMDP: {n_states} states, {n_actions} actions, γ={gamma}")
print(f"  Optimal value range: [{V.min():.4f}, {V.max():.4f}]")
print(f"  Optimal policy: {policy}")

print(f"\nBellman Optimality Equation:")
print(f"  V*(s) = max_a [R(s,a) + γ·Σ P(s'|s,a)·V*(s')]")
print(f"  Q*(s,a) = R(s,a) + γ·Σ P(s'|s,a)·V*(s')")

print(f"\nValue iteration converged in {len(conv_traj)} iterations")
print(f"  γ={gamma}: V(s₀)={V[0]:.4f}")
print(f"  At γ=0.5: V(s₀)={V_s0[np.argmin(np.abs(gammas-0.5))]:.4f}")
print(f"  At γ=0.9: V(s₀)={V_s0[np.argmin(np.abs(gammas-0.9))]:.4f}")

print(f"\nKey concepts:")
print(f"  • Markov property: P(s_{t+1}|s_t, a_t) independent of history")
print(f"  • Bellman equation: recursive decomposition of value")
print(f"  • Value iteration: dynamic programming in state space")
print(f"  • Policy: π: S → A (deterministic) or π: S × A → [0,1] (stochastic)")
