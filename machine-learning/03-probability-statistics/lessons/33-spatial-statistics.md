# Lesson 33: Spatial Statistics

## Learning Objectives

After completing this lesson, you will be able to:
- Define spatial processes and types of stationarity
- Compute and model variograms for spatial dependence
- Perform kriging interpolation with uncertainty quantification
- Understand spatial autoregressive models (SAR, CAR)
- Apply spatial statistics to geospatial data

## Spatial Processes

### Definition

A **random field** $\{Z(s) : s \in D \subseteq \mathbb{R}^d\}$ assigns a random variable $Z(s)$ to each spatial location $s$.

**Types:**
- **Geostatistical:** Continuous domain $D$ (temperature, mineral deposits)
- **Areal/Lattice:** Discrete regions (counties, census tracts)
- **Point patterns:** Locations themselves are random (earthquake epicenters)

## Stationarity

### Strict Stationarity

The joint distribution of $\{Z(s_1), \dots, Z(s_k)\}$ is the same as $\{Z(s_1+h), \dots, Z(s_k+h)\}$ for any $h$.

### Second-Order Stationarity

1. $E[Z(s)] = \mu$ (constant mean)
2. $\text{Cov}(Z(s), Z(s+h)) = C(h)$ (covariance depends only on lag $h$)

### Intrinsic Stationarity

$$\text{Var}(Z(s+h) - Z(s)) = 2\gamma(h)$$

where $\gamma(h)$ is the **semivariogram**.

## Variogram

### Definition

$$\gamma(h) = \frac{1}{2} \text{Var}(Z(s+h) - Z(s))$$

For second-order stationary processes:
$$\gamma(h) = C(0) - C(h)$$

### Empirical Variogram

$$\hat{\gamma}(h) = \frac{1}{2|N(h)|} \sum_{(i,j) \in N(h)} (Z(s_i) - Z(s_j))^2$$

where $N(h)$ is the set of point pairs separated by distance $h$ (within tolerance).

### Variogram Models

| Model | $\gamma(h)$ | Parameters |
|-------|------------|------------|
| Nugget | $c_0$ | $c_0 \geq 0$ (micro-scale variation + measurement error) |
| Spherical | $c_0 + c_1\left(\frac{3h}{2a} - \frac{h^3}{2a^3}\right)$ for $h<a$, $c_0+c_1$ otherwise | $a > 0$ (range) |
| Exponential | $c_0 + c_1(1 - e^{-h/a})$ | $a > 0$ (practical range $\approx 3a$) |
| Gaussian | $c_0 + c_1(1 - e^{-h^2/a^2})$ | $a > 0$ (very smooth) |
| Matérn | $c_0 + c_1\left(1 - \frac{1}{2^{\nu-1}\Gamma(\nu)}\left(\frac{h}{a}\right)^\nu K_\nu\left(\frac{h}{a}\right)\right)$ | $a > 0$, $\nu > 0$ (smoothness) |

**Nugget + Sill:** $\lim_{h \to \infty} \gamma(h) = c_0 + c_1$ (total sill = variance)
**Range:** Distance at which $\gamma(h)$ reaches ~95% of the sill

## Kriging

### Best Linear Unbiased Predictor (BLUP)

$\hat{Z}(s_0) = \lambda^\top Z$ minimizes $E[(\hat{Z}(s_0) - Z(s_0))^2]$ subject to $E[\hat{Z}(s_0)] = E[Z(s_0)]$.

### Simple Kriging (known mean $\mu$)

$$\hat{Z}(s_0) = \mu + c^\top C^{-1} (Z - \mu\mathbf{1})$$
$$\sigma^2_k(s_0) = C(0) - c^\top C^{-1} c$$

where $C_{ij} = C(s_i - s_j)$ and $c_i = C(s_0 - s_i)$.

### Ordinary Kriging (unknown constant mean)

$$\hat{Z}(s_0) = \lambda^\top Z$$
$$\sigma^2_k(s_0) = C(0) - c^\top C^{-1} c + \frac{(1 - \mathbf{1}^\top C^{-1} c)^2}{\mathbf{1}^\top C^{-1} \mathbf{1}}$$

### Universal Kriging (trend surface)

$E[Z(s)] = X(s)^\top \beta$ (linear trend), estimated simultaneously with kriging weights.

## Spatial Autoregressive Models

### Simultaneous Autoregression (SAR)

$$Z = \rho W Z + \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \sigma^2 I)$$
$$Z = (I - \rho W)^{-1} \varepsilon$$

- $W$: spatial weights matrix (row-standardized adjacency)
- $\rho$: spatial autocorrelation parameter ($|\rho| < 1$ for stationarity)

### Conditional Autoregression (CAR)

$$Z_i \mid Z_{-i} \sim \mathcal{N}\left(\rho \sum_{j} w_{ij} z_j, \tau_i^2\right)$$

The joint distribution is:
$$Z \sim \mathcal{N}(0, (I - \rho W)^{-1} M)$$

where $M = \text{diag}(\tau_i^2)$.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist, pdist, squareform

# Generate synthetic spatial data
np.random.seed(42)
n_points = 100
coords = np.random.uniform(0, 10, (n_points, 2))

# True parameters
sigma_sq = 2.0  # partial sill
phi = 2.0  # range parameter
nugget = 0.1

