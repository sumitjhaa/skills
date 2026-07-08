"""03.35 Causal Inference: IPTW and regression adjustment for confounding."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit
from scipy.stats import norm

np.random.seed(42)
n = 2000

Z = np.random.normal(0, 1, n)
p = expit(0.5 * Z)
X = np.random.binomial(1, p)
Y = 0.5 * X + 0.8 * Z + np.random.normal(0, 0.5, n)

naive = np.mean(Y[X == 1]) - np.mean(Y[X == 0])

ps = expit(-0.5 + Z * 0.5)
weights = X / ps + (1 - X) / (1 - ps)
iptw_est = (np.sum(X * Y / ps) / np.sum(X / ps) -
            np.sum((1 - X) * Y / (1 - ps)) / np.sum((1 - X) / (1 - ps)))

XZ = np.column_stack([X, Z, np.ones(n)])
coef_full = np.linalg.lstsq(XZ, Y, rcond=None)[0]
adj_est = coef_full[0]

strata = np.digitize(Z, np.percentile(Z, [20, 40, 60, 80]))
strata_effects = []
strata_sizes = []
for s in range(5):
    mask = strata == s
    if mask.sum() > 10 and X[mask].sum() > 0 and (1 - X[mask]).sum() > 0:
        e = np.mean(Y[mask][X[mask] == 1]) - np.mean(Y[mask][X[mask] == 0])
        strata_effects.append(e)
        strata_sizes.append(mask.sum())

strat_est = np.mean(strata_effects)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].scatter(Z, Y, alpha=0.3, s=5, c=X, cmap='coolwarm', label=f"X=0/1")
axes[0, 0].set_xlabel("Confounder Z")
axes[0, 0].set_ylabel("Outcome Y")
axes[0, 0].set_title("Confounding: Z → X, Z → Y")
plt.colorbar(axes[0, 0].collections[0], ax=axes[0, 0], label="X")

axes[0, 1].bar(["Naive\n(confounded)", "IPTW", "Regression\nadjustment", "Stratification"],
               [naive, iptw_est, adj_est, strat_est],
               color=['red', 'green', 'blue', 'orange'], alpha=0.7)
axes[0, 1].axhline(0.5, color='k', ls='--', lw=2, label="True ATE = 0.5")
axes[0, 1].set_ylabel("Estimated ATE")
axes[0, 1].set_title("Causal Effect Estimates")
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, axis='y', alpha=0.3)

axes[0, 2].scatter(Z, ps, alpha=0.4, s=5, c=X, cmap='coolwarm')
axes[0, 2].set_xlabel("Z")
axes[0, 2].set_ylabel("Propensity Score P(X=1|Z)")
axes[0, 2].set_title("Propensity Score Distribution")
plt.colorbar(axes[0, 2].collections[0], ax=axes[0, 2], label="X")

z_grid = np.linspace(-3, 3, 100)
y0_cond = 0.8 * z_grid
y1_cond = 0.5 + 0.8 * z_grid
axes[1, 0].plot(z_grid, y0_cond, 'b-', lw=2, label="E[Y|X=0, Z]")
axes[1, 0].plot(z_grid, y1_cond, 'r-', lw=2, label="E[Y|X=1, Z]")
axes[1, 0].fill_between(z_grid, y0_cond, y1_cond, alpha=0.2, color='purple',
                         label="ATE=0.5 (constant)")
axes[1, 0].scatter(Z, Y, alpha=0.15, s=3, c=X, cmap='coolwarm')
axes[1, 0].set_xlabel("Z")
axes[1, 0].set_ylabel("E[Y|X, Z]")
axes[1, 0].set_title("Conditional Expectations\n(no interaction: ATE constant)")
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

for s in range(5):
    mask = strata == s
    z_mean = np.mean(Z[mask])
    y_diff = (np.mean(Y[mask][X[mask] == 1]) - np.mean(Y[mask][X[mask] == 0])
              if mask.sum() > 0 and X[mask].sum() > 0 and (1-X[mask]).sum() > 0 else 0)
    axes[1, 1].plot(z_mean, y_diff, 'o', markersize=10,
                    color='green', alpha=0.7)
axes[1, 1].axhline(0.5, color='k', ls='--', label="True ATE")
axes[1, 1].set_xlabel("Z (stratum mean)")
axes[1, 1].set_ylabel("Stratum-specific ATE")
axes[1, 1].set_title("Stratification: Within-Strata Effects")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

propensity_bins = np.digitize(ps, np.percentile(ps, np.linspace(0, 100, 6))) - 1
propensity_effects = []
for s in range(5):
    mask = propensity_bins == s
    if mask.sum() > 10:
        e = np.mean(Y[mask][X[mask] == 1]) - np.mean(Y[mask][X[mask] == 0])
        propensity_effects.append(e)

axes[1, 2].bar(range(len(propensity_effects)), propensity_effects,
               color='steelblue', alpha=0.7)
axes[1, 2].axhline(0.5, color='k', ls='--', label="True ATE")
axes[1, 2].set_xlabel("Propensity score stratum")
axes[1, 2].set_ylabel("ATE estimate")
axes[1, 2].set_title("Stratification by Propensity Score")
axes[1, 2].legend()
axes[1, 2].grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/35-causal-inference.png")
plt.close()

print("=" * 60)
print("CAUSAL INFERENCE: ATE ESTIMATION")
print("=" * 60)
print(f"\nTrue ATE (Average Treatment Effect) = 0.5")
print(f"\n{'Method':<25s} {'Estimate':>10s} {'Bias':>10s}")
print("-" * 45)
methods = [
    ("Naive (confounded)", naive),
    ("IPTW", iptw_est),
    ("Regression adjustment", adj_est),
    ("Stratification", strat_est),
]
for name, est in methods:
    print(f"{name:<25s} {est:>10.4f} {est - 0.5:>10.4f}")

print(f"\nKey insight:")
print(f"  Naive estimate is biased because of confounding by Z")
print(f"  IPTW, regression adjustment, and stratification all")
print(f"  control for confounding and recover the true ATE")
print(f"\nAssumptions for causal identification:")
print(f"  1. Consistency: Y = Y(X) (no interference)")
print(f"  2. Positivity: 0 < P(X=1|Z) < 1")
print(f"  3. Ignorability: Y(1), Y(0) ⟂ X | Z (no unmeasured confounders)")
