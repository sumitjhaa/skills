"""
07.30 SOTA Reproduction guide and minimal benchmark.
"""
import numpy as np
import matplotlib.pyplot as plt
import time


def benchmark_speed(name, fn, n_runs=10):
    times = []
    for _ in range(n_runs):
        t0 = time.time()
        fn()
        times.append(time.time() - t0)
    return np.mean(times), np.std(times)


def verify_learning_rate(lr, model_fn, data_fn, epochs=200):
    """Check if a given LR works for the model."""
    X, y = data_fn()
    params = [np.random.randn(8, 16) * 0.1, np.zeros(16),
              np.random.randn(16, 1) * 0.1, np.zeros(1)]
    losses = []
    for epoch in range(epochs):
        h = np.maximum(X @ params[0] + params[1], 0)
        y_pred = h @ params[2] + params[3]
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        grad = 2 * (y_pred - y) / len(X)
        params[0] -= lr * (X.T @ (grad @ params[2].T * (h > 0)))
        params[2] -= lr * (h.T @ grad)
        params[3] -= lr * grad.mean(axis=0)
    return losses


class Reproduction:
    """Template for reproducing a paper result."""
    def __init__(self, paper_name):
        self.paper_name = paper_name
        self.results = {}

    def add_result(self, metric, value, expected=None):
        self.results[metric] = {'value': value, 'expected': expected, 'match': None}
        if expected is not None:
            self.results[metric]['match'] = abs(value - expected) < 0.1

    def report(self):
        print(f"\n=== Reproduction Report: {self.paper_name} ===")
        for k, v in self.results.items():
            status = "✓" if v['match'] else "?" if v['match'] is None else "✗"
            print(f"  {status} {k}: {v['value']:.4f} (expected: {v['expected']})")


if __name__ == "__main__":
    np.random.seed(42)
    print("=== SOTA Reproduction Guide ===\n")

    # Benchmark different operations
    sizes = [100, 500, 1000]
    for n in sizes:
        A = np.random.randn(n, n)
        def matmul():
            return A @ A
        mean_t, std_t = benchmark_speed(f'Matmul {n}x{n}', matmul)
        print(f"Matmul {n}x{n}: {mean_t*1000:.2f} ± {std_t*1000:.2f} ms")

    print("\n=== LR Verification ===")
    def data():
        X = np.random.randn(200, 8)
        y = np.sin(X[:, 0:1]) + 0.1 * np.random.randn(200, 1)
        return X, y

    for lr in [0.1, 0.01, 0.001]:
        losses = verify_learning_rate(lr, None, data, epochs=200)
        final_loss = losses[-1]
        print(f"  LR={lr:.3f}: final loss={final_loss:.6f}")

    print("\n=== Reproduction Report ===")
    # Simulate reproducing a paper: "MLP for regression on synthetic data"
    repro = Reproduction("Example et al. 2024")
    repro.add_result("Test MSE", 0.042, expected=0.05)
    repro.add_result("Train MSE", 0.038, expected=0.04)
    repro.report()

    plt.figure(figsize=(8, 4))
    for i, lr in enumerate([0.1, 0.01, 0.001]):
        losses = verify_learning_rate(lr, None, data, epochs=200)
        plt.plot(losses, label=f'LR={lr}')
    plt.yscale('log')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend()
    plt.title('Learning Rate Sensitivity')
    plt.savefig('../../assets/phase07/sota_reproduction.png')
    plt.close()
    print("\nSaved sota_reproduction.png")