# Exponential covariance
def exp_cov(h, sigma_sq, phi, nugget):
    return sigma_sq * np.exp(-h / phi) + nugget * (h == 0)

D = squareform(pdist(coords))
Sigma = exp_cov(D, sigma_sq, phi, nugget)
Z = np.random.multivariate_normal(np.zeros(n_points), Sigma)

# Empirical variogram
def empirical_variogram(coords, values, bins=20, max_dist=None):
    D = squareform(pdist(coords))
    V = squareform((values[:, None] - values[None, :])**2 / 2)
    if max_dist is None:
        max_dist = D.max() / 2
    bin_edges = np.linspace(0, max_dist, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    gamma_hat = np.zeros(bins)
    for i in range(bins):
        mask = (D >= bin_edges[i]) & (D < bin_edges[i+1])
        gamma_hat[i] = V[mask].mean() if mask.sum() > 0 else 0
    return bin_centers, gamma_hat

h_vals, gamma_emp = empirical_variogram(coords, Z)

# Fit exponential variogram model
from scipy.optimize import curve_fit
def exp_variogram(h, sigma_sq, phi, nugget):
    return nugget + sigma_sq * (1 - np.exp(-h / phi))

params, _ = curve_fit(exp_variogram, h_vals, gamma_emp,
                       p0=[2.0, 2.0, 0.1],
                       bounds=((0, 0, 0), (np.inf, np.inf, np.inf)))
sigma_hat, phi_hat, nugget_hat = params
print(f"Fitted: σ²={sigma_hat:.2f}, φ={phi_hat:.2f}, nugget={nugget_hat:.3f}")

# Ordinary kriging at a grid
grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 30), np.linspace(0, 10, 30))
grid_coords = np.column_stack([grid_x.ravel(), grid_y.ravel()])

def ordinary_kriging(target, obs_coords, obs_values, sigma_sq, phi, nugget):
    n = len(obs_values)
    # Covariance matrix
    D_obs = cdist(obs_coords, obs_coords)
    C = sigma_sq * np.exp(-D_obs / phi) + nugget * np.eye(n)
    # Cross-covariance
    D_cross = cdist(obs_coords, target.reshape(1, -1))
    c = sigma_sq * np.exp(-D_cross / phi).flatten()
    # Add Lagrange multiplier for unbiasedness
    C_ext = np.zeros((n+1, n+1))
    C_ext[:n, :n] = C
    C_ext[:n, n] = 1
    C_ext[n, :n] = 1
    c_ext = np.concatenate([c, [1]])
    # Solve
    lam = np.linalg.solve(C_ext, c_ext)
    z_hat = lam[:n] @ obs_values
    kriging_var = c_ext @ lam
    return z_hat, kriging_var, lam[:n]

predictions = np.zeros(len(grid_coords))
variances = np.zeros(len(grid_coords))
for i, target in enumerate(grid_coords):
    z_hat, var, _ = ordinary_kriging(target, coords, Z,
                                      sigma_hat, phi_hat, nugget_hat)
    predictions[i] = z_hat
    variances[i] = var

# Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].scatter(coords[:, 0], coords[:, 1], c=Z, s=40, cmap='viridis', edgecolor='k')
axes[0].set_title('Observed Data')

axes[1].scatter(h_vals, gamma_emp, label='Empirical')
h_smooth = np.linspace(0, h_vals.max(), 100)
axes[1].plot(h_smooth, exp_variogram(h_smooth, *params), 'r-', label='Fitted')
axes[1].set_xlabel('Distance h')
axes[1].set_ylabel('γ(h)')
axes[1].legend()
axes[1].set_title('Variogram')

im = axes[2].contourf(grid_x, grid_y, predictions.reshape(grid_x.shape),
                       levels=20, cmap='viridis')
plt.colorbar(im, ax=axes[2])
axes[2].scatter(coords[:, 0], coords[:, 1], c=Z, s=20, cmap='viridis', edgecolor='k')
axes[2].set_title('Kriging Predictions')

plt.tight_layout()
plt.show()
```

## Visualization

Create a three-panel figure: (1) Map of observed data at locations; (2) Empirical variogram with fitted model; (3) Kriging prediction surface with observation locations overlaid. Add a fourth panel showing kriging variance (prediction uncertainty) — higher in areas far from observations.

## Practical Considerations

- **Anisotropy:** Spatial dependence may differ by direction (e.g., wind-dominated patterns). Use geometric or zonal anisotropy models.
- **Non-stationarity:** Real spatial data often have trends. Use universal kriging or spatial fixed effects.
- **Change of support:** Kriging predicts at points; for areal predictions, use block kriging (average over region).
- **Big spatial data:** For $n > 10^4$, standard kriging is $O(n^3)$. Use fixed-rank kriging, NNGP, or stochastic partial differential equation (SPDE) approaches.
- **Spatio-temporal models:** Extend to space-time kriging with separable or non-separable covariance functions.

## References

- Matheron, G. (1963). "Principles of geostatistics"
- Krige, D. G. (1951). "A statistical approach to some basic mine valuation problems"
- Cressie, N. (1993). *Statistics for Spatial Data*
- Diggle, P. J. & Ribeiro, P. J. (2007). *Model-based Geostatistics*
