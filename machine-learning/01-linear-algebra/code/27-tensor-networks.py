import numpy as np
import matplotlib.pyplot as plt


def tensor_to_mps(X, max_bond=10):
    """Convert a d-dimensional tensor to MPS via successive SVDs."""
    d = len(X.shape)
    cores = []
    current = X.copy()
    rank = 1

    for k in range(d - 1):
        n_k = current.shape[1]
        current = current.reshape(rank * current.shape[0], -1)
        U, s, Vt = np.linalg.svd(current, full_matrices=False)

        r = min(max_bond, len(s))
        U = U[:, :r]
        s = s[:r]
        Vt = Vt[:r, :]

        core = U.reshape(rank, -1, r)
        cores.append(core)
        rank = r
        current = np.diag(s) @ Vt

    core_last = current.reshape(rank, -1, 1)
    cores.append(core_last)

    return cores


def mps_to_tensor(cores, shape):
    """Reconstruct full tensor from MPS cores."""
    d = len(cores)
    result = cores[0]
    for k in range(1, d):
        result = np.tensordot(result, cores[k], axes=(-1, 0))

    idx = 0
    perm = []
    for k in range(d):
        perm.append(idx)
        idx += 1
        if k < d - 1:
            idx += 1

    result = result.reshape(*shape)
    return result


def mps_contract(cores):
    """Contract MPS to full tensor (without given shape)."""
    result = cores[0]
    for k in range(1, len(cores)):
        result = np.tensordot(result, cores[k], axes=(-1, 0))

    shape = [int(np.prod(result.shape) ** (1 / len(cores)))] * len(cores)
    try:
        result = result.reshape(*shape)
    except:
        pass
    return result


def random_mps(d, n, bond_dim):
    """Generate random MPS with bond dimension bond_dim."""
    cores = []
    for k in range(d):
        if k == 0:
            core = np.random.randn(1, n, min(bond_dim, 1))
        elif k == d - 1:
            prev_bond = min(bond_dim, cores[-1].shape[2])
            core = np.random.randn(prev_bond, n, 1)
        else:
            prev_bond = min(bond_dim, cores[-1].shape[2])
            core = np.random.randn(prev_bond, n, min(bond_dim, prev_bond * n))
        cores.append(core)
    return cores


def mps_vector_inner(cores_A, cores_B):
    """Inner product of two MPS vectors."""
    d = len(cores_A)
    result = np.tensordot(cores_A[0], cores_B[0], axes=([1], [1]))
    result = np.tensordot(result, np.eye(1), axes=([-1, -2], [0, 1]))

    for k in range(1, d):
        result = np.tensordot(result, cores_A[k], axes=([-1], [0]))
        result = np.tensordot(result, cores_B[k], axes=([1, -1], [1, 2]))
        if k < d - 1:
            result = np.trace(result, axis1=-2, axis2=-1)

    return result.item()


def dmrg_sweep(cores, reg_param=1e-4):
    """Single DMRG sweep (right-to-left then left-to-right)."""
    d = len(cores)

    for k in range(d - 1, 0, -1):
        U, s, Vt = np.linalg.svd(cores[k].reshape(cores[k].shape[0], -1),
                                  full_matrices=False)
        r = min(len(s), cores[k].shape[0])
        cores[k] = Vt[:r].reshape(r, cores[k].shape[1], cores[k].shape[2])
        cores[k - 1] = np.tensordot(cores[k - 1], U[:, :r].T, axes=(-1, 0))

    for k in range(0, d - 1):
        shape = cores[k].shape
        U, s, Vt = np.linalg.svd(cores[k].reshape(-1, shape[-1]),
                                  full_matrices=False)
        r = min(len(s), cores[k + 1].shape[-1])
        cores[k] = U[:, :r].reshape(shape[0], shape[1], r)
        cores[k + 1] = np.tensordot(Vt[:r], cores[k + 1], axes=(-1, 0))

    return cores


def main():
    print("=" * 60)
    print("TENSOR NETWORKS - MPS, TT, DMRG")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- MPS Decomposition ---")
    d, n = 4, 5
    X_full = np.random.randn(*([n] * d))
    print(f"Full tensor shape: {X_full.shape}, elements: {X_full.size}")

    max_bond = 4
    cores = tensor_to_mps(X_full, max_bond=max_bond)
    print(f"MPS cores: {len(cores)}")
    for i, core in enumerate(cores):
        print(f"  Core {i+1}: {core.shape}")

    total_params = sum(core.size for core in cores)
    print(f"Total MPS parameters: {total_params}")
    print(f"Compression ratio: {X_full.size / total_params:.1f}x")

    X_recon = mps_to_tensor(cores, X_full.shape)
    recon_err = np.linalg.norm(X_full - X_recon) / np.linalg.norm(X_full)
    print(f"Reconstruction error: {recon_err:.4f}")

    print("\n--- MPS Compression vs Bond Dimension ---")
    for bond in [2, 3, 4, 6, 10]:
        cores_t = tensor_to_mps(X_full, max_bond=bond)
        params_t = sum(c.size for c in cores_t)
        X_t = mps_to_tensor(cores_t, X_full.shape)
        err_t = np.linalg.norm(X_full - X_t) / np.linalg.norm(X_full)
        print(f"  Bond={bond}: params={params_t}, error={err_t:.4f}")

    print("\n--- DMRG Sweep ---")
    cores_dmrg = random_mps(6, 4, 3)
    for sweep in range(5):
        cores_dmrg = dmrg_sweep(cores_dmrg)
        X_dmrg = mps_contract(cores_dmrg)
        # Just verifying we can run sweeps
        print(f"  Sweep {sweep + 1} completed")

    print("\n--- MPS Inner Product ---")
    cores_A = random_mps(4, 3, 2)
    cores_B = random_mps(4, 3, 2)

    X_A = mps_contract(cores_A)
    X_B = mps_contract(cores_B)
    inner_direct = np.sum(X_A * X_B)

    try:
        inner_mps = mps_vector_inner(cores_A, cores_B)
        print(f"Inner product (direct): {inner_direct:.6f}")
        print(f"Inner product (MPS):    {inner_mps:.6f}")
    except:
        print("Inner product calculation encountered dimension mismatch")

    print("\n--- Tensor Train Storage Comparison ---")
    dims = [10, 20, 50, 100]
    for n_ten in dims:
        d_ten = 4
        full_params = n_ten ** d_ten
        mps_params = d_ten * n_ten * max_bond ** 2
        print(f"n={n_ten}, d={d_ten}: full={full_params:.2e}, "
              f"MPS={mps_params:.2e}, ratio={full_params / mps_params:.0f}x")

    print("\n--- Visualization ---")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    bonds = range(1, 8)
    errors_viz = []
    params_viz = []
    for b in bonds:
        c_t = tensor_to_mps(X_full, max_bond=b)
        p_t = sum(c.size for c in c_t)
        X_t = mps_to_tensor(c_t, X_full.shape)
        e_t = np.linalg.norm(X_full - X_t) / np.linalg.norm(X_full)
        errors_viz.append(e_t)
        params_viz.append(p_t)

    axes[0].plot(list(bonds), errors_viz, 'bo-')
    axes[0].set_xlabel('Bond dimension')
    axes[0].set_ylabel('Reconstruction error')
    axes[0].set_title('MPS Accuracy vs Bond Dimension')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(list(bonds), params_viz, 'rs-')
    axes[1].set_xlabel('Bond dimension')
    axes[1].set_ylabel('Number of parameters')
    axes[1].set_title('MPS Parameters vs Bond Dimension')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
