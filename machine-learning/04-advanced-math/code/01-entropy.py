"""04.01 Entropy, cross-entropy, and KL divergence."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy, norm, binom, beta as beta_dist

p = np.array([0.2, 0.3, 0.5])
q = np.array([0.25, 0.25, 0.5])
r = np.array([0.1, 0.4, 0.5])

H_p = entropy(p, base=2)
H_q = entropy(q, base=2)
H_r = entropy(r, base=2)

kl_pq = np.sum(p * np.log2(p / q))
kl_pr = np.sum(p * np.log2(p / r))
kl_qp = np.sum(q * np.log2(q / p))

ce_pq = H_p + kl_pq

joint = np.array([[0.1, 0.2], [0.3, 0.4]])
p_x = joint.sum(axis=1)
p_y = joint.sum(axis=0)
p_xp_y = np.outer(p_x, p_y)
mi = np.sum(joint * np.log2(joint / p_xp_y))

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

x_idx = np.arange(3)
width = 0.3
axes[0].bar(x_idx - width, p, width, label="p", alpha=0.8)
axes[0].bar(x_idx, q, width, label="q", alpha=0.8)
axes[0].bar(x_idx + width, r, width, label="r", alpha=0.8)
axes[0].set_xticks(x_idx)
axes[0].set_xticklabels(["x₁", "x₂", "x₃"])
axes[0].set_ylabel("Probability")
axes[0].set_title("Distributions")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

measures = ["H(p)", "H(q)", "H(r)", "KL(p||q)", "KL(p||r)", "KL(q||p)", "CE(p,q)"]
values = [H_p, H_q, H_r, kl_pq, kl_pr, kl_qp, ce_pq]
colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'teal']
axes[1].bar(measures, values, color=colors, alpha=0.7)
axes[1].set_ylabel("Bits")
axes[1].set_title("Entropy, KL, and Cross-Entropy")
axes[1].tick_params(axis='x', rotation=30)
axes[1].grid(True, axis='y', alpha=0.3)

x_gauss = np.linspace(-5, 5, 200)
kl_gauss = 0.5 * (np.log(1) - np.log(1) + 1 + 0 - 1)
for mu, sigma, label, color in [(0, 1, "N(0,1)", "blue"), (0, 2, "N(0,4)", "red")]:
    axes[2].plot(x_gauss, norm.pdf(x_gauss, mu, sigma), lw=2, label=label, color=color)
axes[2].set_xlabel("x")
axes[2].set_ylabel("Density")
axes[2].set_title(f"KL(N(0,4)||N(0,1))={0.5*(np.log(1)-np.log(4)+1+(0-0)/1-1):.3f} nats")
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/01-entropy.png")
plt.close()

print("=" * 60)
print("ENTROPY, CROSS-ENTROPY, AND KL DIVERGENCE")
print("=" * 60)
print(f"\nDistributions:")
print(f"  p = {p}")
print(f"  q = {q}")
print(f"  r = {r}")
print(f"\nEntropy:")
print(f"  H(p) = {H_p:.4f} bits")
print(f"  H(q) = {H_q:.4f} bits")
print(f"  H(r) = {H_r:.4f} bits")
print(f"\nKL Divergence:")
print(f"  KL(p||q) = {kl_pq:.4f} bits")
print(f"  KL(p||r) = {kl_pr:.4f} bits")
print(f"  KL(q||p) = {kl_qp:.4f} bits")
print(f"  KL(p||q) = 0 iff p = q (asymmetry: KL(p||q) ≠ KL(q||p))")
print(f"\nCross-Entropy:")
print(f"  CE(p,q) = {ce_pq:.4f} bits")
print(f"  CE(p,q) = H(p) + KL(p||q) = {H_p:.4f} + {kl_pq:.4f} = {H_p + kl_pq:.4f}")
print(f"\nMutual Information (joint distribution):")
print(f"  I(X;Y) = {mi:.4f} bits")
H_xy = -np.sum(joint * np.log2(joint + 1e-300))
print(f"  H(X,Y) = {H_xy:.4f} bits")
print(f"  I(X;Y) = H(X) + H(Y) - H(X,Y) = {entropy(p_x, base=2):.4f} + {entropy(p_y, base=2):.4f} - {H_xy:.4f} = {entropy(p_x, base=2) + entropy(p_y, base=2) - H_xy:.4f}")
