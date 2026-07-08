# Lesson 27: Time Series Analysis

## Learning Objectives

After completing this lesson, you will be able to:
- Define stationarity and test for it
- Identify ARIMA model orders using ACF/PACF
- Estimate ARIMA parameters and diagnose residuals
- Forecast future values with prediction intervals
- Analyze time series in the frequency domain

## Stationarity

### Strict Stationarity

A time series $\{X_t\}$ is **strictly stationary** if for any $h$ and any $t_1, \dots, t_k$:
$$(X_{t_1}, \dots, X_{t_k}) \overset{d}{=} (X_{t_1+h}, \dots, X_{t_{k+h}})$$

### Weak (Covariance) Stationarity

1. $E[X_t] = \mu$ (constant mean)
2. $\text{Var}(X_t) = \sigma^2$ (constant variance)
3. $\text{Cov}(X_t, X_{t+h}) = \gamma(h)$ (depends only on lag $h$)

### Non-Stationarity

Common sources:
- **Trend:** Deterministic ($\beta t$) or stochastic (random walk)
- **Seasonality:** Periodic patterns
- **Heteroscedasticity:** Changing variance (GARCH models)

## Autocorrelation Function (ACF)

### Definition

$$\rho(h) = \frac{\gamma(h)}{\gamma(0)} = \text{Corr}(X_t, X_{t+h})$$

### Partial Autocorrelation Function (PACF)

PACF at lag $h$ is $\phi_{hh} = \text{Corr}(X_t, X_{t+h} \mid X_{t+1}, \dots, X_{t+h-1})$.

### Properties

| Model | ACF | PACF |
|-------|-----|------|
| AR($p$) | Tails off (exponential/oscillating) | Cuts off after lag $p$ |
| MA($q$) | Cuts off after lag $q$ | Tails off |
| ARMA($p,q$) | Tails off | Tails off |

## ARIMA Models

### Autoregressive Model AR($p$)

$$X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \dots + \phi_p X_{t-p} + \varepsilon_t$$

- **Stationarity condition:** All roots of $1 - \phi_1 z - \cdots - \phi_p z^p = 0$ lie outside the unit circle.
- **Yule-Walker equations:** $\gamma(h) = \sum_{j=1}^p \phi_j \gamma(h-j)$ for $h > 0$

### Moving Average Model MA($q$)

$$X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \dots + \theta_q \varepsilon_{t-q}$$

- Always stationary
- **Invertibility condition:** All roots of $1 + \theta_1 z + \cdots + \theta_q z^q = 0$ lie outside the unit circle.

### ARMA($p,q$)

$$X_t = \sum_{i=1}^p \phi_i X_{t-i} + \varepsilon_t + \sum_{j=1}^q \theta_j \varepsilon_{t-j}$$

### ARIMA($p,d,q$)

Apply $d$ differences before fitting ARMA: $\nabla^d X_t = (1-B)^d X_t$.

### Seasonal ARIMA: SARIMA($p,d,q$)$\times(P,D,Q)_s$

Includes seasonal lags at period $s$:
$$(1-B)^d (1-B^s)^D X_t = \frac{\Theta(B)\Theta_S(B)}{\Phi(B)\Phi_S(B)} \varepsilon_t$$

## Box-Jenkins Methodology

1. **Identification:** Determine $p, d, q$ using ACF/PACF, stationarity tests (ADF, KPSS)
2. **Estimation:** MLE or conditional least squares
3. **Diagnostic checking:** Residual ACF should be white noise (Ljung-Box test)
4. **Forecasting:** Minimum MSE forecasts with prediction intervals

## Forecasting

### Linear Predictor

Minimum MSE forecast at horizon $h$:
$$\hat{X}_{t+h \mid t} = E[X_{t+h} \mid X_t, X_{t-1}, \dots]$$

For AR($p$):
$$\hat{X}_{t+h \mid t} = \sum_{i=1}^p \phi_i \hat{X}_{t+h-i \mid t}$$

