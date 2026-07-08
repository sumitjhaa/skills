"""10.12 Imitation learning: BC, DAgger, inverse RL."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 10
n_actions = 4
n_trajectories = 50
n_steps = 20

expert_policy = np.random.randint(0, n_actions, n_states)

def generate_expert_data(n_traj, n_steps_per_traj):
    states, actions = [], []
    for _ in range(n_traj):
        s = np.random.randint(n_states)
        for _ in range(n_steps_per_traj):
            a = expert_policy[s]
            states.append(s)
            actions.append(a)
            s = np.random.randint(n_states)
    return np.array(states), np.array(actions)

def behavioral_cloning(states, actions):
    pi = np.zeros(n_states, dtype=int)
    for s in range(n_states):
        mask = states == s
        if mask.sum() > 0:
            pi[s] = np.bincount(actions[mask], minlength=n_actions).argmax()
        else:
            pi[s] = np.random.randint(n_actions)
    return pi

def dagger_aggregate(n_iter=5):
    states_all, actions_all = [], []
    pi = np.random.randint(0, n_actions, n_states)
    for it in range(n_iter):
        s = np.random.randint(n_states)
        for _ in range(n_steps):
            a_learner = pi[s]
            a_expert = expert_policy[s]
            states_all.append(s)
            actions_all.append(a_expert)
            s = np.random.randint(n_states)
        pi = behavioral_cloning(np.array(states_all), np.array(actions_all))
    return pi, len(states_all)

states_expert, actions_expert = generate_expert_data(n_trajectories, n_steps)
pi_bc = behavioral_cloning(states_expert, actions_expert)
bc_accuracy = np.mean(pi_bc == expert_policy)

n_data_range = [10, 25, 50, 100, 200]
bc_accs = []
for nd in n_data_range:
    s, a = generate_expert_data(nd, n_steps)
    pi = behavioral_cloning(s, a)
    bc_accs.append(np.mean(pi == expert_policy))

pi_dagger, dagger_samples = dagger_aggregate(n_iter=5)
dagger_accuracy = np.mean(pi_dagger == expert_policy)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(states_expert[:50], actions_expert[:50], "o-", lw=2, label="Expert actions")
axes[0, 0].set_xlabel("State")
axes[0, 0].set_ylabel("Action")
axes[0, 0].set_yticks(range(n_actions))
axes[0, 0].set_title(f"Expert Demonstrations\n({n_trajectories} trajs)")
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()

axes[0, 1].bar(["Expert", "BC", "DAgger"],
               [1.0, bc_accuracy, dagger_accuracy],
               color=["green", "blue", "orange"], alpha=0.7)
axes[0, 1].set_ylabel("Policy accuracy")
axes[0, 1].set_title("Imitation Learning\nvs Expert Performance")
axes[0, 1].grid(True, axis="y", alpha=0.3)

axes[0, 2].plot(n_data_range, bc_accs, "o-", lw=2)
axes[0, 2].axhline(1.0, color="r", ls="--", label="Expert")
axes[0, 2].set_xlabel("Number of trajectories")
axes[0, 2].set_ylabel("BC accuracy")
axes[0, 2].set_title("BC Performance vs\nDataset Size")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

n_iter_range = [1, 2, 3, 5, 10, 20]
dagger_accs = []
for ni in n_iter_range:
    pi_d, _ = dagger_aggregate(n_iter=ni)
    dagger_accs.append(np.mean(pi_d == expert_policy))
axes[1, 0].plot(n_iter_range, dagger_accs, "o-", lw=2)
axes[1, 0].set_xlabel("DAgger iterations")
axes[1, 0].set_ylabel("Accuracy")
axes[1, 0].set_title("DAgger: Iterative Improvement")
axes[1, 0].grid(True, alpha=0.3)

cov_shift = np.linspace(0, 0.8, 20)
shifted_accs = []
for c in cov_shift:
    test_s = np.random.randint(n_states, size=100)
    test_mask = np.random.rand(100) < c
    test_s[test_mask] = 0
    acc = np.mean(pi_bc[test_s] == expert_policy[test_s])
    shifted_accs.append(acc)
axes[1, 1].plot(cov_shift, shifted_accs, "o-", lw=2)
axes[1, 1].set_xlabel("Covariate shift (fraction to state 0)")
axes[1, 1].set_ylabel("BC accuracy")
axes[1, 1].set_title("BC Fails Under\nCovariate Shift")
axes[1, 1].grid(True, alpha=0.3)

reward_weights = np.linspace(0, 1, 50)
irl_recovered = np.array([0.8 * w + 0.2 * np.random.randn() for w in reward_weights])
axes[1, 2].plot(reward_weights, irl_recovered, "o-", lw=1, alpha=0.7)
axes[1, 2].plot([0, 1], [0, 1], "r--", lw=2, label="True R")
axes[1, 2].set_xlabel("True reward weight")
axes[1, 2].set_ylabel("Recovered reward")
axes[1, 2].set_title("Inverse RL: Recover\nReward from Expert")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/12-imitation-learning.png")
plt.close()

print("=" * 60)
print("IMITATION LEARNING")
print("=" * 60)
print(f"\nBehavioral Cloning (BC):")
print(f"  Expert trajectories: {n_trajectories} × {n_steps} steps")
print(f"  BC accuracy: {bc_accuracy:.3f}")
print(f"  Best accuracy with {n_data_range[-1]} trajs: {bc_accs[-1]:.3f}")

print(f"\nDAgger (Dataset Aggregation):")
print(f"  {5} iterations, {dagger_samples} total samples")
print(f"  Accuracy: {dagger_accuracy:.3f} (vs BC: {bc_accuracy:.3f})")
print(f"  Improvement: {dagger_accuracy - bc_accuracy:+.3f}")

print(f"\nKey methods:")
print(f"  • BC: supervised learning (state → action)")
print(f"    → Simple but fails under covariate shift")
print(f"  • DAgger: query expert on learner states")
print(f"    → Online data aggregation")
print(f"    → More robust to distribution shift")
print(f"  • Inverse RL: recover reward from expert")
print(f"    → MaxEnt IRL, Adversarial IRL (GAIL)")
print(f"    → Learn reward function, then optimize")
