"""04.05 Rate-distortion theory and the Blahut-Arimoto algorithm."""
import numpy as np
import matplotlib.pyplot as plt

def rate_distortion_blahut_arimoto(Px, d, beta, max_iter=1000, tol=1e-8):
    n, m = d.shape
    Q = np.random.rand(n, m)
    Q /= Q.sum(axis=1, keepdims=True)
    for _ in range(max_iter):
        Q_old = Q.copy()
        r_marg = (Px[:, None] * Q).sum(axis=0)
        r_marg += 1e-300
        phi = np.exp(-beta * d)
        num = r_marg[None, :] * phi
        Q = num / num.sum(axis=1, keepdims=True)
        Q = np.nan_to_num(Q, nan=1/m)
        Q /= Q.sum(axis=1, keepdims=True)
        if np.max(np.abs(Q - Q_old)) < tol:
            break
    r_marg = (Px[:, None] * Q).sum(axis=0)
    r_marg += 1e-300
    r_marg /= r_marg.sum()
    distortion = np.sum(Px[:, None] * Q * d)
    mi = 0
    for i in range(n):
        for j in range(m):
            if Px[i] > 0 and Q[i, j] > 0 and r_marg[j] > 0:
                mi += Px[i] * Q[i, j] * np.log2(Q[i, j] / r_marg[j])
    return max(mi, 0), distortion

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

Px = np.array([0.5, 0.5])
d = np.array([[0., 1.], [1., 0.]])
betas = np.logspace(-1, 3, 30)
rates, dists = [], []
for beta in betas:
    R, D = rate_distortion_blahut_arimoto(Px, d, beta)
    rates.append(R)
    dists.append(D)

axes[0, 0].plot(dists, rates, 'o-', lw=2)
axes[0, 0].set_xlabel("Distortion D")
axes[0, 0].set_ylabel("Rate R (bits)")
axes[0, 0].set_title("Rate-Distortion Curve\nBinary Source, Hamming Distortion")
axes[0, 0].grid(True, alpha=0.3)

D_target = np.linspace(0.01, 0.5, 10)
R_theory = 1 - (-D_target * np.log2(D_target) - (1-D_target) * np.log2(1-D_target))
R_theory = np.maximum(R_theory, 0)
axes[0, 0].plot(D_target, R_theory, 'r--', lw=2, label="Theoretical R(D)")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

Px_3 = np.array([0.3, 0.4, 0.3])
d_3 = np.array([[0., 1., 1.], [1., 0., 1.], [1., 1., 0.]])
rates_3, dists_3 = [], []
for beta in betas:
    R, D = rate_distortion_blahut_arimoto(Px_3, d_3, beta)
    rates_3.append(R)
    dists_3.append(D)

axes[0, 1].plot(dists_3, rates_3, 'o-', lw=2, color='orange')
axes[0, 1].set_xlabel("Distortion D")
axes[0, 1].set_ylabel("Rate R (bits)")
axes[0, 1].set_title("Rate-Distortion: 3-ary Source\n(Uniform)")
axes[0, 1].grid(True, alpha=0.3)

sigma2 = 1.0
D_grid = np.linspace(0.01, 0.5, 50)
R_gauss = 0.5 * np.maximum(np.log2(sigma2 / D_grid), 0)
axes[0, 2].plot(D_grid, R_gauss, 'g-', lw=2)
axes[0, 2].set_xlabel("Distortion D (MSE)")
axes[0, 2].set_ylabel("Rate R (bits)")
axes[0, 2].set_title("Gaussian R(D): R = ½log₂(σ²/D)")
axes[0, 2].grid(True, alpha=0.3)

beta_idx = [0, 5, 10, 15, 20, 25]
axes[1, 0].semilogx(betas, rates, 'o-', lw=2, label="Binary")
axes[1, 0].semilogx(betas, rates_3, 's-', lw=2, label="3-ary")
axes[1, 0].set_xlabel("β (inverse temperature)")
axes[1, 0].set_ylabel("Rate R (bits)")
axes[1, 0].set_title("Rate vs β in Blahut-Arimoto")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

Px_skew = np.array([0.9, 0.1])
rates_skew, dists_skew = [], []
for beta in betas:
    R, D = rate_distortion_blahut_arimoto(Px_skew, d, beta)
    rates_skew.append(R)
    dists_skew.append(D)

axes[1, 1].plot(dists, rates, 'o-', lw=2, label="Uniform Px=(0.5,0.5)")
axes[1, 1].plot(dists_skew, rates_skew, 's-', lw=2, label="Skewed Px=(0.9,0.1)")
axes[1, 1].set_xlabel("Distortion D")
axes[1, 1].set_ylabel("Rate R (bits)")
axes[1, 1].set_title("Effect of Source Distribution on R(D)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

d_cont = np.array([[0., 0.5, 1.], [1., 0.5, 0.]])
rates_cont, dists_cont = [], []
for beta in betas:
    R, D = rate_distortion_blahut_arimoto(Px, d_cont, beta)
    rates_cont.append(R)
    dists_cont.append(D)

axes[1, 2].plot(dists_cont, rates_cont, 'o-', lw=2, color='purple')
axes[1, 2].set_xlabel("Distortion D")
axes[1, 2].set_ylabel("Rate R (bits)")
axes[1, 2].set_title("Non-binary Distortion Matrix")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/05-rate-distortion.png")
plt.close()

print("=" * 60)
print("RATE-DISTORTION THEORY")
print("=" * 60)
print("\nBinary source (p=0.5), Hamming distortion:")
print(f"{'β':>8s} {'Rate':>8s} {'Distortion':>12s}")
print("-" * 30)
for i in range(0, len(betas), 5):
    print(f"{betas[i]:>8.2f} {rates[i]:>8.4f} {dists[i]:>12.4f}")

print(f"\nGaussian R(D) benchmark: R(0.1) = 0.5*log₂(1/0.1) = {0.5 * np.log2(1/0.1):.4f}")
print(f"Binary R(D=0) at β=∞: R = {rates[-1]:.4f} bits (should be H(p) = 1.0)")
print(f"\nThe Blahut-Arimoto algorithm iteratively computes R(D).")
