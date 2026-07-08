import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def dot_product(a, b):
    """Compute dot product from scratch."""
    result = 0.0
    for ai, bi in zip(a, b):
        result += ai * bi
    return result


def cross_product(a, b):
    """Compute cross product from scratch."""
    if len(a) != 3 or len(b) != 3:
        raise ValueError("Cross product defined only in R^3")
    return np.array([
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ])


def outer_product(a, b):
    """Compute outer product from scratch."""
    m, n = len(a), len(b)
    result = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            result[i, j] = a[i] * b[j]
    return result


def vector_projection(a, b):
    """Project a onto b."""
    b_dot_b = dot_product(b, b)
    if b_dot_b == 0:
        raise ValueError("Cannot project onto zero vector")
    scalar = dot_product(a, b) / b_dot_b
    return np.array([scalar * bi for bi in b])


def vector_rejection(a, b):
    """Component of a orthogonal to b."""
    proj = vector_projection(a, b)
    return np.array([ai - pi for ai, pi in zip(a, proj)])


def vector_norm(v):
    """Compute Euclidean norm from scratch."""
    return np.sqrt(dot_product(v, v))


def cosine_similarity(a, b):
    """Cosine of angle between a and b."""
    return dot_product(a, b) / (vector_norm(a) * vector_norm(b))


def visualize_2d(a, b, title="Vectors in 2D"):
    """Visualize two vectors in 2D."""
    fig, ax = plt.subplots(figsize=(8, 6))
    origin = np.zeros(2)

    ax.quiver(*origin, *a, angles='xy', scale_units='xy', scale=1,
              color='r', label=f'a = {a}', width=0.05)
    ax.quiver(*origin, *b, angles='xy', scale_units='xy', scale=1,
              color='b', label=f'b = {b}', width=0.05)

    proj = vector_projection(a, b)
    ax.quiver(*origin, *proj, angles='xy', scale_units='xy', scale=1,
              color='g', linestyle='dashed', label=f'proj_b a = ({proj[0]:.2f}, {proj[1]:.2f})',
              width=0.03, alpha=0.7)

    ax.set_xlim(-1, max(a[0], b[0], 1) + 1)
    ax.set_ylim(-1, max(a[1], b[1], 1) + 1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    plt.show()


def visualize_3d(a, b, title="Vectors in 3D"):
    """Visualize two vectors in 3D."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    origin = np.zeros(3)

    ax.quiver(*origin, *a, color='r', label=f'a = {a}', linewidth=2)
    ax.quiver(*origin, *b, color='b', label=f'b = {b}', linewidth=2)

    cross = cross_product(a, b)
    ax.quiver(*origin, *cross, color='g', label=f'a × b = ({cross[0]:.1f}, {cross[1]:.1f}, {cross[2]:.1f})',
              linewidth=2, linestyle='dashed')

    max_val = max(np.abs(a).max(), np.abs(b).max(), np.abs(cross).max()) + 1
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.legend()
    plt.show()


def main():
    print("=" * 60)
    print("VECTOR OPERATIONS - Scratch Implementation")
    print("=" * 60)

    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])

    print(f"\na = {a}")
    print(f"b = {b}")

    dot_scratch = dot_product(a, b)
    dot_numpy = np.dot(a, b)
    print(f"\nDot product (scratch): {dot_scratch}")
    print(f"Dot product (numpy):   {dot_numpy}")
    assert abs(dot_scratch - dot_numpy) < 1e-10

    cross_scratch = cross_product(a, b)
    cross_numpy = np.cross(a, b)
    print(f"\nCross product (scratch): {cross_scratch}")
    print(f"Cross product (numpy):   {cross_numpy}")
    assert np.allclose(cross_scratch, cross_numpy)

    outer_scratch = outer_product(a, b)
    outer_numpy = np.outer(a, b)
    print(f"\nOuter product (scratch):\n{outer_scratch}")
    print(f"Outer product (numpy):\n{outer_numpy}")
    assert np.allclose(outer_scratch, outer_numpy)

    proj = vector_projection(a, b)
    print(f"\nProjection of a onto b: {proj}")

    rej = vector_rejection(a, b)
    print(f"Rejection of a from b: {rej}")

    check = np.allclose(proj + rej, a)
    print(f"proj + rej == a: {check}")
    assert check

    cos_sim = cosine_similarity(a, b)
    numpy_cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    print(f"\nCosine similarity: {cos_sim:.6f} (numpy: {numpy_cos:.6f})")
    assert abs(cos_sim - numpy_cos) < 1e-10

    a2d = np.array([2.0, 3.0])
    b2d = np.array([4.0, 1.0])
    proj_2d = vector_projection(a2d, b2d)
    rej_2d = vector_rejection(a2d, b2d)
    print(f"\n--- 2D Example ---")
    print(f"a = {a2d}, b = {b2d}")
    print(f"Projection: {proj_2d}")
    print(f"Rejection:  {rej_2d}")
    print(f"proj + rej == a: {np.allclose(proj_2d + rej_2d, a2d)}")

    cross_check = np.dot(cross_scratch, a)
    print(f"\nCross product · a: {cross_check} (should be 0)")
    cross_check2 = np.dot(cross_scratch, b)
    print(f"Cross product · b: {cross_check2} (should be 0)")

    print("\n" + "=" * 60)
    print("Geometric visualizations...")
    print("=" * 60)
    visualize_2d(a2d, b2d, "2D Vector Projection")
    visualize_3d(a, b, "3D Vectors with Cross Product")


if __name__ == "__main__":
    main()
