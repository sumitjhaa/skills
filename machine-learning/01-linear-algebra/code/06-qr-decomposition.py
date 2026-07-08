import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import qr as scipy_qr


def cgs_qr(A):
    """Classical Gram-Schmidt QR."""
    m, n = A.shape
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)

    for i in range(n):
        v = A[:, i].astype(float).copy()
        for j in range(i):
            R[j, i] = np.dot(Q[:, j], A[:, i])
            v -= R[j, i] * Q[:, j]
        R[i, i] = np.linalg.norm(v)
        if R[i, i] < 1e-14:
            raise ValueError("Matrix is rank deficient")
        Q[:, i] = v / R[i, i]

    return Q, R


def mgs_qr(A):
    """Modified Gram-Schmidt QR (more stable)."""
    m, n = A.shape
    Q = A.astype(float).copy()
    R = np.zeros((n, n), dtype=float)

    for i in range(n):
        R[i, i] = np.linalg.norm(Q[:, i])
        if R[i, i] < 1e-14:
            raise ValueError("Matrix is rank deficient")
        Q[:, i] /= R[i, i]
        for j in range(i + 1, n):
            R[i, j] = np.dot(Q[:, i], Q[:, j])
            Q[:, j] -= R[i, j] * Q[:, i]

    return Q, R


def householder_qr(A):
    """Householder reflector QR decomposition."""
    m, n = A.shape
    R = A.astype(float).copy()
    Q = np.eye(m)

    for k in range(n):
        x = R[k:, k]
        norm_x = np.linalg.norm(x)

        if norm_x < 1e-14:
            continue

        v = x.copy()
        v[0] += np.sign(x[0]) * norm_x if x[0] != 0 else norm_x
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-14:
            continue
        v = v / v_norm

        R[k:, k:] -= 2 * np.outer(v, v @ R[k:, k:])

        Qk = np.eye(m)
        Qk[k:, k:] -= 2 * np.outer(v, v)
        Q = Q @ Qk.T

    return Q[:, :n], np.triu(R[:n, :n])


def givens_rotation(a, b):
    """Compute Givens rotation (c, s) such that [c -s; s c] [a; b] = [r; 0]."""
    if abs(b) < 1e-14:
        return 1.0, 0.0, a
    r = np.hypot(a, b)
    c = a / r
    s = -b / r
    return c, s, r


def givens_qr(A):
    """Givens rotation QR decomposition."""
    m, n = A.shape
    R = A.astype(float).copy()
    Q = np.eye(m)

    for j in range(n):
        for i in range(m - 1, j, -1):
            a = R[j, j]
            b = R[i, j]
            if abs(b) < 1e-14 and abs(a) < 1e-14:
                continue
            c, s, r = givens_rotation(a, b)
            G = np.array([[c, -s], [s, c]])
            R[[j, i], j:] = G @ R[[j, i], j:]
            Q[[j, i], :] = G @ Q[[j, i], :]

    return Q.T, np.triu(R[:n, :n])


def qr_lstsq(A, b):
    """Solve least squares Ax = b using QR."""
    Q, R = mgs_qr(A)
    n = R.shape[1]
    y = Q.T @ b
    return np.linalg.solve(R[:n], y[:n])


def stability_comparison():
    """Compare numerical stability of different QR methods."""
    n = 20
    results = {'cond': [], 'cgs_err': [], 'mgs_err': [], 'house_err': [], 'givens_err': []}

    for _ in range(50):
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        cond = np.random.uniform(1, 1e12)
        s = np.logspace(0, -np.log10(cond), n)
        A = U @ np.diag(s) @ Vt

        Q_ref, R_ref = np.linalg.qr(A)

        cgs_err = np.linalg.norm(cgs_qr(A)[0].T @ cgs_qr(A)[0] - np.eye(n))
        mgs_err = np.linalg.norm(mgs_qr(A)[0].T @ mgs_qr(A)[0] - np.eye(n))
        h_err = np.linalg.norm(householder_qr(A)[0].T @ householder_qr(A)[0] - np.eye(n))
        g_err = np.linalg.norm(givens_qr(A)[0].T @ givens_qr(A)[0] - np.eye(n))

        results['cond'].append(cond)
        results['cgs_err'].append(cgs_err)
        results['mgs_err'].append(mgs_err)
        results['house_err'].append(h_err)
        results['givens_err'].append(g_err)

    return results


