"""04.16 Stochastic calculus: Ito integrals and SDEs."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

def euler_maruyama(drift, diffusion, x0, T=1.0, dt=0.001, n_paths=5):
    n_steps = int(T / dt)
    x = np.zeros((n_steps + 1, n_paths))
    x[0] = x0
    t = np.linspace(0, T, n_steps + 1)
    for i in range(n_steps):
        dw = np.sqrt(dt) * np.random.randn(n_paths)
        x[i+1] = x[i] + drift(x[i], t[i]) * dt + diffusion(x[i], t[i]) * dw
    return t, x

def ito_integral(f, T=1.0, dt=0.0001, n_paths=1):
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps + 1)
    dw = np.sqrt(dt) * np.random.randn(n_steps, n_paths)
    w_path = np.vstack([np.zeros((1, n_paths)), np.cumsum(dw, axis=0)])
    integrand = f(w_path[:-1], t[:-1])
    if integrand.ndim == 1:
        integrand = integrand[:, None]
    integral = np.cumsum(integrand * dw, axis=0)
    return t, w_path, integral

drift_gbm = lambda x, t: 0.05 * x
diff_gbm = lambda x, t: 0.2 * x
t, gbm = euler_maruyama(drift_gbm, diff_gbm, 1.0, T=2.0, dt=0.001, n_paths=5)

drift_ou = lambda x, t: -1.0 * x
diff_ou = lambda x, t: 0.5 * np.ones_like(x)
t_ou, ou_paths = euler_maruyama(drift_ou, diff_ou, 2.0, T=3.0, dt=0.001, n_paths=5)

drift_linear = lambda x, t: 0.0 * x
diff_linear = lambda x, t: t
t_ito, w_ito, ito_int = ito_integral(lambda w, t: t, T=1.0, dt=0.0001, n_paths=3)

drift_sin = lambda x, t: np.sin(t)
diff_sin = lambda x, t: 0.3 * np.ones_like(x)
t_sin, sin_paths = euler_maruyama(drift_sin, diff_sin, 0.0, T=5.0, dt=0.01, n_paths=3)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for i in range(gbm.shape[1]):
    axes[0, 0].plot(t, gbm[:, i], lw=1.5)
axes[0, 0].set_xlabel("t")
axes[0, 0].set_ylabel("S(t)")
axes[0, 0].set_title("Geometric Brownian Motion\ndS = 0.05·S·dt + 0.2·S·dW")
axes[0, 0].grid(True, alpha=0.3)

gbm_theory = 1.0 * np.exp((0.05 - 0.5*0.2**2) * t)
axes[0, 0].plot(t, gbm_theory, "k--", lw=2, label="E[S(t)]")
axes[0, 0].legend()

for i in range(ou_paths.shape[1]):
    axes[0, 1].plot(t_ou, ou_paths[:, i], lw=1.5)
axes[0, 1].axhline(0, color="k", ls="--", alpha=0.5)
axes[0, 1].set_xlabel("t")
axes[0, 1].set_ylabel("X(t)")
axes[0, 1].set_title("Ornstein-Uhlenbeck Process\ndX = -X·dt + 0.5·dW")
axes[0, 1].grid(True, alpha=0.3)

for i in range(ito_int.shape[1]):
    axes[0, 2].plot(t_ito[1:], ito_int[:, i], lw=1.5)
axes[0, 2].set_xlabel("t")
axes[0, 2].set_ylabel("∫₀ᵗ s·dW(s)")
axes[0, 2].set_title("Ito Integral: ∫₀ᵗ s·dW(s)")
axes[0, 2].grid(True, alpha=0.3)

for i in range(sin_paths.shape[1]):
    axes[1, 0].plot(t_sin, sin_paths[:, i], lw=1.5, label=f"Path {i+1}" if i == 0 else "")
axes[1, 0].set_xlabel("t")
axes[1, 0].set_ylabel("X(t)")
axes[1, 0].set_title("SDE with Sinusoidal Drift\ndX = sin(t)·dt + 0.3·dW")
axes[1, 0].grid(True, alpha=0.3)

dts = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
gbm_final = {}
for dt_val in dts:
    t_dt, gbm_dt = euler_maruyama(drift_gbm, diff_gbm, 1.0, T=1.0, dt=dt_val, n_paths=1000)
    gbm_final[dt_val] = np.mean(gbm_dt[-1])
dts_plot = [d for d in dts]
final_vals = [gbm_final[d] for d in dts]
axes[1, 1].loglog(dts, final_vals, "o-", lw=2)
axes[1, 1].axhline(np.exp(0.05), color="r", ls="--", label="True E[S(1)]")
axes[1, 1].set_xlabel("dt")
axes[1, 1].set_ylabel("E[S(1)] (empirical)")
axes[1, 1].set_title("SDE Discretization Error\n(1000 paths)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

n_paths_plot = [10, 50, 100, 500, 1000, 5000]
mean_ests = []
for np_ in n_paths_plot:
    t_n, gbm_n = euler_maruyama(drift_gbm, diff_gbm, 1.0, T=1.0, dt=0.01, n_paths=np_)
    mean_ests.append(np.mean(gbm_n[-1]))
axes[1, 2].loglog(n_paths_plot, np.abs(np.array(mean_ests) - np.exp(0.05)), "o-", lw=2)
axes[1, 2].loglog(n_paths_plot, 1/np.sqrt(n_paths_plot), "--", lw=2, label="O(1/√n)")
axes[1, 2].set_xlabel("Number of paths")
axes[1, 2].set_ylabel("|Error in E[S(1)]|")
axes[1, 2].set_title("MC Convergence for SDEs")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase04/16-stochastic-calculus.png")
plt.close()

print("=" * 60)
print("STOCHASTIC CALCULUS")
print("=" * 60)
gbm_final_t = gbm[-1]
print(f"\nGeometric Brownian Motion (S₀=1, μ=0.05, σ=0.2):")
print(f"  E[S(2)] = {np.mean(gbm_final_t):.4f} (theoretical: {np.exp(0.05*2):.4f})")
print(f"  Var[S(2)] = {np.var(gbm_final_t):.4f}")

ou_final = ou_paths[-1]
print(f"\nOrnstein-Uhlenbeck (θ=1, σ=0.5, X₀=2):")
print(f"  E[X(3)] = {np.mean(ou_final):.4f} (theoretical: 0)")
print(f"  Var[X(3)] = {np.var(ou_final):.6f} (theoretical: σ²/(2θ) = 0.125)")

print(f"\nIto integral ∫₀¹ s·dW(s) stats:")
print(f"  E[I] = {np.mean(ito_int[-1]):.4f} (theoretical: 0)")
print(f"  Var[I] = {np.var(ito_int[-1]):.6f} (theoretical: ∫₀¹ s²·ds = 1/3 = {1/3:.6f})")

print(f"\nIto's formula: df = (∂f/∂t + μ·∂f/∂x + ½σ²·∂²f/∂x²)dt + σ·∂f/∂x·dW")
print(f"Euler-Maruyama: strong order 0.5, weak order 1.0")
