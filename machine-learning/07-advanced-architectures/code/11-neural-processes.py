"""
07.11 Neural Processes: Meta-learn function distribution from context.
"""
import numpy as np
import matplotlib.pyplot as plt

class NeuralProcess:
    def __init__(self, x_dim=1, y_dim=1, r_dim=128):
        self.encoder_W1 = np.random.randn(x_dim + y_dim, 64) * 0.1
        self.encoder_b1 = np.zeros(64)
        self.encoder_W2 = np.random.randn(64, r_dim) * 0.1
        self.encoder_b2 = np.zeros(r_dim)
        self.decoder_W1 = np.random.randn(x_dim + r_dim, 64) * 0.1
        self.decoder_b1 = np.zeros(64)
        self.decoder_W2 = np.random.randn(64, y_dim) * 0.1
        self.decoder_b2 = np.zeros(y_dim)

    def encode(self, x_c, y_c):
        h = np.hstack([x_c, y_c])
        h = np.tanh(h @ self.encoder_W1 + self.encoder_b1)
        h = h @ self.encoder_W2 + self.encoder_b2
        r = np.mean(h, axis=0, keepdims=True)
        return r

    def decode(self, x_t, r):
        r_exp = np.tile(r, (x_t.shape[0], 1))
        h = np.hstack([x_t, r_exp])
        h = np.tanh(h @ self.decoder_W1 + self.decoder_b1)
        mu = h @ self.decoder_W2 + self.decoder_b2
        return mu

    def forward(self, x_c, y_c, x_t):
        r = self.encode(x_c, y_c)
        mu = self.decode(x_t, r)
        return mu

def test_multi_context(model, x_target, n_trials=5):
    results = []
    for _ in range(n_trials):
        x_c = np.random.uniform(-2, 2, (10, 1))
        y_c = np.sin(x_c) + 0.05 * np.random.randn(10, 1)
        y_p = model.forward(x_c, y_c, x_target)
        results.append((x_c, y_c, y_p))
    return results

def test_context_size(model, x_target, x_truth, sizes=[3, 10, 30]):
    results = {}
    for n_ctx in sizes:
        x_c = np.random.uniform(-2, 2, (n_ctx, 1))
        y_c = np.sin(x_c) + 0.05 * np.random.randn(n_ctx, 1)
        y_p = model.forward(x_c, y_c, x_target)
        mse = np.mean((y_p - x_truth)**2)
        results[n_ctx] = (x_c, y_c, y_p, mse)
    return results

