"""
Mock A/B Testing — demonstrates statistical inference for model comparison,
including t-test, minimum sample size estimation, and Thompson Sampling.
"""

import numpy as np
from scipy.stats import ttest_ind, norm, beta as beta_dist


def minimum_sample_size(
    effect_size: float = 0.05,
    control_rate: float = 0.10,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    """Estimate sample size per variant for a proportion-based metric."""
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    p_pooled = control_rate * 2 / 2
    n = (
        (z_alpha + z_beta) ** 2
        * 2
        * p_pooled
        * (1 - p_pooled)
        / (effect_size ** 2)
    )
    return int(np.ceil(n))


def ab_test_decision(control: np.ndarray, treatment: np.ndarray, alpha: float = 0.05) -> dict:
    """Run a two-sample t-test between control and treatment."""
    stat, p = ttest_ind(control, treatment)
    return {
        "control_mean": float(control.mean()),
        "treatment_mean": float(treatment.mean()),
        "lift_pct": float((treatment.mean() - control.mean()) / control.mean() * 100),
        "t_statistic": float(stat),
        "p_value": float(p),
        "significant": p < alpha,
        "alpha": alpha,
    }


class ThompsonSampling:
    """Multi-armed bandit using Thompson Sampling (Beta-Bernoulli)."""

    def __init__(self, n_arms: int):
        self.alphas = np.ones(n_arms)
        self.betas = np.ones(n_arms)

    def select_arm(self) -> int:
        samples = np.random.beta(self.alphas, self.betas)
        return int(np.argmax(samples))

    def update(self, arm: int, reward: float):
        self.alphas[arm] += reward
        self.betas[arm] += 1 - reward

    def best_arm(self) -> int:
        expected = self.alphas / (self.alphas + self.betas)
        return int(np.argmax(expected))


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # Simulate an A/B test
    control = rng.beta(10, 90, 5000)  # ~10% conversion
    treatment = rng.beta(12, 88, 5000)  # ~12% conversion

    result = ab_test_decision(control, treatment)
    print("=== A/B Test Result ===")
    for k, v in result.items():
        print(f"  {k}: {v}")

    n = minimum_sample_size(effect_size=0.02, control_rate=0.10)
    print(f"\nMinimum sample size per variant: {n}")

    # Thompson Sampling simulation
    print("\n=== Thompson Sampling (Multi-Armed Bandit) ===")
    bandit = ThompsonSampling(n_arms=3)
    true_rates = [0.10, 0.12, 0.08]

    for step in range(2000):
        arm = bandit.select_arm()
        reward = float(rng.random() < true_rates[arm])
        bandit.update(arm, reward)

    best = bandit.best_arm()
    print(f"True best arm: {np.argmax(true_rates)} (rate={max(true_rates):.2f})")
    print(f"Bandit selected arm: {best}")
    expected = bandit.alphas / (bandit.alphas + bandit.betas)
    for i, e in enumerate(expected):
        print(f"  Arm {i}: estimated rate = {e:.4f}")
