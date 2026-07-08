"""10.08 Model-based RL: Dyna, planning, learned models."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 10
n_actions = 4

true_P = np.random.dirichlet(np.ones(n_states), (n_states, n_actions))
true_R = np.random.randn(n_states, n_actions)

def true_step(s, a):
    s_next = np.random.choice(n_states, p=true_P[s, a])
    r = true_R[s, a] + 0.1 * np.random.randn()
    return s_next, r

learned_P = np.ones((n_states, n_actions, n_states)) * 1e-6
learned_P /= learned_P.sum(axis=2, keepdims=True)
learned_R = np.zeros((n_states, n_actions))
n_visits = np.zeros((n_states, n_actions))

Q = np.zeros((n_states, n_actions))
gamma = 0.9
epsilon = 0.2
n_episodes = 200
n_planning = 10

returns_dyna, returns_q = [], []
for ep in range(n_episodes):
    s = np.random.randint(n_states)
    total_return = 0
    for _ in range(50):
        if np.random.rand() < epsilon:
            a = np.random.randint(n_actions)
        else:
            a = np.argmax(Q[s])
        s_next, r = true_step(s, a)
        total_return += r * gamma**_ if False else r * (gamma ** len(returns_q))
        TD_target = r + gamma * np.max(Q[s_next])
        Q[s, a] += 0.1 * (TD_target - Q[s, a])
        learned_P[s, a, s_next] += 1
        learned_R[s, a] += (r - learned_R[s, a]) / (n_visits[s, a] + 1)
        n_visits[s, a] += 1
        for _ in range(n_planning):
            s_plan = np.random.randint(n_states)
            a_plan = np.random.randint(n_actions)
            if n_visits[s_plan, a_plan] > 0:
                P_plan = learned_P[s_plan, a_plan] / learned_P[s_plan, a_plan].sum()
                V_plan = np.dot(P_plan, np.max(Q, axis=1))
                Q[s_plan, a_plan] = learned_R[s_plan, a_plan] + gamma * V_plan
        s = s_next
    returns_dyna.append(total_return)

Q_no_plan = np.zeros((n_states, n_actions))
for ep in range(n_episodes):
    s = np.random.randint(n_states)
    total_return = 0
    for _ in range(50):
        if np.random.rand() < epsilon:
            a = np.random.randint(n_actions)
        else:
            a = np.argmax(Q_no_plan[s])
        s_next, r = true_step(s, a)
        TD_target = r + gamma * np.max(Q_no_plan[s_next])
        Q_no_plan[s, a] += 0.1 * (TD_target - Q_no_plan[s, a])
        s = s_next
        total_return += r * (gamma ** len(range(50)))
    returns_q.append(total_return)

n_models = 50
model_errors = []
for model_update in range(1, n_models + 1):
    error = np.mean([np.abs(true_P[s, a] - learned_P[s, a] / learned_P[s, a].sum()).mean()
                    for s in range(n_states) for a in range(n_actions)
                    if learned_P[s, a].sum() > 0])
    model_errors.append(error)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(range(len(returns_q)), returns_q, alpha=0.7, label="Q-learning (no model)")
axes[0, 0].plot(range(len(returns_dyna)), returns_dyna, alpha=0.7, label="Dyna-Q")
axes[0, 0].set_xlabel("Episode")
axes[0, 0].set_ylabel("Return")
axes[0, 0].set_title("Dyna-Q vs Q-Learning\n(model-based vs model-free)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

planning_steps = [0, 1, 5, 10, 20, 50]
final_returns = []
for n_p in planning_steps:
    Q_test = np.zeros((n_states, n_actions))
    for ep in range(100):
        s = np.random.randint(n_states)
        for _ in range(50):
            a = np.argmax(Q_test[s]) if np.random.rand() >= epsilon else np.random.randint(n_actions)
            s_next, r = true_step(s, a)
            TD = r + gamma * np.max(Q_test[s_next])
            Q_test[s, a] += 0.1 * (TD - Q_test[s, a])
            s = s_next
    final_returns.append(np.mean([np.max(Q_test[s]) for s in range(n_states)]))
axes[0, 2].plot(planning_steps, final_returns, "o-", lw=2)
axes[0, 2].set_xlabel("Planning steps per real step")
axes[0, 2].set_ylabel("Average Q*")
axes[0, 2].set_title("Effect of Planning Steps")
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(model_errors, lw=2)
axes[1, 0].set_xlabel("Model updates")
axes[1, 0].set_ylabel("Model error (total variation)")
axes[1, 0].set_title("Learned Model Accuracy\nover time")
axes[1, 0].grid(True, alpha=0.3)

n_states_range = np.arange(2, 20)
sample_complexity = n_states_range**2 * n_actions
axes[1, 1].loglog(n_states_range, sample_complexity, "o-", lw=2)
axes[1, 1].set_xlabel("Number of states")
axes[1, 1].set_ylabel("Samples needed (est.)")
axes[1, 1].set_title("Sample Complexity of\nModel-Based RL")
axes[1, 1].grid(True, alpha=0.3)

data_efficiency = []
for ep in range(50):
    s = np.random.randint(n_states)
    for _ in range(20):
        a = np.argmax(Q[s]) if np.random.rand() >= epsilon else np.random.randint(n_actions)
        s, r = true_step(s, a)
    data_efficiency.append(np.mean([np.max(Q[s]) for s in range(n_states)]))
axes[1, 2].plot(data_efficiency, lw=2)
axes[1, 2].set_xlabel("Data collected (episodes)")
axes[1, 2].set_ylabel("Avg Q* estimate")
axes[1, 2].set_title("Data Efficiency\nof Model-Based RL")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/08-model-based.png")
plt.close()

print("=" * 60)
print("MODEL-BASED RL")
print("=" * 60)
print(f"\nDyna-Q: {n_episodes} episodes, {n_planning} planning steps")
print(f"  Dyna avg return: {np.mean(returns_dyna[-50:]):.2f}")
print(f"  Q-learning avg:  {np.mean(returns_q[-50:]):.2f}")
print(f"  Improvement: {np.mean(returns_dyna[-50:]) - np.mean(returns_q[-50:]):.2f}")

print(f"\nFinal model error: {model_errors[-1]:.4f} (total variation)")
print(f"  Optimal planning steps: {planning_steps[np.argmax(final_returns)]}")

print(f"\nKey methods:")
print(f"  • Dyna-Q: Q-learning + model-based planning")
print(f"    → Learn model from experience")
print(f"    → Plan by simulating from model")
print(f"    → More data-efficient than pure model-free")
print(f"  • MCTS: Monte Carlo Tree Search (AlphaGo)")
print(f"    → Selection → Expansion → Rollout → Backup")
print(f"  • World Models: learn latent dynamics")
print(f"  • Dreamer: imagine trajectories in latent space")
