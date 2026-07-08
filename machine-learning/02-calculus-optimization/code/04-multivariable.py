import numpy as np
import matplotlib.pyplot as plt

def partial_derivative(f, x, i, h=1e-7):
    x_plus = x.copy(); x_plus[i] += h
    x_minus = x.copy(); x_minus[i] -= h
    return (f(x_plus) - f(x_minus)) / (2 * h)

def gradient(f, x, h=1e-7):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        grad[i] = partial_derivative(f, x, i, h)
    return grad

def directional_derivative(f, x, v, h=1e-7):
    v = v / np.linalg.norm(v)
    return (f(x + h * v) - f(x - h * v)) / (2 * h)

def main():
    print("=" * 60)
    print("MULTIVARIABLE CALCULUS")
    print("=" * 60)

    f = lambda x: x[0]**2 + 3*x[1]**2 + 2*x[0]*x[1]
    x = np.array([1.0, 2.0])

    print(f"\nf(x, y) = x² + 3y² + 2xy")
    print(f"At point ({x[0]}, {x[1]})")

    grad = gradient(f, x)
    print(f"\n∇f = [{grad[0]:.6f}, {grad[1]:.6f}]")
    print(f"Analytical: [4, 16] (∂f/∂x = 2x+2y = 6, ∂f/∂y = 6y+2x = 14)")
    grad_analytical = np.array([6.0, 14.0])
    print(f"  Gradient error: {np.linalg.norm(grad / grad_analytical - 1):.2e}")

    v = np.array([1.0, 0.0])
    dd = directional_derivative(f, x, v)
    print(f"\nDirectional derivative in direction [1,0]: {dd:.6f}")
    print(f"  Expected (first component of gradient): {grad[0]:.6f}")

    v2 = grad / np.linalg.norm(grad)
    dd_max = directional_derivative(f, x, v2)
    print(f"\nDirectional derivative in gradient direction: {dd_max:.6f}")
    print(f"  Should equal ‖∇f‖ = {np.linalg.norm(grad):.6f}")

    print(f"\n--- Jacobian of vector-valued function ---")
    F = lambda x: np.array([x[0]**2 + x[1], x[0] * x[1] + x[1]**2])
    x0 = np.array([1.0, 2.0])
    J_numerical = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            x_plus = x0.copy(); x_plus[j] += 1e-7
            x_minus = x0.copy(); x_minus[j] -= 1e-7
            J_numerical[i, j] = (F(x_plus)[i] - F(x_minus)[i]) / (2e-7)
    print(f"Jacobian of F(x) = [x²+y, xy+y²] at (1,2):")
    print(f"  Numerical:\n{J_numerical}")
    J_analytical = np.array([[2, 1], [2, 5]])
    print(f"  Analytical:\n{J_analytical}")
    print(f"  Error: {np.linalg.norm(J_numerical - J_analytical):.2e}")

    X, Y = np.meshgrid(np.linspace(-3, 3, 30), np.linspace(-3, 3, 30))
    Z = f([X, Y])
    gx, gy = np.gradient(Z, 0.2, 0.2)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    cp = axes[0].contour(X, Y, Z, levels=20, cmap='viridis')
    axes[0].quiver(X[::3, ::3], Y[::3, ::3], -gx[::3, ::3], -gy[::3, ::3],
                   color='r', alpha=0.5, scale=50)
    axes[0].plot(x[0], x[1], 'ko', markersize=8)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    axes[0].set_title('Contour with Negative Gradient (Descent Direction)')
    plt.colorbar(cp, ax=axes[0])

    from mpl_toolkits.mplot3d import Axes3D
    ax = axes[1], fig.add_subplot(122, projection='3d')
    surf = ax[0].plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax[0].set_xlabel('x'); ax[0].set_ylabel('y'); ax[0].set_zlabel('f(x,y)')
    ax[0].set_title('Surface Plot')
    plt.tight_layout()
    plt.savefig('../../assets/phase02/04_multivariable.png', dpi=100)
    print(f"\nPlot saved to /tmp/04_multivariable.png")

if __name__ == "__main__":
    main()
