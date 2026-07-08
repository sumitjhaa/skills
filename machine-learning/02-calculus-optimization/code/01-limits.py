import numpy as np
import matplotlib.pyplot as plt

def derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def limit_demo():
    print("=" * 60)
    print("LIMITS, CONTINUITY & DIFFERENTIATION")
    print("=" * 60)

    x_vals = np.linspace(-2, 2, 100)
    f = lambda x: x**3 - 2*x + 1

    analytical = 3*x_vals**2 - 2
    numerical = np.array([derivative(f, x) for x in x_vals])
    max_err = np.max(np.abs(analytical - numerical))
    print(f"\nf(x) = x³ - 2x + 1")
    print(f"Max numerical vs analytical derivative error: {max_err:.2e}")

    h_vals = 10.0**np.arange(-1, -12, -1)
    errors = []
    for h in h_vals:
        num = derivative(f, 1.0, h=h)
        err = abs(num - 1.0)
        errors.append(err)
        print(f"  h={h:.0e}: error={err:.2e}")
    print(f"\nCentral difference converges as O(h²)")

    tau = np.linspace(-3, 3, 100)
    f_sinc = lambda x: np.sin(x) / x if x != 0 else 1.0
    f_sinc_vec = np.vectorize(f_sinc)
    vals = f_sinc_vec(tau)
    print(f"\nsinc(0) = {f_sinc(0):.6f} (limit as x→0)")
    print(f"sinc(π) = {f_sinc(np.pi):.6f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    x = np.linspace(-2, 2, 100)
    y = f(x)
    axes[0].plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - 2x + 1')
    for pt in [-1.5, -0.5, 0.5, 1.5]:
        slope = derivative(f, pt)
        tangent = slope * (x - pt) + f(pt)
        axes[0].plot(x, tangent, '--', alpha=0.5, label=f'Tangent at x={pt}')
    axes[0].axhline(0, color='gray', alpha=0.3)
    axes[0].axvline(0, color='gray', alpha=0.3)
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('Function with Tangent Lines')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].loglog(h_vals, errors, 'ro-', linewidth=2)
    axes[1].loglog(h_vals, h_vals**2, 'b--', label='O(h²) reference')
    axes[1].set_xlabel('Step size h')
    axes[1].set_ylabel('Error')
    axes[1].set_title('Convergence of Central Difference')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/01_limits.png', dpi=100)
    print(f"\nPlot saved to /tmp/01_limits.png")

if __name__ == "__main__":
    limit_demo()
