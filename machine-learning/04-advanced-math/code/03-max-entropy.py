"""04.03 Maximum entropy principle: exponential family."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, fsolve
from scipy.stats import entropy, norm, expon

def max_ent_gaussian(mu, sigma, n_bins=100):
    xs = np.linspace(-5, 5, n_bins)
    dx = xs[1] - xs[0]
    p = np.exp(-0.5 * ((xs - mu) / sigma)**2) / (sigma * np.sqrt(2*np.pi))
    p /= p.sum()
    H = entropy(p, base=2)
    return xs, p, H

def max_ent_exponential(lmbda, x_max=10, n_bins=200):
    xs = np.linspace(1e-6, x_max, n_bins)
    dx = xs[1] - xs[0]
    p = lmbda * np.exp(-lmbda * xs)
    p /= p.sum()
    H = entropy(p, base=2)
    return xs, p, H

def max_ent_uniform(x_min, x_max, n_bins=200):
    xs = np.linspace(x_min, x_max, n_bins)
    p = np.ones_like(xs) / len(xs)
    H = entropy(p, base=2)
    return xs, p, H

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

xs, p, H_gauss = max_ent_gaussian(0, 1)
axes[0, 0].plot(xs, p, lw=2, label=f"Gaussian (μ=0, σ=1)\nH={H_gauss:.3f} bits")
axes[0, 0].set_xlabel("x")
axes[0, 0].set_ylabel("Probability")
axes[0, 0].set_title(f"Max Entropy given μ, σ²\n$\\rightarrow$ Gaussian")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

xs_exp, p_exp, H_exp = max_ent_exponential(1.0)
axes[0, 1].plot(xs_exp, p_exp, lw=2, color='orange',
                label=f"Exp(λ=1)\nH={H_exp:.3f} bits")
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("Probability")
axes[0, 1].set_title("Max Entropy given E[X]=1/λ\n$\\rightarrow$ Exponential")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

xs_unif, p_unif, H_unif = max_ent_uniform(-1, 1)
axes[0, 2].plot(xs_unif, p_unif, lw=2, color='green',
                label=f"Uniform[-1,1]\nH={H_unif:.3f} bits")
axes[0, 2].set_xlabel("x")
axes[0, 2].set_ylabel("Probability")
axes[0, 2].set_title("Max Entropy given [a,b]\n$\\rightarrow$ Uniform")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

sigmas = np.linspace(0.1, 3, 50)
entropies_g = [entropy(np.exp(-0.5 * ((xs - 0) / s)**2) / (s * np.sqrt(2*np.pi)), base=2)
               for s in sigmas]
axes[1, 0].plot(sigmas, entropies_g, lw=2)
axes[1, 0].set_xlabel("σ")
axes[1, 0].set_ylabel("Entropy (bits)")
axes[1, 0].set_title("Gaussian Entropy vs σ\nH = ½log(2πeσ²)/log(2)")
axes[1, 0].grid(True, alpha=0.3)
theoretical = 0.5 * np.log2(2 * np.pi * np.e * sigmas**2)
axes[1, 0].plot(sigmas, theoretical, 'r--', lw=2, label="Theoretical")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

lambdas = np.linspace(0.1, 5, 50)
xs_e_loop = np.linspace(1e-6, 10, 200)
entropies_e = []
for lmbda in lambdas:
    p_e_loop = lmbda * np.exp(-lmbda * xs_e_loop)
    p_e_loop /= p_e_loop.sum()
    entropies_e.append(entropy(p_e_loop, base=2))
axes[1, 1].plot(lambdas, entropies_e, lw=2, color='orange')
axes[1, 1].set_xlabel("λ")
axes[1, 1].set_ylabel("Entropy (bits)")
axes[1, 1].set_title("Exponential Entropy vs λ\nH = 1 - log(λ)")
axes[1, 1].grid(True, alpha=0.3)

dist_labels = ["Normal\n(μ,σ²)", "Exponential\n(λ)", "Uniform\n[a,b]", "Poisson\n(λ)",
               "Binomial\n(n,p)", "Bernoulli\n(p)"]
dist_entropies = [H_gauss, H_exp, H_unif, 1.0, 0.5, 0.5]
axes[1, 2].bar(dist_labels, dist_entropies, color=plt.cm.viridis(np.linspace(0.2, 0.8, 6)))
axes[1, 2].set_ylabel("Max Entropy (bits)")
axes[1, 2].set_title("Maximum Entropy by Constraint Type")
axes[1, 2].tick_params(axis='x', rotation=20)
axes[1, 2].grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/03-max-entropy.png")
plt.close()

print("=" * 60)
print("MAXIMUM ENTROPY PRINCIPLE")
print("=" * 60)
print(f"\nGiven constraints → Max ent distribution:")
print(f"  E[X] = μ, Var[X] = σ² → Gaussian(μ, σ²)")
print(f"  E[X] = 1/λ, X ≥ 0    → Exponential(λ)")
print(f"  a ≤ X ≤ b           → Uniform(a, b)")
print(f"  E[X] = λ, X ∈ ℕ      → Poisson(λ)")

print(f"\nEntropy values (bits):")
print(f"  Gaussian(0,1):   H = {H_gauss:.4f}")
print(f"  Exponential(1):  H = {H_exp:.4f}")
print(f"  Uniform[-1,1]:   H = {H_unif:.4f}")

H_exp_theory = 1 - np.log2(1)
print(f"  Exponential(1) theoretical: H = 1 - log₂(1) = {H_exp_theory:.4f}")
H_gauss_theory = 0.5 * np.log2(2 * np.pi * np.e * 1)
print(f"  Gaussian(0,1) theoretical:  H = ½log₂(2πe) = {H_gauss_theory:.4f}")

print(f"\nThe maximum entropy distribution is the most 'honest'")
print(f"distribution given the constraints (Jaynes' principle).")
