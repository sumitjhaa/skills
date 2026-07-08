#!/usr/bin/env python3
"""03.39 Measurement Error: SIMEX and attenuation bias."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 500
sigma_x = 1.0
sigma_u = 0.5
beta_true = 2.0

# True X
X = np.random.normal(0, sigma_x, n)
Y = beta_true * X + np.random.normal(0, 0.5, n)

# Classical measurement error
U = np.random.normal(0, sigma_u, n)
W = X + U

# Naive regression (with error)
beta_naive = np.polyfit(W, Y, 1)[0]
beta_true_est = np.polyfit(X, Y, 1)[0]

# Attenuation factor
lambda_atten = sigma_x**2 / (sigma_x**2 + sigma_u**2)

# SIMEX
lambdas = np.array([0, 0.5, 1.0, 1.5, 2.0])
B = 200
beta_simex = np.zeros(len(lambdas))

for i, lam in enumerate(lambdas):
    betas = np.zeros(B)
    for b in range(B):
        U_extra = np.random.normal(0, np.sqrt(lam * sigma_u**2), n)
        W_star = W + U_extra
        betas[b] = np.polyfit(W_star, Y, 1)[0]
    beta_simex[i] = np.mean(betas)

# Extrapolate to λ = -1
extrap = np.polyfit(lambdas, beta_simex, 2)
beta_simex_corrected = np.polyval(extrap, -1)

plt.figure(figsize=(8, 5))
plt.plot(lambdas, beta_simex, 'o-', lw=2, markersize=8, label="SIMEX estimates")
plt.axhline(beta_true, color='r', lw=2, label=f"True β = {beta_true}")
plt.axhline(beta_naive, color='gray', ls='--', label=f"Naive β (with error) = {beta_naive:.3f}")
plt.axvline(-1, color='g', ls=':', lw=2)
plt.scatter([-1], [beta_simex_corrected], color='g', s=100, zorder=5, 
            label=f"SIMEX corrected: {beta_simex_corrected:.3f}")
plt.xlabel("λ (extra variance multiplier)")
plt.ylabel("β estimate")
plt.title(f"SIMEX: Naive={beta_naive:.3f}, Corrected={beta_simex_corrected:.3f}, True={beta_true}")
plt.legend()
plt.grid(True)
plt.savefig("../../assets/phase03/39-measurement-error.png")
plt.close()

print(f"True β = {beta_true}")
print(f"OLS on true X: β̂ = {beta_true_est:.3f}")
print(f"Naive OLS (W = X + U): β̂ = {beta_naive:.3f}")
print(f"SIME-corrected: β̂ = {beta_simex_corrected:.3f}")
print(f"Attenuation factor λ = {lambda_atten:.3f}, Naive/True = {beta_naive/beta_true:.3f}")
