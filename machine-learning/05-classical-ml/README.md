# Phase 05: Classical Machine Learning — Every Algorithm from Scratch

Build every major classical ML algorithm from first principles using NumPy/SciPy. Each lesson includes a mathematical derivation, a from-scratch implementation, and a comparison against scikit-learn.

## Lesson Table

| # | Topic | Code | Key Concepts |
|---|-------|------|-------------|
| 01 | Linear Regression (OLS, Ridge, Lasso, ElasticNet) | [code/01-linear-regression.py](code/01-linear-regression.py) | Normal equation, gradient descent, L1/L2 regularization, coordinate descent |
| 02 | Logistic Regression | [code/02-logistic-regression.py](code/02-logistic-regression.py) | Sigmoid, cross-entropy, Newton-Raphson, multinomial |
| 03 | Generalized Linear Models | [code/03-glms.py](code/03-glms.py) | Exponential family, link functions, IRLS, Poisson/Bernoulli |
| 04 | Naive Bayes | [code/04-naive-bayes.py](code/04-naive-bayes.py) | Bayes rule, Gaussian/Multinomial/Bernoulli, log-space |
| 05 | LDA / QDA | [code/05-lda-qda.py](code/05-lda-qda.py) | Bayes classifier, quadratic discriminant, covariance pooling |
| 06 | Decision Trees (CART, ID3, C4.5) | [code/06-decision-trees.py](code/06-decision-trees.py) | Information gain, Gini, pruning, categorical splits |
| 07 | Random Forest | [code/07-random-forest.py](code/07-random-forest.py) | Bagging, random subspace, OOB error, feature importance |
| 08 | Gradient Boosting | [code/08-gradient-boosting.py](code/08-gradient-boosting.py) | Stagewise additive, pseudo-residuals, shrinkage |
| 09 | XGBoost | [code/09-xgboost.py](code/09-xgboost.py) | Newton boosting, quantile sketch, column block, sparsity |
| 10 | LightGBM | [code/10-lightgbm.py](code/10-lightgbm.py) | GOSS, EFB, leaf-wise tree, histograms |
| 11 | CatBoost | [code/11-catboost.py](code/11-catboost.py) | Ordered boosting, categorical encoding, symmetric trees |
| 12 | Histogram-based GBM | [code/12-histogram-gbm.py](code/12-histogram-gbm.py) | Binning, gradient histograms, bin splitting |
| 13 | SVM (Primal, Dual, SMO) | [code/13-svm.py](code/13-svm.py) | Hinge loss, dual, KKT, SMO algorithm |
| 14 | Kernel SVM | [code/14-kernel-svm.py](code/14-kernel-svm.py) | Kernel trick, RBF/poly/sigmoid, representer theorem |
| 15 | k-Nearest Neighbors | [code/15-knn.py](code/15-knn.py) | Brute force, KD-tree, Ball tree, distance weighting |
| 16 | k-Means Clustering | [code/16-kmeans.py](code/16-kmeans.py) | Lloyd, MacQueen, k-Means++, inertia, elbow |
| 17 | DBSCAN / HDBSCAN / OPTICS | [code/17-dbscan.py](code/17-dbscan.py) | Eps-neighborhood, core points, reachability, hierarchy |
| 18 | Gaussian Mixture Models | [code/18-gmm.py](code/18-gmm.py) | EM algorithm, variational inference, BIC |
| 19 | Hierarchical Clustering | [code/19-hierarchical.py](code/19-hierarchical.py) | Single/average/complete linkage, dendrogram, agglomerative |
| 20 | Spectral Clustering | [code/20-spectral.py](code/20-spectral.py) | Graph Laplacian, normalized cuts, eigenmaps |
| 21 | PCA (Kernel, Sparse, Robust) | [code/21-pca.py](code/21-pca.py) | SVD, explained variance, kernel PCA, SPCA, RPCA |
| 22 | t-SNE / UMAP / LargeVis | [code/22-tsne-umap.py](code/22-tsne-umap.py) | SNE, perplexity, KL divergence, neighbor graphs |
| 23 | Isomap / LLE / Laplacian Eigenmaps | [code/23-manifold.py](code/23-manifold.py) | Geodesic distances, barycentric, graph embedding |
| 24 | ICA (FastICA, Infomax) | [code/24-ica.py](code/24-ica.py) | Non-Gaussianity, negentropy, kurtosis, fixed-point |
| 25 | Factor Analysis / CCA / PLS | [code/25-factor-cca-pls.py](code/25-factor-cca-pls.py) | Latent factors, canonical correlation, PLS regression |
| 26 | Gaussian Processes | [code/26-gp.py](code/26-gp.py) | Kernels, posterior, Cholesky, hyperparameter learning |
| 27 | Bayesian Networks | [code/27-bayesian-networks.py](code/27-bayesian-networks.py) | DAGs, conditional independence, structure learning |
| 28 | Hidden Markov Models | [code/28-hmm.py](code/28-hmm.py) | Forward-backward, Viterbi, Baum-Welch |
| 29 | Conditional Random Fields | [code/29-crf.py](code/29-crf.py) | Log-linear, feature functions, L-BFGS, inference |
| 30 | Maximum Entropy Models | [code/30-maxent.py](code/30-maxent.py) | MaxEnt principle, GIS, IIS, feature expectations |
| 31 | Anomaly Detection | [code/31-anomaly.py](code/31-anomaly.py) | Isolation Forest, LOF, One-Class SVM, Elliptic Envelope |
| 32 | Learning to Rank | [code/32-learning-to-rank.py](code/32-learning-to-rank.py) | Pairwise, listwise, NDCG, RankNet, LambdaRank |
| 33 | Online Learning | [code/33-online-learning.py](code/33-online-learning.py) | Perceptron, PA, SGD, OGD, follow-the-leader |
| 34 | Bandit Algorithms | [code/34-bandits.py](code/34-bandits.py) | UCB, Thompson sampling, epsilon-greedy, EXP3 |
| 35 | Active Learning | [code/35-active-learning.py](code/35-active-learning.py) | Uncertainty sampling, query-by-committee, expected error |
| 36 | Semi-Supervised Learning | [code/36-semi-supervised.py](code/36-semi-supervised.py) | Self-training, co-training, label propagation, TSVM |
| 37 | Imbalanced Learning | [code/37-imbalanced.py](code/37-imbalanced.py) | SMOTE, ADASYN, Tomek links, cost-sensitive, EasyEnsemble |
| 38 | Multi-Label Learning | [code/38-multi-label.py](code/38-multi-label.py) | Binary relevance, classifier chains, LP, RAKEL |
| 39 | Multi-Instance / Multi-Output | [code/39-multi-instance.py](code/39-multi-instance.py) | MI assumption, DD, APR, multi-output regression |
| 40 | Probability Calibration | [code/40-calibration.py](code/40-calibration.py) | Platt scaling, isotonic regression, reliability curves |
| 41 | Conformal Prediction | [code/41-conformal.py](code/41-conformal.py) | Nonconformity, p-values, inductive/transductive, CP |
| 42 | Stacking / Blending | [code/42-stacking.py](code/42-stacking.py) | Meta-learners, CV stacking, feature-weighted stacking |
| 43 | Symbolic Regression | [code/43-symbolic-regression.py](code/43-symbolic-regression.py) | Genetic programming, expression trees, Pareto frontier |
| 44 | Bayesian Optimization | [code/44-bayesian-opt.py](code/44-bayesian-opt.py) | GP surrogate, EI, UCB, Thompson sampling, PoI |
| 45 | Learning Theory (VC / PAC) | [code/45-learning-theory.py](code/45-learning-theory.py) | VC dimension, PAC bound, SRM, concentration |
| 46 | PAC-Bayes | [code/46-pac-bayes.py](code/46-pac-bayes.py) | Gibbs classifier, KL divergence, posterior bound |
| 47 | Proper Loss Functions | [code/47-proper-losses.py](code/47-proper-losses.py) | Brier, log-loss, hinge, composite, classification calibration |
| 48 | Model Selection (AIC / BIC) | [code/48-model-selection.py](code/48-model-selection.py) | Likelihood, complexity penalty, MDL, CV comparison |
| 49 | Association Rules (Apriori, FP-Growth) | [code/49-association-rules.py](code/49-association-rules.py) | Support, confidence, lift, FP-tree, frequent itemsets |
| 50 | Subgroup Discovery | [code/50-subgroup-discovery.py](code/50-subgroup-discovery.py) | Exceptional model mining, quality measures, SD-Map |
| 51 | Rule Learning (CN2, RIPPER) | [code/51-rule-learning.py](code/51-rule-learning.py) | Separate-and-conquer, sequential covering, pruning |
| 52 | Robust Statistics | [code/52-robust-statistics.py](code/52-robust-statistics.py) | M-estimators, Huber, Tukey, breakdown point, median polish |
| 53 | Streaming Algorithms | [code/53-streaming.py](code/53-streaming.py) | Reservoir sampling, Count-Min Sketch, Bloom filter, HyperLogLog |
| 54 | Similarity / Distance Measures | [code/54-similarity.py](code/54-similarity.py) | Mahalanobis, DTW, edit distance, kernel alignment |
| 55 | Full AutoML Pipeline | [code/55-automl.py](code/55-automl.py) | CASH, meta-learning, hyperopt, pipeline synthesis |

## Usage

```bash
# Run any lesson
python code/01-linear-regression.py

# Study the theory
cat lessons/01-linear-regression.md

# Practice
python practice/phase05-exercises.py
```

All code is standalone. Each file depends only on `numpy`, `scipy`, `matplotlib`, and optionally `sklearn` for comparison.
