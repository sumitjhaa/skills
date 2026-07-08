# Lesson 06: Joint, Marginal, and Conditional Distributions

## Learning Objectives

After completing this lesson, you will be able to:
- Derive marginal distributions from joint distributions
- Compute conditional distributions from joint distributions
- Apply Bayes' rule in continuous and discrete settings
- Use the chain rule of probability for high-dimensional problems
- Understand conditional expectation and its properties

## Joint Distributions (Review)

A **joint distribution** describes the simultaneous behavior of multiple random variables.

- **Discrete:** $p_{X,Y}(x, y) = P(X = x, Y = y)$
- **Continuous:** $f_{X,Y}(x, y)$ such that $P((X,Y) \in A) = \iint_A f_{X,Y}(x,y) \, dx \, dy$

The joint distribution completely describes the probabilistic relationship between $X$ and $Y$.

## Marginal Distributions

### From Joint PMF

To obtain the marginal distribution of $X$ from the joint PMF:
$$p_X(x) = \sum_{y} p_{X,Y}(x, y)$$

This "sums out" the variable $Y$. Analogously:
$$p_Y(y) = \sum_{x} p_{X,Y}(x, y)$$

### From Joint PDF

To obtain the marginal density of $X$ from the joint PDF:
$$f_X(x) = \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy$$

This "integrates out" $Y$. The resulting $f_X(x)$ is a valid PDF (non-negative, integrates to 1).

**Intuition:** Marginalization projects the joint distribution onto a lower-dimensional subspace, aggregating over all possibilities of the marginalized variable.

## Conditional Distributions

### Conditional PMF

$$p_{Y|X}(y \mid x) = \frac{p_{X,Y}(x, y)}{p_X(x)} \quad \text{provided } p_X(x) > 0$$

This gives the probability distribution of $Y$ given we know $X = x$.

### Conditional PDF

$$f_{Y|X}(y \mid x) = \frac{f_{X,Y}(x, y)}{f_X(x)} \quad \text{provided } f_X(x) > 0$$

### Conditional CDF

$$F_{Y|X}(y \mid x) = \int_{-\infty}^{y} f_{Y|X}(t \mid x) \, dt$$

## Chain Rule of Probability

For any collection of random variables:
$$p(x_1, x_2, \dots, x_n) = p(x_1) p(x_2 \mid x_1) p(x_3 \mid x_1, x_2) \cdots p(x_n \mid x_1, \dots, x_{n-1})$$

This factorization is always valid (no independence assumptions). It is the foundation of autoregressive models, Bayesian networks, and sequential data modeling.

## Bayes' Rule

### General Form

$$P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$$

### In Statistical Inference

$$f(\theta \mid x) = \frac{f(x \mid \theta) f(\theta)}{f(x)}$$

Where:
- $f(\theta \mid x)$ is the **posterior** distribution
- $f(x \mid \theta)$ is the **likelihood**
- $f(\theta)$ is the **prior** distribution
- $f(x) = \int f(x \mid \theta) f(\theta) d\theta$ is the **marginal likelihood** (evidence)

### In Generative Modeling

$$p(y \mid x) = \frac{p(x \mid y) p(y)}{p(x)}$$

Used in Naive Bayes classifiers: $p(y \mid x) \propto p(y) \prod_{i=1}^d p(x_i \mid y)$

## Law of Total Probability

### Discrete Form

For a partition $\{B_1, B_2, \dots\}$ of the sample space:
$$P(A) = \sum_i P(A \mid B_i) P(B_i)$$

### Continuous Form

$$f_X(x) = \int f_{X \mid Y}(x \mid y) f_Y(y) \, dy$$

### Law of Total Expectation (Tower Property)

$$E[Y] = E[E[Y \mid X]]$$

The inner expectation $E[Y \mid X]$ is a random variable (function of $X$). Its expectation recovers $E[Y]$.

### Law of Total Variance (Eve's Law)

$$\text{Var}(Y) = E[\text{Var}(Y \mid X)] + \text{Var}(E[Y \mid X])$$

This decomposes variance into "within-group" and "between-group" components. Used in ANOVA, random effects models, and Bayesian hierarchical models.

## Conditional Expectation

### Definition

For continuous variables:
$$E[Y \mid X = x] = \int y \, f_{Y \mid X}(y \mid x) \, dy$$

For discrete variables:
$$E[Y \mid X = x] = \sum_y y \, p_{Y \mid X}(y \mid x)$$

### Properties

