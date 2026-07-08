# Phase 03 — Probability & Statistics

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 03 — Probability & Statistics |
| **Lessons** | 40 |
| **Core topics** | Probability axioms, random variables, distributions, multivariate distributions, expectation/variance, joint/marginal/conditional, covariance/correlation, transformations, sums/CLT, LLN/CLT, concentration inequalities, order statistics, MLE, MAP, exponential family, Bayesian inference, hypothesis testing, confidence intervals, bootstrap, ANOVA, linear regression, GLMs, mixed effects, Bayesian linear regression, GPs, multivariate methods, time series, state-space/Kalman, survival analysis, empirical processes, extreme value theory, copulas, spatial statistics, missing data, causal inference, causal discovery, Bayesian nonparametrics, ABC, measurement error, Bayesian workflow |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (vector spaces, covariance matrices)
- **Python frameworks:** [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (simulation, data handling), [`../../python-frameworks/scikit-learn/`](../../python-frameworks/scikit-learn/) (stats models)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Probability Axioms | Kolmogorov axioms, basic probability rules | [lesson](lessons/01-probability-axioms.md) | [code](code/01-probability-axioms.py) | Foundation for all later phases |
| 02 | Random Variables | Discrete, continuous, PMF, PDF, CDF | [lesson](lessons/02-random-variables.md) | [code](code/02-random-variables.py) | Used in: Phase 04 (entropy) |
| 03 | Distributions | Bernoulli, Binomial, Poisson, Gaussian, Exponential | [lesson](lessons/03-distributions.md) | [code](code/03-distributions.py) | Used in: Phase 05 (Naive Bayes), Phase 06 (output layers) |
| 04 | Multivariate Distributions | Joint PDF, marginal, conditional | [lesson](lessons/04-multivariate-distributions.md) | [code](code/04-multivariate-distributions.py) | Used in: Phase 05 (GMM), Phase 07 (normalizing flows) |
| 05 | Expectation Variance Moments | Mean, variance, skewness, kurtosis, MGF | [lesson](lessons/05-expectation-variance-moments.md) | [code](code/05-expectation-variance-moments.py) | Used in: Phase 06 (loss functions) |
| 06 | Joint Marginal Conditional | Law of total probability, Bayes' rule | [lesson](lessons/06-joint-marginal-conditional.md) | [code](code/06-joint-marginal-conditional.py) | Used in: Phase 09 (language models) |
| 07 | Covariance Correlation | Covariance matrix, Pearson/Spearman correlation | [lesson](lessons/07-covariance-correlation.md) | [code](code/07-covariance-correlation.py) | Used in: Phase 05 (PCA), Phase 01 (eigenvalues) |
| 08 | Transformations | Change of variables, Jacobian | [lesson](lessons/08-transformations.md) | [code](code/08-transformations.py) | Used in: Phase 07 (normalizing flows) |
| 09 | Sums & CLT | Convolution, sums of RVs, central limit theorem | [lesson](lessons/09-sums-clt.md) | [code](code/09-sums-clt.py) | Used in: Phase 05 (ensemble methods) |
| 10 | LLN & CLT | Law of large numbers, central limit theorem | [lesson](lessons/10-lln-clt.md) | [code](code/10-lln-clt.py) | Used in: Phase 06 (SGD convergence) |
| 11 | Concentration Inequalities | Markov, Chebyshev, Chernoff, Hoeffding | [lesson](lessons/11-concentration-inequalities.md) | [code](code/11-concentration-inequalities.py) | Used in: Phase 05 (PAC learning), Phase 04 (stat-mech) |
| 12 | Order Statistics | Min, max, quantiles, extreme values | [lesson](lessons/12-order-statistics.md) | [code](code/12-order-statistics.py) | Used in: Phase 05 (anomaly detection) |
| 13 | MLE | Maximum likelihood estimation, properties | [lesson](lessons/13-mle.md) | [code](code/13-mle.py) | Used in: Phase 05 (logistic regression), Phase 06 (cross-entropy) |
| 14 | MAP | Maximum a posteriori, regularization as prior | [lesson](lessons/14-map.md) | [code](code/14-map.py) | Used in: Phase 06 (weight decay) |
| 15 | Exponential Family | Natural parameters, sufficient statistics, GLMs | [lesson](lessons/15-exponential-family.md) | [code](code/15-exponential-family.py) | Used in: Phase 05 (GLMs), Phase 07 (VAEs) |
| 16 | Bayesian Inference | Prior, likelihood, posterior, conjugate priors | [lesson](lessons/16-bayesian-inference.md) | [code](code/16-bayesian-inference.py) | Used in: Phase 05 (Bayesian methods), Phase 09 (LLM alignment) |
| 17 | Hypothesis Testing | Null/alternative, p-values, t-test, chi-squared | [lesson](lessons/17-hypothesis-testing.md) | [code](code/17-hypothesis-testing.py) | Used in: Phase 11 (A/B testing) |
| 18 | Confidence Intervals | Bootstrap CI, analytic CI, coverage | [lesson](lessons/18-confidence-intervals.md) | [code](code/18-confidence-intervals.py) | Used in: Phase 11 (model evaluation) |
| 19 | Bootstrap | Resampling, empirical distribution | [lesson](lessons/19-bootstrap.md) | [code](code/19-bootstrap.py) | Used in: Phase 05 (bagging) |
| 20 | ANOVA | One-way, two-way, MANOVA | [lesson](lessons/20-anova.md) | [code](code/20-anova.py) | Used in: Phase 05 (feature selection) |
| 21 | Linear Regression | OLS, ridge, LASSO, elastic net | [lesson](lessons/21-linear-regression.md) | [code](code/21-linear-regression.py) | Used in: Phase 05 (all linear models) |
| 22 | GLMs | Logistic, Poisson, multinomial regression | [lesson](lessons/22-glms.md) | [code](code/22-glms.py) | Used in: Phase 05 (classification) |
| 23 | Mixed Effects | Fixed vs random effects, hierarchical models | [lesson](lessons/23-mixed-effects.md) | [code](code/23-mixed-effects.py) | Used in: Phase 09 (NLP) |
| 24 | Bayesian Linear Regression | Gaussian prior, posterior predictive | [lesson](lessons/24-bayesian-linear-regression.md) | [code](code/24-bayesian-linear-regression.py) | Used in: Phase 05 (Bayesian methods) |
| 25 | Gaussian Processes | GP prior, kernel, posterior, regression | [lesson](lessons/25-gaussian-processes.md) | [code](code/25-gaussian-processes.py) | Used in: Phase 05 (GP), Phase 02 (Bayesian opt) |
| 26 | Multivariate Methods | MANOVA, CCA, factor analysis | [lesson](lessons/26-multivariate-methods.md) | [code](code/26-multivariate-methods.py) | Used in: Phase 05 (factor analysis) |
| 27 | Time Series | ARIMA, seasonality, stationarity | [lesson](lessons/27-time-series.md) | [code](code/27-time-series.py) | Used in: Phase 11 (monitoring) |
| 28 | State Space & Kalman | State-space models, Kalman filter, smoothing | [lesson](lessons/28-state-space-kalman.md) | [code](code/28-state-space-kalman.py) | Used in: Phase 10 (RL), Phase 08 (tracking) |
| 29 | Survival Analysis | Kaplan–Meier, Cox proportional hazards | [lesson](lessons/29-survival-analysis.md) | [code](code/29-survival-analysis.py) | Used in: Phase 11 (churn models) |
| 30 | Empirical Processes | Donsker, Glivenko–Cantelli, VC dimension | [lesson](lessons/30-empirical-processes.md) | [code](code/30-empirical-processes.py) | Used in: Phase 05 (learning theory) |
| 31 | Extreme Value Theory | GEV, GPD, return levels | [lesson](lessons/31-extreme-value-theory.md) | [code](code/31-extreme-value-theory.py) | Used in: Phase 05 (anomaly) |
| 32 | Copulas | Sklar's theorem, Archimedean, Gaussian copula | [lesson](lessons/32-copulas.md) | [code](code/32-copulas.py) | Used in: Phase 11 (risk) |
| 33 | Spatial Statistics | Kriging, variograms, spatial autocorrelation | [lesson](lessons/33-spatial-statistics.md) | [code](code/33-spatial-statistics.py) | Used in: Phase 08 (geospatial) |
| 34 | Missing Data | MCAR, MAR, MNAR, imputation | [lesson](lessons/34-missing-data.md) | [code](code/34-missing-data.py) | Used in: Phase 11 (data pipelines) |
| 35 | Causal Inference | DAGs, do-operator, IV, matching | [lesson](lessons/35-causal-inference.md) | [code](code/35-causal-inference.py) | Used in: Phase 11 (A/B testing) |
| 36 | Causal Discovery | PC, FCI, LiNGAM, additive noise | [lesson](lessons/36-causal-discovery.md) | [code](code/36-causal-discovery.py) | Used in: Phase 05 (Bayesian nets) |
| 37 | Bayesian Nonparametrics | Dirichlet process, CRP, Indian buffet | [lesson](lessons/37-bayesian-nonparametrics.md) | [code](code/37-bayesian-nonparametrics.py) | Used in: Phase 07 (infinite models) |
| 38 | ABC | Approximate Bayesian computation, likelihood-free | [lesson](lessons/38-abc.md) | [code](code/38-abc.py) | Used in: Phase 07 (simulation-based) |
| 39 | Measurement Error | Errors-in-variables, attenuation, SIMEX | [lesson](lessons/39-measurement-error.md) | [code](code/39-measurement-error.py) | Used in: Phase 11 (data quality) |
| 40 | Bayesian Workflow | Prior predictive, posterior predictive, model checking | [lesson](lessons/40-bayesian-workflow.md) | [code](code/40-bayesian-workflow.py) | Used in: Phase 05 (model evaluation) |

## 4. Builds Toward

- **Phase 05** (probabilistic models: Naive Bayes, GMM, Bayesian methods, learning theory)
- **Phase 06** (loss functions as negative log-likelihood, regularization as prior)
- **Phase 07** (VAEs, normalizing flows, diffusion models, Bayesian deep learning)
- **Phase 09** (language models as probability distributions, uncertainty)
- **Phase 10** (exploration vs exploitation, Bayesian RL)
- **Phase 11** (A/B testing, experimentation, monitoring)

## 5. Quick Start

```bash
python3 code/01-probability-axioms.py
```
