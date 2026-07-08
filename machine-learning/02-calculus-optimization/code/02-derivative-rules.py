import numpy as np
import matplotlib.pyplot as plt

def product_rule(f, g, fp, gp, x):
    return fp(x) * g(x) + f(x) * gp(x)

def chain_rule(f, g, fp, gp, x):
    return fp(g(x)) * gp(x)

def quotient_rule(f, g, fp, gp, x):
    return (fp(x) * g(x) - f(x) * gp(x)) / (g(x)**2)

def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

def derivative_rules_demo():
    print("=" * 60)
    print("DERIVATIVE RULES")
    print("=" * 60)

    x = 1.5
    f = lambda x: x**3
    g = lambda x: np.sin(x)
    fp = lambda x: 3*x**2
    gp = lambda x: np.cos(x)

    prod_analytic = product_rule(f, g, fp, gp, x)
    prod_numeric = numerical_derivative(lambda x: f(x) * g(x), x)
    print(f"\nProduct rule at x={x}:")
    print(f"  Analytic: {prod_analytic:.6f}")
    print(f"  Numeric:  {prod_numeric:.6f}")
    print(f"  Error:    {abs(prod_analytic - prod_numeric):.2e}")

    quot_analytic = quotient_rule(f, g, fp, gp, x)
    quot_numeric = numerical_derivative(lambda x: f(x) / g(x), x)
    print(f"\nQuotient rule at x={x}:")
    print(f"  Analytic: {quot_analytic:.6f}")
    print(f"  Numeric:  {quot_numeric:.6f}")
    print(f"  Error:    {abs(quot_analytic - quot_numeric):.2e}")

    f2 = lambda u: u**2
    g2 = lambda x: 3*x + 1
    fp2 = lambda u: 2*u
    gp2 = lambda x: 3
    chain_analytic = chain_rule(f2, g2, fp2, gp2, x)
    chain_numeric = numerical_derivative(lambda x: (3*x + 1)**2, x)
    print(f"\nChain rule (f(g(x)) = (3x+1)²) at x={x}:")
    print(f"  Analytic: {chain_analytic:.6f}")
    print(f"  Numeric:  {chain_numeric:.6f}")
    print(f"  Exact:    {18*x + 6:.6f}")

    print(f"\n--- Automatic Differentiation (Forward Mode) ---")
    class Var:
        def __init__(self, val, grad=1.0):
            self.val = val
            self.grad = grad
        def __add__(self, other):
            if isinstance(other, (int, float)):
                other = Var(other, 0)
            return Var(self.val + other.val, self.grad + other.grad)
        def __mul__(self, other):
            if isinstance(other, (int, float)):
                other = Var(other, 0)
            return Var(self.val * other.val,
                       self.grad * other.val + self.val * other.grad)
        def __repr__(self):
            return f"Var(val={self.val:.4f}, grad={self.grad:.4f})"

    x_var = Var(2.0)
    result = x_var * x_var + 3 * x_var
    print(f"f(x) = x² + 3x at x=2:")
    print(f"  Value: {result.val}")
    print(f"  Derivative: {result.grad} (expected 7)")

    xs = np.linspace(0.1, 3, 100)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    f_log = lambda x: np.log(x)
    f_exp = lambda x: np.exp(x)
    f_sin = lambda x: np.sin(x)
    axes[0].plot(xs, f_log(xs), label='f(x)=ln(x)')
    axes[0].plot(xs, 1/xs, '--', label="f'(x)=1/x")
    axes[1].plot(xs, f_exp(xs), label='f(x)=e^x')
    axes[1].plot(xs, f_exp(xs), '--', label="f'(x)=e^x")
    axes[2].plot(xs, f_sin(xs), label='f(x)=sin(x)')
    axes[2].plot(xs, np.cos(xs), '--', label="f'(x)=cos(x)")
    for ax in axes:
        ax.axhline(0, color='gray', alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/02_derivative_rules.png', dpi=100)
    print(f"\nPlot saved to /tmp/02_derivative_rules.png")

if __name__ == "__main__":
    derivative_rules_demo()
