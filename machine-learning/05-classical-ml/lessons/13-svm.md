# Lesson 05.13: SVM (Primal, Dual, SMO)

## Learning Objectives
- Derive SVM from maximum margin principle
- Understand primal, dual, and kernel formulations
- Implement SMO (Sequential Minimal Optimization)
- Apply KKT conditions for convergence checking

## Maximum Margin Classifier
For linearly separable data, SVM finds the hyperplane maximizing the margin (distance to nearest points):

$$\min_{w,b} \frac12 \|w\|^2 \quad \text{s.t.} \quad y_i(w^\top x_i + b) \geq 1, \forall i$$

The margin width is $2/\|w\|$. The support vectors are points with $y_i(w^\top x_i + b) = 1$.

## Soft Margin SVM
For non-separable data, introduce slack variables $\xi_i$:

$$\min_{w,b,\xi} \frac12 \|w\|^2 + C \sum_{i=1}^n \xi_i$$

$$\text{s.t.} \quad y_i(w^\top x_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0$$

$C$ controls the tradeoff: large $C$ = narrow margin (hard margin, overfitting), small $C$ = wide margin (softer, underfitting).

## Dual Formulation
Using Lagrange multipliers $\alpha_i \geq 0$:

$$\max_\alpha \sum_{i=1}^n \alpha_i - \frac12 \sum_{i,j=1}^n \alpha_i \alpha_j y_i y_j x_i^\top x_j$$

$$\text{s.t.} \quad 0 \leq \alpha_i \leq C, \quad \sum_{i=1}^n \alpha_i y_i = 0$$

Decision function: $f(x) = \sum_{i=1}^n \alpha_i y_i x_i^\top x + b$

Only support vectors ($\alpha_i > 0$) contribute to the decision function, making SVM sparse.

## KKT Conditions
At optimal solution:
- $\alpha_i = 0 \implies y_i f(x_i) \geq 1$ (correctly classified, outside margin)
- $0 < \alpha_i < C \implies y_i f(x_i) = 1$ (on margin — free support vectors)
- $\alpha_i = C \implies y_i f(x_i) \leq 1$ (within margin or misclassified — bounded support vectors)

### Bias $b$ from KKT
For any $i$ with $0 < \alpha_i < C$: $b = y_i - \sum_{j} \alpha_j y_j x_j^\top x_i$

## SMO (Sequential Minimal Optimization)
Solve dual by updating two $\alpha$'s at a time:

1. **Select working set**: Find pair $(\alpha_i, \alpha_j)$ violating KKT conditions
   - First choice: maximal violation of KKT
   - Second choice: maximize step size
2. **Analytical solution** for 2-variable constrained QP:
   - $\alpha_j^{\text{new}} = \alpha_j^{\text{old}} + \frac{y_j(E_i - E_j)}{\eta}$ where $E_i = f(x_i) - y_i$ and $\eta = K(x_i, x_i) + K(x_j, x_j) - 2K(x_i, x_j)$
   - Clip to bounds: $L \leq \alpha_j^{\text{new}} \leq H$
   - Recover $\alpha_i$ from $\alpha_i + \alpha_j = \text{constant}$
3. **Update bias $b$**: using KKT conditions for the two updated alphas

## Code: Simplified SMO

```python
import numpy as np

class SVM:
    def __init__(self, C=1.0, kernel='linear', tol=1e-3, max_iter=100):
        self.C = C
        self.kernel = kernel
        self.tol = tol
        self.max_iter = max_iter

    def _K(self, x1, x2):
        if self.kernel == 'linear':
            return x1 @ x2
        elif self.kernel == 'rbf':
            return np.exp(-self.gamma * np.sum((x1 - x2)**2))

    def fit(self, X, y):
        n, d = X.shape
        self.X, self.y = X, y
        self.alpha = np.zeros(n)
        self.b = 0.0
        self.E = -y.copy()
        passes = 0
        while passes < self.max_iter:
            num_changed = 0
            for i in range(n):
                E_i = self._decision(X[i]) - y[i]
                if (y[i] * E_i < -self.tol and self.alpha[i] < self.C) or \
                   (y[i] * E_i > self.tol and self.alpha[i] > 0):
                    j = np.random.choice([x for x in range(n) if x != i])
                    E_j = self._decision(X[j]) - y[j]
                    alpha_i_old, alpha_j_old = self.alpha[i], self.alpha[j]
                    if y[i] != y[j]:
                        L = max(0, self.alpha[j] - self.alpha[i])
                        H = min(self.C, self.C + self.alpha[j] - self.alpha[i])
                    else:
                        L = max(0, self.alpha[i] + self.alpha[j] - self.C)
                        H = min(self.C, self.alpha[i] + self.alpha[j])
                    if L == H: continue
                    eta = 2 * self._K(X[i], X[j]) - self._K(X[i], X[i]) - self._K(X[j], X[j])
                    if eta >= 0: continue
                    self.alpha[j] -= y[j] * (E_i - E_j) / eta
                    self.alpha[j] = np.clip(self.alpha[j], L, H)
                    if abs(self.alpha[j] - alpha_j_old) < 1e-5: continue
                    self.alpha[i] += y[i] * y[j] * (alpha_j_old - self.alpha[j])
                    b1 = self.b - E_i - y[i]*(self.alpha[i]-alpha_i_old)*self._K(X[i],X[i]) - y[j]*(self.alpha[j]-alpha_j_old)*self._K(X[i],X[j])
                    b2 = self.b - E_j - y[i]*(self.alpha[i]-alpha_i_old)*self._K(X[i],X[j]) - y[j]*(self.alpha[j]-alpha_j_old)*self._K(X[j],X[j])
                    self.b = (b1 + b2) / 2
                    num_changed += 1
            passes = passes + 1 if num_changed == 0 else 0

    def _decision(self, x):
        return np.sum(self.alpha * self.y * np.array([self._K(self.X[i], x) for i in range(len(self.y))])) + self.b
```

## Practical Considerations
- **Feature scaling**: Essential for SVM (especially RBF kernel); normalize to zero mean, unit variance
- **Choice of $C$**: Grid search on log scale ($2^{-5}, 2^{-3}, \dots, 2^{15}$)
- **Large $n$**: Use LibLinear (linear SVM with $O(n)$) instead of LibSVM ($O(n^2)$-$O(n^3)$)
- **Large $d$**: Linear kernel often sufficient and much faster
- **Support vectors**: SVs fraction indicates problem difficulty; near 1 means poor fit
- **Probability estimates**: Platt scaling needed (adds calibration layer)

## Key Properties
- Primal: $O(nd)$ per iteration (suitable for large $n$, use SGD)
- Dual: $O(n^2)$ to $O(n^3)$ (suitable for high $d$)
- SMO: $O(n^2)$ to $O(n^3)$ in practice, but fast for moderate $n$ ($n < 10^5$)
- Support vectors determine the model — sparse solution
- Maximum margin principle provides strong theoretical guarantees

## References
- Cortes & Vapnik, "Support-Vector Networks" (Machine Learning, 1995)
- Platt, "Sequential Minimal Optimization: A Fast Algorithm for Training SVMs" (1998)
- Christianini & Shawe-Taylor, "An Introduction to Support Vector Machines"
- Hastie et al., "ESL", Ch. 12
