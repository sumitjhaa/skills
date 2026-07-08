"""03.08 Transformations of RVs: Box-Muller and PIT."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, chi2

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

U1 = np.random.uniform(0, 1, 5000)
U2 = np.random.uniform(0, 1, 5000)
Z1 = np.sqrt(-2 * np.log(U1)) * np.cos(2 * np.pi * U2)
Z2 = np.sqrt(-2 * np.log(U1)) * np.sin(2 * np.pi * U2)

axes[0, 0].hist(Z1, bins=60, density=True, alpha=0.7, label="Box-Muller Z1", color='steelblue')
axes[0, 0].hist(Z2, bins=60, density=True, alpha=0.3, label="Box-Muller Z2", color='orange')
x = np.linspace(-4, 4, 200)
axes[0, 0].plot(x, norm.pdf(x), 'r-', lw=2, label="N(0,1)")
axes[0, 0].set_title("Box-Muller: Uniform → Normal")
axes[0, 0].set_xlabel("Z")
axes[0, 0].set_ylabel("Density")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(Z1, Z2, alpha=0.3, s=2)
axes[0, 1].set_title("Box-Muller: Z1 vs Z2\n(should be independent)")
axes[0, 1].set_xlabel("Z1")
axes[0, 1].set_ylabel("Z2")
axes[0, 1].grid(True, alpha=0.3)
corr_bm = np.corrcoef(Z1, Z2)[0, 1]
axes[0, 1].text(-3, 3, f"Corr: {corr_bm:.4f}", fontsize=10,
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

U_exp = np.random.exponential(scale=1, size=5000)
U_trans = 1 - np.exp(-U_exp)

axes[0, 2].hist(U_trans, bins=60, density=True, alpha=0.7, color='green')
axes[0, 2].axhline(1.0, color='r', linestyle='--', lw=2, label="Uniform(0,1)")
axes[0, 2].set_title("PIT: Exp(1) → Uniform(0,1)")
axes[0, 2].set_xlabel("U")
axes[0, 2].set_ylabel("Density")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

X_chi2 = np.random.chisquare(5, 5000)
U_chi2 = chi2.cdf(X_chi2, 5)

axes[1, 0].hist(U_chi2, bins=60, density=True, alpha=0.7, color='purple')
axes[1, 0].axhline(1.0, color='r', linestyle='--', lw=2, label="Uniform(0,1)")
axes[1, 0].set_title("PIT: Chi2(5) → Uniform(0,1)")
axes[1, 0].set_xlabel("U")
axes[1, 0].set_ylabel("Density")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

U3 = np.random.uniform(0, 1, 5000)
X_inv = -np.log(1 - U3)
axes[1, 1].hist(X_inv, bins=60, density=True, alpha=0.7, color='coral', label="Inverse CDF")
x_exp = np.linspace(0, 6, 200)
axes[1, 1].plot(x_exp, expon.pdf(x_exp), 'r-', lw=2, label="Exp(1) PDF")
axes[1, 1].set_title("Inverse Transform: U → Exp(1)")
axes[1, 1].set_xlabel("X")
axes[1, 1].set_ylabel("Density")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

U4a = np.random.uniform(0, 1, 5000)
U4b = np.random.uniform(0, 1, 5000)
X_cauchy = np.tan(np.pi * (U4a - 0.5))
axes[1, 2].hist(X_cauchy, bins=80, density=True, alpha=0.7, color='teal', range=(-10, 10))
from scipy.stats import cauchy
xc = np.linspace(-10, 10, 200)
axes[1, 2].plot(xc, cauchy.pdf(xc), 'r-', lw=2, label="Cauchy PDF")
axes[1, 2].set_title("Inverse Transform: U → Cauchy")
axes[1, 2].set_xlabel("X")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_xlim(-10, 10)
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/08-transformations.png")
plt.close()

print("=" * 60)
print("TRANSFORMATIONS OF RANDOM VARIABLES")
print("=" * 60)
print(f"\nBox-Muller:")
print(f"  Z1 mean = {np.mean(Z1):.4f}, std = {np.std(Z1):.4f} (expected: 0, 1)")
print(f"  Z2 mean = {np.mean(Z2):.4f}, std = {np.std(Z2):.4f} (expected: 0, 1)")
print(f"  Correlation Z1, Z2: {corr_bm:.4f} (expected: 0)")

print(f"\nPIT (Exp(1) → Uniform):")
print(f"  Mean = {np.mean(U_trans):.4f} (expected: 0.5)")
print(f"  Std  = {np.std(U_trans):.4f} (expected: {1/np.sqrt(12):.4f})")

print(f"\nInverse Transform:")
print(f"  Exp(1) mean = {np.mean(X_inv):.4f} (expected: 1.0)")
print(f"  Cauchy median = {np.median(X_cauchy):.4f} (expected: 0.0)")

ks_bm, p_bm = np.max(np.abs(np.sort(Z1) - norm.ppf(np.linspace(1/5000, 1-1/5000, 5000)))), 0
print(f"\nGoodness-of-fit (KS stat for Z1): {ks_bm:.4f}")
