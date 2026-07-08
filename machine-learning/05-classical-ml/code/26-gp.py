"""Gaussian Processes from scratch with multiple kernels and visualization."""
import numpy as np
import matplotlib.pyplot as plt

def rbf_kernel(x1, x2, l=1.0, sigma_f=1.0):
    sq_dist = np.sum(x1**2, axis=1)[:, None] + np.sum(x2**2, axis=1)[None, :] - 2 * x1 @ x2.T
    return sigma_f**2 * np.exp(-0.5 / l**2 * sq_dist)

def matern_kernel(x1, x2, l=1.0, sigma_f=1.0, nu=1.5):
    sq_dist = np.sum(x1**2, axis=1)[:, None] + np.sum(x2**2, axis=1)[None, :] - 2 * x1 @ x2.T
    d = np.sqrt(np.maximum(sq_dist, 0))
    if nu == 0.5:
        return sigma_f**2 * np.exp(-d / l)
    elif nu == 1.5:
        arg = np.sqrt(3) * d / l
        return sigma_f**2 * (1 + arg) * np.exp(-arg)
    elif nu == 2.5:
        arg = np.sqrt(5) * d / l
        return sigma_f**2 * (1 + arg + arg**2 / 3) * np.exp(-arg)
    return sigma_f**2 * np.exp(-0.5 / l**2 * sq_dist)

def periodic_kernel(x1, x2, l=1.0, sigma_f=1.0, p=1.0):
    diff = x1[:, None, :] - x2[None, :, :]
    sq_sin = np.sin(np.pi * diff / p) ** 2
    return sigma_f**2 * np.exp(-2 * np.sum(sq_sin, axis=-1) / l**2)

class GaussianProcess:
    def __init__(self, kernel=rbf_kernel, sigma_n=1e-2):
        self.kernel = kernel
        self.sigma_n = sigma_n

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        K = self.kernel(X, X)
        K.flat[::K.shape[0] + 1] += self.sigma_n**2
        for extra_jitter in [0, 1e-6, 1e-4, 1e-2]:
            try:
                L = np.linalg.cholesky(K + extra_jitter * np.eye(X.shape[0]))
                self.L_ = L
                break
            except np.linalg.LinAlgError:
                continue
        else:
            K.flat[::K.shape[0] + 1] += 0.1
            self.L_ = np.linalg.cholesky(K)
        self.alpha_ = np.linalg.solve(self.L_.T, np.linalg.solve(self.L_, y))
        return self

    def predict(self, X_test, return_std=False):
        K_s = self.kernel(self.X_train, X_test)
        K_ss = self.kernel(X_test, X_test) + 1e-10 * np.eye(X_test.shape[0])
        mu = K_s.T @ self.alpha_
        v = np.linalg.solve(self.L_, K_s)
        cov = K_ss - v.T @ v
        if return_std:
            return mu, np.sqrt(np.maximum(np.diag(cov), 0))
        return mu

    def sample_prior(self, X_test, n_samples=5):
        K = self.kernel(X_test, X_test)
        L = np.linalg.cholesky(K + 1e-8 * np.eye(X_test.shape[0]))
        return L @ np.random.randn(X_test.shape[0], n_samples)

    def sample_posterior(self, X_test, n_samples=5):
        mu = self.predict(X_test)
        K_s = self.kernel(self.X_train, X_test)
        K_ss = self.kernel(X_test, X_test)
        v = np.linalg.solve(self.L_, K_s)
        cov = K_ss - v.T @ v
        L = np.linalg.cholesky(cov + 1e-8 * np.eye(X_test.shape[0]))
        return mu[:, None] + L @ np.random.randn(X_test.shape[0], n_samples)

