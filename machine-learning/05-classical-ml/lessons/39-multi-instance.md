# Lesson 05.39: Multi-Instance / Multi-Output

## Learning Objectives
- Understand multi-instance learning (bag-level classification)
- Implement diverse density and axis-parallel rectangle methods
- Apply multi-output regression with output correlation
- Distinguish MIL assumptions (standard, count-based, threshold)

## Multi-Instance Learning (MIL)
**Setup**: Data organized into bags $B = \{x_1, \dots, x_m\}$, label $y_B \in \{0, 1\}$.

**Standard MIL assumption**: Bag is positive iff at least one instance is positive.

MIL arises naturally in:
- Drug discovery: molecule activity (conformation determines activity)
- Image classification: image positive if contains target object
- Text classification: document positive if contains relevant passage

### Diverse Density (DD)
Find a point $t$ in instance space that is "dense" in positive bags and "sparse" in negative bags:

$$\max_t DD(t) = \prod_i P(B_i^+ | t) \cdot \prod_i P(B_i^- | t)$$

$$P(B^+ | t) \propto 1 - \prod_j (1 - \exp(-\|x_{ij} - t\|^2 / \sigma^2))$$

$$P(B^- | t) \propto \prod_j (1 - \exp(-\|x_{ij} - t\|^2 / \sigma^2))$$

Optimization via gradient ascent from multiple starting points.

### Axis-Parallel Rectangle (APR)
Learn hyper-rectangle covering positive instances:
1. Start with a positive instance's feature values
2. Iteratively shrink rectangle boundaries to exclude negative instances
3. Classify bag positive if any instance falls inside rectangle

### MIL Approaches

**Instance-space methods**:
- Classify each instance independently
- Aggregate: max of instance scores (standard MIL), average, or threshold
- Example: MI-SVM, MIL logistic regression

**Embedding-space methods**:
- Convert bag to fixed-length feature vector
- Bag-level features: statistics of instance predictions (mean, max, min, variance)
- Train standard classifier on bag features

**Bag-space methods**:
- Define kernel between bags: $K(B_i, B_j) = \sum_{p} \sum_{q} k(x_{ip}, x_{jq})$ (set kernel)
- Train SVM on bag-kernel matrix

## Multi-Output Regression
Predict multiple continuous targets $y \in \mathbb{R}^L$:

### Problem Transformation
- **Single-target**: Train $L$ independent regressors
- **Multi-target regressor stack**: Chain targets (include previous target predictions as features)
- **PLS, CCA**: Capture output correlations via latent components

### Algorithm Adaptation
- **Multi-output RF**: Trees predict output vector (mean per leaf)
- **Multi-output GP**: Coregionalization kernels: $K((x, i), (x', j)) = k_x(x, x') \cdot k_t(i, j)$
- **Multi-output Neural Nets**: $L$ output units with MSE loss

### Evaluation
- **Average RMSE**: $\sqrt{\frac{1}{L} \sum_{j=1}^L (y_{ij} - \hat{y}_{ij})^2}$
- **Relative RMSE**: Normalized per target
- **Improvement over mean**: $1 - \text{RMSE} / \text{RMSE}_{\text{mean}}$

## Code: MI-SVM using Instance Max

```python
import numpy as np
from sklearn.svm import SVC

class MISVM:
    def __init__(self, kernel='rbf', C=1.0):
        self.svm = SVC(kernel=kernel, C=C, probability=True)

    def fit(self, bags, y):
        # Flatten bags to instances
        X_inst = np.vstack(bags)
        y_inst = np.repeat(y, [len(b) for b in bags])
        self.svm.fit(X_inst, y_inst)

    def predict_bag(self, bag):
        probs = self.svm.predict_proba(bag)[:, 1]
        return 1 if np.max(probs) > 0.5 else 0
```

## Key Points
- MIL used in drug discovery (molecule activity), image classification, text categorization
- Standard assumption: bag positive iff at least one positive instance
- Other assumptions: count-based (need $k$ positive instances), threshold-based
- Single-target baseline often strong for multi-output regression
- Output correlation modeling helps when targets are strongly related

## References
- Dietterich, Lathrop, Lozano-Pérez, "Solving the Multiple Instance Problem with Axis-Parallel Rectangles" (Artificial Intelligence, 1997)
- Maron & Lozano-Pérez, "A Framework for Multiple-Instance Learning" (NIPS 1997)
- Andrews, Tsochantaridis, Hofmann, "Support Vector Machines for Multiple-Instance Learning" (NIPS 2002)
- Borchani, Varando, Bielza, Larrañaga, "A Survey on Multi-Output Regression" (WIREs Data Mining, 2015)
- Zhou, "Multi-Instance Learning: A Survey" (Technical Report, 2004)
