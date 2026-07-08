# 04.01 Entropy, Cross-Entropy, and KL Divergence

## Motivation
Entropy quantifies uncertainty in a random variable. Cross-entropy and KL divergence measure how one probability distribution differs from another — they are the workhorses of classification, variational inference, and information theory. Understanding these quantities is essential for designing loss functions, regularization terms, and evaluation metrics across nearly every subfield of machine learning.

## Learning Objectives
- Define Shannon entropy, joint entropy, conditional entropy, cross-entropy, KL divergence, and mutual information from first principles.
- Derive and prove key inequalities: Gibbs' inequality, non-negativity of KL divergence, chain rules, and the data processing inequality.
- Implement entropy-based losses in Python for classification and generative modelling.
- Connect information-theoretic quantities to practical ML algorithms including decision trees, VAEs, and representation learning.

## Math Foundation

### Shannon Entropy
For a discrete random variable $X$ with probability mass function $p(x)$, the Shannon entropy is:

$$H(X) = -\sum_{x \in \mathcal{X}} p(x) \log p(x)$$

with the convention $0 \log 0 = 0$. Entropy is measured in bits when the logarithm is base 2, or nats when using the natural logarithm. It satisfies $0 \le H(X) \le \log |\mathcal{X}|$, with maximum attained for the uniform distribution and minimum for a deterministic variable.

### Joint and Conditional Entropy
The joint entropy of two discrete random variables $(X,Y)$ with joint distribution $p(x,y)$ is:

$$H(X,Y) = -\sum_{x,y} p(x,y) \log p(x,y)$$

The conditional entropy $H(Y|X)$ is the expected uncertainty in $Y$ given knowledge of $X$:

$$H(Y|X) = \sum_x p(x) H(Y|X=x) = -\sum_{x,y} p(x,y) \log p(y|x)$$

The chain rule relates them: $H(X,Y) = H(X) + H(Y|X)$.

### Cross-Entropy
For two distributions $p$ and $q$ over the same set $\mathcal{X}$, the cross-entropy is:

$$H(p,q) = -\sum_{x \in \mathcal{X}} p(x) \log q(x)$$

Cross-entropy is not symmetric: $H(p,q) \ne H(q,p)$ in general. It lower-bounds the entropy: $H(p,q) \ge H(p)$.

### KL Divergence
The Kullback-Leibler divergence from $q$ to $p$ is:

$$D_{\text{KL}}(p \| q) = \sum_{x \in \mathcal{X}} p(x) \log \frac{p(x)}{q(x)}$$

