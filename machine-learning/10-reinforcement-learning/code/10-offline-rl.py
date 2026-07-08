"""10.10 Offline RL: batch learning, conservative methods."""
import numpy as np
import matplotlib.pyplot as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_states = 10
n_actions = 4
n_transitions = 5000

dataset_s = np.random.randint(0, n_states, n_transitions)
dataset_a = np.random.randint(0, n_actions, n_transitions)
dataset_s_next = np.random.randint(0, n_states, n_transitions)
dataset_r = np.random.randn(n_transitions)

Q_behavior = np.random.randn(n_states, n_actions)
mu_behavior = np.exp(Q_behavior) / np.exp(Q_behavior).sum(axis=1, keepdims=True)

gamma = 0.9

def fitted_q_iteration(dataset_s, dataset_a, dataset_r, dataset_s_next,
                        n_iter=50, alpha=0.0):
    n_states = max(dataset_s) + 1
    n_actions = max(dataset_a) + 1
    Q = np.zeros((n_states, n_actions))
    for _ in range(n_iter):
        for s, a, r, s_next in zip(dataset_s, dataset_a, dataset_r, dataset_s_next):
            TD_target = r + gamma * np.max(Q[s_next])
            Q[s, a] += 0.01 * (TD_target - Q[s, a])
        if alpha > 0:
            for s in range(n_states):
                Q[s] -= alpha * Q[s].mean()
    return Q

def conservative_q_learning(dataset_s, dataset_a, dataset_r, dataset_s_next,
                             n_iter=50, alpha=0.5):
    n_states = max(dataset_s) + 1
    n_actions = max(dataset_a) + 1
    Q = np.zeros((n_states, n_actions))
    for _ in range(n_iter):
        for s, a, r, s_next in zip(dataset_s, dataset_a, dataset_r, dataset_s_next):
            pi_s = np.eye(n_actions)[np.argmax(Q[s])]
            mu_s = mu_behavior[s]
            conservative_penalty = alpha * (pi_s @ Q[s] - mu_s @ Q[s])
            TD_target = r + gamma * np.max(Q[s_next]) - conservative_penalty
            Q[s, a] += 0.01 * (TD_target - Q[s, a])
    return Q

Q_fqi = fitted_q_iteration(dataset_s, dataset_a, dataset_r, dataset_s_next)
Q_cql = conservative_q_learning(dataset_s, dataset_a, dataset_r, dataset_s_next, alpha=0.5)
Q_onpolicy = fitted_q_iteration(dataset_s * 2, np.concatenate([dataset_a, np.argmax(mu_behavior[dataset_s], axis=1)]),
                                 np.concatenate([dataset_r, dataset_r]),
                                 np.concatenate([dataset_s_next, dataset_s_next]))

n_samples_range = [100, 500, 1000, 2000, 5000]
fqi_perf, cql_perf = [], []
for n_s in n_samples_range:
    ds_s = dataset_s[:n_s]
    ds_a = dataset_a[:n_s]
    ds_r = dataset_r[:n_s]
    ds_sn = dataset_s_next[:n_s]
    Qf = fitted_q_iteration(ds_s, ds_a, ds_r, ds_sn)
    Qc = conservative_q_learning(ds_s, ds_a, ds_r, ds_sn, alpha=0.5)
    fqi_perf.append(np.mean(np.max(Qf, axis=1)))
    cql_perf.append(np.mean(np.max(Qc, axis=1)))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].bar(["FQI", "CQL (α=0.5)"],
               [np.mean(np.max(Q_fqi, axis=1)), np.mean(np.max(Q_cql, axis=1))],
               color=["steelblue", "coral"], alpha=0.7)
axes[0, 0].set_ylabel("Average Q*")
axes[0, 0].set_title("Offline RL: Value Estimation\nFQI vs CQL")
axes[0, 0].grid(True, axis="y", alpha=0.3)

