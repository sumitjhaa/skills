import numpy as np
import matplotlib.pyplot as plt


def frobenius_norm(A):
    """Frobenius norm from scratch."""
    return np.sqrt(np.sum(A ** 2))


def spectral_norm(A):
    """Spectral norm (largest singular value)."""
    _, s, _ = np.linalg.svd(A, compute_uv=False)
    return s[0]


def nuclear_norm(A):
    """Nuclear norm (sum of singular values)."""
    s = np.linalg.svd(A, compute_uv=False)
    return np.sum(s)


def induced_1_norm(A):
    """Induced 1-norm = max column sum."""
    return np.max(np.sum(np.abs(A), axis=0))


def induced_inf_norm(A):
    """Induced infinity-norm = max row sum."""
    return np.max(np.sum(np.abs(A), axis=1))


def frobenius_from_trace(A):
    """Frobenius norm via trace(A^T A)."""
    return np.sqrt(np.trace(A.T @ A))


def norm_inequalities(A):
    """Check norm inequalities."""
    frob = frobenius_norm(A)
    spec = spectral_norm(A)
    nuc = nuclear_norm(A)
    r = np.linalg.matrix_rank(A)

    print(f"Frobenius: {frob:.4f}")
    print(f"Spectral:  {spec:.4f}")
    print(f"Nuclear:   {nuc:.4f}")
    print(f"Rank: {r}")

    print(f"\nInequalities:")
    print(f"spectral <= frobenius: {spec:.4f} <= {frob:.4f} ({spec <= frob + 1e-10})")
    print(f"frobenius <= sqrt(rank) * spectral: {frob:.4f} <= {np.sqrt(r) * spec:.4f} "
          f"({frob <= np.sqrt(r) * spec + 1e-10})")
    print(f"nuclear >= frobenius: {nuc:.4f} >= {frob:.4f} ({nuc >= frob - 1e-10})")
    print(f"nuclear >= spectral: {nuc:.4f} >= {spec:.4f} ({nuc >= spec - 1e-10})")

    for p in [1, 2, np.inf]:
        print(f"||A||_{p}: ", end="")
        if p == 1:
            print(f"{induced_1_norm(A):.4f}")
        elif p == 2:
            print(f"{spectral_norm(A):.4f}")
        else:
            print(f"{induced_inf_norm(A):.4f}")


def low_rank_inequalities(k, m=10, n=8):
    """Create random rank-k matrix and verify norm equalities."""
    U = np.random.randn(m, k)
    V = np.random.randn(k, n)
    A = U @ V

    frob = frobenius_norm(A)
    spec = spectral_norm(A)
    nuc = nuclear_norm(A)

    print(f"\nRank-{k} matrix ({m}x{n}):")
    print(f"  Frobenius norm: {frob:.4f}")
    print(f"  Spectral norm:  {spec:.4f}")
    print(f"  Nuclear norm:   {nuc:.4f}")

    return frob, spec, nuc


def main():
    print("=" * 60)
    print("MATRIX NORMS - Frobenius, Spectral, Nuclear, Induced")
    print("=" * 60)

    np.random.seed(42)

    A = np.random.randn(5, 5)
    print(f"\nRandom 5x5 matrix A:\n{np.round(A, 3)}")

    print("\n--- Scratch Implementation ---")
    frob_scratch = frobenius_norm(A)
    frob_numpy = np.linalg.norm(A, 'fro')
    print(f"Frobenius (scratch): {frob_scratch:.6f}")
    print(f"Frobenius (numpy):   {frob_numpy:.6f}")
    print(f"Frobenius via trace: {frobenius_from_trace(A):.6f}")
    assert abs(frob_scratch - frob_numpy) < 1e-10

    spec_scratch = spectral_norm(A)
    spec_numpy = np.linalg.norm(A, 2)
    print(f"\nSpectral (scratch): {spec_scratch:.6f}")
    print(f"Spectral (numpy):   {spec_numpy:.6f}")
    assert abs(spec_scratch - spec_numpy) < 1e-10

    nuc_scratch = nuclear_norm(A)
    nuc_numpy = np.linalg.norm(A, 'nuc')
    print(f"\nNuclear (scratch): {nuc_scratch:.6f}")
    print(f"Nuclear (numpy):   {nuc_numpy:.6f}")
    assert abs(nuc_scratch - nuc_numpy) < 1e-10

    print(f"\nInduced 1-norm: {induced_1_norm(A):.6f}")
    print(f"Induced inf-norm: {induced_inf_norm(A):.6f}")

    print("\n--- Norm Relationships ---")
    norm_inequalities(A)

    print("\n--- Rank-1 Special Case ---")
    low_rank_inequalities(1)
    low_rank_inequalities(2)
    low_rank_inequalities(3)

    print("\n--- Norm Scaling Behavior ---")
    sizes = range(2, 12)
    frobs = []
    specs = []
    nucs = []

    for n in sizes:
        B = np.random.randn(n, n)
        frobs.append(frobenius_norm(B))
        specs.append(spectral_norm(B))
        nucs.append(nuclear_norm(B))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(list(sizes), frobs, 'o-', label='Frobenius')
    ax.plot(list(sizes), specs, 's-', label='Spectral')
    ax.plot(list(sizes), nucs, '^-', label='Nuclear')
    ax.set_xlabel('Matrix size (n)')
    ax.set_ylabel('Norm value')
    ax.set_title('Matrix Norms vs Size')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print("\n--- Norm Ratio Distribution ---")
    ratios_frob_spec = []
    ratios_nuc_frob = []
    for _ in range(1000):
        B = np.random.randn(10, 10)
        frob = frobenius_norm(B)
        spec = spectral_norm(B)
        nuc = nuclear_norm(B)
        ratios_frob_spec.append(frob / spec)
        ratios_nuc_frob.append(nuc / frob)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(ratios_frob_spec, bins=30, alpha=0.7, color='blue')
    axes[0].axvline(1, color='black', linestyle='--', label='lower bound')
    axes[0].axvline(np.sqrt(10), color='red', linestyle='--', label=f'sqrt(n)={np.sqrt(10):.2f}')
    axes[0].set_xlabel('Frobenius / Spectral')
    axes[0].set_title('Frobenius-to-Spectral Ratio')
    axes[0].legend()

    axes[1].hist(ratios_nuc_frob, bins=30, alpha=0.7, color='green')
    axes[1].axvline(1, color='black', linestyle='--', label='lower bound')
    axes[1].set_xlabel('Nuclear / Frobenius')
    axes[1].set_title('Nuclear-to-Frobenius Ratio')
    axes[1].legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Condition Number (Spectral) ---")
    for n in [5, 10, 20, 50]:
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        s = np.logspace(0, -6, n)
        B = U @ np.diag(s) @ Vt
        cond = spectral_norm(B) / spectral_norm(np.linalg.inv(B))
        print(f"n={n}: condition number = {cond:.2e}")


if __name__ == "__main__":
    main()