KL divergence is non-negative (Gibbs' inequality), zero iff $p = q$ almost everywhere, and convex in the pair $(p,q)$. It is not a metric because it is asymmetric and does not satisfy the triangle inequality.

### Mutual Information
Mutual information measures the reduction in uncertainty about one variable given knowledge of another:

$$I(X;Y) = D_{\text{KL}}(p(x,y) \| p(x)p(y)) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$

Mutual information is symmetric, non-negative, and equals zero iff $X$ and $Y$ are independent.

## Key Properties and Inequalities

### Gibbs' Inequality
For any two probability distributions $p$ and $q$ over the same event space:

$$D_{\text{KL}}(p \| q) \ge 0$$

with equality if and only if $p = q$ almost everywhere. This follows from Jensen's inequality applied to the convex function $-\log(\cdot)$:

$$-\sum p(x) \log \frac{q(x)}{p(x)} \ge -\log \sum p(x) \frac{q(x)}{p(x)} = -\log 1 = 0$$

### Data Processing Inequality
If $X \to Y \to Z$ form a Markov chain, then:

$$I(X;Y) \ge I(X;Z)$$

No amount of processing of $Y$ can increase the information about $X$. This fundamental limit underlies the information bottleneck method and guarantees that downstream representations cannot improve upon their input features.

### Chain Rules
- $H(X_1,\dots,X_n) = \sum_{i=1}^n H(X_i | X_{i-1},\dots,X_1)$
- $I(X_1,\dots,X_n; Y) = \sum_{i=1}^n I(X_i; Y | X_{i-1},\dots,X_1)$

## Python Implementation

```python
import numpy as np
from scipy.special import xlogy, rel_entr

def entropy(p, base=np.e):
    """Shannon entropy of distribution p."""
    p = np.asarray(p, dtype=float)
    p = p / p.sum()
    # xlogy handles 0 log 0 = 0
    H = -np.sum(xlogy(p, p))
    if base == 2:
        H /= np.log(2)
    return H

def cross_entropy(p, q, base=np.e):
    """Cross-entropy H(p, q)."""
    p = np.asarray(p, dtype=float) / np.sum(p)
    q = np.asarray(q, dtype=float) / np.sum(q)
    ce = -np.sum(xlogy(p, q))
    if base == 2:
        ce /= np.log(2)
    return ce

def kl_divergence(p, q):
    """KL divergence D_KL(p || q)."""
    p = np.asarray(p, dtype=float) / np.sum(p)
    q = np.asarray(q, dtype=float) / np.sum(q)
    return np.sum(rel_entr(p, q))

def mutual_information(joint, base=np.e):
    """Mutual information from a joint probability matrix."""
    joint = np.asarray(joint, dtype=float)
    joint /= joint.sum()
    px = joint.sum(axis=1, keepdims=True)
    py = joint.sum(axis=0, keepdims=True)
    mi = np.sum(xlogy(joint, joint / (px @ py)))
    if base == 2:
        mi /= np.log(2)
    return mi

# Example: compare two distributions
p = np.array([0.7, 0.2, 0.1])
q = np.array([0.4, 0.4, 0.2])
print(f"H(p) = {entropy(p):.3f} nats")
print(f"CE(p,q) = {cross_entropy(p, q):.3f} nats")
print(f"KL(p||q) = {kl_divergence(p, q):.3f} nats")
print(f"H(p) + KL = {entropy(p) + kl_divergence(p, q):.3f} (matches CE)")
```

## Visualization
Plot three distributions (left-skewed, uniform, right-skewed) and show their entropy values as horizontal bars. A second panel shows the KL divergence matrix between all pairs. For mutual information, display a 3D bar plot of a joint distribution alongside its marginals, with the MI value annotated.

## Practical Considerations

### Numerical Stability
KL divergence can be numerically unstable when $q(x)$ is very close to zero but $p(x)$ is not. The `scipy.special.rel_entr` function handles $0 \log 0 = 0$ and returns $\infty$ when $q(x)=0 < p(x)$. For cross-entropy loss in classification, always clip logits (e.g., using `torch.clamp` or `tf.clip_by_value`) before computing $\log$.

### Choosing the Base
- **Natural log (nats)**: preferred in variational inference and information geometry because derivatives are simpler.
- **Base 2 (bits)**: standard in communication theory and decision tree literature (information gain in bits).
- **Base 10 (dits/digits)**: rarely used in ML but appears in some signal processing contexts.

### Bias in Entropy Estimation
Plug-in entropy estimators (replacing probabilities with empirical frequencies) are biased downward, especially for small sample sizes. The Miller-Madow correction adds $-(m-1)/(2n)$ where $m$ is the number of non-empty bins and $n$ is the sample count. For high-dimensional distributions, consider nearest-neighbor entropy estimators (Kraskov-Stögbauer-Grassberger) which are more sample-efficient.

## Connections to ML

### Classification Loss
The categorical cross-entropy loss for $K$-class classification is exactly $H(p, q)$ where $p$ is the one-hot label and $q$ is the predicted probability vector. Minimizing cross-entropy is equivalent to minimizing KL divergence from the empirical distribution to the model, because $H(p)$ is constant w.r.t. model parameters.

### Variational Autoencoders
The evidence lower bound (ELBO) decomposes as:

$$\log p(x) \ge \mathbb{E}_{z \sim q(z|x)} [\log p(x|z)] - D_{\text{KL}}(q(z|x) \| p(z))$$

The KL term acts as a regularizer, pulling the approximate posterior toward the prior.

### Decision Trees
Information gain for a split $S$ is the reduction in entropy:

$$\text{IG}(\text{feature}) = H(\text{target}) - \sum_{v \in \text{feature}} \frac{|S_v|}{|S|} H(S_v)$$

Splits that maximize information gain produce shallower, more accurate trees.

### t-SNE
t-SNE defines high-dimensional similarities $p_{j|i}$ (Gaussian kernel) and low-dimensional similarities $q_{j|i}$ (Cauchy kernel), then minimizes $KL(P\|Q)$. The asymmetry of KL places high cost on mapping nearby points far apart, preserving local structure at the expense of global structure.

### Representation Learning and InfoNCE
The InfoNCE loss used in contrastive learning (SimCLR, MoCo, CLIP) maximizes a lower bound on mutual information between augmentations of the same example:

$$\mathcal{L}_{\text{NCE}} = -\mathbb{E} \left[ \log \frac{\exp(f(x)^T f(x^+))}{\sum_{j} \exp(f(x)^T f(x_j^-))} \right]$$

This is equivalent to a categorical cross-entropy over the set of $N$ negative samples plus one positive.

## References
- Cover & Thomas, *Elements of Information Theory*, 2nd ed.
- MacKay, *Information Theory, Inference, and Learning Algorithms*
- Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, 1948
- Kraskov, Stögbauer, Grassberger, "Estimating mutual information," *Physical Review E*, 2004
