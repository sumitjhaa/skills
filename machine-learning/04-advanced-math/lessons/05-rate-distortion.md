# 04.05 Rate–Distortion Theory

## Motivation
Rate–distortion theory answers a fundamental question: *What is the minimum number of bits needed to represent a source with at most a given distortion?* It is the foundation of lossy compression, the information bottleneck method, and modern neural compression systems. The theory reveals fundamental trade-offs between compression rate, reconstruction fidelity, and perceptual quality.

## Learning Objectives
- Define the rate–distortion function $R(D)$ and derive its properties.
- Compute $R(D)$ for Gaussian and binary sources analytically.
- Implement the Blahut–Arimoto algorithm for rate–distortion computation.
- Connect rate–distortion to the VAE objective, information bottleneck, and neural compression.

## Math Foundation

### Rate–Distortion Function
Let $X \sim p(x)$ be a source, $\hat{X}$ a reconstruction, and $d(x, \hat{x})$ a distortion measure. The rate–distortion function is:

$$R(D) = \min_{p(\hat{x}|x): \mathbb{E}[d(X,\hat{X})] \le D} I(X; \hat{X})$$

This minimises the mutual information (rate) between $X$ and $\hat{X}$ subject to an expected distortion constraint. The minimisation is over conditional distributions $p(\hat{x}|x)$ — the "test channel" or "compression mapping."

### Properties of $R(D)$
1. **Non-increasing**: increasing $D$ cannot increase the minimum rate.
2. **Convex**: $R(\alpha D_1 + (1-\alpha)D_2) \le \alpha R(D_1) + (1-\alpha) R(D_2)$.
3. **$R(0) = H(X)$** for discrete sources (lossless compression).
4. **$R(D_{\max}) = 0$**: at or above the maximum distortion, no bits are needed (output the mean).
5. **Shannon lower bound**: $R(D) \ge H(X) - \max_{p(\hat{x})} \mathbb{E}[-\log p(\hat{x})]$.

### Gaussian Source with MSE Distortion
For $X \sim \mathcal{N}(0, \sigma^2)$ and $d(x,\hat{x}) = (x - \hat{x})^2$:

$$R(D) = \begin{cases}
\frac12 \log_2 \left(\frac{\sigma^2}{D}\right) & 0 \le D \le \sigma^2 \\
0 & D > \sigma^2
\end{cases}$$

This is achieved by the test channel $\hat{X} = X + Z$ where $Z \sim \mathcal{N}(0, D)$ independent of $X$, and the optimal reconstruction distribution is $\hat{X} \sim \mathcal{N}(0, \sigma^2 - D)$. This is called *reverse water-filling*.

### Reverse Water-Filling
For $k$ independent Gaussian sources with variances $\sigma_1^2, \dots, \sigma_k^2$, the optimal bit allocation minimises total distortion by allocating bits to components with larger variance first:

$$R_i(D) = \frac12 \log_2 \left( \frac{\sigma_i^2}{D_i} \right), \quad D = \sum_i D_i$$

The solution is $D_i = \min(\sigma_i^2, \theta)$ where $\theta$ is chosen so that $\sum_i \min(\sigma_i^2, \theta) = D$. Sources with $\sigma_i^2 < \theta$ get zero bits; sources with larger variance get $\frac12 \log_2(\sigma_i^2/\theta)$ bits.

## Blahut–Arimoto Algorithm for Rate–Distortion

The algorithm iteratively updates the test channel and the marginal distribution of $\hat{X}$ to converge to $R(D)$:

1. Initialise $p(\hat{x}|x)$ (e.g., randomly).
2. Compute $r(\hat{x}) = \sum_x p(x) p(\hat{x}|x)$.
3. Update: $p(\hat{x}|x) \propto r(\hat{x}) \exp(-\beta d(x,\hat{x}))$ where $\beta > 0$ is a Lagrange multiplier.
4. Normalise and repeat until convergence. The achieved rate is $R = I(X;\hat{X})$ and distortion is $D = \mathbb{E}[d]$.

```python
import numpy as np

def rate_distortion_ba(px, distortion, beta, max_iter=1000, tol=1e-8):
    """Blahut-Arimoto algorithm for rate-distortion.
    
    Args:
        px: source distribution (n,)
        distortion: matrix d(x, x_hat) of shape (n, m)
        beta: Lagrange multiplier (inverse temperature)
    Returns:
        R: rate (nats)
        D: distortion
        p_hat_given_x: optimal test channel
    """
    n, m = distortion.shape
    # initialise uniform test channel
    p_hat_given_x = np.ones((n, m)) / m
    
    for _ in range(max_iter):
        # marginal of reconstruction
        r_hat = px @ p_hat_given_x
        
        # update test channel via Gibbs distribution
        logits = np.log(r_hat + 1e-12) - beta * distortion
        logits -= logits.max(axis=1, keepdims=True)  # numerical stability
        p_new = np.exp(logits)
        p_new /= p_new.sum(axis=1, keepdims=True)
        
        # check convergence
        if np.max(np.abs(p_new - p_hat_given_x)) < tol:
            break
        p_hat_given_x = p_new
    
    joint = px[:, None] * p_hat_given_x
    # compute mutual information I(X; X_hat)
    px_marg = px[:, None]
    r_hat = joint.sum(axis=0)
    mi = np.sum(joint * np.log(joint / (px_marg * r_hat[None, :]) + 1e-12))
    avg_dist = np.sum(joint * distortion)
    
    return mi, avg_dist, p_hat_given_x

# Example: binary source with Hamming distortion
px = np.array([0.7, 0.3])
dist = 1.0 - np.eye(2)  # Hamming: 0 on diagonal, 1 off
beta = 2.0
R, D, _ = rate_distortion_ba(px, dist, beta)
print(f"beta={beta}: R = {R:.4f} nats, D = {D:.4f}")
```

