# Lesson 28: State Space Models & Kalman Filter

## Learning Objectives

After completing this lesson, you will be able to:
- Formulate state space models for dynamic systems
- Implement the Kalman filter for online state estimation
- Apply the Rauch-Tung-Striebel smoother for offline estimation
- Estimate parameters via the EM algorithm
- Use particle filters for nonlinear/non-Gaussian systems

## State Space Model

### Linear Gaussian State Space Model

**State equation (transition):**
$$x_t = F_t x_{t-1} + B_t u_t + w_t, \quad w_t \sim \mathcal{N}(0, Q_t)$$

**Observation equation (emission):**
$$y_t = H_t x_t + v_t, \quad v_t \sim \mathcal{N}(0, R_t)$$

where:
- $x_t \in \mathbb{R}^k$: latent state vector
- $y_t \in \mathbb{R}^p$: observation vector
- $F_t \in \mathbb{R}^{k \times k}$: state transition matrix
- $H_t \in \mathbb{R}^{p \times k}$: observation matrix
- $u_t$: control input
- $w_t$, $v_t$: independent Gaussian noise processes
- Initial state: $x_0 \sim \mathcal{N}(\mu_0, P_0)$

### Independence Assumptions

- $w_t \perp w_s$ for $t \neq s$ (white noise)
- $v_t \perp v_s$ for $t \neq s$
- $w_t \perp v_s$ for all $t, s$
- $x_0 \perp w_t, v_t$ for all $t$

## Kalman Filter

The Kalman filter computes $p(x_t \mid y_{1:t})$ — the filtering distribution — recursively.

### Predict Step

$$\hat{x}_{t \mid t-1} = F_t \hat{x}_{t-1 \mid t-1} + B_t u_t$$
$$P_{t \mid t-1} = F_t P_{t-1 \mid t-1} F_t^\top + Q_t$$

### Update Step

**Innovation (residual):** $\nu_t = y_t - H_t \hat{x}_{t \mid t-1}$
**Innovation covariance:** $S_t = H_t P_{t \mid t-1} H_t^\top + R_t$
**Kalman gain:** $K_t = P_{t \mid t-1} H_t^\top S_t^{-1}$

$$\hat{x}_{t \mid t} = \hat{x}_{t \mid t-1} + K_t \nu_t$$
$$P_{t \mid t} = (I - K_t H_t) P_{t \mid t-1}$$

### Interpretation

- The Kalman gain $K_t$ balances prediction vs observation
- When $R_t$ is large (noisy observations), $K_t$ is small (trust prediction)
- When $Q_t$ is large (noisy dynamics), $K_t$ is large (trust observation)

## Kalman Smoother

The Rauch-Tung-Striebel (RTS) smoother computes $p(x_t \mid y_{1:T})$ for $t < T$.

**Backward recursion:**

$$G_t = P_{t \mid t} F_{t+1}^\top P_{t+1 \mid t}^{-1}$$
$$\hat{x}_{t \mid T} = \hat{x}_{t \mid t} + G_t (\hat{x}_{t+1 \mid T} - \hat{x}_{t+1 \mid t})$$
$$P_{t \mid T} = P_{t \mid t} + G_t (P_{t+1 \mid T} - P_{t+1 \mid t}) G_t^\top$$

## Parameter Estimation via EM

### E-Step

Run the RTS smoother to compute expected sufficient statistics:
$$\hat{x}_{t \mid T}, \quad P_{t \mid T}, \quad P_{t, t-1 \mid T}$$

### M-Step

Update parameters by maximizing expected log-likelihood:
$$F = \left(\sum_{t=2}^T P_{t, t-1 \mid T} + \hat{x}_{t \mid T}\hat{x}_{t-1 \mid T}^\top\right) \left(\sum_{t=2}^T P_{t-1 \mid T} + \hat{x}_{t-1 \mid T}\hat{x}_{t-1 \mid T}^\top\right)^{-1}$$
$$Q = \frac{1}{T-1} \sum_{t=2}^T \left[P_{t \mid T} + \hat{x}_{t \mid T}\hat{x}_{t \mid T}^\top - F(P_{t, t-1 \mid T} + \hat{x}_{t-1 \mid T}\hat{x}_{t \mid T}^\top)\right]$$

## Nonlinear Extensions

### Extended Kalman Filter (EKF)

Linearize nonlinear dynamics $f$ and observation $g$ via Taylor expansion:
$$F_t = \frac{\partial f}{\partial x}\Big|_{x=\hat{x}_{t-1}}, \quad H_t = \frac{\partial g}{\partial x}\Big|_{x=\hat{x}_{t \mid t-1}}$$

### Unscented Kalman Filter (UKF)

