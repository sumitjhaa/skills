"""10.02 Dynamic programming: policy evaluation and improvement."""
import numpy as np
import matplotlib.pyplot as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 5
n_actions = 2
P = np.random.dirichlet(np.ones(n_states), (n_states, n_actions))
R = np.random.randn(n_states, n_actions)
gamma = 0.9

def policy_evaluation(pi, P, R, gamma=0.9, theta=1e-6):
    n = P.shape[0]
    V = np.zeros(n)
    while True:
        delta = 0
        for s in range(n):
            a = pi[s]
            v = V[s]
            V[s] = R[s, a] + gamma * P[s, a] @ V
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V

def policy_improvement(V, P, R, gamma=0.9):
    n = P.shape[0]
    n_actions = P.shape[1]
    Q = np.zeros((n, n_actions))
    for s in range(n):
        for a in range(n_actions):
            Q[s, a] = R[s, a] + gamma * P[s, a] @ V
    return np.argmax(Q, axis=1)

def policy_iteration(P, R, gamma=0.9):
    n = P.shape[0]
    pi = np.zeros(n, dtype=int)
    for _ in range(100):
        V = policy_evaluation(pi, P, R, gamma)
        pi_new = policy_improvement(V, P, R, gamma)
        if np.all(pi_new == pi):
            break
        pi = pi_new
    return pi, V

pi_random = np.random.randint(0, n_actions, n_states)
V_random = policy_evaluation(pi_random, P, R, gamma)

pi_optimal, V_optimal = policy_iteration(P, R, gamma)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(range(n_states), V_random, color="lightcoral", alpha=0.7,
              label="Random policy")
axes[0, 0].bar(range(n_states) if False else range(n_states), V_optimal,
              color="steelblue", alpha=0.5, label="Optimal policy")
axes[0, 0].set_xlabel("State")
axes[0, 0].set_ylabel("V(s)")
axes[0, 0].set_title("Policy Evaluation\nV^π vs V*")
axes[0, 0].legend()
axes[0, 0].grid(True, axis="y", alpha=0.3)

axes[0, 1].bar(np.arange(n_states) - 0.15, pi_random, width=0.3, alpha=0.7,
              label="Random π", color="coral")
axes[0, 1].bar(np.arange(n_states) + 0.15, pi_optimal, width=0.3, alpha=0.7,
              label="Optimal π*", color="steelblue")
axes[0, 1].set_xlabel("State")
axes[0, 1].set_ylabel("Action")
axes[0, 1].set_yticks([0, 1])
axes[0, 1].set_title("Policy Improvement")
axes[0, 1].legend()
axes[0, 1].grid(True, axis="y", alpha=0.3)

V_traj = []
pi_test = np.zeros(n_states, dtype=int)
for _ in range(20):
    V_test = policy_evaluation(pi_test, P, R, gamma)
    V_traj.append(V_test.copy())
    pi_test = policy_improvement(V_test, P, R, gamma)
V_arr = np.array(V_traj)
for s in range(n_states):
    axes[0, 2].plot(range(len(V_arr)), V_arr[:, s], "o-", lw=2, label=f"S{s}")
axes[0, 2].set_xlabel("Policy iteration")
axes[0, 2].set_ylabel("V(s)")
axes[0, 2].set_title("Policy Iteration: Value Convergence")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

gammas = np.linspace(0.1, 0.99, 30)
V_g1, V_g2 = [], []
for g in gammas:
    pi1, v1 = policy_iteration(P, R, g)
    rpi = np.random.randint(0, n_actions, n_states)
    V_g1.append(v1[0])
    V_g2.append(policy_evaluation(rpi, P, R, g)[0])
axes[1, 0].plot(gammas, V_g1, "b-", lw=2, label="Optimal")
axes[1, 0].plot(gammas, V_g2, "r--", lw=2, label="Random π")
axes[1, 0].set_xlabel("γ")
axes[1, 0].set_ylabel("V(s₀)")
axes[1, 0].set_title("Value vs Discount Factor")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

def value_iteration(P, R, gamma=0.9, theta=1e-6, max_iter=100):
    n = P.shape[0]
    V = np.zeros(n)
    for _ in range(max_iter):
        delta = 0
        for s in range(n):
            v = V[s]
            V[s] = max(R[s, a] + gamma * P[s, a] @ V for a in range(n_actions))
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    pi = np.zeros(n, dtype=int)
    for s in range(n):
        pi[s] = np.argmax([R[s, a] + gamma * P[s, a] @ V for a in range(n_actions)])
    return pi, V

pi_vi, V_vi = value_iteration(P, R, gamma)
vi_optimal = np.all(pi_vi == pi_optimal)
axes[1, 1].bar(["Value Iter.", "Policy Iter.", "Same?"],
               [np.mean(V_vi), np.mean(V_optimal), float(vi_optimal)],
               color=["green", "blue", "orange"], alpha=0.7)
axes[1, 1].set_ylabel("Mean V")
axes[1, 1].set_title("Value vs Policy Iteration\n(should converge to same V*)")
axes[1, 1].grid(True, axis="y", alpha=0.3)

n_values = [5, 10, 20, 50]
comp_times = [n * n_actions * 50 for n in n_values]
axes[1, 2].plot(n_values, comp_times, "o-", lw=2)
axes[1, 2].plot(n_values, [n * n_actions * 100 for n in n_values], "s--", lw=2,
               label="Policy Iteration")
axes[1, 2].set_xlabel("Number of states")
axes[1, 2].set_ylabel("Relative iterations")
axes[1, 2].set_title("Computational Complexity")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/02-dynamic-programming.png")
plt.close()

print("=" * 60)
print("DYNAMIC PROGRAMMING")
print("=" * 60)
print(f"\nPolicy Evaluation (random π):")
print(f"  V^π(range) = [{V_random.min():.4f}, {V_random.max():.4f}]")
print(f"\nPolicy Iteration:")
print(f"  Converged optimal policy: {pi_optimal}")
print(f"  V*(range) = [{V_optimal.min():.4f}, {V_optimal.max():.4f}]")
print(f"\nValue Iteration:")
print(f"  Same as policy iteration: {vi_optimal}")
print(f"  V*(s₀) = {V_vi[0]:.4f} (PI: {V_optimal[0]:.4f})")
print(f"\nGeneralized Policy Iteration (GPI):")
print(f"  π' = greedy(V^π)  (improvement)")
print(f"  V^{{π'}} = eval(π') (evaluation)")
print(f"  Converges to optimal π*, V*")
