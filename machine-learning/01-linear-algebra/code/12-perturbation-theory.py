import numpy as np
import matplotlib.pyplot as plt


def condition_number_svd(A):
    """Condition number via SVD."""
    s = np.linalg.svd(A, compute_uv=False)
    return s[0] / s[-1]


def backward_error(A, b, x):
    """Compute backward error for linear system Ax = b with computed x."""
    r = A @ x - b
    eta = np.linalg.norm(r) / (np.linalg.norm(A) * np.linalg.norm(x) + np.linalg.norm(b))
    return eta


def forward_error(x_true, x_computed):
    """Compute forward (relative) error."""
    return np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)


def perturbation_experiment(A, x_true, eps=1e-8, n_trials=100):
    """Perturb A and b, measure forward/backward errors."""
    b = A @ x_true
    forward_errors = []
    backward_errors = []
    predicted_errors = []
    cond = condition_number_svd(A)

    for _ in range(n_trials):
        dA = np.random.randn(*A.shape) * eps * np.linalg.norm(A)
        db = np.random.randn(*b.shape) * eps * np.linalg.norm(b)

        A_pert = A + dA
        b_pert = b + db

        x_pert = np.linalg.solve(A_pert, b_pert)

        fwd = forward_error(x_true, x_pert)
        bwd = backward_error(A_pert, b_pert, x_pert)
        predicted = cond * (np.linalg.norm(dA) / np.linalg.norm(A) +
                           np.linalg.norm(db) / np.linalg.norm(b))

        forward_errors.append(fwd)
        backward_errors.append(bwd)
        predicted_errors.append(predicted)

    return np.array(forward_errors), np.array(backward_errors), \
           np.array(predicted_errors), cond


def create_ill_conditioned(n, cond_desired):
    """Create a matrix with a desired condition number."""
    U, _, Vt = np.linalg.svd(np.random.randn(n, n))
    s = np.logspace(0, -np.log10(cond_desired), n)
    return U @ np.diag(s) @ Vt


def main():
    print("=" * 60)
    print("PERTURBATION THEORY AND CONDITION NUMBERS")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- Condition Number Estimation ---")
    A_well = np.random.randn(5, 5)
    A_ill = create_ill_conditioned(5, 1e8)

    print(f"Well-conditioned cond: {condition_number_svd(A_well):.4f}")
    print(f"Ill-conditioned cond:  {condition_number_svd(A_ill):.4f}")

    print("\n--- Forward/Backward Error ---")
    for A, name in [(A_well, "well-conditioned"), (A_ill, "ill-conditioned")]:
        x_true = np.random.randn(5)
        b = A @ x_true
        x_solved = np.linalg.solve(A, b)
        fwd = forward_error(x_true, x_solved)
        bwd = backward_error(A, b, x_solved)
        print(f"{name}: forward={fwd:.2e}, backward={bwd:.2e}")
        print(f"  Residual: {np.linalg.norm(A @ x_solved - b):.2e}")

    print("\n--- Perturbation Theory Verification ---")
    x_true = np.random.randn(5)
    eps_values = [1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for A, name, color, marker in [(A_well, "Well-Conditioned", 'b', 'o'),
                                     (A_ill, "Ill-Conditioned", 'r', 's')]:
        max_fwd = []
        mean_pred = []

        for eps in eps_values:
            fwd_errs, _, pred_errs, cond = perturbation_experiment(
                A, x_true, eps=eps, n_trials=50)
            max_fwd.append(np.max(fwd_errs))
            mean_pred.append(np.mean(pred_errs))

        axes[0].loglog(eps_values, max_fwd, f'{marker}-{color}',
                       label=f'{name} (actual)')
        axes[0].loglog(eps_values, mean_pred, f'--{color}',
                       label=f'{name} (predicted)')

    axes[0].set_xlabel('Perturbation magnitude ε')
    axes[0].set_ylabel('Forward Error')
    axes[0].set_title('Forward Error vs Perturbation')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    print("\n--- Condition Number vs Error ---")
    conds = np.logspace(1, 10, 20)
    actual_errors = []
    predicted_bounds = []

    for cond_desired in conds:
        A = create_ill_conditioned(5, cond_desired)
        n_trials = 20

        eps = 1e-10
        fwd_errs, _, pred_errs, actual_cond = perturbation_experiment(
            A, x_true, eps=eps, n_trials=n_trials)

        actual_errors.append(np.median(fwd_errs))
        predicted_bounds.append(np.median(pred_errs))

    axes[1].loglog(conds, actual_errors, 'go-', label='Actual error')
    axes[1].loglog(conds, predicted_bounds, 'b--', label='Predicted bound')
    axes[1].loglog(conds, conds * eps, 'r:', label=f'κ · ε (ε={eps})')
    axes[1].set_xlabel('Condition Number κ')
    axes[1].set_ylabel('Forward Error')
    axes[1].set_title('Error vs Condition Number')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("\n--- Componentwise Perturbation ---")
    A = np.array([[1, 1], [1, 1.0001]])
    x_true = np.array([1, 1])
    b = A @ x_true

    for eps in [1e-6, 1e-4, 1e-2]:
        dA = np.random.randn(2, 2) * eps
        db = np.random.randn(2) * eps * 10

        x_pert = np.linalg.solve(A + dA, b + db)
        fwd = forward_error(x_true, x_pert)

        print(f"eps={eps}: x={np.round(x_pert, 6)}, forward_error={fwd:.2e}")

    print("\n--- Stability of Different Factorizations ---")
    n = 10
    A = create_ill_conditioned(n, 1e6)
    x_true = np.random.randn(n)
    b = A @ x_true

    x_lu = np.linalg.solve(A, b)
    Q, R = np.linalg.qr(A)
    x_qr = np.linalg.solve(R, Q.T @ b)
    U, s, Vt = np.linalg.svd(A)
    x_svd = Vt.T @ np.diag(1 / s) @ U.T @ b

    print(f"LU solve error:  {forward_error(x_true, x_lu):.2e}")
    print(f"QR solve error:  {forward_error(x_true, x_qr):.2e}")
    print(f"SVD solve error: {forward_error(x_true, x_svd):.2e}")


if __name__ == "__main__":
    main()
