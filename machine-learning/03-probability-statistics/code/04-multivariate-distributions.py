"""03.04 Multivariate Distributions: Bivariate normal and multinomial."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal, wishart, dirichlet

np.random.seed(42)

mu = [0, 0]
cov = [[1, 0.7], [0.7, 1]]
x, y = np.mgrid[-3:3:.05, -3:3:.05]
pos = np.dstack((x, y))
rv = multivariate_normal(mu, cov)
z = rv.pdf(pos)

fig = plt.figure(figsize=(15, 10))

ax1 = fig.add_subplot(231, projection='3d')
ax1.plot_surface(x, y, z, cmap='viridis', alpha=0.8)
ax1.set_title("Bivariate Normal (ρ=0.7)")
ax1.set_xlabel("X1")
ax1.set_ylabel("X2")
ax1.set_zlabel("Density")

ax2 = fig.add_subplot(232)
contour = ax2.contourf(x, y, z, levels=30, cmap="viridis")
plt.colorbar(contour, ax=ax2, label="Density")
ax2.set_title("Bivariate Normal PDF\n(contour)")
ax2.set_xlabel("X1")
ax2.set_ylabel("X2")

n_trials, n_cats = 1000, 5
probs = [0.1, 0.2, 0.3, 0.25, 0.15]
samples = np.random.multinomial(n_trials, probs, size=200)

ax3 = fig.add_subplot(233)
bp = ax3.boxplot(samples, labels=[f"Cat{i}" for i in range(1, 6)], patch_artist=True)
for patch, color in zip(bp['boxes'], plt.cm.viridis(np.linspace(0.2, 0.8, 5))):
    patch.set_facecolor(color)
ax3.set_title(f"Multinomial (n={n_trials}, k={n_cats})")
ax3.set_ylabel("Counts")
ax3.grid(True, axis='y', alpha=0.3)

samples_3d = np.random.multinomial(100, [0.3, 0.4, 0.3], size=500)
ax4 = fig.add_subplot(234, projection='3d')
ax4.scatter(samples_3d[:, 0], samples_3d[:, 1], samples_3d[:, 2], alpha=0.4, s=5)
ax4.set_title("Multinomial (3 cats)\n500 draws")
ax4.set_xlabel("Cat 1")
ax4.set_ylabel("Cat 2")
ax4.set_zlabel("Cat 3")

df, scale = 5, np.eye(2)
wishart_samples = [wishart.rvs(df, scale) for _ in range(100)]
mean_cov = np.mean(wishart_samples, axis=0)
ax5 = fig.add_subplot(235)
im = ax5.imshow(mean_cov, cmap='coolwarm', vmin=0, vmax=10)
plt.colorbar(im, ax=ax5)
ax5.set_xticks([0, 1])
ax5.set_yticks([0, 1])
ax5.set_xticklabels(["X1", "X2"])
ax5.set_yticklabels(["X1", "X2"])
ax5.set_title(f"Mean Wishart(d={df})\n(avg of 100 samples)")

alpha_vals = [1, 2, 3, 4]
dirichlet_samples = dirichlet.rvs(alpha_vals, size=200)
ax6 = fig.add_subplot(236)
for i in range(4):
    ax6.hist(dirichlet_samples[:, i], bins=30, alpha=0.5, label=f"θ{i+1}")
ax6.set_title("Dirichlet(1,2,3,4)\nMarginal Histograms")
ax6.set_xlabel("Probability")
ax6.set_ylabel("Frequency")
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/04-multivariate-distributions.png")
plt.close()

print("=" * 60)
print("MULTIVARIATE DISTRIBUTIONS ANALYSIS")
print("=" * 60)
print(f"\nBivariate Normal (μ=0, ρ=0.7):")
sample_bvn = np.random.multivariate_normal(mu, cov, 5000)
print(f"  Sample mean: {np.mean(sample_bvn, axis=0)}")
print(f"  Sample corr: {np.corrcoef(sample_bvn.T)[0,1]:.4f}")

print(f"\nMultinomial (n={n_trials}, k={n_cats}):")
sample_means = np.mean(samples, axis=0)
expected = [p * n_trials for p in probs]
print(f"  Observed means: {sample_means}")
print(f"  Expected:       {np.round(expected, 1)}")

print(f"\nWishart(d={df}, Σ=I):")
print(f"  Theoretical E[Σ]: {df * np.eye(2)}")
print(f"  Sample mean: {mean_cov}")

print(f"\nDirichlet(1,2,3,4):")
print(f"  Sample means: {np.mean(dirichlet_samples, axis=0)}")
print(f"  Theoretical:  {np.array(alpha_vals) / sum(alpha_vals)}")
