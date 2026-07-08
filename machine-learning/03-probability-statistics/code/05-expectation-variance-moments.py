"""03.05 Expectation, Variance, Moments: Compute empirical moments."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 100000

X = np.random.gamma(shape=3, scale=2, size=n)

mu = np.mean(X)
var = np.var(X)
std = np.std(X)
skew = np.mean((X - mu)**3) / std**3
kurt = np.mean((X - mu)**4) / std**4 - 3
median = np.median(X)
q25, q75 = np.percentile(X, [25, 75])
iqr = q75 - q25

print("=" * 60)
print("EMPIRICAL MOMENTS OF GAMMA(3, 2)")
print("=" * 60)
print(f"\nFirst Moment (Mean):")
print(f"  μ = {mu:.4f}  (true = 6.0)")
print(f"\nSecond Moments:")
print(f"  Variance  = {var:.4f}  (true = 12.0)")
print(f"  Std Dev   = {std:.4f}  (true = {np.sqrt(12):.4f})")
print(f"\nThird Moment (Skewness):")
gamma_skew = 2 / np.sqrt(3)
print(f"  γ₁ = {skew:.4f}  (true = {gamma_skew:.4f})")
print(f"\nFourth Moment (Kurtosis):")
print(f"  γ₂(ex) = {kurt:.4f}  (true = 2.0)")
print(f"\nRobust Statistics:")
print(f"  Median = {median:.4f}")
print(f"  IQR    = {iqr:.4f}")

print("\n" + "=" * 60)
print("LAW OF TOTAL EXPECTATION (LOTUS) VERIFICATION")
print("=" * 60)
E_X2_lotus = np.mean(X**2)
E_X2_formula = var + mu**2
print(f"  E[X²] via LOTUS:       {E_X2_lotus:.4f}")
print(f"  E[X²] = Var + (E[X])²: {E_X2_formula:.4f}")
print(f"  Match: {np.isclose(E_X2_lotus, E_X2_formula)}")

E_X3_lotus = np.mean(X**3)
E_X3_raw = skew * std**3 + 3 * mu * var + mu**3
print(f"  E[X³] via LOTUS:       {E_X3_lotus:.4f}")
print(f"  E[X³] via moments:     {E_X3_raw:.4f}")

E_X4_lotus = np.mean(X**4)
print(f"  E[X⁴] via LOTUS:       {E_X4_lotus:.4f}")

print("\n" + "=" * 60)
print("MOMENT GENERATING FUNCTION (empirical)")
print("=" * 60)
t_vals = np.linspace(-0.2, 0.2, 10)
mgf = np.array([np.mean(np.exp(t * X)) for t in t_vals])
mgf_true = np.array([(1 - 3 * t)**(-3) if t < 1/3 else np.inf for t in t_vals])
print("  t       MGF_emp    MGF_true")
for t_pt, mgf_pt, mgf_t in zip(t_vals, mgf, mgf_true):
    print(f"  {t_pt:+.2f}   {mgf_pt:8.4f}   {mgf_t:8.4f}")

print("\n" + "=" * 60)
print("CONVERGENCE OF SAMPLE MEAN (LLN DEMO)")
print("=" * 60)
cum_mean = np.cumsum(X[:10000]) / np.arange(1, 10001)
print(f"  Mean after n=10:    {cum_mean[9]:.4f}")
print(f"  Mean after n=100:   {cum_mean[99]:.4f}")
print(f"  Mean after n=1000:  {cum_mean[999]:.4f}")
print(f"  Mean after n=10000: {cum_mean[9999]:.4f}")

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].hist(X, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes[0, 0].axvline(mu, color='r', lw=2, label=f"Mean={mu:.2f}")
axes[0, 0].axvline(median, color='g', lw=2, ls='--', label=f"Median={median:.2f}")
axes[0, 0].axvline(q25, color='orange', lw=1, ls=':', label=f"Q25={q25:.2f}")
axes[0, 0].axvline(q75, color='orange', lw=1, ls=':')
axes[0, 0].set_xlabel("Value")
axes[0, 0].set_ylabel("Density")
axes[0, 0].set_title("Gamma(3,2) Distribution")
axes[0, 0].legend(fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(np.arange(1, 10001), cum_mean, lw=1)
axes[0, 1].axhline(6.0, color='r', ls='--', label="True mean = 6")
axes[0, 1].set_xlabel("n")
axes[0, 1].set_ylabel("Cumulative mean")
axes[0, 1].set_title("Convergence of Sample Mean (LLN)")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

ns = np.logspace(1, 5, 20, dtype=int)
var_ests = [np.var(X[:ni]) for ni in ns]
axes[1, 0].loglog(ns, var_ests, 'o-', label="Empirical var")
axes[1, 0].axhline(12.0, color='r', ls='--', label="True var = 12")
axes[1, 0].set_xlabel("n")
axes[1, 0].set_ylabel("Variance estimate")
axes[1, 0].set_title("Convergence of Variance")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(t_vals, mgf, 'o-', label="Empirical MGF")
axes[1, 1].plot(t_vals, mgf_true, 'rs--', label="True MGF")
axes[1, 1].set_xlabel("t")
axes[1, 1].set_ylabel("M(t)")
axes[1, 1].set_title("Moment Generating Function")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/05-expectation-variance-moments.png")
plt.close()
print("\nMoments plot saved.")
