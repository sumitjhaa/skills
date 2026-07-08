import numpy as np
import matplotlib.pyplot as plt


def compute_jacobian(f, x, eps=1e-5):
    """Compute Jacobian of f at x via finite differences."""
    if x.ndim == 1:
        x = x.reshape(1, -1)
    n = x.shape[1]
    m = len(f(x[0]))

    J = np.zeros((m, n))
    for i in range(n):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[:, i] += eps
        x_minus[:, i] -= eps
        J[:, i] = (f(x_plus[0]) - f(x_minus[0])) / (2 * eps)

    return J


def lipschitz_estimate(f, X, n_samples=200):
    """Estimate Lipschitz constant via random sampling."""
    n = len(X)
    ratios = []

    for _ in range(n_samples):
        i, j = np.random.randint(n, size=2)
        if i == j:
            continue
        fx_i = f(X[i])
        fx_j = f(X[j])
        num = np.linalg.norm(fx_i - fx_j)
        den = np.linalg.norm(X[i] - X[j])
        if den > 1e-14:
            ratios.append(num / den)

    return max(ratios) if ratios else 0


def nn_forward(W_list, b_list, x, activation='relu'):
    """Simple feedforward neural network."""
    a = x.copy()
    for W, b in zip(W_list[:-1], b_list[:-1]):
        z = W @ a + b
        if activation == 'relu':
            a = np.maximum(z, 0)
        elif activation == 'tanh':
            a = np.tanh(z)

    z = W_list[-1] @ a + b_list[-1]
    return z


def nn_jacobian_condition(W_list, b_list, x):
    """Compute condition number of NN Jacobian at x."""
    def f(x_i):
        return nn_forward(W_list, b_list, x_i)

    J = compute_jacobian(f, x)
    s = np.linalg.svd(J, compute_uv=False)

    if len(s) <= 1 or s[-1] < 1e-14:
        return np.inf, s

    return s[0] / s[-1], s


def fgsm_attack(f, x, y, eps=0.1):
    """Fast Gradient Sign Method adversarial attack."""
    def loss(x_i):
        fx = f(x_i)
        return -fx[y] + np.log(np.sum(np.exp(fx)))

    grad = compute_jacobian(lambda x_i: np.array([loss(x_i)]), x)
    x_adv = x + eps * np.sign(grad[0])
    return x_adv, grad


def spectral_normalize(W):
    """Normalize W by its spectral norm."""
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    return W / s[0]


def main():
    print("=" * 60)
    print("SENSITIVITY AND STABILITY IN ML")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Lipschitz Constant Estimation ---")
    n_samples = 100
    X = np.random.randn(n_samples, 5)

    def linear_fn(x):
        W = np.random.randn(3, 5)
        return W @ x

    L_est = lipschitz_estimate(linear_fn, X, n_samples=500)
    W_actual = np.random.randn(3, 5)
    W_s = np.linalg.svd(W_actual, compute_uv=False)
    L_true = W_s[0]
    print(f"Estimated Lipschitz: {L_est:.4f}")
    print(f"True Lipschitz (||W||_2): {L_true:.4f}")

    print("\n--- Neural Network Jacobian Condition Number ---")
    n_in, n_hidden, n_out = 10, 20, 3
    W_list = [np.random.randn(n_hidden, n_in) / np.sqrt(n_in),
              np.random.randn(n_out, n_hidden) / np.sqrt(n_hidden)]
    b_list = [np.random.randn(n_hidden), np.random.randn(n_out)]

    for _ in range(10):
        x_test = np.random.randn(n_in)
        cond, s = nn_jacobian_condition(W_list, b_list, x_test)
        if np.isfinite(cond):
            print(f"  Sample: cond={cond:.4f}, "
                  f"sigma_max={s[0]:.4f}, sigma_min={s[-1]:.4f}")
            break

    print("\n--- Layer-wise Condition Numbers ---")
    for i, W in enumerate(W_list):
        s_W = np.linalg.svd(W, compute_uv=False)
        cond_W = s_W[0] / s_W[-1] if s_W[-1] > 1e-14 else np.inf
        print(f"  Layer {i}: shape={W.shape}, cond={cond_W:.4f}")

    print("\n--- Spectral Normalization ---")
    W_test = np.random.randn(5, 5)
    spec_before = np.linalg.norm(W_test, 2)
    W_sn = spectral_normalize(W_test)
    spec_after = np.linalg.norm(W_sn, 2)
    print(f"  Spectral norm before: {spec_before:.4f}")
    print(f"  Spectral norm after:  {spec_after:.4f}")

    print("\n--- Adversarial Example (FGSM) ---")
    n_classes = 5
    def classifier(x):
        W_c = np.random.randn(n_classes, 10) * 0.1
        return W_c @ x

    x_clean = np.random.randn(10)
    y_clean = np.argmax(classifier(x_clean))

    for eps in [0.01, 0.05, 0.1, 0.2, 0.5]:
        x_adv, _ = fgsm_attack(classifier, x_clean, y_clean, eps=eps)
        y_adv = np.argmax(classifier(x_adv))
        dist = np.linalg.norm(x_adv - x_clean)
        changed = y_clean != y_adv
        print(f"  eps={eps:.2f}: dist={dist:.4f}, label changed={changed}")

    print("\n--- Lipschitz and Condition Number vs Layer Depth ---")
    depths = [1, 2, 3, 5, 10]
    for depth in depths:
        W_d = [np.random.randn(10, 10) / 3 for _ in range(depth)]
        b_d = [np.random.randn(10) for _ in range(depth)]

        x_d = np.random.randn(10)

        def f_d(x_i):
            return nn_forward(W_d, b_d, x_i)

        L_d = 1.0
        for W in W_d:
            L_d *= np.linalg.norm(W, 2)

        print(f"  Depth {depth}: product of spectral norms = {L_d:.4f}")

    print("\n--- Singular Value Distribution in Deep Networks ---")
    fig, ax = plt.subplots(figsize=(10, 6))
    for depth in [1, 3, 10]:
        W_deep = np.random.randn(depth, 50, 50) / 5
        s_all = []
        for w in W_deep:
            s = np.linalg.svd(w, compute_uv=False)
            s_all.extend(s)
        ax.hist(s_all, bins=30, alpha=0.5, label=f'Depth {depth}')
    ax.set_xlabel('Singular value')
    ax.set_ylabel('Frequency')
    ax.set_title('Singular Value Distribution of Random Weight Matrices')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
