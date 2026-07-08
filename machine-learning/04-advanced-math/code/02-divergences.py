"""04.02 f-divergences, JS, and Wasserstein distance."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wasserstein_distance, norm, beta
from scipy.special import rel_entr

p = np.array([0.2, 0.3, 0.5])
q = np.array([0.25, 0.25, 0.5])
m = 0.5 * (p + q)

kl = np.sum(rel_entr(p, q))
js = 0.5 * np.sum(rel_entr(p, m)) + 0.5 * np.sum(rel_entr(q, m))
tv = 0.5 * np.sum(np.abs(p - q))
chi2 = np.sum((p - q)**2 / q)
h2 = 1 - np.sum(np.sqrt(p * q))

w1 = wasserstein_distance(np.arange(3), np.arange(3), p, q)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

div_names = ["KL", "JS", "TV", "χ²", "H²", "Wasserstein"]
div_values = [kl, js, tv, chi2, h2, w1]
colors_div = plt.cm.viridis(np.linspace(0.2, 0.8, 6))
axes[0, 0].bar(div_names, div_values, color=colors_div, alpha=0.7)
axes[0, 0].set_ylabel("Divergence")
axes[0, 0].set_title("Divergences between p and q")
axes[0, 0].grid(True, axis='y', alpha=0.3)

np.random.seed(0)
samples_p = np.random.normal(0, 1, 1000)
samples_q = np.random.normal(2, 1, 1000)
samples_r = np.random.normal(0, 3, 1000)

axes[0, 1].hist(samples_p, bins=50, density=True, alpha=0.5, label="N(0,1)")
axes[0, 1].hist(samples_q, bins=50, density=True, alpha=0.5, label="N(2,1)")
x_g = np.linspace(-4, 6, 200)
axes[0, 1].plot(x_g, norm.pdf(x_g, 0, 1), 'b-', lw=2)
axes[0, 1].plot(x_g, norm.pdf(x_g, 2, 1), 'r-', lw=2)
axes[0, 1].set_xlabel("x")
axes[0, 1].set_ylabel("Density")
axes[0, 1].set_title("N(0,1) vs N(2,1)")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

w1_gauss = wasserstein_distance(samples_p, samples_q)
w2_gauss = wasserstein_distance(samples_p, samples_q)  # W1 in 1D
w1_gauss_r = wasserstein_distance(samples_p, samples_r)
print(f"W1(N(0,1), N(2,1)) = {w1_gauss:.4f} (true = 2.0)")
print(f"W1(N(0,1), N(0,3)) = {w1_gauss_r:.4f}")

shifts = np.linspace(0, 5, 30)
w_distances = []
for shift in shifts:
    sq = np.random.normal(shift, 1, 1000)
    w_distances.append(wasserstein_distance(samples_p, sq))
axes[0, 2].plot(shifts, w_distances, 'o-', lw=2)
axes[0, 2].set_xlabel("Mean shift δ")
axes[0, 2].set_ylabel("Wasserstein distance")
axes[0, 2].set_title("Wasserstein-1 vs Mean Shift")
axes[0, 2].grid(True, alpha=0.3)

pi = np.array([0.3, 0.4, 0.3])
qi = np.array([0.33, 0.34, 0.33])
mis = 0.5 * (pi + qi)
js_3 = 0.5 * np.sum(rel_entr(pi, mis)) + 0.5 * np.sum(rel_entr(qi, mis))
tv_3 = 0.5 * np.sum(np.abs(pi - qi))

scales = np.logspace(-1, 1, 30)
js_divs = []
tv_divs = []
for s in scales:
    p_s = np.array([0.2, 0.3, 0.5])
    q_s = np.array([0.2*s, 0.3*s, 1 - 0.2*s - 0.3*s])
    q_s = q_s / q_s.sum()
    m_s = 0.5 * (p_s + q_s)
    js_divs.append(0.5 * np.sum(rel_entr(p_s, m_s)) + 0.5 * np.sum(rel_entr(q_s, m_s)))
    tv_divs.append(0.5 * np.sum(np.abs(p_s - q_s)))

axes[1, 0].semilogx(scales, js_divs, 'o-', label="JS", lw=2)
axes[1, 0].semilogx(scales, tv_divs, 's-', label="TV", lw=2)
axes[1, 0].set_xlabel("Scale factor")
axes[1, 0].set_ylabel("Divergence")
axes[1, 0].set_title("JS vs TV Divergence")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

x_g2 = np.linspace(-4, 4, 200)
for mu, sigma, label in [(0, 1, "N(0,1)"), (0.5, 1.2, "N(0.5,1.2)"), (1, 0.5, "N(1,0.5)")]:
    axes[1, 1].plot(x_g2, norm.pdf(x_g2, mu, sigma), lw=2, label=label)
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("Density")
axes[1, 1].set_title("Gaussian Distributions\nfor Divergence Comparison")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

beta_dist = beta(2, 5)
x_b = np.linspace(0, 1, 100)
axes[1, 2].plot(x_b, beta_dist.pdf(x_b), 'b-', lw=2, label="Beta(2,5)")
axes[1, 2].fill_between(x_b, beta_dist.pdf(x_b), alpha=0.3)
axes[1, 2].set_xlabel("x")
axes[1, 2].set_ylabel("Density")
axes[1, 2].set_title("Beta(2,5) - example density\nfor divergence computation")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/02-divergences.png")
plt.close()

print("=" * 60)
print("f-DIVERGENCES AND PROBABILITY METRICS")
print("=" * 60)
print(f"\nDiscrete distributions (p vs q):")
print(f"  KL(p||q)       = {kl:.6f}")
print(f"  JS(p,q)        = {js:.6f}")
print(f"  TV(p,q)        = {tv:.6f}")
print(f"  Chi^2(p||q)    = {chi2:.6f}")
print(f"  Hellinger²     = {h2:.6f}")
print(f"  Wasserstein-1  = {w1:.6f}")
print(f"\nWasserstein distances:")
print(f"  W1(N(0,1), N(2,1))  = {w1_gauss:.4f}")
print(f"  W1(N(0,1), N(0,3))  = {w1_gauss_r:.4f}")
print(f"\nKey relationships:")
print(f"  TV ≤ √(JS/2)  (Pinsker: KL ≥ 2·TV²)")
print(f"  H² ≤ KL")
print(f"  JS is bounded [0, log(2)], symmetric")
print(f"  Wasserstein captures geometry of the underlying space")
