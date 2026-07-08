# Lesson 29: Survival Analysis

## Learning Objectives

After completing this lesson, you will be able to:
- Define survival, hazard, and cumulative hazard functions
- Handle censored data appropriately
- Estimate survival curves using Kaplan-Meier
- Compare survival across groups with log-rank test
- Fit Cox proportional hazards models and interpret hazard ratios

## Key Quantities

### Survival Function

$$S(t) = P(T > t)$$

The probability of surviving beyond time $t$. $S(0) = 1$, $S(\infty) = 0$.

### Hazard Function

$$\lambda(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t + \Delta t \mid T \geq t)}{\Delta t}$$

The instantaneous risk of failure at time $t$, conditional on survival to $t$.

### Cumulative Hazard

$$\Lambda(t) = \int_0^t \lambda(u) du$$

### Relationships

$$S(t) = \exp(-\Lambda(t)) = \exp\left(-\int_0^t \lambda(u) du\right)$$
$$\lambda(t) = -\frac{d}{dt} \log S(t) = \frac{f(t)}{S(t)}$$

## Censoring

### Types

- **Right censoring:** True event time > observed time (most common in clinical trials)
- **Left censoring:** Event occurred before study start
- **Interval censoring:** Event occurred in a known time interval

### Independent Censoring Assumption

Censoring time $C$ is independent of event time $T$: $C \perp T$. This is crucial for valid inference. Violations occur when patients drop out due to disease progression.

## Kaplan-Meier Estimator

### Product-Limit Estimator

$$\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

where $d_i$ is the number of events at time $t_i$, and $n_i$ is the number at risk just before $t_i$.

### Greenwood's Formula

$$\widehat{\text{Var}}(\hat{S}(t)) = \hat{S}(t)^2 \sum_{t_i \leq t} \frac{d_i}{n_i(n_i - d_i)}$$

### Confidence Intervals

$$\hat{S}(t) \pm z_{\alpha/2} \cdot \widehat{\text{SE}}(\hat{S}(t))$$

Better: Use log-log transformation for pointwise confidence intervals that stay within $[0,1]$:
$$\hat{S}(t)^{\exp(\pm z_{\alpha/2} \cdot \widehat{\text{SE}}(\log(-\log \hat{S}(t))))}$$

### Median Survival

$$\hat{t}_{0.5} = \min\{t: \hat{S}(t) \leq 0.5\}$$

## Log-Rank Test

### Hypotheses

$H_0: S_1(t) = S_2(t)$ for all $t$ (groups have same survival)

### Test Statistic

$$\chi^2 = \frac{(O_1 - E_1)^2}{\text{Var}(O_1 - E_1)} \sim \chi^2_1$$

where $O_1$ is observed events in group 1, and $E_1 = \sum \frac{n_{1i}}{n_i} d_i$ is expected events under $H_0$.

## Cox Proportional Hazards Model

### Model

$$\lambda(t \mid X) = \lambda_0(t) \exp(X^\top \beta)$$

- $\lambda_0(t)$: baseline hazard (unspecified, non-parametric)
- $\exp(\beta_j)$: **hazard ratio** for a unit increase in $X_j$
- The "proportional hazards" assumption: hazard ratios are constant over time

### Partial Likelihood

$$L(\beta) = \prod_{i: \delta_i = 1} \frac{\exp(X_i^\top \beta)}{\sum_{j \in R(t_i)} \exp(X_j^\top \beta)}$$

where $R(t_i)$ is the risk set at time $t_i$.

### Breslow Estimator of Baseline Hazard

$$\hat{\Lambda}_0(t) = \sum_{t_i \leq t} \frac{d_i}{\sum_{j \in R(t_i)} \exp(X_j^\top \hat{\beta})}$$

## Parametric Survival Models

