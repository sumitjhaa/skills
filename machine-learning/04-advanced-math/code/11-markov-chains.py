"""04.11 Markov chains, ergodicity, and stationary distributions."""
import numpy as np
import matplotlib.pyplot as plt

P = np.array([[0.7, 0.3], [0.4, 0.6]])

def simulate_markov(P, n_steps, start=0):
    n = P.shape[0]
    states = [start]
    for _ in range(n_steps):
        states.append(np.random.choice(n, p=P[states[-1]]))
    return np.array(states)

np.random.seed(42)
n_steps = 100
states = simulate_markov(P, n_steps)

n_states = P.shape[0]
pi = np.ones(n_states) / n_states
for _ in range(100):
    pi = pi @ P

eigvals, eigvecs = np.linalg.eig(P.T)
stationary_idx = np.argmin(np.abs(eigvals - 1.0))
pi_eig = np.real(eigvecs[:, stationary_idx])
pi_eig = pi_eig / pi_eig.sum()

P_3 = np.array([[0.5, 0.3, 0.2], [0.2, 0.6, 0.2], [0.1, 0.3, 0.6]])
pi_3 = np.ones(3) / 3
for _ in range(100):
    pi_3 = pi_3 @ P_3

states_3 = [0]
for _ in range(n_steps):
    states_3.append(np.random.choice(3, p=P_3[states_3[-1]]))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].step(range(n_steps+1), states, lw=1.5)
axes[0, 0].set_xlabel("Time step")
axes[0, 0].set_ylabel("State")
axes[0, 0].set_yticks([0, 1])
axes[0, 0].set_title(f"2-State Markov Chain\nP(0→1)={P[0,1]}, P(1→0)={P[1,0]}")
axes[0, 0].grid(True, alpha=0.3)

empirical_dist = np.zeros(2)
for s in states[n_steps//2:]:
    empirical_dist[s] += 1
empirical_dist /= empirical_dist.sum()
axes[0, 1].bar(np.arange(2) - 0.15, pi, width=0.3, alpha=0.7, label="Stationary")
axes[0, 1].bar(np.arange(2) + 0.15, empirical_dist, width=0.3, alpha=0.7,
               label="Empirical")
axes[0, 1].set_xticks([0, 1])
axes[0, 1].set_ylabel("Probability")
axes[0, 1].set_title("Stationary Distribution")
axes[0, 1].legend()
axes[0, 1].grid(True, axis="y", alpha=0.3)

im = axes[0, 2].imshow(P, cmap="Blues", vmin=0, vmax=1, interpolation="nearest")
for i in range(2):
    for j in range(2):
        axes[0, 2].text(j, i, f"{P[i, j]:.2f}", ha="center", va="center", fontsize=12)
axes[0, 2].set_xlabel("Next state")
axes[0, 2].set_ylabel("Current state")
axes[0, 2].set_title("Transition Matrix P")
plt.colorbar(im, ax=axes[0, 2])

taus = np.arange(1, 50)
acf = np.array([np.corrcoef(states[:-t], states[t:])[0, 1] if t < len(states) else 0
                for t in taus])
axes[1, 0].plot(taus, acf, "o-", lw=2)
axes[1, 0].axhline(0, color="gray", ls="--")
axes[1, 0].set_xlabel("Lag τ")
axes[1, 0].set_ylabel("Autocorrelation")
axes[1, 0].set_title("Autocorrelation Function\n(2-state chain)")
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].step(range(n_steps+1), states_3, lw=1.5)
axes[1, 1].set_xlabel("Time step")
axes[1, 1].set_ylabel("State")
axes[1, 1].set_yticks([0, 1, 2])
axes[1, 1].set_title(f"3-State Markov Chain\nStationary π={np.round(pi_3, 3)}")
axes[1, 1].grid(True, alpha=0.3)

P_multi = np.linalg.matrix_power(P, 5)
P_multi_10 = np.linalg.matrix_power(P, 10)
P_multi_50 = np.linalg.matrix_power(P, 50)
step_range = [1, 2, 5, 10, 50]
entries = []
for k in step_range:
    Pk = np.linalg.matrix_power(P, k)
    entries.append(Pk[0, 0])
axes[1, 2].plot(step_range, entries, "o-", lw=2)
axes[1, 2].axhline(pi[0], color="r", ls="--", label=f"π₀={pi[0]:.3f}")
axes[1, 2].set_xlabel("Steps k")
axes[1, 2].set_ylabel("P^k(0→0)")
axes[1, 2].set_title("Convergence to Stationarity\nP^k(0→0) vs k")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/11-markov-chains.png")
plt.close()

print("=" * 60)
print("MARKOV CHAINS")
print("=" * 60)
print(f"\nTransition matrix P (2-state):")
print(P)
print(f"\nStationary distribution:")
print(f"  Power iteration:  π = [{pi[0]:.4f}, {pi[1]:.4f}]")
print(f"  Eigendecomposition: π = [{pi_eig[0]:.4f}, {pi_eig[1]:.4f}]")

print(f"\nP^5:")
print(np.round(P_multi, 4))
print(f"P^10:")
print(np.round(P_multi_10, 4))
print(f"P^50:")
print(np.round(P_multi_50, 4))

print(f"\n3-state chain:")
print(f"  Stationary: {np.round(pi_3, 4)}")
empirical_3 = np.zeros(3)
for s in states_3[len(states_3)//2:]:
    empirical_3[s] += 1
empirical_3 /= empirical_3.sum()
print(f"  Empirical:  {np.round(empirical_3, 4)}")

print(f"\nStationary condition: π = πP")
print(f"  πP - π = {np.round(pi @ P - pi, 6)}")
print(f"Detailed balance: π_i P_ij = π_j P_ji")
print(f"  Check: {pi[0]*P[0,1]:.4f} vs {pi[1]*P[1,0]:.4f}")
