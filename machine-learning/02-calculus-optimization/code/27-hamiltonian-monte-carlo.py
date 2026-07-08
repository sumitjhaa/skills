import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def leapfrog(grad_U, q, p, dt, L):
    q = q.copy()
    p = p.copy()
    p = p - (dt / 2) * grad_U(q)
    for i in range(L - 1):
        q = q + dt * p
        p = p - dt * grad_U(q)
    q = q + dt * p
    p = p - (dt / 2) * grad_U(q)
    return q, p

def U(q):
    return 0.5 * q**2 + 0.1 * q**4

def grad_U(q):
    return q + 0.4 * q**3

def hmc(grad_U, q0, dt=0.1, L=10, n_iter=1000, burnin=200):
    n = len(q0)
    q = q0.copy()
    samples = []
    accepted = 0
    for i in range(n_iter + burnin):
        p = np.random.randn(n)
        H_current = 0.5 * np.sum(p**2) + U(q)
        q_prop, p_prop = leapfrog(grad_U, q, p, dt, L)
        H_proposed = 0.5 * np.sum(p_prop**2) + U(q_prop)
        log_accept = min(0, H_current - H_proposed)
        if np.log(np.random.rand()) < log_accept:
            q = q_prop
            accepted += 1
        if i >= burnin:
            samples.append(q.copy())
    return np.array(samples), accepted / (n_iter + burnin)

def main():
    print("=" * 60)
    print("HAMILTONIAN MONTE CARLO")
    print("=" * 60)

    print("\n--- HMC for 1D Double-well Distribution ---")
    np.random.seed(42)
    q0 = np.array([1.0])

    samples, accept_rate = hmc(grad_U, q0, dt=0.2, L=20, n_iter=2000, burnin=500)
    print(f"  Acceptance rate: {accept_rate:.2%}")
    print(f"  Mean: {samples.mean():.4f} (theoretical: 0)")
    print(f"  Std:  {samples.std():.4f}")

    print(f"\n--- Effect of Leapfrog Steps (L) ---")
    for L in [1, 5, 20, 100]:
        samps, acc = hmc(grad_U, q0, dt=0.2, L=L, n_iter=500, burnin=100)
        print(f"  L={L:3d}: acceptance={acc:.2%}, effective samples={samps.std():.4f}")

    print(f"\n--- Effect of Step Size (dt) ---")
    for dt in [0.01, 0.05, 0.2, 0.5]:
        samps, acc = hmc(grad_U, q0, dt=dt, L=10, n_iter=500, burnin=100)
        print(f"  dt={dt:.2f}: acceptance={acc:.2%}, mean={samps.mean():.4f}")

    print(f"\n--- Comparison: HMC vs Random Walk Metropolis ---")
    n_rwm = 2500
    q_rwm = 1.0
    rwm_samples = []
    rwm_acc = 0
    for i in range(n_rwm):
        q_prop = q_rwm + np.random.randn() * 0.5
        log_accept = -(U(q_prop) - U(q_rwm))
        if np.log(np.random.rand()) < min(0, log_accept):
            q_rwm = q_prop
            rwm_acc += 1
        rwm_samples.append(q_rwm)
    rwm_ar = rwm_acc / n_rwm
    rwm_samples = np.array(rwm_samples[500:])

    hmc_samples, hmc_ar = hmc(grad_U, q0, dt=0.2, L=20, n_iter=2000, burnin=500)
    print(f"  RWM acceptance rate: {rwm_ar:.2%}")
    print(f"  HMC acceptance rate: {hmc_ar:.2%}")
    print(f"  RWM effective std: {rwm_samples.std():.4f}")
    print(f"  HMC effective std: {hmc_samples.std():.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    qs = np.linspace(-3, 3, 200)
    target_pdf = np.exp(-U(qs))
    target_pdf /= np.trapz(target_pdf, qs)
    axes[0].hist(hmc_samples.flatten(), bins=40, density=True, alpha=0.6, label='HMC samples')
    axes[0].plot(qs, target_pdf, 'r-', linewidth=2, label='Target')
    axes[0].set_xlabel('q'); axes[0].set_ylabel('Density')
    axes[0].set_title('HMC Samples vs Target Distribution')
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].plot(hmc_samples.flatten()[:500], 'b-', alpha=0.7, label='HMC')
    axes[1].plot(rwm_samples[:500], 'r-', alpha=0.5, label='RWM')
    axes[1].set_xlabel('Iteration'); axes[1].set_ylabel('q')
    axes[1].set_title('Trace Plot: HMC vs Random Walk')
    axes[1].legend(); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../assets/phase02/27_hamiltonian_monte_carlo.png', dpi=100)
    print(f"\nPlot saved to /tmp/27_hamiltonian_monte_carlo.png")

if __name__ == "__main__":
    main()
