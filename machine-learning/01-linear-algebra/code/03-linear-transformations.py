import numpy as np
import matplotlib.pyplot as plt


def rotation_matrix(theta):
    """2D rotation matrix for angle theta (radians)."""
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


def scaling_matrix(sx, sy):
    """2D scaling matrix."""
    return np.array([[sx, 0], [0, sy]])


def shear_matrix(sx, sy):
    """2D shear matrix."""
    return np.array([[1, sx], [sy, 1]])


def reflection_matrix(axis='x'):
    """2D reflection matrix."""
    if axis == 'x':
        return np.array([[1, 0], [0, -1]])
    elif axis == 'y':
        return np.array([[-1, 0], [0, 1]])
    elif axis == 'origin':
        return np.array([[-1, 0], [0, -1]])
    else:
        raise ValueError("axis must be 'x', 'y', or 'origin'")


def apply_transform(T, points):
    """Apply transformation matrix T to a set of points (n x 2)."""
    return (T @ points.T).T


def compose_transforms(*matrices):
    """Compose transformations: apply in order."""
    result = np.eye(2)
    for M in matrices:
        result = M @ result
    return result


def unit_square():
    """Return vertices of the unit square."""
    return np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])


def unit_circle(n_points=100):
    """Return points on the unit circle."""
    theta = np.linspace(0, 2 * np.pi, n_points)
    return np.column_stack([np.cos(theta), np.sin(theta)])


def visualize_transformation(T, title="Transformation", points=None):
    """Visualize the effect of transformation T on a set of points."""
    if points is None:
        points = unit_square()

    transformed = apply_transform(T, points)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(points[:, 0], points[:, 1], 'b-', linewidth=2, label='Original')
    axes[0].fill(points[:, 0], points[:, 1], alpha=0.1, color='blue')
    axes[0].set_title('Original')
    axes[0].set_xlim(-3, 3)
    axes[0].set_ylim(-3, 3)
    axes[0].axhline(y=0, color='gray', alpha=0.3)
    axes[0].axvline(x=0, color='gray', alpha=0.3)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_aspect('equal')

    axes[1].plot(transformed[:, 0], transformed[:, 1], 'r-', linewidth=2, label='Transformed')
    axes[1].fill(transformed[:, 0], transformed[:, 1], alpha=0.1, color='red')
    axes[1].set_title(f'After {title}')
    axes[1].set_xlim(-3, 3)
    axes[1].set_ylim(-3, 3)
    axes[1].axhline(y=0, color='gray', alpha=0.3)
    axes[1].axvline(x=0, color='gray', alpha=0.3)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_aspect('equal')

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("LINEAR TRANSFORMATIONS - Matrix Representations")
    print("=" * 60)

    square = unit_square()

    print("\n--- Rotation ---")
    theta = np.pi / 4  # 45 degrees
    R = rotation_matrix(theta)
    print(f"Rotation by 45° matrix:\n{R}")
    visualize_transformation(R, "Rotation by 45°", square)

    print("\n--- Scaling ---")
    S = scaling_matrix(2.0, 0.5)
    print(f"Scaling matrix (2x, 0.5y):\n{S}")
    visualize_transformation(S, "Scaling (sx=2, sy=0.5)", square)

    print("\n--- Shear ---")
    Sh = shear_matrix(0.5, 0.0)
    print(f"Shear matrix:\n{Sh}")
    visualize_transformation(Sh, "Horizontal Shear", square)

    print("\n--- Reflection ---")
    Ref = reflection_matrix('x')
    print(f"Reflection over x-axis:\n{Ref}")
    visualize_transformation(Ref, "Reflection over x-axis", square)

    print("\n--- Composition: Scale then Rotate ---")
    composed1 = compose_transforms(R, S)
    print(f"Rotate then Scale:\n{composed1}")
    print(f"Determinant: {np.linalg.det(composed1):.4f}")
    transformed1 = apply_transform(composed1, square)
    visualize_transformation(composed1, "Rotate then Scale", square)

    print("\n--- Composition: Rotate then Scale (reversed order) ---")
    composed2 = compose_transforms(S, R)
    print(f"Scale then Rotate:\n{composed2}")
    transformed2 = apply_transform(composed2, square)
    print("Same result? ", np.allclose(transformed1, transformed2))
    visualize_transformation(composed2, "Scale then Rotate", square)

    print("\n--- Circle Deformation ---")
    circle = unit_circle()
    stretch = scaling_matrix(2.0, 0.5)
    rotated_stretch = rotation_matrix(np.pi / 3) @ stretch
    visualize_transformation(rotated_stretch, "Rotated Stretch", circle)

    print("\n--- Matrix Properties ---")
    print(f"det(R) = {np.linalg.det(R):.4f} (should be 1)")
    print(f"det(S) = {np.linalg.det(S):.4f} (should be {2.0 * 0.5})")
    print(f"det(Ref) = {np.linalg.det(Ref):.4f} (should be -1)")
    print(f"R^T R =\n{np.round(R.T @ R, 4)} (should be I)")
    print(f"R^{-1} = R^T: {np.allclose(np.linalg.inv(R), R.T)}")

    print("\n--- 3D-like 2D Transformations ---")
    v = np.array([1.0, 0.0])
    w = R @ v
    print(f"v = {v}")
    print(f"R(v) = {w}")
    print(f"||v|| = {np.linalg.norm(v):.4f}, ||R(v)|| = {np.linalg.norm(w):.4f}")
    print("Rotation preserves norm:", np.allclose(np.linalg.norm(v), np.linalg.norm(w)))


if __name__ == "__main__":
    main()
