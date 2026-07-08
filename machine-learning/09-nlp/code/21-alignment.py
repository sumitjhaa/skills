"""
09.21 Alignment — DPO Loss Implementation
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


def dpo_loss(policy_log_probs_chosen, policy_log_probs_rejected,
             ref_log_probs_chosen, ref_log_probs_rejected, beta=0.1):
    """
    Direct Preference Optimization loss.

    L = -E[ log sigmoid(beta * (log(π(y_w|x) / π_ref(y_w|x))
                              - log(π(y_l|x) / π_ref(y_l|x)))) ]
    """
    # Log ratio of chosen and rejected
    log_ratio_chosen = policy_log_probs_chosen - ref_log_probs_chosen
    log_ratio_rejected = policy_log_probs_rejected - ref_log_probs_rejected

    # DPO loss
    logits = beta * (log_ratio_chosen - log_ratio_rejected)
    loss = -np.log(1 / (1 + np.exp(-np.clip(logits, -20, 20))))

    return loss.mean()


class PreferenceDataset:
    """Simple synthetic preference dataset (chosen > rejected)."""

    def __init__(self, n_samples=100, vocab_size=50, seq_len=10):
        self.n_samples = n_samples
        self.vocab_size = vocab_size
        self.seq_len = seq_len

    def generate_batch(self, batch_size=8):
        chosen = np.random.randint(0, self.vocab_size, (batch_size, self.seq_len))
        rejected = np.random.randint(0, self.vocab_size, (batch_size, self.seq_len))
        return chosen, rejected


def simulate_log_probs(sequences, vocab_size=50, base_prob=-1.0):
    """Simulate model log probabilities for sequences."""
    B, T = sequences.shape
    log_probs = np.full((B, T), base_prob) + np.random.randn(B, T) * 0.1
    # Higher probability for chosen (first half of vocab)
    mask = sequences < vocab_size // 2
    log_probs[mask] += 0.5
    return log_probs.sum(axis=1)


if __name__ == "__main__":
    np.random.seed(42)
    dataset = PreferenceDataset(n_samples=100, vocab_size=50, seq_len=10)

    chosen, rejected = dataset.generate_batch(batch_size=8)

    policy_log_p_chosen = simulate_log_probs(chosen, base_prob=-0.5)
    policy_log_p_rejected = simulate_log_probs(rejected, base_prob=-1.5)
    ref_log_p_chosen = simulate_log_probs(chosen, base_prob=-1.0)
    ref_log_p_rejected = simulate_log_probs(rejected, base_prob=-1.0)

    loss = dpo_loss(policy_log_p_chosen, policy_log_p_rejected,
                    ref_log_p_chosen, ref_log_p_rejected, beta=0.1)

    print(f"DPO Loss: {loss:.4f}")
    print(f"Policy prefers chosen: {policy_log_p_chosen.mean():.2f} vs rejected: {policy_log_p_rejected.mean():.2f}")
    print(f"DPO increases probability of chosen responses, decreases rejected.")