## The Information Bottleneck

The information bottleneck (IB) method generalises rate–distortion by introducing a relevance variable $Y$:

$$\min_{p(z|x)} I(X;Z) - \beta I(Z;Y)$$

Here $Z$ is a compressed representation of $X$, and $Y$ is the target variable we want to preserve information about. This is exactly a rate–distortion problem where the distortion is $-\log p(y|z)$, making the IB the rate–distortion problem for the "sufficient statistics" of $Y$.

The IB curve $I(Z;Y)$ vs $I(X;Z)$ traces the optimal trade-off between compression and prediction — analogous to the rate–distortion curve with $D = -\mathbb{E}[\log p(y|z)]$. The VAE's ELBO can be interpreted as a variational IB with $\beta = 1$.

## Connection to Variational Autoencoders

The VAE objective can be rearranged as:

$$\mathbb{E}_{q(z|x)}[-\log p(x|z)] + \beta D_{\text{KL}}(q(z|x) \| p(z))$$

The first term is the expected distortion (reconstruction error). The second term is the rate — the KL divergence from the prior $p(z)$ to the approximate posterior $q(z|x)$ measures the additional bits needed to encode $x$ under the variational code. With $\beta = 1$, the VAE minimises an upper bound on $R(D)$. The $\beta$-VAE variant scales the KL term to adjust the rate–distortion trade-off, exactly mirroring the Lagrange multiplier formulation of $R(D)$.

## Neural Compression

Modern neural compression systems (e.g., Ballé et al. 2017, 2018) parameterise the test channel $p(\hat{x}|x)$ as a neural network with a hyperprior to capture spatial dependencies. The loss function is:

$$\mathcal{L} = \underbrace{\mathbb{E}[-\log_2 p(\hat{z})]}_{\text{rate}} + \lambda \underbrace{\mathbb{E}[d(x, \hat{x})]}_{\text{distortion}}$$

where $\hat{z}$ is a quantised latent representation. This is end-to-end differentiable using uniform noise for the quantisation (instead of rounding), enabling gradient-based training. These methods outperform traditional codecs like JPEG and BPG on perceptual quality at low bitrates.

## Rate–Distortion–Perception Trade-off

Blau & Michaeli (2018) introduced the rate–distortion–perception trade-off, adding a perceptual quality constraint:

$$R(D,P) = \min_{p(\hat{x}|x): \mathbb{E}[d] \le D, \text{div}(p_X, p_{\hat{X}}) \le P} I(X;\hat{X})$$

At a fixed rate, improving perceptual quality (closer to the true source distribution) necessarily increases distortion. This explains why generative models like GANs produce perceptually appealing but potentially inaccurate reconstructions, while MSE-optimised models may be blurry.

## Practical Considerations

### Choosing the Distortion Measure
- **MSE**: tractable, closed-form for Gaussians, but does not capture perceptual quality.
- **Perceptual metrics**: LPIPS, SSIM, or GAN-based discriminators — better aligned with human judgement but non-convex and harder to optimise.
- **Log-loss**: $-\log p(y|x)$ — ties rate–distortion directly to likelihood and the information bottleneck.

### Computing $R(D)$ in Practice
- The Blahut–Arimoto algorithm is $O(nm)$ per iteration for $n$ source symbols and $m$ reconstruction symbols.
- For continuous sources, Monte Carlo approximation or variational upper bounds are necessary.
- The VAE bound $\mathbb{E}[-\log p(x|z)] + \beta D_{\text{KL}}(q(z|x) \| p(z))$ provides a variational upper bound on $R(D)$ that is computationally tractable for high-dimensional data.

## References
- Cover & Thomas, *Elements of Information Theory*, 2nd ed.
- Shannon, "Coding Theorems for a Discrete Source With a Fidelity Criterion," *IRE National Convention Record*, 1959
- Tishby, Pereira, Bialek, "The Information Bottleneck Method," *Allerton Conference*, 1999
- Alemi et al., "Deep Variational Information Bottleneck," *ICLR 2017*
- Ballé et al., "Variational Image Compression with a Scale Hyperprior," *ICLR 2018*
- Blau & Michaeli, "The Perception-Distortion Tradeoff," *CVPR 2018*
