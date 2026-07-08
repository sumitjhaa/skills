"""03.15 Exponential Family: Natural parameters and sufficient statistics."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli, norm, poisson, gamma as gamma_dist

p = np.linspace(0.01, 0.99, 100)
eta = np.log(p / (1 - p))
A = np.log(1 + np.exp(eta))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(p, eta, lw=2)
axes[0, 0].set_xlabel("p")
axes[0, 0].set_ylabel("η = log(p/(1-p))")
axes[0, 0].set_title("Bernoulli Natural Parameter")
axes[0, 0].grid(True, alpha=0.3)

A_grad = np.exp(eta) / (1 + np.exp(eta))
axes[0, 1].plot(eta, A_grad, lw=2, label="dA/dη")
axes[0, 1].plot(eta, p, '--', lw=2, label="p")
axes[0, 1].set_xlabel("η")
axes[0, 1].set_ylabel("Mean parameter")
axes[0, 1].set_title("Mean Parameter Mapping")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

A_second = np.exp(eta) / (1 + np.exp(eta))**2
axes[0, 2].plot(eta, A_second, lw=2, label="d²A/dη² = Var[T]")
axes[0, 2].plot(eta, p * (1 - p), '--', lw=2, label="p(1-p)")
axes[0, 2].set_xlabel("η")
axes[0, 2].set_title("Variance Function (2nd derivative)")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

mu = np.linspace(-3, 3, 100)
eta_norm = mu / 1.0
A_norm = mu**2 / 2

axes[1, 0].plot(mu, A_norm, lw=2)
axes[1, 0].set_xlabel("μ")
axes[1, 0].set_ylabel("A(η)")
axes[1, 0].set_title("Normal(μ,1): Log-Partition")
axes[1, 0].grid(True, alpha=0.3)

lmbda = np.linspace(0.1, 5, 100)
eta_pois = np.log(lmbda)
A_pois = lmbda
axes[1, 1].plot(lmbda, eta_pois, lw=2, label="η = log(λ)")
axes[1, 1].plot(lmbda, A_pois, '--', lw=2, label="A(η) = e^η = λ")
axes[1, 1].set_xlabel("λ")
axes[1, 1].set_title("Poisson(λ): Natural Parameter")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

theta = np.linspace(0.1, 3, 100)
eta_gamma = -theta
A_gamma = -np.log(theta)
axes[1, 2].plot(theta, eta_gamma, lw=2, label="η = -θ")
axes[1, 2].plot(theta, A_gamma, '--', lw=2, label="A(η) = -log(θ)")
axes[1, 2].set_xlabel("θ (rate)")
axes[1, 2].set_title("Gamma: Natural Parameter")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/15-exponential-family.png")
plt.close()

print("=" * 60)
print("EXPONENTIAL FAMILY ANALYSIS")
print("=" * 60)
print("\nBernoulli:")
print(f"  Natural parameter: η = log(p/(1-p))")
print(f"  Log-partition: A(η) = log(1+e^η)")
print(f"  E[T] = dA/dη = p = {np.mean(A_grad):.4f} (verified: {np.allclose(A_grad, p)})")
print(f"  Var[T] = d²A/dη² = p(1-p) (verified: {np.allclose(A_second, p*(1-p))})")

print("\nNormal (known σ²=1):")
print(f"  Natural parameter: η = μ")
print(f"  Log-partition: A(η) = η²/2")
print(f"  Sufficient statistic: T(x) = x")

print("\nPoisson:")
print(f"  Natural parameter: η = log(λ)")
print(f"  Log-partition: A(η) = e^η = λ")

print("\nConjugacy:")
print("  Likelihood: p(x|η) ∝ exp{ηT(x) - A(η)}")
print("  Prior: p(η) ∝ exp{τT(x) - νA(η)}")
print("  Posterior: p(η|x) ∝ exp{(T(x)+τ)η - (1+ν)A(η)}")

np.random.seed(42)
n_bern = 100
p_true = 0.3
data_bern = bernoulli.rvs(p_true, size=n_bern)
alpha_prior, beta_prior = 2, 2
alpha_post = alpha_prior + data_bern.sum()
beta_post = beta_prior + n_bern - data_bern.sum()
print(f"\nBernoulli Conjugate Update:")
print(f"  Data: {data_bern.sum()}/{n_bern} successes")
print(f"  Prior: Beta({alpha_prior},{beta_prior})")
print(f"  Posterior: Beta({alpha_post},{beta_post})")
print(f"  Posterior mean: {alpha_post/(alpha_post+beta_post):.4f} vs MLE: {data_bern.mean():.4f}")