1. $E[Y \mid X]$ minimizes $E[(Y - g(X))^2]$ over all measurable functions $g$ — it is the best predictor of $Y$ given $X$ under squared error loss.
2. $E[g(X)Y \mid X] = g(X) E[Y \mid X]$
3. If $X \perp Y$, then $E[Y \mid X] = E[Y]$ (and $E[X \mid Y] = E[X]$)
4. $E[E[Y \mid X] \mid X] = E[Y \mid X]$ (idempotent)

## Graphical Perspective

Conditional distributions can be visualized as slices of the joint distribution:

- For **discrete** case, fix $X = x$ and renormalize the column of the joint PMF.
- For **continuous** case, slice the joint PDF at $X = x$. The slice's shape is proportional to $f_{Y|X}(y|x)$, scaled by $1/f_X(x)$.

When $X$ and $Y$ are independent: $f_{Y|X}(y|x) = f_Y(y)$ for all $x$ — all slices look identical.

## Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# Bivariate normal example
mu = np.array([1.0, 2.0])
sigma = np.array([[2.0, 1.2], [1.2, 1.0]])

# Grid
x = np.linspace(-3, 5, 100)
y = np.linspace(-1, 5, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
rv = multivariate_normal(mu, sigma)

# Joint PDF
joint_pdf = rv.pdf(pos)

# Marginal of X
def marginal_x(x_val):
    return multivariate_normal(mu[0], sigma[0,0]).pdf(x_val)

# Conditional of Y | X = x0
def conditional_y_given_x(y_val, x0):
    mu_y_given_x = mu[1] + sigma[1,0] * (1/sigma[0,0]) * (x0 - mu[0])
    sigma_y_given_x = sigma[1,1] - sigma[1,0] * (1/sigma[0,0]) * sigma[0,1]
    return multivariate_normal(mu_y_given_x, sigma_y_given_x).pdf(y_val)

# Visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 1. Joint PDF
axes[0].contourf(X, Y, joint_pdf, levels=20, cmap='viridis')
axes[0].set_xlabel('X')
axes[0].set_ylabel('Y')
axes[0].set_title('Joint PDF f(x,y)')
axes[0].axvline(x=1.5, color='r', linestyle='--', lw=2)

# 2. Marginal of X
axes[1].plot(x, marginal_x(x), 'b-', lw=2)
axes[1].fill_between(x, marginal_x(x), alpha=0.3)
axes[1].set_xlabel('X')
axes[1].set_ylabel('f(x)')
axes[1].set_title('Marginal PDF f_X(x)')

# 3. Conditional of Y | X = 1.5
y_vals = np.linspace(-1, 5, 200)
cond_pdf = conditional_y_given_x(y_vals, 1.5)
axes[2].plot(y_vals, cond_pdf, 'r-', lw=2)
axes[2].fill_between(y_vals, cond_pdf, alpha=0.3)
axes[2].set_xlabel('Y')
axes[2].set_ylabel('f(y|x=1.5)')
axes[2].set_title('Conditional PDF f(y|x=1.5)')

plt.tight_layout()
plt.show()

# Verification of Law of Total Expectation
samples = rv.rvs(100000)
E_Y_given_X_approx = np.mean(samples[:, 1])  # E[Y]
E_EYgX = np.mean(
    mu[1] + sigma[1,0] * (1/sigma[0,0]) * (samples[:, 0] - mu[0])
)  # E[E[Y|X]]
print(f"E[Y] = {E_Y_given_X_approx:.4f}")
print(f"E[E[Y|X]] = {E_EYgX:.4f}")
print(f"Match: {np.isclose(E_Y_given_X_approx, E_EYgX, atol=0.1)}")
```

## Visualization

Create a three-panel figure: (1) contour plot of joint PDF with a vertical slice at $x = x_0$; (2) the marginal PDF $f_X(x)$ with a point at $x_0$; (3) the conditional PDF $f_{Y|X}(y|x_0)$ showing how it's a renormalized slice of the joint. The conditional mean $E[Y|X=x_0]$ is the regression line through the distribution's "ridge".

## Practical Considerations

- **Marginalization is expensive:** For $d$ variables each with $k$ values, marginalization costs $O(k^{d-1})$. This is why graphical models use structure to factorize the joint.
- **Conditioning can introduce dependence:** Two independent variables can become dependent when conditioning on a common effect (explaining away / Berkson's paradox).
- **Simpson's paradox:** Marginal and conditional associations can have opposite directions. Always consider confounding variables.
- **Regression as conditional expectation:** $E[Y|X]$ is the population regression function. Linear regression assumes this is linear in $X$.

## References

- Casella, G., & Berger, R. L. (2002). *Statistical Inference*
- Wasserman, L. (2004). *All of Statistics*
- Koller, D., & Friedman, N. (2009). *Probabilistic Graphical Models*
