"""03.29 Survival Analysis: Kaplan-Meier estimator."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 200
shape, scale = 1.5, 2.0
T = scale * np.random.weibull(shape, n)
C = np.random.uniform(0, 5, n)
Y = np.minimum(T, C)
delta = (T <= C).astype(float)

order = np.argsort(Y)
Y_sorted = Y[order]
delta_sorted = delta[order]
unique_times = np.unique(Y_sorted[delta_sorted == 1])

survival = np.ones(len(unique_times) + 1)
at_risk = n
for i, t in enumerate(unique_times):
    events = np.sum((Y_sorted >= t) & (delta_sorted == 1) & (np.abs(Y_sorted - t) < 1e-10))
    censored_before = np.sum((Y_sorted < t) & (delta_sorted == 0))
    if at_risk > 0:
        survival[i+1] = survival[i] * (1 - events / at_risk)
    at_risk -= events + (np.sum(np.abs(Y_sorted - t) < 1e-10) - events)

survival = survival[:-1]
t_grid = np.linspace(0, 5, 200)
true_surv = np.exp(-(t_grid / scale)**shape)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].step(unique_times, survival, where='post', lw=2, label="Kaplan-Meier")
axes[0, 0].plot(t_grid, true_surv, 'r--', lw=2, label="True Weibull S(t)")
axes[0, 0].set_xlabel("Time")
axes[0, 0].set_ylabel("Survival Probability")
axes[0, 0].set_title(f"Kaplan-Meier Estimator (censoring rate: {1 - delta.mean():.1%})")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

n_at_risk = np.zeros(len(unique_times))
for i, t in enumerate(unique_times):
    n_at_risk[i] = np.sum(Y_sorted >= t)
ax2 = axes[0, 0].twinx()
ax2.plot(unique_times, n_at_risk, 'g:', lw=1, alpha=0.5)
ax2.set_ylabel("Number at risk", color='g')

greenwood_var = survival**2 * np.cumsum(
    [delta_sorted[np.argmin(np.abs(Y_sorted - t))] /
     (n_at_risk[i] * (n_at_risk[i] - 1) + 1e-10)
     for i, t in enumerate(unique_times)])
greenwood_se = np.sqrt(np.maximum(greenwood_var, 0))
ci_upper = np.minimum(survival + 1.96 * greenwood_se, 1)
ci_lower = np.maximum(survival - 1.96 * greenwood_se, 0)

axes[0, 1].step(unique_times, survival, where='post', lw=2, label="KM Estimate")
axes[0, 1].fill_between(unique_times, ci_lower, ci_upper, step='post', alpha=0.3, color='b', label="95% CI")
axes[0, 1].plot(t_grid, true_surv, 'r--', lw=2, label="True S(t)")
axes[0, 1].set_xlabel("Time")
axes[0, 1].set_ylabel("Survival Probability")
axes[0, 1].set_title("KM with 95% Greenwood Confidence Bands")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

n_sim = 500
km_sims = []
for s in range(n_sim):
    T_sim = scale * np.random.weibull(shape, n)
    C_sim = np.random.uniform(0, 5, n)
    Y_sim = np.minimum(T_sim, C_sim)
    delta_sim = (T_sim <= C_sim).astype(float)
    order_s = np.argsort(Y_sim)
    Ys = Y_sim[order_s]
    ds = delta_sim[order_s]
    ut = np.unique(Ys[ds == 1])
    surv = np.ones(len(ut))
    ar = n
    for j, t in enumerate(ut):
        ev = np.sum((Ys >= t) & (ds == 1) & (np.abs(Ys - t) < 1e-10))
        if ar > 0:
            surv[j] = surv[j-1] * (1 - ev / ar)
        ar -= ev + (np.sum(np.abs(Ys - t) < 1e-10) - ev)
    km_interp = np.interp(t_grid, ut, surv, left=1, right=0)
    km_sims.append(km_interp)

km_sims = np.array(km_sims)
km_mean = np.mean(km_sims, axis=0)
km_lower = np.percentile(km_sims, 2.5, axis=0)
km_upper = np.percentile(km_sims, 97.5, axis=0)

axes[1, 0].plot(t_grid, km_mean, 'b-', lw=2, label="Mean KM (500 sims)")
axes[1, 0].fill_between(t_grid, km_lower, km_upper, alpha=0.3, color='b', label="95% band")
axes[1, 0].plot(t_grid, true_surv, 'r--', lw=2, label="True S(t)")
axes[1, 0].set_xlabel("Time")
axes[1, 0].set_ylabel("Survival Probability")
axes[1, 0].set_title("KM Variability (500 Simulations)")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

hazard_est = -np.diff(np.log(np.maximum(survival, 1e-10))) / np.diff(unique_times)
axes[1, 1].step(unique_times[:-1], hazard_est, where='post', lw=2, label="KM Hazard Estimate")
true_hazard = shape / scale * (t_grid / scale)**(shape - 1)
axes[1, 1].plot(t_grid, true_hazard, 'r--', lw=2, label=f"Weibull hazard (α={shape}, β={scale})")
axes[1, 1].set_xlabel("Time")
axes[1, 1].set_ylabel("Hazard Rate")
axes[1, 1].set_title("Hazard Function Estimate")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase03/29-survival-analysis.png")
plt.close()

print("=" * 60)
print("SURVIVAL ANALYSIS: KAPLAN-MEIER ESTIMATOR")
print("=" * 60)
print(f"\nData: n={n}, Weibull(shape={shape}, scale={scale})")
print(f"Events observed: {int(delta.sum())}/{n}")
print(f"Censoring rate: {1 - delta.mean():.1%}")
mean_time = np.trapezoid(survival, unique_times) if len(unique_times) > 1 else np.nan
true_mean = scale * np.exp(np.log(1 + 1/shape))
print(f"KM estimated mean survival: {mean_time:.3f} (true: {true_mean:.3f})")

print(f"\nSurvival estimates:")
for t_q in [0.5, 1.0, 2.0, 3.0]:
    idx_t = np.argmin(np.abs(unique_times - t_q))
    if idx_t < len(survival):
        print(f"  S({t_q:.1f}) = {survival[idx_t]:.4f} (true: {np.exp(-(t_q/scale)**shape):.4f})")

print(f"\nMedian survival time:")
median_idx = np.argmin(np.abs(survival - 0.5))
print(f"  KM estimate: {unique_times[median_idx]:.3f} (true: {scale * np.log(2)**(1/shape):.3f})")
