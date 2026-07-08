"""04.13 MCMC: Metropolis-Hastings, Gibbs, HMC."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, multivariate_normal as mvn

np.random.seed(42)

def metropolis_hastings(log_target, n_iter=10000, proposal_std=1.0, x0=0.0):
    samples = np.zeros(n_iter)
    current = x0
    n_accept = 0
    for i in range(n_iter):
        proposal = current + proposal_std * np.random.randn()
        log_alpha = log_target(proposal) - log_target(current)
        if np.log(np.random.rand()) < log_alpha:
            current = proposal
            n_accept += 1
        samples[i] = current
    return samples, n_accept / n_iter

def gibbs_sampler(n_iter=5000, rho=0.8):
    samples = np.zeros((n_iter, 2))
    x, y = 0.0, 0.0
    for i in range(n_iter):
        x = rho * y + np.sqrt(1 - rho**2) * np.random.randn()
        y = rho * x + np.sqrt(1 - rho**2) * np.random.randn()
        samples[i] = [x, y]
    return samples

def hmc_sample(U, grad_U, n_iter=500, eps=0.1, L=10, x0=0.0):
    samples = np.zeros(n_iter)
    current = x0
    n_accept = 0
    for i in range(n_iter):
        p = np.random.randn()
        current_q, current_p = current, p
        q, p_new = current, p
        p_new -= 0.5 * eps * grad_U(q)
        for _ in range(L):
            q += eps * p_new
            p_new -= eps * grad_U(q)
        p_new -= 0.5 * eps * grad_U(q)
        p_new = -p_new
        H_old = 0.5 * current_p**2 + U(current_q)
        H_new = 0.5 * p_new**2 + U(q)
        if np.log(np.random.rand()) < min(0, H_old - H_new):
            current = q
            n_accept += 1
        samples[i] = current
    return samples, n_accept / n_iter

log_target_mix = lambda x: np.log(0.3 * norm.pdf(x, -2, 0.5) + 0.7 * norm.pdf(x, 2, 0.8))
samples_mh, ar_mh = metropolis_hastings(log_target_mix, n_iter=10000, proposal_std=1.5)

samples_gibbs = gibbs_sampler(n_iter=5000, rho=0.8)

U_1d = lambda x: 0.5 * x**2 + 0.5 * np.sin(3*x)**2
grad_U_1d = lambda x: x + 3 * np.sin(3*x) * np.cos(3*x)
samples_hmc, ar_hmc = hmc_sample(U_1d, grad_U_1d, n_iter=1000, eps=0.15, L=15)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xs = np.linspace(-4, 4, 200)
p_mix = 0.3 * norm.pdf(xs, -2, 0.5) + 0.7 * norm.pdf(xs, 2, 0.8)
axes[0, 0].hist(samples_mh, bins=60, density=True, alpha=0.6, label="MH samples")
axes[0, 0].plot(xs, p_mix, "r-", lw=2, label="Target")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title("Metropolis-Hastings\nBimodal Mixture")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(samples_mh[:500], "b-", lw=1)
axes[0, 1].set_xlabel("Iteration")
axes[0, 1].set_ylabel("x")
axes[0, 1].set_title(f"MH Trace (AR={ar_mh:.3f})")
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].scatter(samples_gibbs[:, 0], samples_gibbs[:, 1], s=3, alpha=0.5)
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("y")
axes[0, 2].set_title("Gibbs Sampler: Bivariate Normal\nρ=0.8")
axes[0, 2].axis("equal")
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].hist(samples_hmc, bins=40, density=True, alpha=0.6, label="HMC samples")
p_hmc = np.exp(-U_1d(xs))
p_hmc /= np.sum(p_hmc) * (xs[1] - xs[0])
axes[1, 0].plot(xs, p_hmc, "r-", lw=2, label="Target ∝ exp(-U)")
axes[1, 0].set_xlabel("x")
axes[1, 0].set_ylabel("Density")
axes[1, 0].set_title(f"HMC (eps=0.15, L=15)\nAR={ar_hmc:.3f}")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(samples_hmc, "b-", lw=1)
axes[1, 1].set_xlabel("Iteration")
axes[1, 1].set_ylabel("x")
axes[1, 1].set_title("HMC Trace")
axes[1, 1].grid(True, alpha=0.3)

proposal_stds = np.linspace(0.1, 5, 30)
ars = []
for ps in proposal_stds:
    _, ar = metropolis_hastings(log_target_mix, n_iter=2000, proposal_std=ps, x0=0.0)
    ars.append(ar)
axes[1, 2].plot(proposal_stds, ars, "o-", lw=2)
axes[1, 2].axhline(0.234, color="r", ls="--", label="Optimal 23.4%")
axes[1, 2].set_xlabel("Proposal std σ")
axes[1, 2].set_ylabel("Acceptance Rate")
axes[1, 2].set_title("MH: Acceptance Rate vs Proposal")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/13-mcmc.png")
plt.close()

print("=" * 60)
print("MCMC: METROPOLIS-HASTINGS, GIBBS, HMC")
print("=" * 60)
print(f"\nMetropolis-Hastings (bimodal):")
print(f"  Acceptance rate: {ar_mh:.3f}")
print(f"  Sample mean: {np.mean(samples_mh):.4f} (target: {0.3*(-2)+0.7*2:.4f})")
print(f"  Sample std:  {np.std(samples_mh):.4f}")

print(f"\nGibbs Sampler (bivariate normal, ρ=0.8):")
print(f"  Sample mean(x) = {np.mean(samples_gibbs[:,0]):.4f}")
print(f"  Sample mean(y) = {np.mean(samples_gibbs[:,1]):.4f}")
print(f"  Sample ρ = {np.corrcoef(samples_gibbs[:,0], samples_gibbs[:,1])[0,1]:.4f}")

print(f"\nHamiltonian Monte Carlo:")
print(f"  Acceptance rate: {ar_hmc:.3f}")
print(f"  Sample mean: {np.mean(samples_hmc):.4f}")

ess_mh = len(samples_mh) / (1 + 2 * np.sum(
    [np.corrcoef(samples_mh[:-t], samples_mh[t:])[0, 1]**2
     for t in range(1, min(100, len(samples_mh)))]))
print(f"\nKey concepts:")
print(f"  MH: propose & accept/reject (tune σ for ~23.4% AR)")
print(f"  Gibbs: sample from conditionals (no tuning)")
print(f"  HMC: uses gradient info for efficient exploration")
