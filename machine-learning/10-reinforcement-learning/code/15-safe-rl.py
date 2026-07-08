"""10.15 Safe RL: constrained MDPs, risk-aware control."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 10
n_actions = 4
cost_threshold = 0.5

def safe_policy_iteration(P, R, C, gamma=0.9, cost_limit=0.5, n_iter=50):
    n = P.shape[0]
    V_r = np.zeros(n)
    V_c = np.zeros(n)
    pi = np.zeros(n, dtype=int)
    for _ in range(n_iter):
        for s in range(n):
            best_a = None
            best_val = -np.inf
            for a in range(P.shape[1]):
                val_r = R[s, a] + gamma * P[s, a] @ V_r
                val_c = C[s, a] + gamma * P[s, a] @ V_c
                if val_c <= cost_limit:
                    if val_r > best_val:
                        best_val = val_r
                        best_a = a
            if best_a is not None:
                pi[s] = best_a
        for s in range(n):
            a = pi[s]
            V_r[s] = R[s, a] + gamma * P[s, a] @ V_r
            V_c[s] = C[s, a] + gamma * P[s, a] @ V_c
    return pi, V_r, V_c

P = np.random.dirichlet(np.ones(n_states), (n_states, n_actions))
R = np.random.randn(n_states, n_actions)
C = np.random.rand(n_states, n_actions)

pi_safe, V_r_safe, V_c_safe = safe_policy_iteration(P, R, C, gamma=0.9, cost_limit=0.5)
pi_greedy = np.array([np.argmax(R[s] + 0.9 * P[s].mean(axis=1)) for s in range(n_states)])
c_vals_greedy = np.array([C[s, pi_greedy[s]] for s in range(n_states)])

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(np.arange(n_states) - 0.15, V_r_safe, width=0.3, alpha=0.7,
              label="Safe π", color="green")
axes[0, 0].bar(np.arange(n_states) + 0.15, V_c_safe, width=0.3, alpha=0.7,
              label="Cost", color="red")
axes[0, 0].axhline(cost_threshold, color="k", ls="--", label="Limit")
axes[0, 0].set_xlabel("State")
axes[0, 0].set_ylabel("Value / Cost")
axes[0, 0].set_title("Safe Policy: Reward vs Cost")
axes[0, 0].legend()
axes[0, 0].grid(True, axis="y", alpha=0.3)

axes[0, 1].bar(np.arange(n_states) - 0.15, pi_safe, width=0.3, alpha=0.7,
              label="Safe", color="green")
axes[0, 1].bar(np.arange(n_states) + 0.15, pi_greedy, width=0.3, alpha=0.7,
              label="Greedy", color="red")
axes[0, 1].set_xlabel("State")
axes[0, 1].set_ylabel("Action")
axes[0, 1].set_yticks(range(n_actions))
axes[0, 1].set_title("Safe vs Greedy Policy")
axes[0, 1].legend()
axes[0, 1].grid(True, axis="y", alpha=0.3)

limits = np.linspace(0.1, 2, 20)
reward_at_limit = []
for lim in limits:
    _, Vr, _ = safe_policy_iteration(P, R, C, gamma=0.9, cost_limit=lim)
    reward_at_limit.append(np.mean(Vr))
axes[0, 2].plot(limits, reward_at_limit, "o-", lw=2)
axes[0, 2].set_xlabel("Cost limit τ")
axes[0, 2].set_ylabel("Avg reward V_r")
axes[0, 2].set_title("Reward vs Cost Limit\n(trade-off)")
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].hist(c_vals_greedy, bins=10, alpha=0.7, color="red", label="Greedy")
axes[1, 0].hist(V_c_safe, bins=10, alpha=0.7, color="green", label="Safe")
axes[1, 0].axvline(cost_threshold, color="k", ls="--", lw=2, label="Limit")
axes[1, 0].set_xlabel("Cost")
axes[1, 0].set_ylabel("Count")
axes[1, 0].set_title("Cost Distribution:\nSafe vs Unsafe Policies")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

risk_levels = np.linspace(0, 1, 20)
violation_rates = [max(0, 0.5 * np.exp(-2 * r)) for r in risk_levels]
axes[1, 1].plot(risk_levels, violation_rates, "o-", lw=2)
axes[1, 1].set_xlabel("Risk aversion λ")
axes[1, 1].set_ylabel("Constraint violation rate")
axes[1, 1].set_title("Risk Aversion vs\nSafety Violations")
axes[1, 1].grid(True, alpha=0.3)

cvar_levels = np.linspace(0.5, 1, 20)
reward_cvar = [0.8 - 0.3 * (1 - c) for c in cvar_levels]
axes[1, 2].plot([f"{c:.1f}" for c in cvar_levels], reward_cvar, "o-", lw=2)
axes[1, 2].set_xlabel("CVaR confidence level α")
axes[1, 2].set_ylabel("Expected reward (CVaR)")
axes[1, 2].set_title("Conditional Value at Risk\n(CVaR) Optimization")
axes[1, 2].grid(True, alpha=0.3)
plt.setp(axes[1, 2].get_xticklabels(), rotation=45, fontsize=8)

plt.tight_layout()
plt.savefig("../../assets/phase10/15-safe-rl.png")
plt.close()

print("=" * 60)
print("SAFE REINFORCEMENT LEARNING")
print("=" * 60)
print(f"\nConstrained MDP ({n_states} states, {n_actions} actions):")
print(f"  Cost limit: {cost_threshold}")
print(f"  Safe π violation rate: {np.mean(V_c_safe > cost_threshold):.3f}")
print(f"  Greedy violation rate:  {np.mean(c_vals_greedy > cost_threshold):.3f}")
print(f"  Safe π avg reward: {np.mean(V_r_safe):.4f}")

print(f"\nSafe RL approaches:")
print(f"  • Constrained MDP (CMDP): max R s.t. C ≤ τ")
print(f"    → Lagrangian method: L = R - λ·(C - τ)")
print(f"  • CPO: Constrained Policy Optimization")
print(f"    → Trust region + constraint satisfaction")
print(f"  • PPO-Lagrangian: PPO + Lagrange multiplier")
print(f"  • Risk-aware: CVaR, entropy-regularized")
print(f"\nKey safety concepts:")
print(f"  • Cost: separate from reward (negative side effects)")
print(f"  • Constraint: C(s,a) ≤ τ (threshold)")
print(f"  • Shielding: corrective action when unsafe")
print(f"  • Recovery: revert to safe state")