def main():
    print("=" * 60)
    print("QR DECOMPOSITION - Gram-Schmidt, Householder, Givens")
    print("=" * 60)

    A = np.array([[1.0, -1.0, 4.0],
                  [1.0, 4.0, -2.0],
                  [1.0, 4.0, 2.0],
                  [1.0, -1.0, 0.0]])

    print(f"\nA =\n{A}")

    print("\n--- Classical Gram-Schmidt ---")
    Q_cgs, R_cgs = cgs_qr(A)
    print(f"Q:\n{np.round(Q_cgs, 4)}")
    print(f"R:\n{np.round(R_cgs, 4)}")
    print(f"Q^T Q:\n{np.round(Q_cgs.T @ Q_cgs, 4)}")
    print(f"QR == A: {np.allclose(Q_cgs @ R_cgs, A)}")

    print("\n--- Modified Gram-Schmidt ---")
    Q_mgs, R_mgs = mgs_qr(A)
    print(f"Q^T Q:\n{np.round(Q_mgs.T @ Q_mgs, 4)}")
    print(f"QR == A: {np.allclose(Q_mgs @ R_mgs, A)}")

    print("\n--- Householder ---")
    Q_h, R_h = householder_qr(A)
    print(f"Q:\n{np.round(Q_h, 4)}")
    print(f"R:\n{np.round(R_h, 4)}")
    print(f"Q^T Q:\n{np.round(Q_h.T @ Q_h, 4)}")
    print(f"QR == A: {np.allclose(Q_h @ R_h, A)}")

    print("\n--- Givens Rotations ---")
    Q_g, R_g = givens_qr(A)
    print(f"Q:\n{np.round(Q_g, 4)}")
    print(f"R:\n{np.round(R_g, 4)}")
    print(f"Q^T Q:\n{np.round(Q_g.T @ Q_g, 4)}")
    print(f"QR == A: {np.allclose(Q_g @ R_g, A)}")

    print("\n--- Least Squares via QR ---")
    A_ls = np.random.randn(20, 10)
    x_true = np.random.randn(10)
    b_ls = A_ls @ x_true + 0.1 * np.random.randn(20)
    x_qr = qr_lstsq(A_ls, b_ls)
    x_np = np.linalg.lstsq(A_ls, b_ls, rcond=None)[0]
    print(f"QR least-squares error: {np.linalg.norm(x_qr - x_true):.4e}")
    print(f"NumPy least-squares error: {np.linalg.norm(x_np - x_true):.4e}")

    print("\n--- Stability Comparison ---")
    np.random.seed(123)
    results = stability_comparison()

    fig, ax = plt.subplots(figsize=(10, 6))
    conds = np.array(results['cond'])
    ax.loglog(conds, results['cgs_err'], 'o', alpha=0.4, label='CGS')
    ax.loglog(conds, results['mgs_err'], 's', alpha=0.4, label='MGS')
    ax.loglog(conds, results['house_err'], '^', alpha=0.4, label='Householder')
    ax.loglog(conds, results['givens_err'], 'v', alpha=0.4, label='Givens')
    ax.set_xlabel('Condition Number')
    ax.set_ylabel('Orthogonality Error ||Q^T Q - I||')
    ax.set_title('QR Stability Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Rank-Deficient QR ---")
    A_rank_def = np.array([[1.0, 2.0],
                          [2.0, 4.0]])
    try:
        Q_bad, R_bad = mgs_qr(A_rank_def)
        print(f"Rank-deficient QR:\nR = {np.round(R_bad, 4)}")
    except ValueError as e:
        print(f"Expected failure: {e}")


if __name__ == "__main__":
    main()
