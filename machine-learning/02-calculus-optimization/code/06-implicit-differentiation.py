import numpy as np
import matplotlib.pyplot as plt

def implicit_dydx(F, x, y, h=1e-7):
    dF_dx = (F(x + h, y) - F(x - h, y)) / (2 * h)
    dF_dy = (F(x, y + h) - F(x, y - h)) / (2 * h)
    return -dF_dx / dF_dy

def main():
    print("=" * 60)
    print("IMPLICIT DIFFERENTIATION")
    print("=" * 60)

    F_circle = lambda x, y: x**2 + y**2 - 1
    print(f"Implicit: x² + y² = 1")
    theta = np.linspace(0, np.pi/2, 10)
    for t in theta:
        x, y = np.cos(t), np.sin(t)
        dydx = implicit_dydx(F_circle, x, y)
        analytic = -x / y
        print(f"  ({x:.3f}, {y:.3f}): dy/dx = {dydx:.4f} (analytic: {analytic:.4f})")

    F_ellipse = lambda x, y: x**2/4 + y**2 - 1
    print(f"\nImplicit: x²/4 + y² = 1")
    for t in theta:
        x, y = 2*np.cos(t), np.sin(t)
        dydx = implicit_dydx(F_ellipse, x, y)
        analytic = -x / (4 * y)
        print(f"  ({x:.3f}, {y:.3f}): dy/dx = {dydx:.4f} (analytic: {analytic:.4f})")

    F_sin = lambda x, y: np.sin(x*y) - x**2 + y
    x0, y0 = 1.0, 1.0
    dydx = implicit_dydx(F_sin, x0, y0)
    print(f"\nImplicit: sin(xy) - x² + y = 0 at ({x0}, {y0})")
    print(f"  dy/dx = {dydx:.6f}")

    def fixed_point_implicit(z_star, theta):
        f = lambda z, t: np.tanh(z * t)
        return z_star - f(z_star, theta)

    z_star, theta = 0.5, 1.0
    dzdtheta = implicit_dydx(fixed_point_implicit, z_star, theta)
    print(f"\nFixed point: z* = tanh(z*·θ)")
    print(f"  at z*={z_star}, θ={theta}: dz*/dθ = {dzdtheta:.6f}")

    xs = np.linspace(0.1, 2, 100)
    ys_circle = np.sqrt(1 - xs**2)
    ys_safe = np.where(xs < 1, ys_circle, np.nan)

    dydxs = np.array([implicit_dydx(F_circle, x, np.sqrt(max(1-x**2, 1e-10)))
                      for x in xs if x < 1])
    mask = xs < 1

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(xs[mask], ys_circle[mask], 'b-', linewidth=2)
    for t in np.linspace(0.1, 1.3, 8):
        if t < np.pi/2 - 0.1:
            xp, yp = np.cos(t), np.sin(t)
            slope = implicit_dydx(F_circle, xp, yp)
            tangent_xs = np.array([xp-0.3, xp+0.3])
            tangent_ys = yp + slope * (tangent_xs - xp)
            axes[0].plot(tangent_xs, tangent_ys, 'r--', alpha=0.5)
    axes[0].set_xlim(0, 1.2); axes[0].set_ylim(0, 1.2)
    axes[0].set_aspect('equal')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_title('Implicit Differentiation: x² + y² = 1')
    axes[0].grid(True, alpha=0.3)

    xs_small = xs[xs < 1]
    dydx_vals = np.array([implicit_dydx(F_circle, x, np.sqrt(max(1-x**2, 1e-10)))
                          for x in xs_small])
    analytic_vals = -xs_small / np.sqrt(1 - xs_small**2)
    axes[1].plot(xs_small, dydx_vals, 'b-', label='Numerical')
    axes[1].plot(xs_small, analytic_vals, 'r--', label='Analytical')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('dy/dx')
    axes[1].set_title('dy/dx via Implicit Differentiation')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/06_implicit_diff.png', dpi=100)
    print(f"\nPlot saved to /tmp/06_implicit_diff.png")

if __name__ == "__main__":
    main()
