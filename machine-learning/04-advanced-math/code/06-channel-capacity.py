"""04.06 Channel capacity via Blahut-Arimoto."""
import numpy as np
import matplotlib.pyplot as plt

def channel_capacity(P_yx, max_iter=1000, tol=1e-12):
    n, m = P_yx.shape
    P_x = np.ones(n) / n
    for _ in range(max_iter):
        P_x_old = P_x.copy()
        num = P_yx * P_x[:, None]
        denom = num.sum(axis=0)
        num_denom = num / (denom + 1e-300)
        P_x_new = np.exp(np.sum(P_yx * np.log(num_denom + 1e-300), axis=1))
        P_x_new /= P_x_new.sum()
        P_x = P_x_new
        if np.max(np.abs(P_x - P_x_old)) < tol:
            break
    C = 0
    for i in range(n):
        if P_x[i] > 0:
            num = P_yx * P_x[:, None]
            denom = num.sum(axis=0)
            C += P_x[i] * np.sum(P_yx[i] * np.log2(P_yx[i] / (denom + 1e-300)))
    return max(C, 0), P_x

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

p_flip = 0.1
P_yx_bsc = np.array([[1-p_flip, p_flip], [p_flip, 1-p_flip]])
C_bsc, P_x_bsc = channel_capacity(P_yx_bsc)
H_p = -p_flip * np.log2(p_flip) - (1-p_flip) * np.log2(1-p_flip)
C_theory = 1 - H_p

p_range = np.linspace(0.01, 0.99, 50)
caps_bsc = []
for p in p_range:
    P = np.array([[1-p, p], [p, 1-p]])
    c, _ = channel_capacity(P)
    caps_bsc.append(c)

axes[0, 0].plot(p_range, caps_bsc, 'b-', lw=2, label="Blahut-Arimoto")
axes[0, 0].plot(p_range, 1 - (-p_range*np.log2(p_range) - (1-p_range)*np.log2(1-p_range)),
               'r--', lw=2, label="Theoretical C = 1-H(p)")
axes[0, 0].set_xlabel("Crossover probability p")
axes[0, 0].set_ylabel("Capacity (bits)")
axes[0, 0].set_title("BSC: Channel Capacity")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

eps_range = np.linspace(0.01, 0.99, 50)
caps_bec = []
for eps in eps_range:
    P = np.array([[1-eps, eps, 0], [0, eps, 1-eps]])
    c, _ = channel_capacity(P)
    caps_bec.append(c)

axes[0, 1].plot(eps_range, caps_bec, 'orange', lw=2, label="Blahut-Arimoto")
axes[0, 1].plot(eps_range, 1 - eps_range, 'g--', lw=2, label="Theoretical C = 1-ε")
axes[0, 1].set_xlabel("Erasure probability ε")
axes[0, 1].set_ylabel("Capacity (bits)")
axes[0, 1].set_title("BEC: Channel Capacity")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_channels = ["BSC\np=0.1", "BSC\np=0.25", "BEC\nε=0.2", "BEC\nε=0.5"]
n_caps = [C_bsc, channel_capacity(np.array([[0.75, 0.25], [0.25, 0.75]]))[0],
          channel_capacity(np.array([[0.8, 0.2, 0], [0, 0.2, 0.8]]))[0],
          channel_capacity(np.array([[0.5, 0.5, 0], [0, 0.5, 0.5]]))[0]]
axes[0, 2].bar(n_channels, n_caps, color=['blue', 'green', 'orange', 'red'], alpha=0.7)
axes[0, 2].set_ylabel("Capacity (bits)")
axes[0, 2].set_title("Channel Capacity Comparison")
axes[0, 2].grid(True, axis='y', alpha=0.3)

P_x_capacity = P_x_bsc
axes[1, 0].bar([0, 1], P_x_capacity, color='steelblue', alpha=0.7)
axes[1, 0].set_xticks([0, 1])
axes[1, 0].set_xticklabels(["P(X=0)", "P(X=1)"])
axes[1, 0].set_ylabel("Probability")
axes[1, 0].set_title("Capacity-Achieving Distribution\nBSC (should be uniform)")
axes[1, 0].grid(True, axis='y', alpha=0.3)

P_noisy = np.array([[0.6, 0.3, 0.1], [0.1, 0.3, 0.6]])
C_noisy, P_x_noisy = channel_capacity(P_noisy)
caps_history = []
for iters in range(1, 101):
    c, _ = channel_capacity(P_noisy, max_iter=iters)
    caps_history.append(c)
axes[1, 1].plot(range(1, 101), caps_history, lw=2)
axes[1, 1].set_xlabel("Iteration")
axes[1, 1].set_ylabel("Capacity estimate")
axes[1, 1].set_title("Convergence of Blahut-Arimoto\n(3-output noisy channel)")
axes[1, 1].grid(True, alpha=0.3)

P_three = np.array([[0.9, 0.05, 0.05],
                    [0.05, 0.9, 0.05],
                    [0.05, 0.05, 0.9]])
C_three, P_x_three = channel_capacity(P_three)
axes[1, 2].imshow(P_three, cmap='Blues', interpolation='nearest', vmin=0, vmax=1)
for i in range(3):
    for j in range(3):
        axes[1, 2].text(j, i, f"{P_three[i, j]:.2f}", ha='center', va='center', fontsize=10)
axes[1, 2].set_xlabel("Output")
axes[1, 2].set_ylabel("Input")
axes[1, 2].set_title(f"3×3 Channel Matrix\nCapacity={C_three:.4f} bits")
plt.colorbar(axes[1, 2].images[0], ax=axes[1, 2])

plt.tight_layout()
plt.savefig("../../assets/phase04/06-channel-capacity.png")
plt.close()

print("=" * 60)
print("CHANNEL CAPACITY VIA BLAHUT-ARIMOTO")
print("=" * 60)
print(f"\nBinary Symmetric Channel (p={p_flip}):")
print(f"  Capacity = {C_bsc:.6f} bits")
print(f"  Theoretical: C = 1 - H({p_flip}) = 1 - {H_p:.6f} = {C_theory:.6f}")
print(f"  Match: {np.isclose(C_bsc, C_theory, atol=1e-4)}")

eps_val = 0.2
C_bec, P_x_bec = channel_capacity(np.array([[1-eps_val, eps_val, 0], [0, eps_val, 1-eps_val]]))
print(f"\nBinary Erasure Channel (ε={eps_val}):")
print(f"  Capacity = {C_bec:.6f} bits")
print(f"  Theoretical: C = 1 - ε = {1-eps_val:.6f}")

print(f"\nNoisy channel (3 inputs, 3 outputs):")
print(f"  Capacity = {C_three:.6f} bits")
print(f"\nThe Blahut-Arimoto algorithm computes capacity")
print(f"by alternating optimization over input and output distributions.")
