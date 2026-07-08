# Phase 05 — Classical Machine Learning

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 05 — Classical Machine Learning |
| **Lessons** | 55 |
| **Core topics** | Linear/logistic regression, GLMs, Naive Bayes, LDA/QDA, decision trees, random forest, gradient boosting (XGBoost, LightGBM, CatBoost, Histogram GBM), SVM, kernel SVM, kNN, k-means, DBSCAN, GMM, hierarchical clustering, spectral clustering, PCA, t-SNE/UMAP, manifold learning, ICA, factor/CCA/PLS, Gaussian processes, Bayesian networks, HMM, CRF, MaxEnt, anomaly detection, learning to rank, online learning, bandits, active learning, semi-supervised, imbalanced learning, multi-label, multi-instance, calibration, conformal prediction, stacking, symbolic regression, Bayesian optimization, learning theory, PAC-Bayes, proper losses, model selection, association rules, subgroup discovery, rule learning, robust statistics, streaming, similarity learning, AutoML |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (SVD, eigenvalues, vector spaces), [Phase 02](../02-calculus-optimization/INDEX.md) (gradient descent, convexity), [Phase 03](../03-probability-statistics/INDEX.md) (MLE, distributions, hypothesis testing)
- **Python frameworks:** [`../../python-frameworks/scikit-learn/`](../../python-frameworks/scikit-learn/) (compare implementations)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Linear Regression | OLS, SGD, closed-form, assumptions | [lesson](lessons/01-linear-regression.md) | [code](code/01-linear-regression.py) | Used in: Phase 03 (linreg), Phase 11 (baseline models) |
| 02 | Logistic Regression | Binary/multinomial, cross-entropy, IRLS | [lesson](lessons/02-logistic-regression.md) | [code](code/02-logistic-regression.py) | Used in: Phase 06 (binary classification) |
| 03 | GLMs | Exponential family, link functions | [lesson](lessons/03-glms.md) | [code](code/03-glms.py) | Used in: Phase 03 (GLMs) |
| 04 | Naive Bayes | Gaussian, multinomial, Bernoulli | [lesson](lessons/04-naive-bayes.md) | [code](code/04-naive-bayes.py) | Used in: Phase 09 (text classification) |
| 05 | LDA / QDA | Linear/quadratic discriminant analysis | [lesson](lessons/05-lda-qda.md) | [code](code/05-lda-qda.py) | Used in: Phase 08 (feature extraction) |
| 06 | Decision Trees | CART, ID3, C4.5, pruning | [lesson](lessons/06-decision-trees.md) | [code](code/06-decision-trees.py) | Used in: Phase 05 (ensemble base) |
| 07 | Random Forest | Bagging, feature subsampling, OOB | [lesson](lessons/07-random-forest.md) | [code](code/07-random-forest.py) | Used in: Phase 11 (baseline) |
| 08 | Gradient Boosting | Boosting, forward stagewise, trees | [lesson](lessons/08-gradient-boosting.md) | [code](code/08-gradient-boosting.py) | Used in: Phase 11 (production models) |
| 09 | XGBoost | Regularized boosting, sparsity-aware | [lesson](lessons/09-xgboost.md) | [code](code/09-xgboost.py) | Used in: Phase 11 (tuning) |
| 10 | LightGBM | GOSS, EFB, leaf-wise growth | [lesson](lessons/10-lightgbm.md) | [code](code/10-lightgbm.py) | Used in: Phase 11 (efficiency) |
| 11 | CatBoost | Ordered boosting, categorical features | [lesson](lessons/11-catboost.md) | [code](code/11-catboost.py) | Used in: Phase 11 (tabular data) |
| 12 | Histogram GBM | Binning, histogram splits | [lesson](lessons/12-histogram-gbm.md) | [code](code/12-histogram-gbm.py) | Used in: Phase 11 (large-scale) |
| 13 | SVM | Max-margin, dual, support vectors | [lesson](lessons/13-svm.md) | [code](code/13-svm.py) | Used in: Phase 04 (RKHS) |
| 14 | Kernel SVM | Kernel trick, RBF, polynomial | [lesson](lessons/14-kernel-svm.md) | [code](code/14-kernel-svm.py) | Used in: Phase 04 (kernel methods) |
| 15 | kNN | Distance metrics, curse of dimensionality | [lesson](lessons/15-knn.md) | [code](code/15-knn.py) | Used in: Phase 09 (retrieval) |
| 16 | k-Means | Lloyd, k-means++, inertia | [lesson](lessons/16-kmeans.md) | [code](code/16-kmeans.py) | Used in: Phase 08 (segmentation) |
| 17 | DBSCAN | Density-based, eps, minPts | [lesson](lessons/17-dbscan.md) | [code](code/17-dbscan.py) | Used in: Phase 08 (point clouds) |
| 18 | GMM | EM algorithm, mixtures of Gaussians | [lesson](lessons/18-gmm.md) | [code](code/18-gmm.py) | Used in: Phase 07 (VAEs) |
| 19 | Hierarchical Clustering | Agglomerative, dendrograms, linkage | [lesson](lessons/19-hierarchical.md) | [code](code/19-hierarchical.py) | Used in: Phase 09 (topic clustering) |
| 20 | Spectral Clustering | Graph Laplacian, eigen-gap | [lesson](lessons/20-spectral.md) | [code](code/20-spectral.py) | Used in: Phase 01 (graph Laplacians) |
| 21 | PCA | Maximum variance, SVD, explained variance | [lesson](lessons/21-pca.md) | [code](code/21-pca.py) | Used in: Phase 08 (dim reduction), Phase 09 (embeddings) |
| 22 | t-SNE / UMAP | Non-linear dim reduction, manifolds | [lesson](lessons/22-tsne-umap.md) | [code](code/22-tsne-umap.py) | Used in: Phase 08 (visualization) |
| 23 | Manifold Learning | Isomap, LLE, MDS, Laplacian eigenmaps | [lesson](lessons/23-manifold.md) | [code](code/23-manifold.py) | Used in: Phase 07 (manifold hypothesis) |
| 24 | ICA | Independent component analysis, FastICA | [lesson](lessons/24-ica.md) | [code](code/24-ica.py) | Used in: Phase 08 (blind source separation) |
| 25 | Factor / CCA / PLS | Factor analysis, CCA, partial least squares | [lesson](lessons/25-factor-cca-pls.md) | [code](code/25-factor-cca-pls.py) | Used in: Phase 03 (multivariate methods) |
| 26 | Gaussian Processes | GP regression, kernel, marginal likelihood | [lesson](lessons/26-gp.md) | [code](code/26-gp.py) | Used in: Phase 02 (Bayesian opt), Phase 12 |
| 27 | Bayesian Networks | DAGs, d-separation, structure learning | [lesson](lessons/27-bayesian-networks.md) | [code](code/27-bayesian-networks.py) | Used in: Phase 09 (causal NLP) |
| 28 | HMM | Hidden Markov models, Viterbi, Baum–Welch | [lesson](lessons/28-hmm.md) | [code](code/28-hmm.py) | Used in: Phase 09 (speech), Phase 10 (RL) |
| 29 | CRF | Conditional random fields, chain CRF | [lesson](lessons/29-crf.md) | [code](code/29-crf.py) | Used in: Phase 09 (NER, sequence labeling) |
| 30 | MaxEnt | Maximum entropy classification | [lesson](lessons/30-maxent.md) | [code](code/30-maxent.py) | Used in: Phase 04 (MaxEnt), Phase 09 |
| 31 | Anomaly Detection | Isolation forest, LOF, one-class SVM | [lesson](lessons/31-anomaly.md) | [code](code/31-anomaly.py) | Used in: Phase 11 (monitoring) |
| 32 | Learning to Rank | Pointwise, pairwise, listwise | [lesson](lessons/32-learning-to-rank.md) | [code](code/32-learning-to-rank.py) | Used in: Phase 09 (information retrieval) |
| 33 | Online Learning | Regret, experts, Follow-the-Regularized-Leader | [lesson](lessons/33-online-learning.md) | [code](code/33-online-learning.py) | Used in: Phase 11 (continual training) |
| 34 | Bandits | Epsilon-greedy, UCB, Thompson sampling | [lesson](lessons/34-bandits.md) | [code](code/34-bandits.py) | Used in: Phase 10 (exploration), Phase 11 (A/B) |
| 35 | Active Learning | Uncertainty, query-by-committee, expected info gain | [lesson](lessons/35-active-learning.md) | [code](code/35-active-learning.py) | Used in: Phase 11 (data labeling) |
| 36 | Semi-Supervised | Self-training, consistency, pseudo-label | [lesson](lessons/36-semi-supervised.md) | [code](code/36-semi-supervised.py) | Used in: Phase 06 (SSL), Phase 08 (vision SSL) |
| 37 | Imbalanced Learning | SMOTE, cost-sensitive, focal loss | [lesson](lessons/37-imbalanced.md) | [code](code/37-imbalanced.py) | Used in: Phase 06 (focal loss), Phase 11 |
| 38 | Multi-Label | Binary relevance, label powerset, chain | [lesson](lessons/38-multi-label.md) | [code](code/38-multi-label.py) | Used in: Phase 08 (multi-label vision) |
| 39 | Multi-Instance | Bag-level, attention pooling, MIL | [lesson](lessons/39-multi-instance.md) | [code](code/39-multi-instance.py) | Used in: Phase 08 (medical imaging) |
| 40 | Calibration | Platt scaling, isotonic regression, temperature | [lesson](lessons/40-calibration.md) | [code](code/40-calibration.py) | Used in: Phase 06 (NN calibration) |
| 41 | Conformal Prediction | Prediction sets, conformal coverage | [lesson](lessons/41-conformal.md) | [code](code/41-conformal.py) | Used in: Phase 06 (uncertainty) |
| 42 | Stacking | Blending, stacked generalization | [lesson](lessons/42-stacking.md) | [code](code/42-stacking.py) | Used in: Phase 12 (ensemble systems) |
| 43 | Symbolic Regression | GP-based, genetic programming | [lesson](lessons/43-symbolic-regression.md) | [code](code/43-symbolic-regression.py) | Used in: Phase 07 (differentiable prog) |
| 44 | Bayesian Optimization | GP-based, acquisition functions | [lesson](lessons/44-bayesian-opt.md) | [code](code/44-bayesian-opt.py) | Used in: Phase 11 (hyperparam tuning) |
| 45 | Learning Theory | PAC, sample complexity, VC dimension | [lesson](lessons/45-learning-theory.md) | [code](code/45-learning-theory.py) | Used in: Phase 06 (generalization) |
| 46 | PAC-Bayes | PAC-Bayesian bounds, posterior | [lesson](lessons/46-pac-bayes.md) | [code](code/46-pac-bayes.py) | Used in: Phase 06 (Bayesian deep learning) |
| 47 | Proper Losses | Strict properness, classification-calibration | [lesson](lessons/47-proper-losses.md) | [code](code/47-proper-losses.py) | Used in: Phase 06 (loss design) |
| 48 | Model Selection | Cross-validation, AIC/BIC, MDL | [lesson](lessons/48-model-selection.md) | [code](code/48-model-selection.py) | Used in: Phase 11 (model registry) |
| 49 | Association Rules | Apriori, FP-growth, lift | [lesson](lessons/49-association-rules.md) | [code](code/49-association-rules.py) | Used in: Phase 09 (recommendations) |
| 50 | Subgroup Discovery | SD, beam search, quality measures | [lesson](lessons/50-subgroup-discovery.md) | [code](code/50-subgroup-discovery.py) | Used in: Phase 11 (explainability) |
| 51 | Rule Learning | RIPPER, CN2, OneR | [lesson](lessons/51-rule-learning.md) | [code](code/51-rule-learning.py) | Used in: Phase 07 (neuro-symbolic) |
| 52 | Robust Statistics | M-estimators, breakdown point, Huber | [lesson](lessons/52-robust-statistics.md) | [code](code/52-robust-statistics.py) | Used in: Phase 06 (robust training) |
| 53 | Streaming | Data streams, sampling, sketching | [lesson](lessons/53-streaming.md) | [code](code/53-streaming.py) | Used in: Phase 11 (data pipelines) |
| 54 | Similarity Learning | Siamese, triplet, contrastive loss | [lesson](lessons/54-similarity.md) | [code](code/54-similarity.py) | Used in: Phase 08 (face recog), Phase 09 (embeddings) |
| 55 | AutoML | NAS, hyperopt, meta-learning | [lesson](lessons/55-automl.md) | [code](code/55-automl.py) | Used in: Phase 12 (AutoML system) |

## 4. Builds Toward

- **Phase 06** (MLPs, loss functions, regularization — classical concepts extended to deep)
- **Phase 08** (PCA/SVD for vision, clustering for segmentation)
- **Phase 09** (Naive Bayes, HMM, CRF for NLP; ranking for IR)
- **Phase 10** (bandits for exploration, learning theory for RL)
- **Phase 11** (model baselines, A/B testing, AutoML, experiment tracking)
- **Phase 12** (ensemble capstone, AutoML system, monitoring)

## 5. Quick Start

```bash
python3 code/01-linear-regression.py
```
