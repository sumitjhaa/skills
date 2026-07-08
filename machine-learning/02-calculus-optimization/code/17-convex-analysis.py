import numpy as np
import matplotlib.pyplot as plt

def check_convex_function(f, x_range, n_points=100):
    xs = np.linspace(x_range[0], x_range[1], n_points)
    for i in range(n_points - 1):
        for j in range(i + 1, n_points):
            x, y = xs[i], xs[j]
            for theta in np.linspace(0, 1, 10):
                mid = theta * x + (1 - theta) * y
                if f(mid) > theta * f(x) + (1 - theta) * f(y) + 1e-10:
                    return False
    return True

def subgradient_method(f, subgrad, x0, lr=0.1, n_iter=100):
    x = x0.copy()
    traj = [x.copy()]
    for i in range(n_iter):
        x = x - lr * subgrad(x)
        traj.append(x.copy())
    return np.array(traj)

def main():
    print("=" * 60)
    print("CONVEX ANALYSIS")
    print("=" * 60)

    print("\n--- Convexity Check ---")
    f_convex = lambda x: x**2
    f_nonconvex = lambda x: np.sin(x)
    print(f"  f(x) = x² is convex: {check_convex_function(f_convex, [-2, 2])}")
    print(f"  f(x) = sin(x) is convex on [-π, π]: {check_convex_function(f_nonconvex, [-np.pi, np.pi])}")
    print(f"  f(x) = e^x is convex: {check_convex_function(lambda x: np.exp(x), [-2, 2])}")
    print(f"  f(x) = |x| is convex: {check_convex_function(lambda x: abs(x), [-2, 2])}")
    print(f"  f(x) = log(x) is convex: {check_convex_function(lambda x: np.log(x), [0.1, 3])}")

    print(f"\n--- Convexity-Preserving Operations ---")
    print(f"  Sum of convex functions f+g: {check_convex_function(lambda x: x**2 + abs(x), [-2, 2])}")
    print(f"  Max of convex functions max(x², x): {check_convex_function(lambda x: max(x**2, x), [-2, 2])}")
    print(f"  Affine composition f(Ax+b): {check_convex_function(lambda x: (2*x+1)**2, [-2, 2])}")

    print(f"\n--- Subgradient Method for |x| ---")
    subgrad_abs = lambda x: np.sign(x) if x != 0 else np.random.uniform(-1, 1)
    traj = subgradient_method(lambda x: abs(x), subgrad_abs, np.array([5.0]))
    print(f"Min of |x| from x=5: x*={traj[-1, 0]:.6f}")

    print(f"\n--- Jensen's Inequality Verification ---")
    f = lambda x: x**2
    x, y = 0.0, 4.0
    for theta in [0.1, 0.3, 0.5, 0.7, 0.9]:
        lhs = f(theta * x + (1 - theta) * y)
        rhs = theta * f(x) + (1 - theta) * f(y)
        print(f"  θ={theta:.1f}: f(θx+(1-θ)y)={lhs:.2f} ≤ {rhs:.2f}=θf(x)+(1-θ)f(y)")

    print(f"\n--- Epigraph and Convex Sets ---")
    xs = np.linspace(-3, 3, 50)
    ys = np.linspace(0, 10, 50)
    X, Y = np.meshgrid(xs, ys)
    Z_epi = Y - X**2
    epigraph_mask = Z_epi >= 0

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    xs_p = np.linspace(-3, 3, 200)
    f1 = lambda x: x**2
    f2 = lambda x: abs(x)
    f3 = lambda x: np.exp(x)
    axes[0].plot(xs_p, f1(xs_p), label='x² (convex)')
    axes[0].plot(xs_p, f2(xs_p), label='|x| (convex)')
    axes[0].plot(xs_p, f3(xs_p), label='eˣ (convex)')
    axes[0].plot(xs_p, np.sin(xs_p), '--', label='sin(x) (non-convex)')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('Convex vs Non-convex Functions')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].contourf(X, Y, epigraph_mask, levels=[0.5, 1], colors=['lightblue'], alpha=0.5)
    axes[1].plot(xs, xs**2, 'r-', linewidth=2, label='y = x² (boundary)')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')
    axes[1].set_title('Epigraph of x² (convex set)')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/17_convex_analysis.png', dpi=100)
    print(f"\nPlot saved to /tmp/17_convex_analysis.png")

if __name__ == "__main__":
    main()
