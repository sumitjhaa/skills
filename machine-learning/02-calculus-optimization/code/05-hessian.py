import numpy as np
import matplotlib.pyplot as plt

def hessian(f, x, h=1e-5):
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
            x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
            x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
            x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
            H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h**2)
    return H

def gradient(f, x, h=1e-7):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        xp = x.copy(); xp[i] += h
        xm = x.copy(); xm[i] -= h
        grad[i] = (f(xp) - f(xm)) / (2 * h)
    return grad

def main():
    print("=" * 60)
    print("HESSIAN MATRIX")
    print("=" * 60)

    f1 = lambda x: x[0]**2 + 3*x[1]**2 + 2*x[0]*x[1]
    x1 = np.array([1.0, 2.0])
    H1 = hessian(f1, x1)
    H1_analytical = np.array([[2, 2], [2, 6]])
    print(f"\nf(x, y) = x² + 3y² + 2xy")
    print(f"Hessian:\n{H1}")
    print(f"Analytical:\n{H1_analytical}")

    eigvals = np.linalg.eigvalsh(H1)
    print(f"Eigenvalues: {eigvals}")
    print(f"Convex (all eigenvalues ≥ 0): {np.all(eigvals >= -1e-10)}")

    f2 = lambda x: x[0]**2 - x[1]**2
    x2 = np.array([0.0, 0.0])
    H2 = hessian(f2, x2)
    H2_analytical = np.array([[2, 0], [0, -2]])
    print(f"\nf(x, y) = x² - y² (saddle point)")
    print(f"Hessian:\n{H2}")
    eigvals2 = np.linalg.eigvalsh(H2)
    print(f"Eigenvalues: {eigvals2}")
    print(f"Saddle point (mixed eigenvalues): {np.any(eigvals2 > 0) and np.any(eigvals2 < 0)}")

    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2

    x_opt = np.array([1.0, 1.0])
    H_rosen = hessian(rosenbrock, x_opt)
    print(f"\nRosenbrock at minimum (1, 1):")
    print(f"Hessian:\n{H_rosen}")
    eig_rosen = np.linalg.eigvalsh(H_rosen)
    print(f"Eigenvalues: {eig_rosen}")
    print(f"Condition number: {eig_rosen[-1] / eig_rosen[0]:.2f}")

    print(f"\n--- Convexity and Curvature ---")
    X, Y = np.meshgrid(np.linspace(-2, 2, 30), np.linspace(-2, 2, 30))
    Z_flat = np.array([f1([x, y]) for x, y in zip(X.ravel(), Y.ravel())])
    gx, gy = np.gradient(Z_flat.reshape(X.shape))
    gxx, _ = np.gradient(gx)
    _, gyy = np.gradient(gy)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    cp = axes[0].contourf(X, Y, Z_flat.reshape(X.shape), levels=20, cmap='viridis')
    axes[0].set_title(f'Convex Function (∇²f ≽ 0)')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')
    plt.colorbar(cp, ax=axes[0])

    Z_saddle = np.array([f2([x, y]) for x, y in zip(X.ravel(), Y.ravel())])
    cp2 = axes[1].contourf(X, Y, Z_saddle.reshape(X.shape), levels=20, cmap='RdBu_r')
    axes[1].set_title(f'Saddle Point (mixed curvature)')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    plt.colorbar(cp2, ax=axes[1])
    plt.tight_layout()
    plt.savefig('../../assets/phase02/05_hessian.png', dpi=100)
    print(f"\nPlot saved to /tmp/05_hessian.png")

if __name__ == "__main__":
    main()