| Distribution | Hazard $\lambda(t)$ | Survival $S(t)$ | AFT Parameterization |
|-------------|---------------------|-----------------|----------------------|
| Exponential | $\lambda$ | $e^{-\lambda t}$ | $\log T = \mu + \sigma W$ |
| Weibull | $\lambda p t^{p-1}$ | $e^{-\lambda t^p}$ | $\log T = \mu + \sigma W$ |
| Log-normal | — | $1 - \Phi(\frac{\log t - \mu}{\sigma})$ | $\log T = \mu + \sigma Z$ |
| Log-logistic | $\frac{\lambda p t^{p-1}}{1 + \lambda t^p}$ | $\frac{1}{1 + \lambda t^p}$ | $\log T = \mu + \sigma W$ |

AFT (Accelerated Failure Time): Covariates accelerate/decelerate survival time: $\log T = X^\top \beta + \sigma W$.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

# Generate survival data
np.random.seed(42)
n = 200

# Treatment group
T1 = np.random.exponential(scale=5.0, size=n//2)
C1 = np.random.uniform(1, 10, n//2)
Y1 = np.minimum(T1, C1)
event1 = (T1 <= C1).astype(int)

# Control group
T2 = np.random.exponential(scale=3.0, size=n//2)
C2 = np.random.uniform(1, 10, n//2)
Y2 = np.minimum(T2, C2)
event2 = (T2 <= C2).astype(int)

# Combine
times = np.concatenate([Y1, Y2])
events = np.concatenate([event1, event2])
groups = np.concatenate([['treatment']*(n//2), ['control']*(n//2)])

# Kaplan-Meier
kmf = KaplanMeierFitter()
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

kmf.fit(times[groups == 'treatment'], events[groups == 'treatment'],
        label='Treatment')
kmf.plot_survival_function(ax=axes[0])

kmf.fit(times[groups == 'control'], events[groups == 'control'],
        label='Control')
kmf.plot_survival_function(ax=axes[0])
axes[0].set_title('Kaplan-Meier Survival Curves')

# Log-rank test
results = logrank_test(times[groups == 'treatment'],
                        times[groups == 'control'],
                        event_observed_A=events[groups == 'treatment'],
                        event_observed_B=events[groups == 'control'])
print(f"Log-rank test: p-value = {results.p_value:.6f}")

# Cox PH model
df = pd.DataFrame({
    'time': times,
    'event': events,
    'treatment': (groups == 'treatment').astype(int)
})
cph = CoxPHFitter()
cph.fit(df, duration_col='time', event_col='event')
cph.print_summary()

# Proportional hazards assumption check
cph.check_assumptions(df, p_value_threshold=0.05)

# Plot baseline survival
cph.baseline_survival_.plot(ax=axes[1])
axes[1].set_title('Baseline Survival (Cox PH)')
plt.tight_layout()
plt.show()

# Predicted survival for new patients
new_patients = pd.DataFrame({'treatment': [0, 1]})
cph.predict_survival_function(new_patients).plot()
plt.title('Predicted Survival for New Patients')
plt.show()
```

## Visualization

The key plot is the Kaplan-Meier survival curve with confidence bands. Compare treatment vs control. Below it, show the "number at risk" table. A second figure shows the cumulative hazard (Nelson-Aalen estimator) on a log-log scale to check proportional hazards (parallel lines = PH holds). A forest plot of hazard ratios for multiple covariates is useful for model interpretation.

## Practical Considerations

- **Proportional hazards assumption:** Check with Schoenfeld residuals. If violated, use stratified Cox, time-varying coefficients, or AFT models.
- **Competing risks:** When there are multiple event types (death from different causes), use cause-specific hazards or Fine-Gray subdistribution hazards.
- **Time-varying covariates:** Cox model handles time-varying covariates naturally. Use counting process data format (start, stop, event).
- **Sample size:** Survival studies need sufficient events (not total subjects). Rule of thumb: 10-20 events per predictor in Cox model.
- **Frailty models:** Add random effects to Cox model for clustered survival data (e.g., patients within hospitals).

## References

- Kaplan, E. L. & Meier, P. (1958). "Nonparametric estimation from incomplete observations"
- Cox, D. R. (1972). "Regression models and life-tables"
- Therneau, T. M. & Grambsch, P. M. (2000). *Modeling Survival Data: Extending the Cox Model*
- Klein, J. P. & Moeschberger, M. L. (2003). *Survival Analysis: Techniques for Censored and Truncated Data*