### Prediction Intervals

Under Gaussian errors:
$$\hat{X}_{t+h \mid t} \pm z_{\alpha/2} \cdot \sigma \sqrt{\sum_{j=0}^{h-1} \psi_j^2}$$

where $\psi_j$ are the infinite MA coefficients ($\Psi$-weights).

## Spectral Analysis

### Spectral Density

$$f(\omega) = \frac{1}{2\pi} \sum_{h=-\infty}^{\infty} \gamma(h) e^{-i\omega h}, \quad \omega \in [-\pi, \pi]$$

### Periodogram

$$I(\omega_k) = \frac{1}{n} \left| \sum_{t=1}^n X_t e^{-i\omega_k t} \right|^2$$

where $\omega_k = 2\pi k/n$ are the Fourier frequencies.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Generate AR(2) process
np.random.seed(42)
n = 500
phi = [0.7, -0.2]  # AR coefficients
x = np.zeros(n)
for t in range(2, n):
    x[t] = phi[0] * x[t-1] + phi[1] * x[t-2] + np.random.normal(0, 1)

# Stationarity test
adf_stat, adf_pval, _, _, crit_vals, _ = adfuller(x)
print(f"ADF test: stat={adf_stat:.3f}, p-value={adf_pval:.4f}")
print(f"  Critical values: {crit_vals}")

# ACF/PACF plots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(x, lags=30, ax=axes[0])
plot_pacf(x, lags=30, ax=axes[1])
plt.tight_layout()
plt.show()

# Fit ARIMA model
model = ARIMA(x, order=(2, 0, 0))
result = model.fit()
print(result.summary())

# Diagnostics: residual ACF
residuals = result.resid
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(residuals)
axes[0].set_title('Residuals')
plot_acf(residuals, lags=30, ax=axes[1])
plt.tight_layout()
plt.show()

# Ljung-Box test
from statsmodels.stats.diagnostic import acorr_ljungbox
lb = acorr_ljungbox(residuals, lags=[10, 20, 30])
print(f"\nLjung-Box p-values: {lb['lb_pvalue'].values}")

# Forecast
forecast_result = result.get_forecast(steps=20)
forecast = forecast_result.predicted_mean
ci = forecast_result.conf_int()

plt.figure(figsize=(10, 5))
plt.plot(range(n), x, 'b-', label='Observed')
plt.plot(range(n, n+20), forecast, 'r-', label='Forecast')
plt.fill_between(range(n, n+20), ci[:, 0], ci[:, 1], color='r', alpha=0.2)
plt.axvline(x=n, color='k', linestyle='--')
plt.legend()
plt.title('ARIMA Forecast')
plt.show()
```

## Visualization

Create a four-panel figure: (1) Time series plot with trend/seasonality; (2) ACF showing slow decay (non-stationary) vs fast decay (stationary); (3) PACF showing cutoff for AR model; (4) Spectral density plot identifying dominant frequencies. A second figure shows forecast with prediction intervals expanding with horizon.

## Practical Considerations

- **Unit roots:** Use differencing ($d=1$) for random walk behavior. Over-differencing introduces non-invertible MA roots.
- **Model selection:** Use AIC/BIC for ARIMA order selection. Be wary of overfitting with large $p+q$.
- **Outliers:** Additive outliers and level shifts can distort ACF/PACF. Consider outlier detection (tsoutliers).
- **Volatility modeling:** For financial data with changing variance, use GARCH models for the residuals.
- **Multiple seasonality:** For hourly/daily data with daily and weekly patterns, use TBATS or Prophet.

## References

- Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). *Time Series Analysis: Forecasting and Control*
- Brockwell, P. J. & Davis, R. A. (2016). *Introduction to Time Series and Forecasting*
- Hamilton, J. D. (1994). *Time Series Analysis*
- Shumway, R. H. & Stoffer, D. S. (2017). *Time Series Analysis and Its Applications*
