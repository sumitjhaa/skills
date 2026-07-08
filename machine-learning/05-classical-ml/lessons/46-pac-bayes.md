# Lesson 05.46: PAC-Bayes

## Learning Objectives
- Understand PAC-Bayesian generalization bounds
- Derive the PAC-Bayes bound from KL divergence
- Apply to stochastic classifiers and model averaging
- Analyze connections to Bayesian inference and regularization

## Setup
- **Prior $P$**: Distribution over hypotheses $h \in H$ (before seeing data)
- **Posterior $Q$**: Learner's distribution after training
- **True risk**: $R(h) = \mathbb{E}_{(x,y)\sim D}[\ell(h(x), y)]$
- **Empirical risk**: $\hat{R}(h) = \frac{1}{n} \sum_{i=1}^n \ell(h(x_i), y_i)$
- **Gibbs risk**: $R(Q) = \mathbb{E}_{h \sim Q}[R(h)]$, $\hat{R}(Q) = \mathbb{E}_{h \sim Q}[\hat{R}(h)]$

## PAC-Bayes Bound
For any prior $P$ (fixed before seeing data) and any posterior $Q$ (learned from data):

With probability $\geq 1-\delta$ over draw of $S \sim D^n$:

$$R(Q) \leq \hat{R}(Q) + \sqrt{\frac{D_{KL}(Q \| P) + \log \frac{2n}{\delta}}{2(n-1)}}$$

Key tradeoff: minimize empirical Gibbs risk vs keep posterior close to prior.

### Intuition
- $D_{KL}(Q \| P)$ measures "how much the posterior shifted"
- Small KL → posterior is close to prior → tighter bound (less overfitting)
- Large KL → complex posterior → looser bound (more capacity for data fitting)

## KL Divergence
$$D_{KL}(Q \| P) = \mathbb{E}_{h \sim Q} \left[ \log \frac{Q(h)}{P(h)} \right]$$

- $D_{KL} \geq 0$, equals 0 iff $Q = P$
- Finite $H$: $D_{KL}(Q\|P) \leq \log |H|$ if $P$ uniform
- Continuous $H$: $D_{KL}$ can be infinite if supports differ

## Gibbs Classifier
Stochastic classifier: sample $h \sim Q$, predict with $h$.

**Averaged classifier**: predict by averaging predictions: $\mathbb{E}_{h \sim Q}[h(x)]$ — typically lower Gibbs risk due to Jensen's inequality (for convex losses).

## Connections to Regularization

### Bayesian Inference
The optimal posterior for log-loss under correct prior is the true Bayesian posterior:

$$Q^*(h) \propto P(h) \exp(-\eta \hat{R}(h))$$

### Dropout as PAC-Bayes
Dropout in neural networks can be interpreted as a PAC-Bayes posterior:
- Prior: network weights close to zero (Gaussian)
- Posterior: random masking induces multiplicative noise
- Training minimizes $\hat{R}(Q) + \lambda D_{KL}(Q\|P)$

### SVMs
SVM's maximum margin solution has a PAC-Bayes interpretation:
- Prior: spherically symmetric Gaussian over weight vectors
- Posterior: point mass at SVM solution
- Margin $1/\|w\|$ controls KL divergence

## Code: PAC-Bayes Bound for Stochastic Classifier

```python
import numpy as np
from scipy.stats import norm

def pac_bayes_bound(emp_risk, kl_div, n, delta=0.05):
    """Compute PAC-Bayes bound on true risk"""
    bound = emp_risk + np.sqrt((kl_div + np.log(2 * n / delta)) / (2 * (n - 1)))
    return bound

def compute_kl_gaussian(prior_mean, prior_std, post_mean, post_std):
    """KL divergence between two Gaussians"""
    return np.log(post_std / prior_std) + (prior_std**2 + (post_mean - prior_mean)**2) / (2 * post_std**2) - 0.5
```

## Applications
- **SVM generalization bounds**: PAC-Bayes gives tighter bounds than VC theory
- **Neural network bounds**: Explain why overparameterized nets generalize
- **Dropout variational inference**: Gal & Ghahramani (ICML 2016) — dropout as approximate Bayesian inference
- **SGLD**: Stochastic gradient Langevin dynamics as PAC-Bayesian learning
- **Gaussian processes**: Exact PAC-Bayes treatment of kernel methods

## Key Results

### Optimal Posterior
Tightest bound when $Q$ minimizes:

$$Q^* = \arg\min_Q \hat{R}(Q) + \sqrt{\frac{D_{KL}(Q \| P)}{2n}}$$

Bayesian posterior is optimal for log-loss under correct prior.

### Catoni's Bound
Sharper bound (with optimal constant):

$$R(Q) \leq \hat{R}(Q) + \frac{D_{KL}(Q \| P) + \log(1/\delta)}{n\lambda} + \frac{\lambda}{8n}$$

Optimizing $\lambda$ gives bound $O(\sqrt{D_{KL}/n})$.

### PAC-Bayes vs VC
- VC: worst-case over $H$, doesn't use data distribution
- PAC-Bayes: data-dependent, uses prior knowledge
- PAC-Bayes often tighter, especially for complex models

## Practical Considerations
- **Choosing prior**: Can be data-dependent (data is split: prior from one half, posterior from other)
- **Computing KL**: For parametric models with Gaussian posterior, KL is tractable
- **Ensemble interpretation**: Any model ensemble defines a $Q$
- **Bounded losses**: Bounds assume loss in $[0, 1]$; unbounded losses need truncation

## References
- McAllester, "PAC-Bayesian Model Averaging" (COLT 1999)
- McAllester, "A PAC-Bayesian Tutorial with a Dropout Bound" (arXiv, 2013)
- Catoni, "PAC Bayesian Supervised Classification" (IMS Lecture Notes, 2007)
- Germain et al., "PAC-Bayesian Theory Meets Bayesian Inference" (NIPS 2016)
- Dziugaite & Roy, "Computing Nonvacuous Generalization Bounds for Deep Neural Networks" (ICML 2017)
