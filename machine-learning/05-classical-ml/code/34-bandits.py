"""Bandit algorithms (epsilon-greedy, UCB, Thompson Sampling) from scratch."""
import numpy as np

class EpsilonGreedy:
    def __init__(self, n_arms, epsilon=0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)

    def select(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)
        return np.argmax(self.values)

    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] += (reward - self.values[arm]) / n

class UCB:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
        self.t = 0

    def select(self):
        self.t += 1
        for a in range(self.n_arms):
            if self.counts[a] == 0:
                return a
        ucb = self.values + np.sqrt(2 * np.log(self.t) / (self.counts + 1e-10))
        return np.argmax(ucb)

    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] += (reward - self.values[arm]) / n

class ThompsonSampling:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.alphas = np.ones(n_arms)
        self.betas = np.ones(n_arms)

    def select(self):
        samples = np.random.beta(self.alphas, self.betas)
        return np.argmax(samples)

    def update(self, arm, reward):
        self.alphas[arm] += reward
        self.betas[arm] += 1 - reward

def simulate(bandit, n_rounds=1000):
    true_means = [0.1, 0.2, 0.8, 0.3, 0.5]
    total_reward = 0
    for _ in range(n_rounds):
        arm = bandit.select()
        reward = np.random.binomial(1, true_means[arm])
        bandit.update(arm, reward)
        total_reward += reward
    return total_reward

if __name__ == "__main__":
    np.random.seed(42)
    n_rounds = 2000

    eg = EpsilonGreedy(n_arms=5, epsilon=0.1)
    r1 = simulate(eg, n_rounds)
    print(f"Epsilon-Greedy total reward: {r1}")

    ucb = UCB(n_arms=5)
    r2 = simulate(ucb, n_rounds)
    print(f"UCB total reward: {r2}")

    ts = ThompsonSampling(n_arms=5)
    r3 = simulate(ts, n_rounds)
    print(f"Thompson Sampling total reward: {r3}")
