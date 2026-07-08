import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def loss_1d_slice(loss_fn, theta_0, theta_1, n_points=100):
    alphas = np.linspace(-1, 2, n_points)
    losses = []
    for alpha in alphas:
        theta = (1 - alpha) * theta_0 + alpha * theta_1
        losses.append(loss_fn(theta))
    return alphas, np.array(losses)

def loss_2d_slice(loss_fn, theta_star, n_points=50, range_val=1.0):
    n = len(theta_star)
    rng = np.random.RandomState(42)
    d1 = rng.randn(n)
    d1 = d1 / np.linalg.norm(d1)
    d2 = rng.randn(n)
    d2 = d2 - np.dot(d2, d1) * d1
    d2 = d2 / np.linalg.norm(d2)

    alphas = np.linspace(-range_val, range_val, n_points)
    betas = np.linspace(-range_val, range_val, n_points)
    Z = np.zeros((n_points, n_points))

    for i, alpha in enumerate(alphas):
        for j, beta in enumerate(betas):
            theta = theta_star + alpha * d1 + beta * d2
            Z[j, i] = loss_fn(theta)

    return alphas, betas, Z

def curvature_estimate(loss_fn, theta, epsilon=0.01):
    d = np.random.randn(len(theta))
    d = d / np.linalg.norm(d)
    f_plus = loss_fn(theta + epsilon * d)
    f_minus = loss_fn(theta - epsilon * d)
    f_center = loss_fn(theta)
    return (f_plus - 2*f_center + f_minus) / (epsilon**2)

def main():
    print("=" * 60)
    print("LOSS LANDSCAPE VISUALIZATION")
    print("=" * 60)

    print("\n--- 1D Loss Landscape Slice ---")
    np.random.seed(42)

    def loss_1d(theta):
        return 0.5 * theta[0]**2 + 0.1 * theta[0]**4 + 0.5 * theta[1]**2

    theta_0 = np.array([2.0, 0.5])
    theta_1 = np.array([-1.0, -0.3])

    alphas, losses = loss_1d_slice(loss_1d, theta_0, theta_1)
    min_idx = np.argmin(losses)
    print(f"  Minimum at alpha = {alphas[min_idx]:.4f}")
    print(f"  Loss range: [{losses.min():.4f}, {losses.max():.4f}]")

    print("\n--- 2D Loss Landscape near Optimum ---")
    def loss_2d(theta):
        return 0.5 * theta[0]**2 + 5 * theta[1]**2 + 0.3 * theta[0] * theta[1]

    theta_star = np.array([0.0, 0.0])
    alphas_2d, betas_2d, Z = loss_2d_slice(loss_2d, theta_star, n_points=30, range_val=3.0)
    print(f"  Mesh shape: {Z.shape}")
    print(f"  Min value: {Z.min():.4f}")
    print(f"  Max value: {Z.max():.4f}")

    print("\n--- Curvature (Sharp vs Flat Minima) ---")
    theta0 = np.array([0.0])
    sharp_fn = lambda t: 50 * t[0]**2
    flat_fn = lambda t: 0.5 * t[0]**2

    sharp_curv = curvature_estimate(sharp_fn, theta0)
    flat_curv = curvature_estimate(flat_fn, theta0)
    print(f"  Sharp min curvature: {sharp_curv:.4f}")
    print(f"  Flat min curvature:  {flat_curv:.4f}")
    print(f"  Ratio (sharp/flat):  {sharp_curv / flat_curv:.2f}")

    print("\n--- Filter-Normalized vs Random Directions ---")
    theta_full = np.array([1.0, 0.5, 2.0, -1.0, 0.0, 0.3, 0.8, -0.2, 0.5, 0.1, -0.3, 0.7, 0.2, -0.1])

    rng = np.random.RandomState(42)
    d_random = rng.randn(len(theta_full))
    d_random = d_random / np.linalg.norm(d_random)

    d_filtered = rng.randn(len(theta_full))
    d_filtered = d_filtered / np.linalg.norm(d_filtered)
    d_filtered = d_filtered * np.linalg.norm(theta_full) / np.linalg.norm(d_filtered)

    print(f"  Random direction norm: {np.linalg.norm(d_random):.4f}")
    print(f"  Filter-norm direction: {np.linalg.norm(d_filtered):.4f}")

    fig = plt.figure(figsize=(16, 5))
    ax1 = fig.add_subplot(131)
    ax1.plot(alphas, losses, 'b-', linewidth=2)
    ax1.axvline(alphas[min_idx], color='r', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Interpolation parameter α')
    ax1.set_ylabel('Loss')
    ax1.set_title('1D Loss Landscape Slice')
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(132)
    levels = np.logspace(-1, 1, 20)
    cp = ax2.contour(alphas_2d, betas_2d, Z, levels=levels, cmap='viridis')
    ax2.set_xlabel('Direction 1')
    ax2.set_ylabel('Direction 2')
    ax2.set_title('2D Loss Landscape')
    plt.colorbar(cp, ax=ax2)

    ax3 = fig.add_subplot(133)
    ax3.contour(alphas_2d, betas_2d, Z, levels=levels, cmap='viridis')
    xs = np.linspace(-3, 3, 10)
    for x in xs:
        ax3.plot([x, x], [-3, 3], 'r-', alpha=0.1)
        ax3.plot([-3, 3], [x, x], 'r-', alpha=0.1)
    ax3.set_xlabel('Direction 1'); ax3.set_ylabel('Direction 2')
    ax3.set_title('With Coordinate Grid Overlay')

    plt.tight_layout()
    plt.savefig('../../assets/phase02/40_loss_landscape.png', dpi=100)
    print(f"\nPlot saved to /tmp/40_loss_landscape.png")

if __name__ == "__main__":
    main()
