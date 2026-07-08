#!/usr/bin/env python3
"""03.27 Time Series: ARIMA simulation, ACF/PACF, and forecasting."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 300

# AR(2) process: X_t = 0.6*X_{t-1} + 0.3*X_{t-2} + ε_t
phi = [0.6, 0.3]
ar = np.zeros(n + 100)
for t in range(2, n + 100):
    ar[t] = phi[0] * ar[t-1] + phi[1] * ar[t-2] + np.random.normal(0, 1)
ar = ar[100:]  # burn-in

# ACF and PACF
def acf(x, max_lag=40):
    xc = x - x.mean()
    denom = np.sum(xc**2)
    return np.array([np.sum(xc[:len(xc)-lag] * xc[lag:]) / denom for lag in range(max_lag+1)])

def pacf_via_durbin(x, max_lag=40):
    pacf_vals = np.zeros(max_lag+1)
    pacf_vals[0] = 1.0
    r = acf(x, max_lag)[1:]
    phi = np.zeros((max_lag, max_lag))
    for k in range(max_lag):
        if k == 0:
            phi[k, k] = r[0]
        else:
            num = r[k] - phi[k-1, :k] @ r[k-1::-1]
            denom = 1 - phi[k-1, :k] @ r[:k]
            phi[k, k] = num / denom
            phi[k, :k] = phi[k-1, :k] - phi[k, k] * phi[k-1, k-1::-1]
        pacf_vals[k+1] = phi[k, k]
    return pacf_vals

acf_vals = acf(ar, 40)
pacf_vals = pacf_via_durbin(ar, 40)

fig, axes = plt.subplots(3, 1, figsize=(10, 8))
axes[0].plot(ar)
axes[0].set_title("AR(2) Process: X_t = 0.6X_{{t-1}} + 0.3X_{{t-2}} + ε_t")
axes[0].set_xlabel("Time")
axes[0].set_ylabel("Value")

axes[1].stem(range(41), acf_vals, basefmt=" ")
axes[1].axhline(1.96/np.sqrt(n), color='r', linestyle='--', alpha=0.5)
axes[1].axhline(-1.96/np.sqrt(n), color='r', linestyle='--', alpha=0.5)
axes[1].set_title("ACF")
axes[1].set_xlabel("Lag")

axes[2].stem(range(41), pacf_vals, basefmt=" ")
axes[2].axhline(1.96/np.sqrt(n), color='r', linestyle='--', alpha=0.5)
axes[2].axhline(-1.96/np.sqrt(n), color='r', linestyle='--', alpha=0.5)
axes[2].set_title("PACF")
axes[2].set_xlabel("Lag")
plt.tight_layout()
plt.savefig("../../assets/phase03/27-time-series.png")
plt.close()

print("AR(2) series generated. ACF decays gradually, PACF cuts off at lag 2.")
print(f"PACF at lag 1: {pacf_vals[1]:.3f}, lag 2: {pacf_vals[2]:.3f}")
