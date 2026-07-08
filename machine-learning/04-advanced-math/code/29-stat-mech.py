"""04.29 Statistical mechanics: Ising model, Boltzmann distribution."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def ising_energy(spins, J=1.0, H=0.0):
    n = len(spins)
    interaction = 0
    for i in range(n):
        for j in range(i+1, n):
            interaction += spins[i] * spins[j]
    return -J * interaction / (n*(n-1)/2) - H * np.sum(spins) / n

def metropolis_ising(n_spins=100, J=1.0, H=0.0, beta=1.0, n_steps=10000):
    spins = np.random.choice([-1, 1], size=n_spins)
    energies = [ising_energy(spins, J, H)]
    for _ in range(n_steps):
        i = np.random.randint(n_spins)
        dE = 2 * J * spins[i] * np.sum(spins) / (n_spins*(n_spins-1)/2) + 2 * H * spins[i] / n_spins
        if np.random.rand() < np.exp(-beta * dE) or dE < 0:
            spins[i] *= -1
        energies.append(ising_energy(spins, J, H))
    return spins, np.array(energies)

def ising_mean_field(T, J=1.0, tol=1e-8, max_iter=100):
    m = 0.5
    for _ in range(max_iter):
        m_new = np.tanh(J * m / T)
        if abs(m_new - m) < tol:
            break
        m = m_new
    return m

n_spins = 100
betas = np.linspace(0.1, 2, 20)
all_magnetizations = []
for b in betas:
    spins, _ = metropolis_ising(n_spins, J=1.0, H=0.0, beta=b, n_steps=5000)
    all_magnetizations.append(np.abs(np.mean(spins)))

Tc = 1.0
T_range = np.linspace(0.1, 3, 50)
mf_mags = [ising_mean_field(T) for T in T_range]

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

spins_hot, _ = metropolis_ising(n_spins, J=1.0, H=0.0, beta=0.3, n_steps=5000)
spins_cold, _ = metropolis_ising(n_spins, J=1.0, H=0.0, beta=1.5, n_steps=5000)

axes[0, 0].imshow(spins_hot.reshape(10, 10), cmap="coolwarm", vmin=-1, vmax=1,
                  interpolation="nearest")
axes[0, 0].set_title("Ising: High T (disordered)\nβ=0.3")
plt.colorbar(axes[0, 0].images[0], ax=axes[0, 0])

axes[0, 1].imshow(spins_cold.reshape(10, 10), cmap="coolwarm", vmin=-1, vmax=1,
                  interpolation="nearest")
axes[0, 1].set_title("Ising: Low T (ordered)\nβ=1.5")
plt.colorbar(axes[0, 1].images[0], ax=axes[0, 1])

axes[0, 2].plot(betas, all_magnetizations, "o-", lw=2)
axes[0, 2].axvline(1/Tc, color="r", ls="--", label=f"T_c={Tc}")
axes[0, 2].set_xlabel("β = 1/T")
axes[0, 2].set_ylabel("|Magnetization|")
axes[0, 2].set_title("Phase Transition\n1D Ising (finite size)")
axes[0, 2].legend()
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(T_range, mf_mags, "b-", lw=2)
axes[1, 0].axvline(Tc, color="r", ls="--", label=f"T_c={Tc}")
axes[1, 0].set_xlabel("T (temperature)")
axes[1, 0].set_ylabel("m (magnetization)")
axes[1, 0].set_title("Mean Field Ising\nT_c = 1 (1D)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

spins_mc, energies_mc = metropolis_ising(n_spins, J=1.0, H=0.0, beta=0.8, n_steps=10000)
axes[1, 1].plot(energies_mc, lw=1)
axes[1, 1].axhline(np.mean(energies_mc[2000:]), color="r", ls="--",
                   label=f"⟨E⟩={np.mean(energies_mc[2000:]):.4f}")
axes[1, 1].set_xlabel("MCMC step")
axes[1, 1].set_ylabel("Energy per spin")
axes[1, 1].set_title("Energy Convergence\n(β=0.8, near T_c)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

H_range = np.linspace(-1, 1, 20)
mags_H = []
for h in H_range:
    spins_h, _ = metropolis_ising(n_spins, J=1.0, H=h, beta=1.0, n_steps=5000)
    mags_H.append(np.mean(spins_h))
axes[1, 2].plot(H_range, mags_H, "o-", lw=2)
axes[1, 2].set_xlabel("External field H")
axes[1, 2].set_ylabel("Magnetization ⟨m⟩")
axes[1, 2].set_title("Response to External Field\nβ=1")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/29-stat-mech.png")
plt.close()

print("=" * 60)
print("STATISTICAL MECHANICS")
print("=" * 60)
print(f"\nIsing model (1D, {n_spins} spins):")
print(f"  High T (β=0.3): mean |m| = {np.abs(np.mean(spins_hot)):.4f}")
print(f"  Low T  (β=1.5): mean |m| = {np.abs(np.mean(spins_cold)):.4f}")

print(f"\nPhase transition:")
print(f"  Critical temp (mean field): T_c = 1")
print(f"  β_c = 1/T_c = 1.0")

print(f"\nBoltzmann distribution:")
print(f"  P(state) ∝ exp(-β·E(state))")
E_hot = ising_energy(spins_hot)
E_cold = ising_energy(spins_cold)
print(f"  E(high T) = {E_hot:.4f}, E(low T) = {E_cold:.4f}")
ratio = np.exp(-1.5 * E_cold) / np.exp(-0.3 * E_hot)
print(f"  P(cold)/P(hot) ∝ exp(-β_cE_c + β_hE_h)")

print(f"\nKey concepts:")
print(f"  • Boltzmann factor: exp(-βE)")
print(f"  • Partition function: Z = Σ exp(-βE)")
print(f"  • Free energy: F = -T·log Z")
print(f"  • Phase transition at critical T")
print(f"  • MC sampling for high-dimensional state spaces")