Propagate sigma points through the nonlinear function, avoiding linearization:
1. Generate $2k+1$ sigma points from $p(x_{t-1} \mid y_{1:t-1})$
2. Propagate through $f$, compute predicted mean/covariance
3. Propagate through $g$, compute innovation and cross-covariance
4. Update with Kalman-like gain

### Particle Filter (Sequential Monte Carlo)

For non-Gaussian/nonlinear systems:

1. **Sample:** $x_t^{(i)} \sim q(x_t \mid x_{t-1}^{(i)}, y_t)$
2. **Weight:** $w_t^{(i)} = w_{t-1}^{(i)} \frac{p(y_t \mid x_t^{(i)}) p(x_t^{(i)} \mid x_{t-1}^{(i)})}{q(x_t^{(i)} \mid x_{t-1}^{(i)}, y_t)}$
3. **Resample:** Sample $N$ particles with replacement proportional to weights
4. **Estimate:** $\hat{x}_t = \sum w_t^{(i)} x_t^{(i)}$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter:
    def __init__(self, F, H, Q, R, x0, P0):
        self.F = F  # state transition
        self.H = H  # observation model
        self.Q = Q  # process noise covariance
        self.R = R  # observation noise covariance
        self.x = x0  # initial state
        self.P = P0  # initial covariance

    def predict(self, u=None):
        if u is None:
            u = np.zeros((self.F.shape[0], 1))
        self.x = self.F @ self.x  # + B @ u
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x

    def update(self, z):
        y = z - self.H @ self.x  # innovation
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)  # Kalman gain
        self.x = self.x + K @ y
        self.P = (np.eye(self.P.shape[0]) - K @ self.H) @ self.P
        return self.x, self.P

# Example: 1D tracking
dt = 1.0
F = np.array([[1, dt], [0, 1]])  # position, velocity
H = np.array([[1, 0]])  # observe position
Q = np.array([[0.1, 0], [0, 0.1]])  # process noise
R = np.array([[1.0]])  # measurement noise
x0 = np.array([[0], [1]])  # initial pos, vel
P0 = np.eye(2) * 10

kf = KalmanFilter(F, H, Q, R, x0, P0)

# Simulate true trajectory and measurements
n_steps = 100
true_states = np.zeros((n_steps, 2))
measurements = np.zeros((n_steps, 1))
state = np.array([0.0, 1.0])
for t in range(n_steps):
    state = F @ state + np.random.multivariate_normal([0, 0], Q)
    true_states[t] = state
    measurements[t] = H @ state + np.random.normal(0, np.sqrt(R[0, 0]))

# Run Kalman filter
estimates = np.zeros((n_steps, 2))
for t in range(n_steps):
    kf.predict()
    est, _ = kf.update(measurements[t:t+1].T)
    estimates[t] = est.flatten()

# Plot
plt.figure(figsize=(12, 5))
plt.subplot(121)
plt.plot(true_states[:, 0], 'b-', label='True position', lw=2)
plt.plot(measurements, 'g.', alpha=0.5, label='Measurements')
plt.plot(estimates[:, 0], 'r-', label='Filtered estimate', lw=2)
plt.legend()
plt.title('Position Tracking')

plt.subplot(122)
plt.plot(true_states[:, 1], 'b-', label='True velocity', lw=2)
plt.plot(estimates[:, 1], 'r-', label='Filtered velocity', lw=2)
plt.legend()
plt.title('Velocity Estimation')

plt.tight_layout()
plt.show()
```

## Visualization

Create a tracking plot showing: (1) True trajectory (smooth line), (2) Noisy observations (dots), (3) Kalman filter estimates (line tracking close to truth), (4) 95% confidence ellipse at each step. The filter should smooth the observations; estimates should be closer to the truth than raw observations. A second plot shows the Kalman gain converging to a steady-state value.

## Practical Considerations

- **Numerical stability:** Use Joseph form for covariance update: $P = (I-KH)P(I-KH)^\top + KRK^\top$ (guarantees symmetry).
- **Divergence:** If model is misspecified, the filter may diverge. Use adaptive Q/R estimation or outlier-robust updates.
- **High-dimensional states:** For $k > 100$, use ensemble Kalman filter or reduced-rank filters.
- **Unknown parameters:** Use EM algorithm, dual estimation (joint state and parameter), or Bayesian approaches (particle MCMC).

## References

- Kalman, R. E. (1960). "A new approach to linear filtering and prediction problems"
- Rauch, H. E., Tung, F., & Striebel, C. T. (1965). "Maximum likelihood estimates of linear dynamic systems"
- Julier, S. J. & Uhlmann, J. K. (1997). "A new extension of the Kalman filter to nonlinear systems"
- Doucet, A., Godsill, S., & Andrieu, C. (2000). "On sequential Monte Carlo sampling methods for Bayesian filtering"
- Durbin, J. & Koopman, S. J. (2012). *Time Series Analysis by State Space Methods*
