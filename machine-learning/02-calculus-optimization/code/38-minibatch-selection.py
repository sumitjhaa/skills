import numpy as np
import matplotlib.pyplot as plt

def importance_sampled_batch(losses, gradients, batch_size, temperature=1.0):
    norms = np.array([np.linalg.norm(g) for g in gradients])
    weights = norms ** temperature
    weights = weights / weights.sum()
    idx = np.random.choice(len(gradients), size=batch_size, p=weights)
    return idx

def self_paced_batch(losses, batch_size, epoch, total_epochs):
    threshold = epoch / total_epochs
    threshold_loss = np.percentile(losses, threshold * 100)
    eligible = np.where(losses <= threshold_loss)[0]
    if len(eligible) < batch_size:
        eligible = np.arange(len(losses))
    return np.random.choice(eligible, size=batch_size)

def gradient_diversity(gradients):
    n = len(gradients)
    grad_mean = np.mean(gradients, axis=0)
    grad_var = np.mean([np.linalg.norm(g - grad_mean)**2 for g in gradients])
    return grad_var / (np.linalg.norm(grad_mean)**2 + 1e-10)

def main():
    print("=" * 60)
    print("MINI-BATCH SELECTION STRATEGIES")
    print("=" * 60)

    print("\n--- Importance Sampling vs Uniform Sampling ---")
    np.random.seed(42)
    n_samples = 1000
    d = 10
    X = np.random.randn(n_samples, d)
    w_true = np.random.randn(d)
    y = X @ w_true + 0.1 * np.random.randn(n_samples)
    batch_size = 32

    trajectories = {}
    for strategy in ['uniform', 'importance']:
        np.random.seed(42)
        w = np.zeros(d)
        losses = []
        for epoch in range(50):
            grad_all = np.array([X[i] * (X[i] @ w - y[i]) for i in range(n_samples)])
            if strategy == 'importance':
                batch = importance_sampled_batch(np.zeros(n_samples),
                                                  [g for g in grad_all],
                                                  batch_size, temperature=0.5)
            else:
                batch = np.random.choice(n_samples, batch_size)

            g = np.mean([X[i] * (X[i] @ w - y[i]) for i in batch], axis=0)
            w = w - 0.1 * g
            losses.append(np.mean((X @ w - y)**2))

        trajectories[strategy] = np.array(losses)
        print(f"  {strategy:10s}: final loss = {losses[-1]:.6f}")

    print(f"\n--- Self-Paced Learning ---")
    np.random.seed(42)
    losses_all = np.abs(np.random.randn(n_samples)) * 2 + 1
    for epoch in range(0, 11, 2):
        batch = self_paced_batch(losses_all, 32, epoch, 10)
        avg_loss = losses_all[batch].mean()
        print(f"  epoch {epoch:2d}: avg sample loss in batch = {avg_loss:.4f}")

    print(f"\n--- Gradient Diversity Across Minibatches ---")
    np.random.seed(42)
    w_test = np.random.randn(d)
    grad_all = np.array([X[i] * (X[i] @ w_test - y[i]) for i in range(n_samples)])

    for bs in [4, 16, 64, 256, 1000]:
        batch = np.random.choice(n_samples, min(bs, n_samples), replace=False)
        batch_grads = [grad_all[i] for i in batch]
        div = gradient_diversity(batch_grads)
        print(f"  batch size {bs:4d}: gradient diversity = {div:.4f}")

    print(f"\n--- Adaptive Batch Size ---")
    def adaptive_batch_size(t, initial=32, factor=1.1):
        return min(8192, int(initial * factor ** t))

    for t in [0, 5, 10, 20, 50, 100]:
        print(f"  iter {t:3d}: batch size = {adaptive_batch_size(t):5d}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for strategy, loss in trajectories.items():
        axes[0].semilogy(loss, label=strategy, linewidth=2)
    axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('MSE')
    axes[0].set_title('Uniform vs Importance Sampling')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    batch_sizes = [4, 16, 64, 256, 1000]
    diversities = []
    for bs in batch_sizes:
        batch = np.random.choice(n_samples, min(bs, n_samples), replace=False)
        batch_grads = [grad_all[i] for i in batch]
        diversities.append(gradient_diversity(batch_grads))
    axes[1].plot(batch_sizes, diversities, 'bo-', linewidth=2)
    axes[1].set_xlabel('Batch Size'); axes[1].set_ylabel('Gradient Diversity')
    axes[1].set_title('Gradient Diversity vs Batch Size')
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/38_minibatch_selection.png', dpi=100)
    print(f"\nPlot saved to /tmp/38_minibatch_selection.png")

if __name__ == "__main__":
    main()
