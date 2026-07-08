import numpy as np
import matplotlib.pyplot as plt

def taylor_exp(x, n_terms):
    s = 0.0
    term = 1.0
    for n in range(n_terms):
        s += term
        term *= x / (n + 1)
    return s

def taylor_sin(x, n_terms):
    s = 0.0
    term = x
    for n in range(n_terms):
        sign = 1 if n % 2 == 0 else -1
        s += sign * term
        term *= x**2 / ((2*n + 2) * (2*n + 3))
    return s

def main():
    print("=" * 60)
    print("TAYLOR SERIES")
    print("=" * 60)

    x_vals = np.linspace(-2, 2, 200)
    exact = np.exp(x_vals)

    print(f"\nTaylor series for e^x around x=0:")
    for n in [1, 2, 3, 5, 10]:
        approx = np.array([taylor_exp(x, n) for x in x_vals])
        max_err = np.max(np.abs(approx - exact))
        print(f"  {n} terms: max error = {max_err:.2e}")

    exact_sin = np.sin(np.pi * x_vals)
    print(f"\nTaylor series for sin(πx) around x=0:")
    for n in [1, 2, 3, 5]:
        approx = np.array([taylor_sin(np.pi * x, n) for x in x_vals])
        max_err = np.max(np.abs(approx - exact_sin))
        print(f"  {n} terms: max error = {max_err:.2e}")

    x_test = 0.5
    true_val = np.exp(x_test)
    print(f"\nConvergence at x={x_test}:")
    print(f"  Exact e^{x_test} = {true_val:.10f}")
    for n in range(1, 12):
        approx = taylor_exp(x_test, n)
        err = abs(approx - true_val)
        print(f"  n={n:2d}: approx={approx:.10f}, error={err:.2e}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].plot(x_vals, exact, 'k-', linewidth=2, label='e^x (exact)')
    for n, color in zip([1, 2, 3, 5], ['r', 'g', 'b', 'm']):
        approx = np.array([taylor_exp(x, n) for x in x_vals])
        axes[0].plot(x_vals, approx, '--', color=color, label=f'{n} terms')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('f(x)')
    axes[0].set_title('Taylor Series for e^x')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(x_vals, exact_sin, 'k-', linewidth=2, label='sin(πx) (exact)')
    for n, color in zip([1, 2, 3, 5], ['r', 'g', 'b', 'm']):
        approx = np.array([taylor_sin(np.pi * x, n) for x in x_vals])
        axes[1].plot(x_vals, approx, '--', color=color, label=f'{n} terms')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('f(x)')
    axes[1].set_title('Taylor Series for sin(πx)')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/03_taylor_series.png', dpi=100)
    print(f"\nPlot saved to /tmp/03_taylor_series.png")

if __name__ == "__main__":
    main()