if __name__ == "__main__":
    np.random.seed(42)
    X = np.linspace(-5, 5, 20).reshape(-1, 1)
    y = np.sin(X).ravel() + np.random.randn(20) * 0.1
    X_test = np.linspace(-6, 6, 200).reshape(-1, 1)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. RBF kernel GP
    gp_rbf = GaussianProcess(kernel=rbf_kernel, sigma_n=0.1)
    gp_rbf.fit(X, y)
    mu, std = gp_rbf.predict(X_test, return_std=True)

    axes[0, 0].fill_between(X_test.ravel(), mu - 2 * std, mu + 2 * std, alpha=0.2, color='C0')
    axes[0, 0].plot(X_test, mu, 'C0-', label='GP mean')
    axes[0, 0].scatter(X, y, c='r', s=30, label='Data')
    axes[0, 0].plot(X_test, np.sin(X_test), 'g--', alpha=0.5, label='True')
    axes[0, 0].set_title("RBF Kernel GP")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Matern kernel (nu=1.5)
    gp_mat = GaussianProcess(kernel=lambda x1, x2: matern_kernel(x1, x2, l=1.0, sigma_f=1.0, nu=1.5), sigma_n=0.1)
    gp_mat.fit(X, y)
    mu_m, std_m = gp_mat.predict(X_test, return_std=True)

    axes[0, 1].fill_between(X_test.ravel(), mu_m - 2 * std_m, mu_m + 2 * std_m, alpha=0.2, color='C1')
    axes[0, 1].plot(X_test, mu_m, 'C1-', label='GP mean')
    axes[0, 1].scatter(X, y, c='r', s=30, label='Data')
    axes[0, 1].plot(X_test, np.sin(X_test), 'g--', alpha=0.5, label='True')
    axes[0, 1].set_title("Matern (ν=1.5) GP")
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Prior samples (RBF)
    gp_prior = GaussianProcess(kernel=rbf_kernel)
    prior_samples = gp_prior.sample_prior(X_test, n_samples=5)
    for i in range(5):
        axes[0, 2].plot(X_test, prior_samples[:, i], lw=1, alpha=0.7)
    axes[0, 2].set_title("GP Prior Samples (RBF)")
    axes[0, 2].grid(True, alpha=0.3)

    # 4. Posterior samples
    post_samples = gp_rbf.sample_posterior(X_test, n_samples=5)
    axes[1, 0].plot(X_test, mu, 'k-', lw=2, label='Mean')
    for i in range(5):
        axes[1, 0].plot(X_test, post_samples[:, i], lw=1, alpha=0.5)
    axes[1, 0].scatter(X, y, c='r', s=30)
    axes[1, 0].set_title("GP Posterior Samples")
    axes[1, 0].grid(True, alpha=0.3)

    # 5. Lengthscale sensitivity
    for l, c in zip([0.3, 1.0, 3.0], ['C0', 'C1', 'C2']):
        gp_l = GaussianProcess(kernel=lambda x1, x2: rbf_kernel(x1, x2, l=l), sigma_n=0.1)
        gp_l.fit(X, y)
        mu_l, _ = gp_l.predict(X_test, return_std=True)
        axes[1, 1].plot(X_test, mu_l, c=c, label=f'l={l}')
    axes[1, 1].scatter(X, y, c='r', s=20)
    axes[1, 1].set_title("Lengthscale Sensitivity")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # 6. Periodic kernel
    gp_per = GaussianProcess(kernel=lambda x1, x2: periodic_kernel(x1, x2, l=1.0, sigma_f=1.0, p=np.pi), sigma_n=0.3)
    gp_per.fit(X, y)
    mu_p, std_p = gp_per.predict(X_test, return_std=True)
    axes[1, 2].fill_between(X_test.ravel(), mu_p - 2 * std_p, mu_p + 2 * std_p, alpha=0.2, color='C3')
    axes[1, 2].plot(X_test, mu_p, 'C3-')
    axes[1, 2].scatter(X, y, c='r', s=20)
    axes[1, 2].set_title("Periodic Kernel GP")
    axes[1, 2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/26-gp.png")
    plt.close()
    print("Figure saved to 26-gp.png")

    # Quantitative analysis
    print("=== Gaussian Process Analysis ===")
    test_truth = np.sin(X_test).ravel()
    mse_rbf = np.mean((mu - test_truth)**2)
    mse_mat = np.mean((mu_m - test_truth)**2)
    mse_per = np.mean((mu_p - test_truth)**2)
    print(f"  RBF MSE:       {mse_rbf:.6f}")
    print(f"  Matern MSE:    {mse_mat:.6f}")
    print(f"  Periodic MSE:  {mse_per:.6f}")

    # Edge case: single data point
    print("\n=== Edge Cases ===")
    X1 = np.array([[0.0]])
    y1 = np.array([1.0])
    gp = GaussianProcess(sigma_n=0.1)
    gp.fit(X1, y1)
    mu1, std1 = gp.predict(X_test[:5], return_std=True)
    print(f"  Single point: predictions={mu1.ravel()[:3]}, stds={std1[:3]}")

    # Edge case: noise-free data
    X_clean = np.linspace(-3, 3, 10).reshape(-1, 1)
    y_clean = np.sin(X_clean).ravel()
    gp_clean = GaussianProcess(sigma_n=1e-6)
    gp_clean.fit(X_clean, y_clean)
    mu_c, std_c = gp_clean.predict(X_clean, return_std=True)
    print(f"  Noise-free: max error={np.max(np.abs(mu_c - y_clean)):.2e}")
