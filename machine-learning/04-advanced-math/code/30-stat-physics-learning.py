"""04.30 Statistical physics of learning: teacher-student."""
import numpy as np
from scipy.special import erfc

def teacher_student_perceptron(n_features=100, n_samples_range=(10, 500), n_trials=5):
    """Generalization error of a perceptron."""
    np.random.seed(0)
    results = []
    for n_samples in np.linspace(*n_samples_range, 20).astype(int):
    for n_samples in np.linspace(*n_samples_range, 20).astype(int):
        gen_errors = []
        for _ in range(n_trials):
            w_true = np.random.randn(n_features)
            w_true /= np.linalg.norm(w_true)
            X = np.random.randn(n_samples, n_features)
            y = np.sign(X @ w_true)
            # Linear regression solution
            w_hat = np.linalg.lstsq(X, y, rcond=None)[0]
            # Generalization error = angle between w_hat and w_true
            cos_angle = np.dot(w_hat, w_true) / (np.linalg.norm(w_hat) * np.linalg.norm(w_true))
            gen_err = np.arccos(np.clip(cos_angle, -1, 1)) / np.pi
            gen_errors.append(gen_err)
        results.append((n_samples / n_features, np.mean(gen_errors)))
    return np.array(results)

results = teacher_student_perceptron(50, (10, 300), 3)
print("Teacher-student perceptron (alpha = n_samples/n_features):")
for alpha, err in results[::4]:
    print(f"  alpha={alpha:.2f}, gen_error={err:.4f}")

# GP equivalence of wide networks
def ntk_kernel(X1, X2, width=1000):
    """Approximate NTK for a wide 1-hidden-layer ReLU network."""
    np.random.seed(0)
    W = np.random.randn(width, X1.shape[1]) / np.sqrt(X1.shape[1])
    b = np.random.randn(width)
    phi1 = np.maximum(X1 @ W.T + b, 0)
    phi2 = np.maximum(X2 @ W.T + b, 0)
    return (phi1 @ phi2.T) / width

X = np.random.randn(10, 5)
K = ntk_kernel(X, X, width=500)
print(f"\nNTK kernel matrix (10x10) trace: {np.trace(K):.4f}")
print(f"Kernel rank: {np.linalg.matrix_rank(K, tol=1e-6)}")

# Double descent simulation
def double_descent(n_train=50, n_features_range=None, noise=0.1):
    np.random.seed(0)
    if n_features_range is None:
        n_features_range = np.arange(5, 200, 10)
    X = np.random.randn(n_train, 200)
    w_true = np.random.randn(200)
    y = X @ w_true + noise * np.random.randn(n_train)
    errors = []
    for d in n_features_range:
        X_sub = X[:, :d]
        w_hat = np.linalg.lstsq(X_sub, y, rcond=None)[0]
        # Test error on fresh data
        X_test = np.random.randn(1000, d)
        y_test = X_test @ w_true[:d] + noise * np.random.randn(1000)
        err = np.mean((y_test - X_test @ w_hat)**2)
        errors.append(err)
    return n_features_range, errors

feats, errs = double_descent(50, np.arange(5, 150, 10))
print(f"\nDouble descent near interpolation (d~n):")
for d, e in zip(feats[::3], errs[::3]):
    print(f"  d={d:3d}, test_error={e:.4f}")
