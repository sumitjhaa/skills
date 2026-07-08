import numpy as np
import matplotlib.pyplot as plt

def euler_maruyama(drift, diffusion, x0, T=1.0, dt=0.001):
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps + 1)
    X = np.zeros(n_steps + 1)
    X[0] = x0
    for i in range(n_steps):
        dW = np.sqrt(dt) * np.random.randn()
        X[i + 1] = X[i] + drift(X[i], t[i]) * dt + diffusion(X[i], t[i]) * dW
    return t, X

def langevin_sampling(grad_U, x0, beta=1.0, T=10.0, dt=0.01):
    drift = lambda x, t: -grad_U(x)
    diff = lambda x, t: np.sqrt(2 / beta)
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps + 1)
    X = np.zeros(n_steps + 1)
    X[0] = x0
    for i in range(n_steps):
        dW = np.sqrt(dt) * np.random.randn()
        X[i + 1] = X[i] + drift(X[i], t[i]) * dt + diff(X[i], t[i]) * dW
    return t, X

def main():
    print("=" * 60)
    print("STOCHASTIC DIFFERENTIAL EQUATIONS")
    print("=" * 60)

    print("\n--- Geometric Brownian Motion ---")
    np.random.seed(42)
    mu, sigma = 0.05, 0.2
    drift = lambda S, t: mu * S
    diffusion = lambda S, t: sigma * S
    t, S = euler_maruyama(drift, diffusion, 100.0, T=2.0, dt=0.001)
    expected = 100 * np.exp(mu * t[-1])
    print(f"  S(0) = 100, S(T) = {S[-1]:.2f}, E[S(T)] = {expected:.2f}")

    n_paths = 1000
    s_final = np.zeros(n_paths)
    for i in range(n_paths):
        _, Si = euler_maruyama(drift, diffusion, 100.0, T=2.0, dt=0.01)
        s_final[i] = Si[-1]
    print(f"  Mean over {n_paths} paths: {s_final.mean():.2f} (expected: {expected:.2f})")
    print(f"  Std over {n_paths} paths:  {s_final.std():.2f}")

    print(f"\n--- Ornstein-Uhlenbeck Process (Mean-Reverting) ---")
    theta, mu_ou, sigma_ou = 1.0, 0.0, 0.5
    drift_ou = lambda x, t: theta * (mu_ou - x)
    diff_ou = lambda x, t: sigma_ou
    t_ou, X_ou = euler_maruyama(drift_ou, diff_ou, 2.0, T=5.0)
    print(f"  X(0) = 2.0, X(T) = {X_ou[-1]:.4f} (mean-reverting to μ={mu_ou})")

    print(f"\n--- Langevin Dynamics (Sampling) ---")
    U = lambda x: x**4 / 4 - x**2 / 2  # Double well potential
    grad_U = lambda x: x**3 - x

    n_paths_ln = 200
    all_samples = []
    for _ in range(n_paths_ln):
        _, X_ln = langevin_sampling(grad_U, -1.5, beta=5.0, T=20.0, dt=0.01)
        all_samples.append(X_ln[-500:])
    all_samples = np.array(all_samples).flatten()
    print(f"  Langevin samples mean: {all_samples.mean():.4f}")
    print(f"  Langevin samples std:  {all_samples.std():.4f}")
    print(f"  Sampling from exp(-βU(x)) with double-well potential")

    print(f"\n--- SDE Discretization Error ---")
    for dt_test in [0.1, 0.01, 0.001]:
        _, S_dt = euler_maruyama(drift, diffusion, 100.0, T=1.0, dt=dt_test)
        err = abs(S_dt[-1] - 100 * np.exp((mu - sigma**2/2) * 1.0 + sigma * np.random.randn() * np.sqrt(1.0)))
        print(f"  dt={dt_test:.3f}: one path final value = {S_dt[-1]:.2f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    np.random.seed(42)
    for i in range(5):
        _, Si = euler_maruyama(drift, diffusion, 100.0, T=2.0, dt=0.01)
        axes[0].plot(_, Si, alpha=0.7)
    axes[0].axhline(100 * np.exp(mu * 2), color='k', linestyle='--', label='E[S(T)]')
    axes[0].set_xlabel('Time'); axes[0].set_ylabel('S(t)')
    axes[0].set_title('Geometric Brownian Motion Paths')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    np.random.seed(42)
    for i in range(3):
        _, X_ou_i = euler_maruyama(drift_ou, diff_ou, 2.0, T=5.0, dt=0.01)
        axes[1].plot(_, X_ou_i, alpha=0.7)
    axes[1].axhline(mu_ou, color='k', linestyle='--', label=f'μ={mu_ou}')
    axes[1].set_xlabel('Time'); axes[1].set_ylabel('X(t)')
    axes[1].set_title('Ornstein-Uhlenbeck (Mean-Reverting)')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/26_sdes.png', dpi=100)
    print(f"\nPlot saved to /tmp/26_sdes.png")

if __name__ == "__main__":
    main()
