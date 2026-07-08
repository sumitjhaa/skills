# Lesson 02: Random Variables

## Learning Objectives

After completing this lesson, you will be able to:
- Define a random variable as a measurable function
- Understand the induced probability distribution
- Work with CDFs, PMFs, and PDFs
- Distinguish discrete, continuous, and singular random variables
- Apply pushforward measures to transformations

## Definition and Measurability

A **random variable** $X$ is a measurable function $X: \Omega \to \mathbb{R}$ such that for every Borel set $B \in \mathcal{B}(\mathbb{R})$:
$$X^{-1}(B) = \{\omega \in \Omega : X(\omega) \in B\} \in \mathcal{F}$$

This measurability condition ensures we can assign probabilities to events defined in terms of $X$. Without it, $P(X \in B)$ might be undefined.

### Induced Distribution

The **probability law** (or distribution) of $X$ is the pushforward measure $P_X$ on $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$ defined by:
$$P_X(B) = P(X \in B) = P(\{\omega: X(\omega) \in B\})$$

This moves the probability from $(\Omega, \mathcal{F})$ to $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$, allowing us to work entirely on the real line.

## Cumulative Distribution Function (CDF)

The **CDF** of $X$ is:
$$F_X(x) = P(X \leq x) = P_X((-\infty, x])$$

### Properties of the CDF

1. **Non-decreasing:** $x_1 \leq x_2 \implies F(x_1) \leq F(x_2)$
2. **Right-continuous:** $\lim_{t \to x^+} F(t) = F(x)$
3. **Limits at boundaries:** $\lim_{x \to -\infty} F(x) = 0$, $\lim_{x \to \infty} F(x) = 1$
4. **Jump size:** $P(X = x) = F(x) - \lim_{t \to x^-} F(t)$

The CDF uniquely determines the distribution of $X$. Two random variables with the same CDF are equal in distribution.

## Types of Random Variables

### Discrete Random Variables

$X$ is **discrete** if it takes values in a countable set $S = \{x_1, x_2, \dots\}$. It is characterized by the **probability mass function (PMF)**:
$$p_X(x) = P(X = x)$$

Properties: $p_X(x) \geq 0$, $\sum_{x \in S} p_X(x) = 1$, $F_X(x) = \sum_{t \leq x} p_X(t)$

The CDF of a discrete random variable is a step function with jumps at each $x_i$ of size $p_X(x_i)$.

### Continuous Random Variables

$X$ is **continuous** if there exists a function $f_X \geq 0$ (the **probability density function, PDF**) such that:
$$F_X(x) = \int_{-\infty}^{x} f_X(t) dt$$
$$f_X(x) = \frac{d}{dx} F_X(x) \quad \text{(where the derivative exists)}$$

Properties: $\int_{-\infty}^{\infty} f_X(x) dx = 1$, $P(a \leq X \leq b) = \int_a^b f_X(x) dx$, $P(X = a) = 0$ for any specific point $a$.

### Singular Random Variables

$X$ is **singular** if its CDF is continuous but there is no density with respect to Lebesgue measure. The canonical example is the **Cantor distribution**, defined by the Cantor set (a fractal with Lebesgue measure zero but uncountably many points).

**Lebesgue decomposition:** Any CDF can be uniquely decomposed as:
$$F = \alpha F_{\text{discrete}} + \beta F_{\text{abs. cont.}} + \gamma F_{\text{singular}}$$
where $\alpha + \beta + \gamma = 1$ and $\alpha, \beta, \gamma \geq 0$.

## Functions of Random Variables

If $X$ is a random variable and $g: \mathbb{R} \to \mathbb{R}$ is a measurable function, then $Y = g(X)$ is a random variable.

### CDF of Transformed Variable
$$F_Y(y) = P(g(X) \leq y) = P(X \in g^{-1}((-\infty, y]))$$

### PDF of Transformed Variable (monotone $g$)
If $g$ is strictly monotone and differentiable with $g^{-1}$ differentiable:
$$f_Y(y) = f_X(g^{-1}(y)) \left|\frac{d}{dy} g^{-1}(y)\right|$$

### PDF of Transformed Variable (general case)
$$f_Y(y) = \sum_{i: g(x_i) = y} \frac{f_X(x_i)}{|g'(x_i)|}$$

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class RandomVariable:
    """Base class for random variables."""

    def cdf(self, x):
        raise NotImplementedError

    def pdf(self, x):
        raise NotImplementedError

    def sample(self, n=1):
        raise NotImplementedError

    def transform(self, g, g_inv, dg_inv):
        """Return PDF of Y = g(X) for monotone g."""
        def pdf_y(y):
            x = g_inv(y)
            return self.pdf(x) * abs(dg_inv(y))
        return pdf_y

# Example: Exponential to Uniform via Probability Integral Transform
# If X ~ Exponential(1) and Y = F_X(X), then Y ~ Uniform(0,1)

lam = 1.0
X = stats.expon(scale=1/lam)
xs = np.linspace(0, 5, 1000)
ys = X.cdf(xs)  # F_X(x)

plt.figure(figsize=(10, 4))
plt.subplot(121)
plt.plot(xs, X.pdf(xs))
plt.title("Exponential(1) PDF")
plt.subplot(122)
plt.hist(X.rvs(10000), bins=50, density=True, alpha=0.7)
plt.title("Sampled Exponential(1)")
plt.tight_layout()
plt.show()

# Probability Integral Transform
samples = X.rvs(10000)
uniform_samples = X.cdf(samples)
plt.figure()
plt.hist(uniform_samples, bins=50, density=True, alpha=0.7)
plt.title("PIT: Uniform(0,1) from Exponential")
plt.show()
```

## Quantile Function

The **quantile function** (inverse CDF) is:
$$F_X^{-1}(p) = \inf\{x \in \mathbb{R}: F_X(x) \geq p\}, \quad p \in [0, 1]$$

Key property: If $U \sim \text{Uniform}(0,1)$, then $X = F_X^{-1}(U)$ has distribution $F_X$. This is the **inverse transform sampling** method.

## Visualization

Plot the CDF as a right-continuous step function for discrete variables and as a smooth curve for continuous variables. Overlay the PDF (for continuous) or PMF (for discrete) below. The median is $F_X^{-1}(0.5)$, and the interquartile range is $F_X^{-1}(0.75) - F_X^{-1}(0.25)$. 

For the probability integral transform, plot the histogram of $U = F_X(X)$ for any continuous $X$ to verify uniformity.

## Practical Considerations

- **Measurability is almost automatic:** Every function you can explicitly define without the axiom of choice is Borel measurable. This includes all continuous functions, piecewise functions, limits of measurable functions, etc.
- **CDF vs PDF:** In high dimensions, CDFs become less useful (curse of dimensionality). PDFs (or parametric models) are preferred for high-dimensional ML.
- **PIT for calibration:** The probability integral transform is used to check whether a predictive model is well-calibrated. If predicted CDFs are correct, the PIT values should be uniform.
- **Quantile functions for VaR:** In finance and risk management, quantiles are used for Value-at-Risk calculations.

## References

- Billingsley, P. (1995). *Probability and Measure*
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*, Vol. I
- Resnick, S. I. (2013). *A Probability Path*