axes[0, 1].plot(n_samples_range, fqi_perf, "o-", lw=2, label="FQI")
axes[0, 1].plot(n_samples_range, cql_perf, "s-", lw=2, label="CQL (α=0.5)")
axes[0, 1].set_xlabel("Number of transitions")
axes[0, 1].set_ylabel("Avg Q*(s)")
axes[0, 1].set_title("Performance vs Dataset Size")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

alphas = np.linspace(0, 2, 20)
perf_alpha = []
for a in alphas:
    Q_a = conservative_q_learning(dataset_s, dataset_a, dataset_r, dataset_s_next, alpha=a)
    perf_alpha.append(np.mean(np.max(Q_a, axis=1)))
axes[0, 2].plot(alphas, perf_alpha, "o-", lw=2)
axes[0, 2].axvline(0.5, color="r", ls="--", label="α=0.5 (typical)")
axes[0, 2].set_xlabel("Conservative penalty α")
axes[0, 2].set_ylabel("Avg Q*(s)")
axes[0, 2].set_title("CQL: α vs Performance")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

ood_actions = dataset_a.copy()
ood_actions[:len(ood_actions)//2] = np.random.randint(n_actions, size=len(ood_actions)//2)
Q_ood = fitted_q_iteration(dataset_s, ood_actions, dataset_r, dataset_s_next)
Q_ood_cql = conservative_q_learning(dataset_s, ood_actions, dataset_r, dataset_s_next, alpha=1.0)
axes[1, 0].bar(["FQI (OOD)", "CQL (OOD)"],
               [np.mean(np.max(Q_ood, axis=1)), np.mean(np.max(Q_ood_cql, axis=1))],
               color=["steelblue", "coral"], alpha=0.7)
axes[1, 0].set_ylabel("Avg Q*")
axes[1, 0].set_title("Out-of-Distribution Actions")
axes[1, 0].grid(True, axis="y", alpha=0.3)

distributions = ["Behavior\ndataset", "On-policy\n(replay)", "Offline\n(batch)"]
values_est = [np.mean(np.max(Q_fqi, axis=1)), np.mean(np.max(Q_onpolicy, axis=1)),
              np.mean(np.max(Q_cql, axis=1))]
axes[1, 1].bar(distributions, values_est, alpha=0.7)
axes[1, 1].set_ylabel("Avg Q*")
axes[1, 1].set_title("Distribution Shift\n(offline vs on-policy)")
axes[1, 1].grid(True, axis="y", alpha=0.3)

overestimation = np.max(Q_fqi, axis=1) - np.max(Q_cql, axis=1)
axes[1, 2].hist(overestimation, bins=20, alpha=0.7)
axes[1, 2].axvline(0, color="k", ls="--")
axes[1, 2].set_xlabel("Q_FQI - Q_CQL (overestimation)")
axes[1, 2].set_ylabel("Count")
axes[1, 2].set_title("CQL: Reducing\nQ-Overestimation")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/10-offline-rl.png")
plt.close()

print("=" * 60)
print("OFFLINE RL")
print("=" * 60)
print(f"\nDataset: {n_transitions} transitions, {n_states} states, {n_actions} actions")
print(f"  FQI avg Q*: {np.mean(np.max(Q_fqi, axis=1)):.4f}")
print(f"  CQL avg Q*: {np.mean(np.max(Q_cql, axis=1)):.4f}")
print(f"  Difference: {np.mean(np.max(Q_fqi - Q_cql, axis=1)):.4f}")

print(f"\nConservative penalty: L(θ) = L_TD(θ) + α·C(Q)")
print(f"  CQL regularizer: min_Q max_μ [E_μ[Q] - E_data[Q]]")
print(f"  Optimal α = {alphas[np.argmax(perf_alpha)]:.2f}")

print(f"\nKey challenges:")
print(f"  • Distribution shift: behavior vs target policy")
print(f"  • Q-overestimation for OOD actions")
print(f"  • Conservative methods penalize unseen actions")
print(f"\nKey methods:")
print(f"  • CQL: conservative Q-learning (adds penalty)")
print(f"  • BCQ: batch-constrained Q-learning")
print(f"  • IQL: implicit Q-learning")
print(f"  • DT: decision transformer (trajectory modeling)")
