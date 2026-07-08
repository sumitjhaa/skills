# Lesson 05.37: Imbalanced Learning

## Learning Objectives
- Understand data-level, algorithm-level, and ensemble approaches
- Implement SMOTE and its variants
- Apply cost-sensitive learning to any classifier
- Evaluate with precision-recall and ROC curves

## Problem
Class imbalance: one class (minority) has far fewer examples than another (majority).

**Ratio**: $r = n_{\text{majority}} / n_{\text{minority}}$. Standard classifiers optimize accuracy → biased toward majority.

## Resampling

### Oversampling (Increase Minority)

**SMOTE (Synthetic Minority Oversampling TEchnique)**:
1. For minority sample $x_i$, find $k$ nearest neighbors (same class)
2. Pick random neighbor $x_j$
3. Generate: $x_{\text{new}} = x_i + \lambda (x_j - x_i)$, $\lambda \sim U(0, 1)$

**SMOTE variants**:
- **Borderline-SMOTE**: Only oversample minority points near decision boundary
- **ADASYN**: Adaptively generate more samples for harder-to-learn minority points
- **SVMSMOTE**: Use support vectors to guide synthesis

### Undersampling (Reduce Majority)
- **Random**: Remove majority samples (loses information)
- **Tomek Links**: Remove majority point if it forms a Tomek link (nearest neighbors of opposite class)
- **Edited Nearest Neighbors (ENN)**: Remove sample if misclassified by 3-NN
- **Near Miss**: Select majority points close to minority points
- **Cluster Centroids**: Cluster majority, replace with centroids

### Hybrid Methods
- **SMOTE + Tomek**: Oversample then clean noisy samples
- **SMOTE + ENN**: Oversample then edit noisy samples
- **EasyEnsemble**: Multiple undersampled datasets, each trains a classifier, ensemble

## Cost-Sensitive Learning

### Weighted Loss
Assign higher misclassification cost to minority class:

$$\text{Loss} = \sum_i w_{y_i} \cdot L(y_i, \hat{y}_i)$$

Weights: $w_{\text{minority}} = \frac{n_{\text{majority}}}{n_{\text{minority}}}$, $w_{\text{majority}} = 1$

### Class Imbalance in Specific Algorithms
- **SVM**: Different $C$ per class: $C_{\text{minority}} = r \cdot C_{\text{majority}}$
- **Trees**: Adjust class weights in impurity calculations
- **Logistic regression**: Weighted gradient: multiply loss by class weight
- **Neural networks**: Weighted cross-entropy loss

### Threshold Moving
After training, adjust decision threshold:

$$P(y=1|x) > \frac{\pi_{\text{majority}}}{\pi_{\text{minority}}} \cdot \frac{C_{\text{FN}}}{C_{\text{FP}}}$$

## Ensemble Methods

### RUSBoost
1. Random undersample to balance classes
2. Train AdaBoost on balanced set
3. Repeat, combine via weighted ensemble

### Balanced Random Forest
- Bootstrap balanced samples (equal majority/minority per tree)
- Each tree sees balanced training set
- Usually outperforms SMOTE + RF

### EasyEnsemble
- Create $T$ subsets, each with all minority + random majority
- Train classifier on each subset
- Average predictions

## Code: SMOTE

```python
import numpy as np
from sklearn.neighbors import NearestNeighbors

def SMOTE(X_min, n_synthetic, k=5):
    n, d = X_min.shape
    nn = NearestNeighbors(n_neighbors=k).fit(X_min)
    X_new = []
    for _ in range(n_synthetic):
        i = np.random.randint(n)
        neighbors = nn.kneighbors(X_min[i:i+1], return_distance=False)[0]
        j = np.random.choice(neighbors)
        lam = np.random.random()
        X_new.append(X_min[i] + lam * (X_min[j] - X_min[i]))
    return np.array(X_new)
```

## Evaluation Metrics

| Metric | Formula | When to use |
|--------|---------|-------------|
| Accuracy | (TP+TN)/(TP+FP+TN+FN) | Never for imbalanced |
| Precision | TP/(TP+FP) | When FP cost high |
| Recall (TPR) | TP/(TP+FN) | When FN cost high |
| F1 Score | 2·P·R/(P+R) | Harmonic mean |
| G-Mean | $\sqrt{\text{TPR} \cdot \text{TNR}}$ | Balance |
| AUC-ROC | Area under TPR vs FPR | Ranking overall |
| AUC-PR | Area under Precision-Recall | Imbalanced benchmark |
| Cohen's Kappa | $\frac{p_o - p_e}{1 - p_e}$ | Chance-adjusted agreement |

**Important**: Use stratified cross-validation to preserve class proportions.

## Practical Considerations
- **SMOTE limitations**: Creates synthetic noise near boundaries, doesn't handle high-dimensional data well
- **Algorithm-level often better than data-level**: Use class weights before resampling
- **Calibration**: Oversampling distorts probabilities — calibrate after resampling
- **Extreme imbalance ($r > 1000$)**: Use anomaly detection (Isolation Forest, OCSVM) instead
- **Ensemble + resampling**: Often produces best results
- **Multi-class imbalance**: Use per-class weights or one-vs-rest with threshold tuning

## References
- Chawla et al., "SMOTE: Synthetic Minority Over-sampling Technique" (JAIR, 2002)
- He & Garcia, "Learning from Imbalanced Data" (IEEE TKDE, 2009)
- Seiffert et al., "RUSBoost: A Hybrid Approach to Alleviating Class Imbalance" (IEEE SMC, 2010)
- Chen, Liaw, Breiman, "Using Random Forest to Learn Imbalanced Data" (Technical Report, 2004)
- Batista, Prati, Monard, "A Study of the Behavior of Several Methods for Balancing Machine Learning Training Data" (SIGKDD Explorations, 2004)
