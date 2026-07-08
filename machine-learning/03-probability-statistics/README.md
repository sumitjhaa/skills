# Phase 03: Probability & Statistics

Building a rigorous foundation in probability theory and statistical inference, from measure-theoretic probability to full Bayesian workflow. 40 lessons with companion code and practice exercises.

## Lesson Table

| #  | Code | Topic | Description |
|----|------|-------|-------------|
| 01 | 03.01 | Probability Axioms & Sigma-Algebras | Kolmogorov axioms, measure spaces, probability triples |
| 02 | 03.02 | Random Variables | Measurable functions, induced distributions, CDFs |
| 03 | 03.03 | Distributions | 20+ discrete & continuous families, properties |
| 04 | 03.04 | Multivariate Distributions | Joint CDF/PDF, multinomial, multivariate normal |
| 05 | 03.05 | Expectation, Variance, Moments | Lebesgue integral, LOTUS, moment generating functions |
| 06 | 03.06 | Joint/Marginal/Conditional | Marginalization, conditional distributions, Bayes rule |
| 07 | 03.07 | Covariance & Correlation | Covariance matrix, Pearson/Spearman correlation |
| 08 | 03.08 | Transformations of RVs | PDF transformation technique, Jacobian |
| 09 | 03.09 | Sums of RVs & CLT | Convolution, characteristic functions, Central Limit Theorem |
| 10 | 03.10 | LLN & CLT | Weak/strong LLN, CLT proofs, Berry-Esseen bounds |
| 11 | 03.11 | Concentration Inequalities | Markov, Chebyshev, Chernoff, Hoeffding, McDiarmid |
| 12 | 03.12 | Order Statistics | Distributions of order statistics, extreme values |
| 13 | 03.13 | Maximum Likelihood Estimation | Likelihood principle, MLE properties, Fisher information |
| 14 | 03.14 | Maximum A Posteriori | Bayesian MAP, regularization, ridge/lasso connections |
| 15 | 03.15 | Exponential Family | Natural parameters, sufficient statistics, conjugacy |
| 16 | 03.16 | Bayesian Inference | Prior/posterior, conjugate models, predictive distributions |
| 17 | 03.17 | Hypothesis Testing | Neyman-Pearson, Wald, score, likelihood ratio tests |
| 18 | 03.18 | Confidence Intervals | Frequentist vs Bayesian intervals, bootstrap intervals |
| 19 | 03.19 | Bootstrap | Parametric/nonparametric bootstrap, jackknife |
| 20 | 03.20 | ANOVA | One-way/two-way ANOVA, F-tests, multiple comparisons |
| 21 | 03.21 | Linear Regression | OLS, Gauss-Markov, diagnostics, regularization |
| 22 | 03.22 | Generalized Linear Models | Logistic, Poisson, link functions, deviance |
| 23 | 03.23 | Mixed Effects Models | Random intercepts/slopes, LMM, REML |
| 24 | 03.24 | Bayesian Linear Regression | Conjugate prior, posterior predictive, model comparison |
| 25 | 03.25 | Gaussian Processes | Covariance functions, GP regression, hyperparameter learning |
| 26 | 03.26 | Multivariate Methods | CCA, factor analysis, ICA |
| 27 | 03.27 | Time Series Analysis | ARIMA, stationarity, spectral analysis |
| 28 | 03.28 | State Space / Kalman Filter | SSM, Kalman filter/smoother, particle filters |
| 29 | 03.29 | Survival Analysis | Kaplan-Meier, Cox PH, Weibull models |
| 30 | 03.30 | Empirical Processes | ECDF, Glivenko-Cantelli, DKW inequality |
| 31 | 03.31 | Extreme Value Theory | GEV, GPD, return levels |
| 32 | 03.32 | Copulas | Sklar's theorem, Archimedean/elliptical copulas |
| 33 | 03.33 | Spatial Statistics | Variograms, Kriging, spatial autoregression |
| 34 | 03.34 | Missing Data | MCAR/MAR/MNAR, imputation, EM algorithm |
| 35 | 03.35 | Causal Inference | Potential outcomes, RCTs, instrumental variables |
| 36 | 03.36 | Causal Discovery | PC algorithm, score-based, functional causal models |
| 37 | 03.37 | Bayesian Nonparametrics | Dirichlet process, CRP, stick-breaking |
| 38 | 03.38 | Approximate Bayesian Computation | Rejection ABC, MCMC-ABC, summary statistics |
| 39 | 03.39 | Measurement Error | Berkson/classical error, SIMEX, regression calibration |
| 40 | 03.40 | Full Bayesian Workflow | Prior predictive checks, posterior diagnostics, model comparison |

## Getting Started

```bash
# Run any lesson's code
python code/03.01.py

# Read a lesson
cat lessons/03-probability-axioms.md

# Do practice exercises
code practice/phase03-exercises.md
```

**Dependencies:** `numpy`, `scipy`, `matplotlib`, `pandas`
