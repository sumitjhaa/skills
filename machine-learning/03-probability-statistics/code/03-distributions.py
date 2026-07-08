"""03.03 Distributions: Sample and visualize 10+ distribution families."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, beta, gamma, poisson, binom, t, f, weibull_min, laplace, chi2, uniform

np.random.seed(42)
n = 100000

dists = {
    "Normal(0,1)": lambda: np.random.normal(0, 1, n),
    "Exp(1)": lambda: np.random.exponential(1, n),
    "Beta(2,5)": lambda: np.random.beta(2, 5, n),
    "Gamma(2,2)": lambda: np.random.gamma(2, 2, n),
    "Poisson(3)": lambda: np.random.poisson(3, n),
    "Binomial(10,0.5)": lambda: np.random.binomial(10, 0.5, n),
    "t(3)": lambda: np.random.standard_t(3, n),
    "F(5,20)": lambda: np.random.f(5, 20, n),
    "Weibull(1.5)": lambda: np.random.weibull(1.5, n),
    "Laplace(0,1)": lambda: np.random.laplace(0, 1, n),
    "Chi2(5)": lambda: np.random.chisquare(5, n),
    "Uniform(0,1)": lambda: np.random.uniform(0, 1, n),
}

dist_items = list(dists.items())
n_dists = len(dist_items)
n_cols = 4
n_rows = int(np.ceil(n_dists / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 3 * n_rows))
axes = axes.ravel()

stats_data = []
for ax, (name, sampler) in zip(axes, dist_items):
    data = sampler()
    ax.hist(data, bins=80, density=True, alpha=0.7, color='steelblue')
    ax.set_title(f"{name}\nμ={np.mean(data):.3f}, σ²={np.var(data):.3f}", fontsize=9)
    ax.set_xlabel("Value", fontsize=7)
    ax.set_ylabel("Density", fontsize=7)
    ax.tick_params(labelsize=6)
    stats_data.append((name, np.mean(data), np.var(data), np.std(data),
                       np.mean((data - np.mean(data))**3) / np.std(data)**3,
                       np.mean((data - np.mean(data))**4) / np.std(data)**4 - 3))

for ax in axes[len(dists):]:
    ax.set_visible(False)

plt.tight_layout()
plt.savefig("../../assets/phase03/03-distributions.png")
plt.close()

print("=" * 70)
print("DISTRIBUTION FAMILIES: SUMMARY STATISTICS")
print("=" * 70)
print(f"{'Distribution':<20s} {'Mean':>8s} {'Var':>8s} {'Std':>8s} {'Skew':>8s} {'Kurt':>8s}")
print("-" * 70)
for name, mu, var_, std, skew, kurt in stats_data:
    print(f"{name:<20s} {mu:>8.3f} {var_:>8.3f} {std:>8.3f} {skew:>8.3f} {kurt:>8.3f}")

print("\n" + "=" * 70)
print("THEORETICAL COMPARISON")
print("=" * 70)
print(f"\nNormal(0,1):      Mean=0.000, Var=1.000, Skew=0.000, Kurt(ex)=0.000")
print(f"Exp(1):           Mean=1.000, Var=1.000, Skew=2.000, Kurt(ex)=6.000")
print(f"Beta(2,5):        Mean=0.286, Var=0.025")
print(f"Poisson(3):       Mean=3.000, Var=3.000, Skew={1/np.sqrt(3):.3f}")
print(f"Uniform(0,1):     Mean=0.500, Var=0.083, Skew=0.000, Kurt(ex)=-1.200")

means_arr = np.array([s[1] for s in stats_data])
vars_arr = np.array([s[2] for s in stats_data])
print(f"\nMean range: [{means_arr.min():.3f}, {means_arr.max():.3f}]")
print(f"Variance range: [{vars_arr.min():.3f}, {vars_arr.max():.3f}]")

fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
names_plot = [s[0] for s in stats_data]
means_plot = [s[1] for s in stats_data]
vars_plot = [s[2] for s in stats_data]
skews_plot = [s[4] for s in stats_data]
kurts_plot = [s[5] for s in stats_data]

axes2[0, 0].barh(names_plot, means_plot, color='steelblue')
axes2[0, 0].set_xlabel("Mean")
axes2[0, 0].set_title("Mean Comparison")
axes2[0, 0].grid(True, axis='x', alpha=0.3)

axes2[0, 1].barh(names_plot, vars_plot, color='coral')
axes2[0, 1].set_xlabel("Variance")
axes2[0, 1].set_title("Variance Comparison")
axes2[0, 1].grid(True, axis='x', alpha=0.3)

axes2[1, 0].barh(names_plot, skews_plot, color='green')
axes2[1, 0].set_xlabel("Skewness")
axes2[1, 0].set_title("Skewness Comparison")
axes2[1, 0].grid(True, axis='x', alpha=0.3)

axes2[1, 1].barh(names_plot, kurts_plot, color='purple')
axes2[1, 1].set_xlabel("Excess Kurtosis")
axes2[1, 1].set_title("Kurtosis Comparison")
axes2[1, 1].grid(True, axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/03-distributions-comparison.png")
plt.close()
print(f"\nDistribution plots saved. Displayed {len(dists)} families.")
