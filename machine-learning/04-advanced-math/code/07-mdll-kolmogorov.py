"""04.07 Minimum description length and Kolmogorov complexity."""
import numpy as np
import matplotlib.pyplot as plt

def kolmogorov_complexity_lower_bound(sequence):
    seq_str = "".join(str(int(s)) for s in sequence)
    n = len(seq_str)
    best = n
    for length in range(1, min(n // 2 + 1, 10)):
        pattern = seq_str[:length]
        repeats = n // length
        compressed = pattern * repeats
        if compressed[:n] == seq_str[:n]:
            complexity = length + 8
            if complexity < best:
                best = complexity
            break
    return best

np.random.seed(42)
random_seq = np.random.randint(0, 2, 100)
periodic_seq = np.tile([1, 0, 1, 1, 0], 20)
constant_seq = np.ones(100, dtype=int)

kc_random = kolmogorov_complexity_lower_bound(random_seq)
kc_periodic = kolmogorov_complexity_lower_bound(periodic_seq)
kc_constant = kolmogorov_complexity_lower_bound(constant_seq)

n_values = [10, 20, 50, 100, 200]
mdl_values = []
for n in n_values:
    seq = np.random.randint(0, 2, n)
    kc = kolmogorov_complexity_lower_bound(seq)
    mdl = kc + 0.5 * n * np.log(n)
    mdl_values.append(mdl)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

labels = ["Random", "Periodic", "Constant"]
complexities = [kc_random, kc_periodic, kc_constant]
colors = ["red", "green", "blue"]
axes[0, 0].bar(labels, complexities, color=colors, alpha=0.7)
axes[0, 0].set_ylabel("Kolmogorov complexity (bits, lower bound)")
axes[0, 0].set_title("Kolmogorov Complexity of Sequences (n=100)")
axes[0, 0].grid(True, axis="y", alpha=0.3)

for i, (seq, name) in enumerate(zip(
        [random_seq, periodic_seq, constant_seq],
        ["Random", "Periodic", "Constant"])):
    axes[0, 1].plot(seq[:50] + i * 1.5, "o-", ms=3, lw=1, label=name, color=colors[i])
axes[0, 1].set_xlabel("Index")
axes[0, 1].set_ylabel("Value (offset)")
axes[0, 1].set_title("Sequence Patterns (first 50)")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(n_values, mdl_values, "o-", lw=2)
axes[0, 2].set_xlabel("n")
axes[0, 2].set_ylabel("MDL score")
axes[0, 2].set_title("MDL for Random Sequences")
axes[0, 2].grid(True, alpha=0.3)

data = np.random.randn(50)
models = [1, 2, 3, 5, 10]
aics, bics = [], []
for k in models:
    coeffs = np.polyfit(np.arange(50), data, k - 1)
    pred = np.polyval(coeffs, np.arange(50))
    residuals = data - pred
    nll = 0.5 * 50 * np.log(2 * np.pi * np.var(residuals)) + 50 / 2
    aic_val = 2 * k + 2 * nll
    bic_val = k * np.log(50) + 2 * nll
    aics.append(aic_val)
    bics.append(bic_val)

axes[1, 0].plot(models, aics, "o-", lw=2, label="AIC")
axes[1, 0].plot(models, bics, "s-", lw=2, label="BIC")
axes[1, 0].set_xlabel("Model complexity (k)")
axes[1, 0].set_ylabel("Criterion")
axes[1, 0].set_title("AIC/BIC vs Model Complexity")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

x_mdl = np.linspace(0, 1, 100)
y_mdl = np.sin(2 * np.pi * x_mdl) + 0.1 * np.random.randn(100)
deg = [1, 3, 10, 20]
axes[1, 1].plot(x_mdl, np.sin(2 * np.pi * x_mdl), "k--", lw=2, label="True")
for d in deg:
    coeffs = np.polyfit(x_mdl, y_mdl, d)
    pred = np.polyval(coeffs, x_mdl)
    axes[1, 1].plot(x_mdl, pred, lw=1.5, label=f"deg={d}")
axes[1, 1].scatter(x_mdl, y_mdl, s=5, alpha=0.3, color="gray")
axes[1, 1].set_xlabel("x")
axes[1, 1].set_ylabel("y")
axes[1, 1].set_title("Polynomial fitting: MDL perspective")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

compression = [kc_random / len(random_seq), kc_periodic / len(periodic_seq),
               kc_constant / len(constant_seq)]
axes[1, 2].bar(labels, compression, color=colors, alpha=0.7)
axes[1, 2].set_ylabel("Bits per symbol")
axes[1, 2].set_title("Compression Ratio")
axes[1, 2].grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/07-mdll-kolmogorov.png")
plt.close()

print("=" * 60)
print("MDL AND KOLMOGOROV COMPLEXITY")
print("=" * 60)
print(f"\nKolmogorov complexity lower bound (n=100):")
print(f"  Random seq:  {kc_random} bits ({kc_random/len(random_seq):.2f} bits/symbol)")
print(f"  Periodic seq: {kc_periodic} bits ({kc_periodic/len(periodic_seq):.2f} bits/symbol)")
print(f"  Constant seq: {kc_constant} bits ({kc_constant/len(constant_seq):.2f} bits/symbol)")

print(f"\nAIC/BIC for polynomial regression:")
best_aic_idx = np.argmin(aics)
best_bic_idx = np.argmin(bics)
print(f"  AIC optimal model: k={models[best_aic_idx]}")
print(f"  BIC optimal model: k={models[best_bic_idx]}")
print(f"\nKey ideas:")
print(f"  MDL = -log P(data|model) + complexity(model)")
print(f"  Kolmogorov complexity = length of shortest program")
print(f"  Occam's razor: simpler explanations are better")
