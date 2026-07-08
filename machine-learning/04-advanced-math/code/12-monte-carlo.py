"""04.12 Monte Carlo methods and importance sampling."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, beta, gaussian_kde

np.random.seed(42)

def mc_integrate(f, a, b, n_samples=10000):
    xs = np.random.uniform(a, b, n_samples)
    return (b - a) * np.mean(f(xs))

def importance_sampling(f, q, rv_p, n_samples=10000):
    xs = rv_p.rvs(n_samples)
    weights = q(xs) / rv_p.pdf(xs)
    return np.mean(f(xs) * weights), np.std(f(xs) * weights) / np.sqrt(n_samples)

def metropolis(f, n_iter=10000, sigma=1.0, x0=0.0):
    samples = [x0]
    for _ in range(n_iter):
        x_curr = samples[-1]
        x_prop = x_curr + sigma * np.random.randn()
        alpha = min(1, f(x_prop) / (f(x_curr) + 1e-300))
        if np.random.rand() < alpha:
            samples.append(x_prop)
        else:
            samples.append(x_curr)
    return np.array(samples)

f_sin = lambda x: np.sin(x)
I_exact = 1 - np.cos(1)
I_mc = mc_integrate(f_sin, 0, 1, 10000)

a_target, b_target = 2, 5
f_beta = lambda x: x**(a_target-1) * (1-x)**(b_target-1)
rv_beta = beta(a_target, b_target)
I_exact_beta = 1
xs_beta = rv_beta.rvs(10000)
I_is, I_is_std = importance_sampling(
    lambda x: x,
    lambda x: x**(a_target-1) * (1-x)**(b_target-1),
    rv_beta, 10000)

std_normal_samples = np.random.randn(5000)
tail_prob_exact = 1 - norm.cdf(3)
tail_prob_mc = np.mean(std_normal_samples > 3)
rv_tail = norm(3, 1)
xs_tail = rv_tail.rvs(5000)
weights_tail = norm.pdf(xs_tail) / rv_tail.pdf(xs_tail)
tail_prob_is = np.mean((xs_tail > 3) * weights_tail)

samples_mh = metropolis(lambda x: np.exp(-x**2/2) * (1 + 0.5*np.sin(3*x)**2),
                         n_iter=10000, sigma=0.8)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

n_range = [100, 500, 1000, 5000, 10000, 50000]
mc_errors = []
for n in n_range:
    I = mc_integrate(f_sin, 0, 1, n)
    mc_errors.append(abs(I - I_exact))
axes[0, 0].loglog(n_range, mc_errors, "o-", lw=2, label="MC error")
axes[0, 0].loglog(n_range, 1/np.sqrt(n_range), "--", lw=2, label="O(1/√n)")
axes[0, 0].set_xlabel("n")
axes[0, 0].set_ylabel("|Error|")
axes[0, 0].set_title("MC Integration: ∫ sin(x) dx on [0,1]\nExact = 1-cos(1)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

x_b = np.linspace(0, 1, 100)
target_pdf = beta.pdf(x_b, a_target, b_target)
proposal_pdf = np.ones_like(x_b)
axes[0, 1].plot(x_b, target_pdf, "b-", lw=2, label=f"Target p(x)=x^{a_target-1}(1-x)^{b_target-1}")
axes[0, 1].plot(x_b, proposal_pdf, "r--", lw=2, label="Proposal Uniform(0,1)")
axes[0, 1].fill_between(x_b, target_pdf, alpha=0.3)
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("Importance Sampling\nfor Beta-like Density")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].hist(samples_mh, bins=50, density=True, alpha=0.6, label="MH samples")
x_true = np.linspace(-4, 4, 200)
p_target = np.exp(-x_true**2/2) * (1 + 0.5*np.sin(3*x_true)**2)
p_target /= np.sum(p_target) * (x_true[1] - x_true[0])
axes[0, 2].plot(x_true, p_target, "r-", lw=2, label="Target")
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("Density")
axes[0, 2].set_title("Metropolis-Hastings\nUnnormalized Target")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(samples_mh[:500], "o-", ms=2, lw=0.5)
axes[1, 0].set_xlabel("Iteration")
axes[1, 0].set_ylabel("Sample value")
axes[1, 0].set_title("MH Trace (first 500)")
axes[1, 0].grid(True, alpha=0.3)

x_tail = np.linspace(2, 6, 100)
axes[1, 1].plot(x_tail, norm.pdf(x_tail), "b-", lw=2, label="N(0,1)")
axes[1, 1].axvline(3, color="k", ls="--", lw=2)
axes[1, 1].fill_between(x_tail[x_tail >= 3], norm.pdf(x_tail[x_tail >= 3]),
                        alpha=0.3, label="P(X>3)")
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Rare Event Estimation\nP(X > 3) via IS")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

ess = 1 / np.sum((weights_tail / weights_tail.sum())**2)
n_range_ess = np.arange(100, 5001, 100)
ess_vals = []
for n in n_range_ess:
    xs_n = rv_tail.rvs(n)
    w = norm.pdf(xs_n) / rv_tail.pdf(xs_n)
    ess_vals.append(1 / np.sum((w / w.sum())**2))
axes[1, 2].plot(n_range_ess, ess_vals, lw=2)
axes[1, 2].plot(n_range_ess, n_range_ess, "k--", lw=1, label="ESS = n (ideal)")
axes[1, 2].set_xlabel("n")
axes[1, 2].set_ylabel("ESS")
axes[1, 2].set_title("Effective Sample Size\nImportance Sampling for Tail")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/12-monte-carlo.png")
plt.close()

print("=" * 60)
print("MONTE CARLO METHODS")
print("=" * 60)
print(f"\nMC Integration: ∫₀¹ sin(x)dx")
print(f"  Exact:   {I_exact:.6f}")
print(f"  MC:      {I_mc:.6f}")
print(f"  Error:   {abs(I_mc - I_exact):.6f}")

print(f"\nRare event estimation P(X > 3) for N(0,1):")
print(f"  Exact:    {tail_prob_exact:.6f}")
print(f"  MC:       {tail_prob_mc:.6f} (naive, 0 hits in {len(std_normal_samples)})")
print(f"  IS:       {tail_prob_is:.6f} (biased proposal N(3,1))")

print(f"\nMetropolis-Hastings:")
accept_rate = np.mean(np.abs(np.diff(samples_mh)) > 1e-10)
print(f"  Acceptance rate: {accept_rate:.3f}")
print(f"  Mean: {np.mean(samples_mh):.4f}, Std: {np.std(samples_mh):.4f}")

print(f"\nESS for tail IS (n=5000): {ess:.1f} (out of 5000)")
print(f"\nMC converges as O(1/√n) regardless of dimension.")
