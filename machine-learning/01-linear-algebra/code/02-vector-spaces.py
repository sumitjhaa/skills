import numpy as np
import matplotlib.pyplot as plt


def check_independence(vectors):
    """Check if a set of vectors is linearly independent via rank."""
    A = np.column_stack(vectors)
    rank = np.linalg.matrix_rank(A)
    n = len(vectors)
    independent = rank == n
    return independent, rank


def gram_schmidt(V):
    """Gram-Schmidt orthonormalization.

    Given matrix V (m x n) with independent columns,
    returns Q (m x n) with orthonormal columns.
    """
    m, n = V.shape
    Q = np.zeros((m, n), dtype=float)
    R = np.zeros((n, n), dtype=float)

    for i in range(n):
        v = V[:, i].astype(float).copy()
        for j in range(i):
            R[j, i] = np.dot(Q[:, j], V[:, i])
            v -= R[j, i] * Q[:, j]
        R[i, i] = np.linalg.norm(v)
        if R[i, i] < 1e-14:
            raise ValueError(f"Vectors are linearly dependent (column {i})")
        Q[:, i] = v / R[i, i]

    return Q, R


def modified_gram_schmidt(V):
    """Modified Gram-Schmidt for better numerical stability."""
    m, n = V.shape
    Q = V.astype(float).copy()
    R = np.zeros((n, n), dtype=float)

    for i in range(n):
        R[i, i] = np.linalg.norm(Q[:, i])
        Q[:, i] /= R[i, i]
        for j in range(i + 1, n):
            R[i, j] = np.dot(Q[:, i], Q[:, j])
            Q[:, j] -= R[i, j] * Q[:, i]

    return Q, R


def change_of_basis(v, basis_vectors):
    """Express vector v in a new basis.

    basis_vectors: matrix where columns are basis vectors.
    Returns coordinates in the new basis.
    """
    B = np.column_stack(basis_vectors)
    return np.linalg.solve(B, v)


def span_check(vectors, target):
    """Check if target is in the span of the given vectors."""
    A = np.column_stack(vectors)
    try:
        coords = np.linalg.lstsq(A, target, rcond=None)[0]
        reconstructed = A @ coords
        return np.allclose(reconstructed, target), coords
    except np.linalg.LinAlgError:
        return False, None


def coordinate_vector(v, basis):
    """Express v in terms of basis (columns of basis matrix)."""
    return np.linalg.solve(basis, v)


def visualize_basis(basis_vectors, title="Basis Vectors in 2D"):
    """Visualize basis vectors."""
    fig, ax = plt.subplots(figsize=(8, 8))
    origin = np.zeros(2)
    colors = ['r', 'b', 'g']

    for i, v in enumerate(basis_vectors):
        ax.quiver(*origin, *v, angles='xy', scale_units='xy', scale=1,
                  color=colors[i % len(colors)],
                  label=f'basis {i+1} = ({v[0]:.2f}, {v[1]:.2f})',
                  width=0.05)

    max_val = max(np.abs(v).max() for v in basis_vectors) + 1
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.legend()
    plt.show()


def main():
    print("=" * 60)
    print("VECTOR SPACES - Linear Independence, Basis, Gram-Schmidt")
    print("=" * 60)

    print("\n--- Linear Independence ---")
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    v3 = np.array([0.0, 0.0, 1.0])

    indep, rank = check_independence([v1, v2, v3])
    print(f"Standard basis R^3: independent={indep}, rank={rank}")

    v4 = np.array([1.0, 2.0, 3.0])
    v5 = np.array([2.0, 4.0, 6.0])
    indep2, rank2 = check_independence([v4, v5])
    print(f"Collinear vectors: independent={indep2}, rank={rank2}")

    print("\n--- Span Check ---")
    target = np.array([3.0, 4.0, 5.0])
    in_span, coords = span_check([v1, v2, v3], target)
    print(f"Target {target} in span of standard basis: {in_span}")
    if in_span:
        print(f"Coordinates: {coords}")

    print("\n--- Gram-Schmidt ---")
    V = np.array([[3.0, 2.0],
                  [1.0, 2.0],
                  [0.0, 1.0]])
    Q, R = gram_schmidt(V)
    print(f"Original V:\n{V}")
    print(f"\nOrthonormal Q:\n{Q}")
    print(f"\nUpper-triangular R:\n{R}")
    print(f"\nQ^T Q (should be identity):\n{np.round(Q.T @ Q, 10)}")
    print(f"QR == V: {np.allclose(Q @ R, V)}")

    Q2, R2 = modified_gram_schmidt(V)
    print(f"\nModified Gram-Schmidt:")
    print(f"Q^T Q:\n{np.round(Q2.T @ Q2, 10)}")
    print(f"QR == V: {np.allclose(Q2 @ R2, V)}")

    print("\n--- Change of Basis ---")
    std_basis = np.eye(2)
    new_basis = [np.array([1.0, 1.0]), np.array([1.0, -1.0])]
    v = np.array([3.0, 2.0])
    coords_new = change_of_basis(v, new_basis)
    print(f"Vector v = {v} in standard basis")
    print(f"Coordinates in new basis: {coords_new}")
    reconstructed = coords_new[0] * new_basis[0] + coords_new[1] * new_basis[1]
    print(f"Reconstructed: {reconstructed}")
    print(f"Match: {np.allclose(v, reconstructed)}")

    print("\n--- 2D Basis Visualization ---")
    basis_2d = [np.array([1.0, 0.5]), np.array([0.5, 1.0])]
    indep_2d, rank_2d = check_independence(basis_2d)
    print(f"Basis vectors: {basis_2d}")
    print(f"Independent: {indep_2d}")

    test_vec = np.array([2.0, 1.0])
    in_span_2d, coords_2d = span_check(basis_2d, test_vec)
    print(f"Test vector {test_vec} in span: {in_span_2d}, coords: {coords_2d}")

    visualize_basis(basis_2d, "Basis Vectors in R^2")

    print("\n--- Dimension Check ---")
    for dim in range(1, 5):
        rand_vecs = [np.random.randn(5) for _ in range(dim)]
        ind, r = check_independence(rand_vecs)
        print(f"{dim} vectors in R^5: independent={ind}, rank={r}")


if __name__ == "__main__":
    main()
