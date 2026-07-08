"""10.09 Exploration: epsilon-greedy, UCB, Thompson sampling."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_arms = 5
n_steps = 1000
true_means = np.array([0.1, 0.3, 0.5, 0.7, 0.9])

def run_epsilon_greedy(epsilon, n_steps=1000):
    Q = np.zeros(n_arms)
    counts = np.zeros(n_arms)
    regrets = []
    for t in range(n_steps):
        if np.random.rand() < epsilon:
            a = np.random.randint(n_arms)
        else:
            a = np.argmax(Q)
        r = np.random.binomial(1, true_means[a])
        counts[a] += 1
        Q[a] += (r - Q[a]) / counts[a]
        regret = t * true_means.max() - np.sum(counts * true_means)
        regrets.append(regret)
    return np.array(regrets)

def run_ucb(n_steps=1000, c=2):
    Q = np.zeros(n_arms)
    counts = np.ones(n_arms) * 1e-6
    regrets = []
    for t in range(1, n_steps + 1):
        ucb = Q + c * np.sqrt(np.log(t) / counts)
        a = np.argmax(ucb)
        r = np.random.binomial(1, true_means[a])
        counts[a] += 1
        Q[a] += (r - Q[a]) / counts[a]
        regret = t * true_means.max() - np.sum(counts * true_means)
        regrets.append(regret)
    return np.array(regrets)

def run_thompson(n_steps=1000):
    alpha = np.ones(n_arms)
    beta = np.ones(n_arms)
    regrets = []
    for t in range(n_steps):
        samples = np.random.beta(alpha, beta)
        a = np.argmax(samples)
        r = np.random.binomial(1, true_means[a])
        alpha[a] += r
        beta[a] += 1 - r
        regret = t * true_means.max() - np.sum(
            (alpha - 1) / (alpha + beta - 2) * (alpha + beta - 2))
        regrets.append(regret)
    return np.array(regrets)

n_trials = 50
eps_regrets = np.zeros((n_trials, n_steps))
ucb_regrets = np.zeros((n_trials, n_steps))
thompson_regrets = np.zeros((n_trials, n_steps))
for trial in range(n_trials):
    eps_regrets[trial] = run_epsilon_greedy(0.1, n_steps)
    ucb_regrets[trial] = run_ucb(n_steps, c=2)
    thompson_regrets[trial] = run_thompson(n_steps)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

eps_mean = eps_regrets.mean(axis=0)
ucb_mean = ucb_regrets.mean(axis=0)
thompson_mean = thompson_regrets.mean(axis=0)
axes[0, 0].plot(eps_mean, lw=2, label="ε-greedy (ε=0.1)")
axes[0, 0].plot(ucb_mean, lw=2, label="UCB (c=2)")
axes[0, 0].plot(thompson_mean, lw=2, label="Thompson")
axes[0, 0].set_xlabel("Step")
axes[0, 0].set_ylabel("Cumulative regret")
axes[0, 0].set_title("Bandit Regret Comparison\n(n_arms=5)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

epsilons = [0.01, 0.05, 0.1, 0.2, 0.5]
eps_final = []
for e in epsilons:
    r = run_epsilon_greedy(e, n_steps)
    eps_final.append(r[-1])
axes[0, 1].bar([str(e) for e in epsilons], eps_final, alpha=0.7)
axes[0, 1].set_xlabel("ε")
axes[0, 1].set_ylabel("Final regret")
axes[0, 1].set_title("ε-greedy: ε vs Regret")
axes[0, 1].grid(True, axis="y", alpha=0.3)

ucb_cs = [0.5, 1, 2, 5, 10]
ucb_final = []
for c in ucb_cs:
    r = run_ucb(n_steps, c)
    ucb_final.append(r[-1])
axes[0, 2].bar([str(c) for c in ucb_cs], ucb_final, alpha=0.7)
axes[0, 2].set_xlabel("c")
axes[0, 2].set_ylabel("Final regret")
axes[0, 2].set_title("UCB: Exploration Constant")
axes[0, 2].grid(True, axis="y", alpha=0.3)

best_arm = np.argmax(true_means)
eps_pulls = []
for eps in epsilons:
    Q_eg = np.zeros(n_arms)
    counts_eg = np.zeros(n_arms)
    for _ in range(n_steps):
        if np.random.rand() < eps:
            a = np.random.randint(n_arms)
        else:
            a = np.argmax(Q_eg)
        r = np.random.binomial(1, true_means[a])
        counts_eg[a] += 1
        Q_eg[a] += (r - Q_eg[a]) / counts_eg[a]
    eps_pulls.append(counts_eg[best_arm])
axes[1, 0].bar([str(e) for e in epsilons], eps_pulls, alpha=0.7)
axes[1, 0].set_xlabel("ε")
axes[1, 0].set_ylabel("Pulls of best arm")
axes[1, 0].set_title("ε-greedy: Best Arm Selection")
axes[1, 0].grid(True, axis="y", alpha=0.3)

n_arms_range = [3, 5, 10, 20, 50]
regret_arms = []
for na in n_arms_range:
    true_m = np.sort(np.random.rand(na))[::-1]
    r = run_ucb(n_steps, c=2) if na <= 20 else run_epsilon_greedy(0.1, n_steps)
    regret_arms.append(r[-1])
axes[1, 1].plot(n_arms_range, regret_arms, "o-", lw=2)
axes[1, 1].set_xlabel("Number of arms")
axes[1, 1].set_ylabel("Final regret")
axes[1, 1].set_title("Regret vs Number of Arms")
axes[1, 1].grid(True, alpha=0.3)

thompson_alpha = np.ones(n_arms)
thompson_beta = np.ones(n_arms)
thompson_means = []
for _ in range(50):
    a = np.argmax(np.random.beta(thompson_alpha, thompson_beta))
    r = np.random.binomial(1, true_means[a])
    thompson_alpha[a] += r
    thompson_beta[a] += 1 - r
    thompson_means.append((thompson_alpha - 1) / (thompson_alpha + thompson_beta - 2))
thompson_arr = np.array(thompson_means)
for arm in range(min(3, n_arms)):
    if thompson_arr.ndim > 1:
        pass
axes[1, 2].bar(range(n_arms), (thompson_alpha - 1) / (thompson_alpha + thompson_beta - 2),
              color="steelblue", alpha=0.7)
axes[1, 2].scatter(range(n_arms), true_means, color="red", s=50, zorder=5)
axes[1, 2].set_xlabel("Arm")
axes[1, 2].set_ylabel("Estimated mean")
axes[1, 2].set_title("Thompson: Posterior Means\nvs True Means")
axes[1, 2].grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase10/09-exploration.png")
plt.close()

print("=" * 60)
print("EXPLORATION STRATEGIES")
print("=" * 60)
print(f"\nBandit: {n_arms} arms, Bernoulli rewards")
print(f"  True means: {true_means}")
print(f"  Best arm: {best_arm} (μ={true_means[best_arm]})")

print(f"\nFinal regrets (mean over {n_trials} trials):")
print(f"  ε-greedy (ε=0.1): {eps_mean[-1]:.2f}")
print(f"  UCB (c=2):        {ucb_mean[-1]:.2f}")
print(f"  Thompson:          {thompson_mean[-1]:.2f}")

print(f"\nRegret bounds:")
print(f"  • ε-greedy: linear regret")
print(f"  • UCB: O(log t) regret (Lai & Robbins)")
print(f"  • Thompson: O(log t) (Bayesian)")
print(f"\nKey principle:")
print(f"  exploration-exploitation dilemma")
print(f"  • Explore to gather information")
print(f"  • Exploit to maximize reward")