if __name__ == "__main__":
    np.random.seed(42)
    print("=== Neural Processes ===\n")

    model = NeuralProcess()

    # Basic forward
    x_context = np.random.uniform(-2, 2, (10, 1))
    y_context = np.sin(x_context) + 0.05 * np.random.randn(10, 1)
    x_target = np.linspace(-3, 3, 100).reshape(-1, 1)
    y_true = np.sin(x_target)

    y_pred = model.forward(x_context, y_context, x_target)

    print(f"Context: {x_context.shape}")
    print(f"Target:  {x_target.shape}")
    print(f"Output:  {y_pred.shape}")
    print(f"MSE vs true: {np.mean((y_pred - y_true)**2):.4f}")

    # Test with different context sets
    print("\nMultiple context sets:")
    multi_results = test_multi_context(model, x_target, 5)
    mses = [np.mean((r[2] - y_true)**2) for r in multi_results]
    print(f"  MSE range: {min(mses):.4f} to {max(mses):.4f}")

    # Test with different context sizes
    print("\nEffect of context size:")
    size_results = test_context_size(model, x_target, y_true, [3, 10, 30])
    for n_ctx, (_, _, _, mse) in size_results.items():
        print(f"  n_ctx={n_ctx:2d}: MSE={mse:.4f}")

    # Latent representation analysis
    print("\nLatent representation:")
    r_all = []
    for _ in range(100):
        x_c = np.random.uniform(-2, 2, (15, 1))
        y_c = np.sin(x_c) + 0.05 * np.random.randn(15, 1)
        r = model.encode(x_c, y_c).ravel()
        r_all.append(r)
    r_all = np.array(r_all)
    print(f"  Latent codes: {r_all.shape}")
    print(f"  Mean latent norm: {np.linalg.norm(r_all, axis=1).mean():.4f}")
    print(f"  Latent variance (first 5 dims): "
          f"{[f'{v:.4f}' for v in np.var(r_all, axis=0)[:5]]}")

    # Visualization
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Single prediction with uncertainty
    axes[0, 0].scatter(x_context, y_context, c='r', s=50, label='Context')
    axes[0, 0].plot(x_target, y_pred, 'b-', lw=2, label='NP prediction')
    axes[0, 0].plot(x_target, y_true, 'g--', alpha=0.7, label='True function')
    axes[0, 0].set_title("Neural Process: Function Regression")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Multiple predictions
    for i, (xc, yc, yp) in enumerate(multi_results):
        axes[0, 1].plot(x_target, yp, lw=1, alpha=0.5, label=f'Trial {i + 1}')
    axes[0, 1].plot(x_target, y_true, 'k--', lw=2, label='True')
    axes[0, 1].set_title("Multiple Context Sets → Different Predictions")
    axes[0, 1].grid(True, alpha=0.3)

    # Context size effect
    for n_ctx, (xc, yc, yp, _) in size_results.items():
        axes[0, 2].plot(x_target, yp, lw=1.5, label=f'n_ctx={n_ctx}')
    axes[0, 2].plot(x_target, y_true, 'k--', lw=2, label='True')
    axes[0, 2].set_title("Effect of Context Size")
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)

    # Prediction error by position
    errors = np.array([np.abs(r[2].ravel() - y_true.ravel()) for r in multi_results])
    axes[1, 0].plot(x_target, errors.mean(axis=0), 'b-', label='Mean |error|')
    axes[1, 0].fill_between(x_target.ravel(), errors.min(axis=0), errors.max(axis=0),
                            alpha=0.2, label='Range')
    axes[1, 0].axvspan(-2, 2, alpha=0.1, color='g', label='Context region')
    axes[1, 0].set_title("Prediction Error vs Position")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Latent representation visualization
    im = axes[1, 1].imshow(r_all[:20, :10].T, aspect='auto', cmap='viridis')
    axes[1, 1].set_xlabel("Function sample")
    axes[1, 1].set_ylabel("Latent dim (first 10)")
    axes[1, 1].set_title("Latent Codes (first 20 functions)")
    plt.colorbar(im, ax=axes[1, 1])

    # Latent dimension variance
    axes[1, 2].bar(range(20), np.var(r_all, axis=0)[:20])
    axes[1, 2].set_xlabel("Latent dimension")
    axes[1, 2].set_ylabel("Variance across functions")
    axes[1, 2].set_title("Latent Dimension Activity")
    axes[1, 2].grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase07/neural_process.png")
    plt.close()
    print("\nFigure saved to neural_process.png")

    # Edge cases
    print("\n=== Edge Cases ===")
    x_c_small = np.random.uniform(-2, 2, (3, 1))
    y_c_small = np.sin(x_c_small) + 0.05 * np.random.randn(3, 1)
    y_p_small = model.forward(x_c_small, y_c_small, x_target[:5])
    print(f"  3 context points: output={y_p_small.ravel()[:3]}")

    x_c_large = np.random.uniform(-2, 2, (50, 1))
    y_c_large = np.sin(x_c_large) + 0.05 * np.random.randn(50, 1)
    y_p_large = model.forward(x_c_large, y_c_large, x_target[:5])
    print(f"  50 context points: output={y_p_large.ravel()[:3]}")

    # Different latent dimensions
    for r_dim in [16, 64, 256]:
        m = NeuralProcess(r_dim=r_dim)
        y_p = m.forward(x_context, y_context, x_target)
        mse_r = np.mean((y_p - y_true)**2)
        print(f"  r_dim={r_dim:3d}: MSE={mse_r:.4f}")
