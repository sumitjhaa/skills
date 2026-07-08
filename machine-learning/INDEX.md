# Machine Learning × Python Frameworks — Master INDEX

This index interconnects every phase of the ML curriculum with every Python framework. Use it to navigate the full ~391-lesson ML path and the ~345-lesson Python frameworks path.

---

## 1. Learning Path (Build Order)

Recommended sequence through all 12 ML phases and 13 Python frameworks, showing prerequisites.

```
Phase 01 — Linear Algebra (30 lessons)
  └─► numpy-pandas (30) — parallel: learn NumPy arrays while doing linear algebra

Phase 02 — Calculus & Optimization (40 lessons)
  └─► numpy-pandas (continues)

Phase 03 — Probability & Statistics (40 lessons)
  └─► scikit-learn (30) — parallel: see sklearn ML while learning stats

Phase 04 — Information Theory & Advanced Math (36 lessons)
  └─► pydantic (10) — data validation concepts

Phase 05 — Classical ML from Scratch (55 lessons)  [needs 01, 02, 03]
  └─► scikit-learn (parallel: reference implementations)
  └─► pytest-deep (15) — test your ML code

Phase 06 — Deep Learning Foundations (32 lessons)  [needs 01, 02, 03, 05]
  └─► PyTorch (40) — parallel: implement everything in PyTorch

Phase 07 — Advanced Architectures (30 lessons)  [needs 06]
  └─► PyTorch (continues)

Phase 08 — Computer Vision (31 lessons)  [needs 06]
  └─► PyTorch (continues)

Phase 09 — NLP (30 lessons)  [needs 06]
  └─► LangChain (20) — parallel: build LLM apps
  └─► FastAPI (30) — serve models via API

Phase 10 — Reinforcement Learning (20 lessons)  [needs 03, 06]
  └─► PyTorch (continues)

Phase 11 — MLOps (16 lessons)  [needs 05, 06]
  └─► Airflow (20) — pipelines & orchestration
  └─► Celery (15) — async task queues
  └─► pytest-deep / Flask / FastAPI — serving

Phase 12 — Capstones (11 lessons)  [needs all]
  └─► All frameworks — integrate everything
```

### Python Frameworks — Independent Arc

For someone focused on frameworks in parallel:

| Order | Framework | ML Relevance |
|-------|-----------|-------------|
| 1 | numpy-pandas (30) | Foundation for ALL numerical ML work |
| 2 | pydantic (10) | Data schemas for ML configs & serving |
| 3 | scikit-learn (30) | Classical ML reference implementations |
| 4 | pytorch (40) | Deep learning framework |
| 5 | langchain (20) | LLM applications, RAG, agents |
| 6 | fastapi (30) | Model serving, API layer |
| 7 | airflow (20) | ML pipeline orchestration |
| 8 | celery (15) | Async task queues for ML |
| 9 | flask (20) | Lightweight model serving |
| 10 | sqlalchemy (20) | ML metadata storage |
| 11 | django (60) | Full ML platform web apps |
| 12 | playwright (15) | E2E testing of ML dashboards |
| 13 | pytest-deep (15) | Testing ML code |

---

## 2. Phase Map — with Cross-References

### Phase 01 — Linear Algebra (30 lessons)

**Prerequisites:** Basic Python
**Builds toward:** All later phases (especially 05 Classical ML, 06 Deep Learning, 08 CV)
**Linked frameworks:** NumPy (numpy-pandas/), PyTorch (pytorch/)

**Key lessons:**
- `01-vectors.md` — Foundation for all ML data representation
- `02-vector-spaces.md` — Span, basis, dimension — underlies feature spaces
- `03-linear-transformations.md` — Matrix as transformation — neural network layers
- `04-gaussian-elimination.md` — Solving linear systems — least squares in Phase 05
- `05-matrix-multiplication.md` — Core operation — forward pass, attention
- `06-qr-decomposition.md` — QR for linear regression — numerical stability
- `07-cholesky.md` — Cholesky decomposition — GPs in Phase 05
- `08-eigenvalues.md` — PCA (Phase 05), spectral methods, convergence analysis
- `09-svd.md` — Matrix factorization — PCA, compression, recommendation
- `10-matrix-norms.md` — Regularization (Phase 06), stability analysis
- `11-low-rank-approximations.md` — Model compression, efficient attention
- `12-perturbation-theory.md` — Sensitivity analysis in ML systems
- `13-positive-definite.md` — Hessians, covariance matrices, kernel methods
- `14-nmf.md` — Non-negative matrix factorization — topic models (Phase 09)
- `15-tensor-decompositions.md` — Multi-way data — multimodal learning
- `16-random-matrix-theory.md` — Spectral of random matrices — Phase 03, Phase 06
- `17-sparse-matrices.md` — Efficient large-scale ML, graph data
- `18-krylov-methods.md` — Iterative solvers — large-scale optimization
- `19-matrix-functions.md` — Neural ODEs (Phase 07), diffusion kernels
- `20-generalized-eigenvalue.md` — Fisher LDA (Phase 05), CCA
- `21-graph-laplacians.md` — Spectral clustering (Phase 05), GNNs
- `22-spectral-graph-theory.md` — Graph partitioning, community detection
- `23-matrix-completion.md` — Recommender systems, collaborative filtering
- `24-tensor-methods.md` — Multimodal fusion, neuroimaging
- `25-indscal-parafac2.md` — Multi-way analysis — longitudinal data
- `26-constrained-cp.md` — Constrained tensor factorization
- `27-tensor-networks.md` — Quantum ML, deep learning theory
- `28-sensitivity-stability.md` — Robust ML, adversarial robustness
- `29-pca-svd-pipeline.md` — End-to-end PCA with SVD
- `30-tensor-recommendation.md` — Tensor-based recommender systems

---

### Phase 02 — Calculus & Optimization (40 lessons)

**Prerequisites:** Phase 01 (linear algebra), basic derivatives
**Builds toward:** Phase 05 (SVM, gradient descent), Phase 06 (training loops), Phase 07 (GANs, VAEs), Phase 10 (policy gradients)
**Linked frameworks:** NumPy (gradient computation), PyTorch (autograd), scikit-learn (SVM solver)

**Key lessons:**
- `01-limits.md` — Foundation for derivatives
- `02-derivative-rules.md` — Chain rule, product rule — backpropagation
- `03-taylor-series.md` — Approximations, second-order methods
- `04-multivariable.md` — Partial derivatives, gradients — neural network training
- `05-hessian.md` — Second-order optimization, curvature
- `06-implicit-differentiation.md` — Deep equilibrium models (Phase 07)
- `07-gradient-descent.md` — Core ML training algorithm
- `08-momentum-nesterov.md` — Accelerated optimization
- `09-adaptive-methods.md` — Adam, RMSProp, AdaGrad (Phase 06)
- `10-newton-methods.md` — Second-order optimization
- `11-quasi-newton-bfgs.md` — Limited-memory BFGS for large models
- `12-conjugate-gradient.md` — Iterative linear system solving
- `13-constrained-optimization.md` — SVM (Phase 05), constrained RL
- `14-linear-programming.md` — Resource allocation, robust optimization
- `15-quadratic-programming.md` — SVM dual formulation
- `16-semidefinite-programming.md` — Maximum margin, kernel learning
- `17-convex-analysis.md` — Convexity guarantees in ML
- `18-proximal-operators.md` — Proximal gradient, L1 regularization
- `19-admm.md` — Distributed optimization, consensus
- `20-operator-splitting.md` — Decomposable optimization
- `21-variance-reduced-sgd.md` — SVRG, SAGA — efficient large-scale training
- `22-second-order-stochastic.md` — AdaHessian, stochastic L-BFGS
- `23-natural-gradient.md` — Natural gradient descent — Phase 06, Bayesian learning
- `24-calculus-of-variations.md` — Functional derivatives — Phase 07 (neural ODEs)
- `25-optimal-control.md` — LQR, iLQR — Phase 10 (control, robotics)
- `26-sdes.md` — Stochastic differential equations — diffusion models (Phase 07)
- `27-hamiltonian-monte-carlo.md` — HMC sampling — Phase 03, Phase 04
- `28-bayesian-optimization.md` — Hyperparameter tuning — Phase 05
- `29-multi-objective.md` — Pareto optimization, multi-task learning
- `30-zeroth-order.md` — Gradient-free optimization — black-box attacks
- `31-genetic-algorithms.md` — Evolutionary strategies — Phase 10
- `32-relaxation.md` — Continuous relaxation — discrete structures
- `33-bilevel-optimization.md` — Meta-learning, GAN training
- `34-compositional-optimization.md` — Multi-step learning problems
- `35-distributed-optimization.md` — Distributed training (Phase 11)
- `36-optimizer-zoo.md` — Comprehensive optimizer comparison
- `37-differentiable-optimization.md` — Opt layers in neural networks
- `38-minibatch-selection.md` — Curriculum learning, sampling strategies
- `39-learn-to-optimize.md` — Learning optimizers with meta-learning
- `40-loss-landscape.md` — Visualization, sharp/flat minima (Phase 06)

---

### Phase 03 — Probability & Statistics (40 lessons)

**Prerequisites:** Phase 01 (linear algebra), basic calculus
**Builds toward:** Phase 05 (Naive Bayes, GMM, Bayesian nets), Phase 06 (probabilistic DL), Phase 07 (VAEs, normalizing flows), Phase 09 (LLMs), Phase 10 (RL)
**Linked frameworks:** numpy-pandas (random, stats), scikit-learn (probabilistic models), PyTorch (distributions)

**Key lessons:**
- `01-probability-axioms.md` — Foundation
- `02-random-variables.md` — Core concept for all uncertainty in ML
- `03-distributions.md` — Common distributions (normal, Bernoulli, etc.)
- `04-multivariate-distributions.md` — Multivariate normal — GMM (Phase 05)
- `05-expectation-variance-moments.md` — Moments, risk, bias-variance tradeoff
- `06-joint-marginal-conditional.md` — Probabilistic graphical models
- `07-covariance-correlation.md` — PCA (Phase 05), feature selection
- `08-transformations.md` — Change of variables — normalizing flows (Phase 07)
- `09-sums-clt.md` — Central limit theorem — convergence guarantees
- `10-lln-clt.md` — Law of large numbers — Monte Carlo methods
- `11-concentration-inequalities.md` — Hoeffding, Bernstein — generalization bounds
- `12-order-statistics.md` — Non-parametric methods, rank-based tests
- `13-mle.md` — Maximum likelihood estimation — standard training objective
- `14-map.md` — Maximum a posteriori — regularization perspective
- `15-exponential-family.md` — GLMs (Phase 05), sufficient statistics
- `16-bayesian-inference.md` — Bayesian ML, uncertainty quantification
- `17-hypothesis-testing.md` — A/B testing (Phase 11), feature significance
- `18-confidence-intervals.md` — Uncertainty estimates for ML predictions
- `19-bootstrap.md` — Resampling — ensemble methods (Phase 05)
- `20-anova.md` — Feature importance analysis
- `21-linear-regression.md` — Foundation for all regression (Phase 05)
- `22-glms.md` — Generalized linear models — classification (Phase 05)
- `23-mixed-effects.md` — Hierarchical models — multi-level data
- `24-bayesian-linear-regression.md` — Bayesian regression — uncertainty
- `25-gaussian-processes.md` — Non-parametric Bayesian regression (Phase 05)
- `26-multivariate-methods.md` — MANOVA, factor analysis — dimensionality reduction
- `27-time-series.md` — ARIMA, forecasting — Phase 11 (monitoring)
- `28-state-space-kalman.md` — Kalman filters — Phase 10 (RL, robotics)
- `29-survival-analysis.md` — Time-to-event prediction — churn modeling
- `30-empirical-processes.md` — Uniform laws — learning theory (Phase 05)
- `31-extreme-value-theory.md` — Anomaly detection (Phase 05), rare events
- `32-copulas.md` — Dependence modeling — financial ML
- `33-spatial-statistics.md` — Geo-spatial ML, Gaussian processes
- `34-missing-data.md` — Imputation strategies — real-world ML
- `35-causal-inference.md` — Causality — Phase 07, Phase 11
- `36-causal-discovery.md` — Structure learning — causal structure
- `37-bayesian-nonparametrics.md` — Dirichlet processes — infinite mixtures
- `38-abc.md` — Approximate Bayesian computation — simulation-based
- `39-measurement-error.md` — Errors-in-variables models
- `40-bayesian-workflow.md` — End-to-end Bayesian analysis

---

### Phase 04 — Information Theory & Advanced Math (36 lessons)

**Prerequisites:** Phase 01, Phase 02, Phase 03
**Builds toward:** Phase 06 (loss functions, information bottleneck), Phase 07 (diffusion, flow matching), Phase 09 (LLM theory, perplexity), Phase 05 (decision trees)
**Linked frameworks:** numpy-pandas, scikit-learn

**Key lessons:**
- `01-entropy.md` — Information content — cross-entropy loss (Phase 06)
- `02-divergences.md` — KL divergence, JS divergence — GANs (Phase 07)
- `03-max-entropy.md` — Maximum entropy principle — MaxEnt models (Phase 05)
- `04-fisher-information.md` — Natural gradient (Phase 02), optimal experiments
- `05-rate-distortion.md` — Compression — VAE theory (Phase 07), quantization
- `06-channel-capacity.md` — Information channel — information bottleneck
- `07-mdll-kolmogorov.md` — Minimum description length — model selection
- `08-information-geometry.md` — Statistical manifolds — natural gradient
- `09-rkhs.md` — Reproducing kernel Hilbert spaces — kernel methods (Phase 05)
- `10-optimal-transport.md` — Wasserstein distance — WGANs, domain adaptation
- `11-markov-chains.md` — Markov property — HMMs (Phase 05), MCMC
- `12-monte-carlo.md` — Monte Carlo estimation — Phase 03, Phase 10
- `13-mcmc.md` — Markov chain Monte Carlo — Bayesian inference
- `14-riemannian-hmc.md` — Riemannian HMC — advanced Bayesian sampling
- `15-stochastic-processes.md` — Stochastic processes — time series (Phase 03)
- `16-stochastic-calculus.md` — Ito calculus — diffusion models (Phase 07)
- `17-fourier-wavelet.md` — Fourier transforms — signal processing, CNNs
- `18-signal-processing.md` — Filtering, convolution — CNNs (Phase 08)
- `19-graph-theory.md` — Graphs — GNNs, spectral clustering (Phase 05)
- `20-tda.md` — Topological data analysis — manifold learning
- `21-differential-geometry.md` — Manifolds — Riemannian optimization, VAEs
- `22-lie-groups.md` — Symmetry groups — equivariant NNs (Phase 08)
- `23-representation-theory.md` — Group representations — invariant networks
- `24-symplectic-geometry.md` — Hamiltonian dynamics — HMC, neural ODEs
- `25-functional-analysis.md` — Banach/Hilbert spaces — kernel methods, neural nets
- `26-measure-theory.md` — Rigorous probability — advanced Bayesian methods
- `27-fixed-point.md` — Fixed-point iteration — DEQs (Phase 07), RL value iteration
- `28-category-theory.md` — Abstract composition — differentiable programming
- `29-stat-mech.md` — Statistical mechanics — energy-based models (Phase 07)
- `30-stat-physics-learning.md` — Spin glasses — generalization theory
- `31-random-graphs.md` — Network science — graph neural networks
- `32-algorithmic-information.md` — Kolmogorov complexity — AGI theory
- `33-game-theory.md` — Game theory — multi-agent RL (Phase 10), GANs
- `34-social-choice.md` — Collective decision-making — RLHF aggregation
- `35-complexity.md` — Computational complexity — ML theory
- `36-feature-selection.md` — Information-theoretic feature selection

---

### Phase 05 — Classical ML from Scratch (55 lessons)

**Prerequisites:** Phase 01 (linear algebra), Phase 02 (optimization), Phase 03 (prob/stats)
**Builds toward:** Phase 06 (DL comparisons), Phase 11 (MLOps deployment), Phase 12 (capstones)
**Linked frameworks:** scikit-learn (reference implementations), numpy-pandas (data handling), pytorch (neural analogs)

**Key lessons:**
- `01-linear-regression.md` — OLS, closed-form — foundation
- `02-logistic-regression.md` — Binary classification, log loss
- `03-glms.md` — Generalized linear models — Poisson, Gamma
- `04-naive-bayes.md` — Generative classifier — NLP baseline
- `05-lda-qda.md` — Linear/quadratic discriminant analysis
- `06-decision-trees.md` — CART, entropy splitting
- `07-random-forest.md` — Bagging ensemble
- `08-gradient-boosting.md` — Boosting framework (Phase 11)
- `09-xgboost.md` — Production gradient boosting
- `10-lightgbm.md` — Efficient GBM, GOSS, EFB
- `11-catboost.md` — Ordered boosting, categorical features
- `12-histogram-gbm.md` — Histogram-based GBM
- `13-svm.md` — Support vector machines, dual formulation
- `14-kernel-svm.md` — RBF kernel, kernel trick
- `15-knn.md` — Nearest neighbors, non-parametric
- `16-kmeans.md` — Clustering, Lloyd's algorithm
- `17-dbscan.md` — Density-based clustering
- `18-gmm.md` — Gaussian mixture models, EM algorithm
- `19-hierarchical.md` — Agglomerative clustering
- `20-spectral.md` — Spectral clustering — graph Laplacian (Phase 01)
- `21-pca.md` — Principal component analysis (Phase 01: eigenvalues/SVD)
- `22-tsne-umap.md` — Manifold visualization (Phase 04: differential geometry)
- `23-manifold.md` — Isomap, LLE, MDS
- `24-ica.md` — Independent component analysis — blind source separation
- `25-factor-cca-pls.md` — Factor analysis, CCA, PLS
- `26-gp.md` — Gaussian processes (Phase 03: 25-gaussian-processes)
- `27-bayesian-networks.md` — Probabilistic graphical models
- `28-hmm.md` — Hidden Markov models (Phase 04: 11-markov-chains)
- `29-crf.md` — Conditional random fields — sequence labeling
- `30-maxent.md` — Maximum entropy models (Phase 04: 03-max-entropy)
- `31-anomaly.md` — Isolation forest, LOF, autoencoders
- `32-learning-to-rank.md` — Ranking algorithms — search, recommendation
- `33-online-learning.md` — Streaming ML (Phase 11)
- `34-bandits.md` — Multi-armed bandits (Phase 10: exploration)
- `35-active-learning.md` — Query strategies — efficient labeling
- `36-semi-supervised.md` — Self-training, consistency regularization
- `37-imbalanced.md` — SMOTE, cost-sensitive learning
- `38-multi-label.md` — Multi-label classification
- `39-multi-instance.md` — Weakly supervised learning
- `40-calibration.md` — Probability calibration (Phase 11: monitoring)
- `41-conformal.md` — Conformal prediction — prediction sets
- `42-stacking.md` — Stacked generalization, meta-learners
- `43-symbolic-regression.md` — Genetic programming — interpretable models
- `44-bayesian-opt.md` — Bayesian optimization (Phase 02: 28-bayesian-optimization)
- `45-learning-theory.md` — VC dimension, Rademacher complexity
- `46-pac-bayes.md` — PAC-Bayesian generalization bounds
- `47-proper-losses.md` — Loss function design
- `48-model-selection.md` — Cross-validation, AIC, BIC
- `49-association-rules.md` — Apriori, FP-growth — pattern mining
- `50-subgroup-discovery.md` — Exceptional model mining
- `51-rule-learning.md` — Rule-based classifiers — RIPPER, OneR
- `52-robust-statistics.md` — Outlier-robust estimation
- `53-streaming.md` — Streaming algorithms, sketching
- `54-similarity.md` — Distance metrics, kernels
- `55-automl.md` — AutoML, hyperparameter optimization, NAS

---

### Phase 06 — Deep Learning Foundations (32 lessons)

**Prerequisites:** Phase 01 (linear algebra), Phase 02 (optimization), Phase 03 (prob/stats)
**Builds toward:** Phase 07 (advanced archs), Phase 08 (CV), Phase 09 (NLP), Phase 10 (RL), Phase 12 (capstones)
**Linked frameworks:** PyTorch (pytorch/), numpy-pandas

**Key lessons:**
- `01-computational-graphs.md` — Graph representation of computations
- `02-reverse-mode-autograd.md` — Backpropagation (Phase 12: 01-autograd-from-scratch)
- `03-forward-mode-autograd.md` — Forward-mode AD for Jacobians
- `04-full-autograd-framework.md` — Building autograd from scratch
- `05-higher-order-gradients.md` — Hessian-vector products, double backprop
- `06-perceptron-mlp.md` — Multilayer perceptron (Phase 01: linear transformations)
- `07-activations.md` — ReLU, sigmoid, tanh, SwiGLU, GELU (Phase 09)
- `08-initialization.md` — Xavier, Kaiming, orthogonal init — training stability
- `09-loss-functions.md` — Cross-entropy, MSE, CTC, contrastive (Phase 04: entropy)
- `10-optimizer-zoo.md` — SGD, Adam, AdamW, Lion (Phase 02: 09-adaptive-methods)
- `11-lr-schedulers.md` — Cosine annealing, warmup, OneCycle
- `12-normalization-layers.md` — BatchNorm, LayerNorm, RMSNorm (Phase 09, 08)
- `13-regularization.md` — Weight decay, dropout, stochastic depth, LabelSmoothing
- `14-augmentation.md` — Data augmentation — MixUp, CutMix, RandAugment
- `15-convolutions.md` — Convolution operation (Phase 04: 18-signal-processing)
- `16-pooling.md` — MaxPool, AvgPool, global pooling
- `17-attention.md` — Scaled dot-product attention (Phase 09: transformers)
- `18-transformer-blocks.md` — Transformer architecture (Phase 12: 02-transformer-from-scratch)
- `19-positional-encodings.md` — Sinusoidal, RoPE, ALiBi (Phase 09)
- `20-transformer-variants.md` — Performer, Linformer, Reformer — efficient attention
- `21-bptt.md` — Backprop through time — RNN training
- `22-rnn-lstm-gru.md` — Recurrent architectures — sequence modeling
- `23-seq2seq.md` — Encoder-decoder — machine translation
- `24-cnn-backbones.md` — ResNet, DenseNet, EfficientNet (Phase 08: CV backbones)
- `25-skip-connections.md` — Residual connections, Dense connections
- `26-normalization-alternatives.md` — GroupNorm, InstanceNorm, AdaIN
- `27-mixed-precision.md` — FP16 training, scaling (Phase 11: GPU optimization)
- `28-gradient-accumulation-checkpointing.md` — Memory-efficient training
- `29-gradient-noise-clipping.md` — Training stability techniques
- `30-loss-symmetries.md` — Understanding loss surface geometry
- `31-cifar-experiments.md` — Empirical comparison of techniques
- `32-training-pipeline.md` — End-to-end training infrastructure (Phase 11)

---

### Phase 07 — Advanced Architectures & Frontier Models (30 lessons)

**Prerequisites:** Phase 06 (deep learning foundations)
**Builds toward:** Phase 08 (CV transformers), Phase 09 (LLMs), Phase 12 (capstones)
**Linked frameworks:** PyTorch, langchain (LLM applications)

**Key lessons:**
- `01-kan.md` — Kolmogorov-Arnold Networks — learnable activation functions
- `02-mlp-alternatives.md` — MLP-Mixer, gMLP, ConvMixer — token mixing
- `03-neural-odes.md` — Continuous-depth models (Phase 02: 24-calculus-of-variations)
- `04-pinns.md` — Physics-informed neural networks — scientific ML
- `05-deq.md` — Deep equilibrium models (Phase 04: 27-fixed-point)
- `06-implicit-neural.md` — NeRF, SIREN — implicit representations
- `07-hypernetworks.md` — Weight-predicting networks — meta-learning
- `08-spiking-nns.md` — Spiking neural networks — neuromorphic computing
- `09-liquid-nns.md` — Liquid time-constant networks — continuous-time RNNs
- `10-capsule-networks.md` — Capsule networks — equivariance (Phase 04: 22-lie-groups)
- `11-neural-processes.md` — Neural processes — meta-learning, uncertainty
- `12-set-functions.md` — Deep sets, PointNet — permutation invariance
- `13-ssms.md` — State space models — Mamba architecture (Phase 12: 04-mamba)
- `14-ssm-variants.md` — S4, S5, DSS — structured state spaces
- `15-hybrid-ssm-attention.md` — Mamba-2, Jamba — hybrid architectures
- `16-ebms.md` — Energy-based models (Phase 04: 29-stat-mech)
- `17-normalizing-flows.md` — Flow-based generative models (Phase 03: 08-transformations)
- `18-autoregressive.md` — Autoregressive models — PixelCNN, WaveNet
- `19-diffusion.md` — Denoising diffusion probabilistic models (Phase 12: 03-diffusion)
- `20-latent-diffusion.md` — LDM, Stable Diffusion (Phase 08: 22-video-generation)
- `21-flow-matching.md` — Flow matching — simplified diffusion training
- `22-vaes.md` — Variational autoencoders (Phase 03: 16-bayesian-inference)
- `23-gans.md` — Generative adversarial networks (Phase 04: 33-game-theory)
- `24-mcmc.md` — MCMC for neural network sampling — Bayesian deep learning
- `25-differentiable-programming.md` — Differentiable primitives
- `26-neural-symbolic.md` — Neural-symbolic reasoning (Phase 09: 25-reasoning-math)
- `27-nas.md` — Neural architecture search (Phase 02: 28-bayesian-optimization)
- `28-contrastive-learning.md` — SimCLR, CLIP, MoCo (Phase 08: 08-self-supervised)
- `29-ml-for-science.md` — ML for physics, biology, chemistry
- `30-sota-reproduction.md` — Reproducing frontier research papers

---

### Phase 08 — Computer Vision (31 lessons)

**Prerequisites:** Phase 06 (deep learning)
**Builds toward:** Phase 09 (multimodal), Phase 12 (capstones)
**Linked frameworks:** PyTorch, numpy-pandas (image data), scikit-learn (feature extraction)

**Key lessons:**
- `01-image-processing.md` — Filtering, edge detection, histograms (Phase 04: 18-signal-processing)
- `02-feature-detection.md` — SIFT, Harris corners, FAST — classical CV
- `03-feature-descriptors.md` — HOG, SIFT, BRIEF — feature matching
- `04-cnn-backbones.md` — VGG, ResNet, Inception (Phase 06: 24-cnn-backbones)
- `05-efficient-backbones.md` — MobileNet, ShuffleNet, EfficientNet
- `06-modern-backbones.md` — ConvNeXt, VAN, ConvNeXt-V2
- `07-vision-transformers.md` — ViT, DeiT, Swin Transformer (Phase 06: 18-transformer-blocks)
- `08-self-supervised-vision.md` — MAE, DINO, iBot (Phase 07: 28-contrastive-learning)
- `09-object-detection.md` — YOLO, Faster R-CNN, DETR
- `10-instance-segmentation.md` — Mask R-CNN, YOLACT, SOLO
- `11-semantic-segmentation.md` — U-Net, DeepLab, SegFormer (Phase 12)
- `12-panoptic-segmentation.md` — Panoptic FPN, MaskFormer
- `13-depth-estimation.md` — Monocular depth — MiDaS, DPT
- `14-human-pose.md` — Pose estimation — OpenPose, HRNet
- `15-3d-pose-shape.md` — 3D human mesh recovery — SMPL, HMR
- `16-neural-face-models.md` — Face reenactment, GAN-based face gen
- `17-neural-rendering.md` — NeRF, 3D Gaussian Splatting (Phase 07: 06-implicit-neural)
- `18-point-cloud.md` — PointNet, PointNet++, 3D detection
- `19-3d-object-detection.md` — VoxelNet, SECOND, PV-RCNN — autonomous driving
- `20-multi-object-tracking.md` — DeepSORT, FairMOT, ByteTrack
- `21-video-understanding.md` — Video classification, I3D, TimeSformer
- `22-video-generation.md` — Video diffusion — Stable Video Diffusion (Phase 07: 19-diffusion)
- `23-image-to-image.md` — Pix2Pix, CycleGAN, InstructPix2Pix
- `24-super-resolution.md` — SRCNN, ESRGAN, SwinIR
- `25-medical-imaging.md` — Medical segmentation, classification, detection
- `26-vqa-captioning.md` — Visual QA, image captioning (Phase 09: multimodal)
- `27-open-vocabulary.md` — CLIP, GLIP, Grounding DINO (Phase 09: 01-text-processing)
- `28-robustness.md` — Adversarial attacks, corruption robustness
- `29-visual-rl.md` — Visual RL — Phase 10 (robotics, control)
- `30-multimodal-generation.md` — Text-to-image, text-to-video (Phase 09)
- `31-cv-system.md` — End-to-end CV production system (Phase 11)

---

### Phase 09 — NLP (30 lessons)

**Prerequisites:** Phase 06 (deep learning)
**Builds toward:** Phase 12 (capstones — RAG system, transformer from scratch)
**Linked frameworks:** langchain, PyTorch, fastapi (LLM serving), pydantic (structured generation)

**Key lessons:**
- `01-text-processing.md` — Regex, Unicode, normalization — text prep
- `02-tokenization.md` — BPE, WordPiece, SentencePiece — tokenizer training
- `03-word-embeddings.md` — Word2Vec, GloVe, FastText
- `04-language-models.md` — N-gram, neural LMs, perplexity (Phase 04: 01-entropy)
- `05-encoder-decoder.md` — BART, T5, PEGASUS — sequence-to-sequence
- `06-multilingual.md` — mBERT, XLM-R — cross-lingual transfer
- `07-long-range.md` — Longformer, BigBird, Sparse Transformers
- `08-efficient-attention.md` — Flash Attention, memory-efficient kernels
- `09-positional-encodings.md` — RoPE, ALiBi, relative positions (Phase 06: 19)
- `10-efficient-finetuning.md` — LoRA, Adapters, Prefix Tuning, QLoRA
- `11-distillation.md` — Knowledge distillation — student-teacher (Phase 11)
- `12-quantization.md` — INT8, GPTQ, AWQ — model compression
- `13-pruning.md` — Magnitude pruning, SparseGPT — sparsity
- `14-mixture-of-experts.md` — MoE layers — Mixtral, Switch Transformers
- `15-inference-optimization.md` — KV-cache, speculative decoding, vLLM
- `16-long-context.md` — Long context — YaRN, NTK-aware scaling
- `17-rag.md` — Retrieval augmented generation (Phase 12: 06-rag-system)
- `18-prompt-engineering.md` — Prompt design, chain-of-thought, few-shot
- `19-structured-generation.md` — JSON mode, grammar-constrained gen — pydantic (Phase 12)
- `20-llm-evaluation.md` — Benchmarks (MMLU, HumanEval, MT-Bench), metrics
- `21-alignment.md` — RLHF, DPO, KTO (Phase 10: 16-rlhf)
- `22-constitutional-ai.md` — Constitutional AI, self-critique
- `23-safety.md` — Red-teaming, guardrails, toxicity filtering
- `24-watermarking.md` — LLM output watermarking — attribution
- `25-reasoning-math.md` — Chain-of-thought, math reasoning — Program of Thought
- `26-code-llms.md` — Code generation — CodeLlama, StarCoder
- `27-agents.md` — LLM agents — ReAct, tool use, planning (langchain: agents)
- `28-ai-governance.md` — AI regulation, ethics — responsible AI
- `29-llm-serving.md` — vLLM, TGI, Triton — serving at scale (Phase 11)
- `30-llm-application.md` — Production LLM app — full stack (langchain + fastapi)

---

### Phase 10 — Reinforcement Learning (20 lessons)

**Prerequisites:** Phase 03 (prob/stats), Phase 06 (deep learning)
**Builds toward:** Phase 12 (capstones — RLHF), Phase 09 (21-alignment RLHF)
**Linked frameworks:** PyTorch, numpy-pandas

**Key lessons:**
- `01-mdp.md` — Markov decision processes — formal RL framework
- `02-dynamic-programming.md` — Value iteration, policy iteration (Phase 04: 27-fixed-point)
- `03-monte-carlo.md` — MC prediction, control — sampling-based RL
- `04-td-learning.md` — TD(0), SARSA, Q-learning — temporal difference
- `05-function-approximation.md` — DQN, Deep Q-learning (Phase 06)
- `06-policy-gradient.md` — REINFORCE, policy gradient theorem (Phase 02: optimization)
- `07-advanced-actor-critic.md` — A2C, A3C, PPO, SAC — modern deep RL
- `08-model-based.md` — Dyna, MuZero, world models — planning
- `09-exploration.md` — Exploration strategies — UCB, Thompson sampling, curiosity
- `10-offline-rl.md` — CQL, IQL — learning from static datasets
- `11-multi-agent.md` — MADDPG, QMIX (Phase 04: 33-game-theory)
- `12-imitation-learning.md` — Behavioral cloning, GAIL, Inverse RL
- `13-hierarchical-rl.md` — HRL, options framework — temporal abstraction
- `14-multi-task-meta.md` — Meta-RL, multi-task RL — generalization
- `15-safe-rl.md` — Constrained MDP, safe exploration (Phase 02: 13-constrained)
- `16-rlhf.md` — RL from human feedback — alignment (Phase 09: 21-alignment)
- `17-continuous-control.md` — Robotics control — DDPG, TD3, SAC (Phase 02: 25-optimal-control)
- `18-planning.md` — Monte Carlo tree search — AlphaGo/Zero (Phase 12)
- `19-robotics.md` — Robot learning, manipulation, locomotion
- `20-rl-system.md` — Production RL system — training, deployment, monitoring

---

### Phase 11 — MLOps & Engineering at Scale (16 lessons)

**Prerequisites:** Phase 05 (classical ML), Phase 06 (deep learning)
**Builds toward:** Phase 12 (capstones — ML monitoring, distributed training)
**Linked frameworks:** airflow, celery, fastapi, flask, pytest-deep, pydantic, sqlalchemy

**Key lessons:**
- `01-experiment-tracking.md` — MLflow, W&B, neptune — tracking experiments
- `02-data-versioning.md` — DVC, lakeFS — data lineage, reproducibility
- `03-feature-engineering.md` — Feature stores (Feast), transformations
- `04-pipeline-orchestration.md` — Airflow, Prefect, Kubeflow — pipeline DAGs
- `05-model-serving.md` — TorchServe, TF Serving, Triton, BentoML — serving infra
- `06-monitoring.md` — Model monitoring, drift detection, observability
- `07-model-governance.md` — Model registry, versioning, audit trails
- `08-ab-testing.md` — Online evaluation, statistical significance (Phase 03: 17-hypothesis-testing)
- `09-continuous-training.md` — Retraining pipelines, data freshness
- `10-infrastructure-as-code.md` — Docker, Kubernetes, Terraform for ML
- `11-distributed-training.md` — FSDP, DeepSpeed, Horovod — multi-GPU (Phase 12: 07)
- `12-gpu-optimization.md` — CUDA, kernel fusion, memory profiling (Phase 06: 27-mixed-precision)
- `13-data-pipeline-optimization.md` — Data loading, preprocessing at scale
- `14-testing-for-ml.md` — CI/CD for ML, data tests, model tests (pytest-deep)
- `15-responsible-ai.md` — Fairness, bias detection, interpretability
- `16-cost-optimization.md` — Cloud cost management, spot instances, auto-scaling

---

### Phase 12 — Grand Capstone Projects (11 lessons)

**Prerequisites:** All prior phases
**Builds toward:** Real-world ML engineering mastery
**Linked frameworks:** ALL — PyTorch, langchain, fastapi, airflow, celery, pytest, pydantic, sqlalchemy

**Key lessons:**
- `01-autograd-from-scratch.md` — Build autograd engine (Phase 06: 02-reverse-mode-autograd)
- `02-transformer-from-scratch.md` — Implement transformer (Phase 06: 18-transformer-blocks)
- `03-diffusion-model.md` — DDPM implementation (Phase 07: 19-diffusion)
- `04-mamba-from-scratch.md` — SSM implementation (Phase 07: 13-ssms)
- `05-rlhf-dpo.md` — RLHF/DPO training pipeline (Phase 10: 16-rlhf)
- `06-rag-system.md` — Full RAG pipeline (Phase 09: 17-rag) + langchain
- `07-distributed-training.md` — Multi-GPU training system (Phase 11: 11-distributed-training)
- `08-automl-system.md` — AutoML pipeline — hyperparameter optimization
- `09-ml-monitoring.md` — Full monitoring stack (Phase 11: 06-monitoring)
- `10-reproduce-paper.md` — Reproduce a frontier ML paper from scratch
- `11-novel-contribution.md` — Design, implement, validate novel contribution

---

## 3. Concept Map — Cross-Phase Dependencies

| Concept | Introduced In | Used In | Linked Frameworks |
|---------|--------------|---------|-------------------|
| Linear Algebra | Phase 01 | Phase 05 (PCA, SVM), Phase 06 (backprop, transformers), Phase 08 (image transforms, backbones), Phase 09 (embeddings, attention) | NumPy, PyTorch |
| Calculus (Derivatives) | Phase 02 | Phase 05 (gradient descent), Phase 06 (autograd, training), Phase 07 (neural ODEs), Phase 09 (backprop) | PyTorch, NumPy |
| Optimization | Phase 02 | Phase 05 (SVM, GD), Phase 06 (optimizers, schedulers), Phase 07 (GANs, VAEs training), Phase 10 (policy gradient) | PyTorch, scikit-learn |
| Probability Distributions | Phase 03 | Phase 05 (Naive Bayes, GMM), Phase 06 (loss functions), Phase 07 (VAEs, normalizing flows), Phase 09 (LMs) | scikit-learn, PyTorch |
| Bayes' Rule | Phase 03 | Phase 05 (Bayesian nets, GPs), Phase 07 (VAEs), Phase 09 (Bayesian LMs), Phase 10 (RLHF) | scikit-learn |
| Maximum Likelihood | Phase 03 | Phase 05 (all models), Phase 06 (cross-entropy loss), Phase 07 (VAEs, flows), Phase 09 (LM training) | scikit-learn, PyTorch |
| Entropy / KL Divergence | Phase 04 | Phase 05 (decision trees, MaxEnt), Phase 06 (cross-entropy loss), Phase 07 (VAEs, GANs), Phase 09 (perplexity) | scikit-learn, PyTorch |
| Monte Carlo Methods | Phase 04 | Phase 03 (Bayesian inference), Phase 07 (MCMC), Phase 10 (MC prediction), Phase 08 (rendering) | NumPy |
| Markov Chains | Phase 04 | Phase 05 (HMMs), Phase 07 (diffusion), Phase 09 (LMs), Phase 10 (MDPs, TD learning) | hmmlearn, PyTorch |
| Convolution | Phase 06 | Phase 08 (all CV tasks), Phase 09 (text CNNs), Phase 07 (CNN backbones) | PyTorch |
| Attention | Phase 06 | Phase 07 (transformers), Phase 08 (ViT), Phase 09 (all NLP), Phase 10 (actor-critic) | PyTorch, LangChain |
| Backpropagation | Phase 06 | Phase 07 (training), Phase 08 (CV training), Phase 09 (NLP training), Phase 10 (policy gradient) | PyTorch |
| Regularization | Phase 06 | Phase 05 (regularized models), Phase 07 (training), Phase 08 (robustness), Phase 11 (monitoring) | PyTorch, scikit-learn |
| Latent Variables | Phase 03 | Phase 07 (VAEs), Phase 08 (self-supervised), Phase 09 (topic models), Phase 10 (world models) | PyTorch |
| Dimensionality Reduction | Phase 05 | Phase 08 (feature compression), Phase 09 (embeddings), Phase 11 (feature stores) | scikit-learn, NumPy |
| Ensemble Methods | Phase 05 | Phase 07 (stacking), Phase 11 (model serving ensembles), Phase 12 (capstones) | scikit-learn |
| Generative Models | Phase 07 | Phase 08 (image gen, video gen), Phase 09 (text gen), Phase 10 (world models) | PyTorch, LangChain |
| Sequence Modeling | Phase 06 (RNN) | Phase 07 (SSMs), Phase 09 (all NLP), Phase 10 (RL trajectories), Phase 08 (video) | PyTorch |
| Transfer Learning | Phase 06 | Phase 08 (CV fine-tuning), Phase 09 (LLM fine-tuning), Phase 11 (model adapters) | PyTorch, LangChain |
| Causality | Phase 03 | Phase 05 (causal ML), Phase 07 (counterfactuals), Phase 11 (A/B testing, fairness) | scikit-learn |
| Game Theory | Phase 04 | Phase 07 (GANs), Phase 10 (multi-agent RL) | PyTorch |
| Fixed-Point Iteration | Phase 04 | Phase 07 (DEQs), Phase 10 (value iteration, policy eval) | PyTorch |
| Graph Theory | Phase 04 | Phase 05 (spectral clustering), Phase 08 (scene graphs), Phase 09 (knowledge graphs), Phase 10 (MDP graphs) | NetworkX |
| Control Theory | Phase 02 | Phase 10 (robotics, continuous control), Phase 07 (neural ODEs) | PyTorch |
| Model Serving | Phase 11 | Phase 09 (LLM serving), Phase 08 (CV inference), Phase 12 (all capstones) | FastAPI, Flask, TorchServe |
| Distributed Computing | Phase 11 | Phase 06 (distributed training), Phase 12 (distributed capstone) | Airflow, Celery, PyTorch |

---

## 4. Framework Interconnection

### Map: Python Frameworks → ML Phases

| Framework | Relevant ML Phases | Why |
|-----------|-------------------|-----|
| **numpy-pandas** (30) | Phase 01–12 (all) | Foundation for all numerical computing. NumPy arrays are the data structure underlying every ML operation. Pandas DataFrames are the standard for tabular data in Phase 05 and Phase 11 feature engineering. |
| **scikit-learn** (30) | Phase 05, Phase 03, Phase 11 | Classical ML reference implementations. Use to verify your scratch implementations (Phase 05). Train-test splits, cross-validation, pipelines in Phase 11. Feature extraction (Phase 03). |
| **PyTorch** (40) | Phase 06–10, Phase 12 | The deep learning framework used throughout the DL curriculum. Autograd (Phase 06), nn.Module, optimizers, data loaders, GPU training, distributed computing. Used in all capstones (Phase 12). |
| **Django** (60) | Phase 11, Phase 12 | Build full-stack ML platforms: model dashboards, data annotation UIs, ML SaaS products. Phase 11 MLOps UI, Phase 12 capstone deployment. |
| **FastAPI** (30) | Phase 09, Phase 11, Phase 12 | High-performance API layer for model serving. LLM serving (Phase 09), ML API endpoints (Phase 11), capstone deployment (Phase 12). Async support for streaming responses. |
| **Flask** (20) | Phase 11, Phase 12 | Lightweight model serving and microservices. Quick prototyping of ML APIs. Simple inference endpoints. |
| **SQLAlchemy** (20) | Phase 11, Phase 12 | ML metadata storage: experiment tracking, model registry, feature store backends. Database abstraction for ML platforms. |
| **pytest-deep** (15) | Phase 05, Phase 11, Phase 12 | Testing ML code: unit tests for data transformations, model invariants, training loop correctness. CI/CD for ML (Phase 11). |
| **Celery** (15) | Phase 11, Phase 12 | Async task queue for ML: batch inference, model retraining pipelines, data preprocessing. Distributed task execution. |
| **LangChain** (20) | Phase 09, Phase 12 | LLM application framework: RAG (Phase 09: 17-rag), agents (Phase 09: 27-agents), prompt engineering, chain-of-thought. Phase 12 capstone RAG system. |
| **Playwright** (15) | Phase 11, Phase 12 | E2E testing of ML dashboards, monitoring UIs, data annotation interfaces. Browser automation for ML platform testing. |
| **Pydantic** (10) | Phase 09, Phase 11, Phase 12 | Data validation for ML configs, inference request/response schemas (FastAPI), structured LLM output (Phase 09: 19-structured-generation). |
| **Airflow** (20) | Phase 05, Phase 11, Phase 12 | ML pipeline orchestration: data pipelines, feature engineering workflows, model retraining, batch inference DAGs. |

### Map: ML Phases → Python Frameworks

| ML Phase | Primary Frameworks | Supporting Frameworks |
|----------|-------------------|----------------------|
| Phase 01 — Linear Algebra | numpy-pandas | — |
| Phase 02 — Calculus & Optimization | numpy-pandas | — |
| Phase 03 — Probability & Statistics | numpy-pandas | scikit-learn |
| Phase 04 — Advanced Math | numpy-pandas | — |
| Phase 05 — Classical ML | scikit-learn, numpy-pandas | pytest-deep |
| Phase 06 — Deep Learning | PyTorch, numpy-pandas | — |
| Phase 07 — Advanced Architectures | PyTorch | — |
| Phase 08 — Computer Vision | PyTorch | numpy-pandas |
| Phase 09 — NLP | PyTorch, LangChain, FastAPI | pydantic |
| Phase 10 — Reinforcement Learning | PyTorch | numpy-pandas |
| Phase 11 — MLOps | Airflow, FastAPI, Celery, pytest-deep, SQLAlchemy | Flask, Pydantic, Django, Playwright |
| Phase 12 — Capstones | PyTorch, LangChain, FastAPI, Airflow | All frameworks |

---

## 5. Quick Navigation

| I want to learn about... | Go to Phase | Lesson / File |
|--------------------------|-------------|---------------|
| Vector operations | Phase 01 | `01-linear-algebra/lessons/01-vectors.md`, `code/01-vectors.py` |
| Matrix multiplication | Phase 01 | `01-linear-algebra/lessons/05-matrix-multiplication.md` |
| Eigenvalues & eigenvectors | Phase 01 | `01-linear-algebra/lessons/08-eigenvalues.md` |
| Singular value decomposition (SVD) | Phase 01 | `01-linear-algebra/lessons/09-svd.md` |
| PCA via SVD | Phase 01 | `01-linear-algebra/lessons/29-pca-svd-pipeline.md` |
| Gradient descent | Phase 02 | `02-calculus-optimization/lessons/07-gradient-descent.md` |
| Adam optimizer | Phase 02 | `02-calculus-optimization/lessons/09-adaptive-methods.md` |
| Momentum & Nesterov | Phase 02 | `02-calculus-optimization/lessons/08-momentum-nesterov.md` |
| Bayesian optimization | Phase 02 | `02-calculus-optimization/lessons/28-bayesian-optimization.md` |
| Natural gradient | Phase 02 | `02-calculus-optimization/lessons/23-natural-gradient.md` |
| Probability distributions | Phase 03 | `03-probability-statistics/lessons/03-distributions.md` |
| Maximum likelihood (MLE) | Phase 03 | `03-probability-statistics/lessons/13-mle.md` |
| Bayesian inference | Phase 03 | `03-probability-statistics/lessons/16-bayesian-inference.md` |
| Gaussian processes | Phase 03 | `03-probability-statistics/lessons/25-gaussian-processes.md` |
| Hypothesis testing / A/B testing | Phase 03 | `03-probability-statistics/lessons/17-hypothesis-testing.md` |
| Time series analysis | Phase 03 | `03-probability-statistics/lessons/27-time-series.md` |
| Causal inference | Phase 03 | `03-probability-statistics/lessons/35-causal-inference.md` |
| Entropy & cross-entropy | Phase 04 | `04-advanced-math/lessons/01-entropy.md` |
| KL divergence | Phase 04 | `04-advanced-math/lessons/02-divergences.md` |
| RKHS & kernel methods | Phase 04 | `04-advanced-math/lessons/09-rkhs.md` |
| Optimal transport / Wasserstein | Phase 04 | `04-advanced-math/lessons/10-optimal-transport.md` |
| MCMC sampling | Phase 04 | `04-advanced-math/lessons/13-mcmc.md` |
| Fourier / wavelet transforms | Phase 04 | `04-advanced-math/lessons/17-fourier-wavelet.md` |
| Differential geometry for ML | Phase 04 | `04-advanced-math/lessons/21-differential-geometry.md` |
| Decision trees | Phase 05 | `05-classical-ml/lessons/06-decision-trees.md` |
| Random forests | Phase 05 | `05-classical-ml/lessons/07-random-forest.md` |
| Gradient boosting (XGBoost) | Phase 05 | `05-classical-ml/lessons/08-gradient-boosting.md` |
| SVM & kernel SVM | Phase 05 | `05-classical-ml/lessons/13-svm.md` |
| PCA | Phase 05 | `05-classical-ml/lessons/21-pca.md` |
| t-SNE / UMAP | Phase 05 | `05-classical-ml/lessons/22-tsne-umap.md` |
| K-means clustering | Phase 05 | `05-classical-ml/lessons/16-kmeans.md` |
| GMM & EM algorithm | Phase 05 | `05-classical-ml/lessons/18-gmm.md` |
| Hidden Markov models | Phase 05 | `05-classical-ml/lessons/28-hmm.md` |
| Anomaly detection | Phase 05 | `05-classical-ml/lessons/31-anomaly.md` |
| Conformal prediction | Phase 05 | `05-classical-ml/lessons/41-conformal.md` |
| AutoML & hyperparameter tuning | Phase 05 | `05-classical-ml/lessons/55-automl.md` |
| Backpropagation | Phase 06 | `06-deep-learning/lessons/02-reverse-mode-autograd.md` |
| MLP / feedforward networks | Phase 06 | `06-deep-learning/lessons/06-perceptron-mlp.md` |
| Activation functions | Phase 06 | `06-deep-learning/lessons/07-activations.md` |
| Loss functions | Phase 06 | `06-deep-learning/lessons/09-loss-functions.md` |
| Normalization (Batch/Layer/RMS) | Phase 06 | `06-deep-learning/lessons/12-normalization-layers.md` |
| Convolutions | Phase 06 | `06-deep-learning/lessons/15-convolutions.md` |
| Attention mechanism | Phase 06 | `06-deep-learning/lessons/17-attention.md` |
| Transformers | Phase 06 | `06-deep-learning/lessons/18-transformer-blocks.md` |
| RNNs, LSTMs, GRUs | Phase 06 | `06-deep-learning/lessons/22-rnn-lstm-gru.md` |
| Skip connections / ResNet | Phase 06 | `06-deep-learning/lessons/25-skip-connections.md` |
| Mixed precision training | Phase 06 | `06-deep-learning/lessons/27-mixed-precision.md` |
| Diffusion models | Phase 07 | `07-advanced-architectures/lessons/19-diffusion.md` |
| VAEs | Phase 07 | `07-advanced-architectures/lessons/22-vaes.md` |
| GANs | Phase 07 | `07-advanced-architectures/lessons/23-gans.md` |
| Normalizing flows | Phase 07 | `07-advanced-architectures/lessons/17-normalizing-flows.md` |
| Neural ODEs | Phase 07 | `07-advanced-architectures/lessons/03-neural-odes.md` |
| State space models (Mamba) | Phase 07 | `07-advanced-architectures/lessons/13-ssms.md` |
| Energy-based models | Phase 07 | `07-advanced-architectures/lessons/16-ebms.md` |
| Contrastive learning | Phase 07 | `07-advanced-architectures/lessons/28-contrastive-learning.md` |
| CNNs for image classification | Phase 08 | `08-computer-vision/lessons/04-cnn-backbones.md` |
| Vision Transformers (ViT) | Phase 08 | `08-computer-vision/lessons/07-vision-transformers.md` |
| Object detection (YOLO, DETR) | Phase 08 | `08-computer-vision/lessons/09-object-detection.md` |
| Semantic segmentation (U-Net) | Phase 08 | `08-computer-vision/lessons/11-semantic-segmentation.md` |
| NeRF / neural rendering | Phase 08 | `08-computer-vision/lessons/17-neural-rendering.md` |
| Self-supervised vision (MAE, DINO) | Phase 08 | `08-computer-vision/lessons/08-self-supervised-vision.md` |
| Video understanding | Phase 08 | `08-computer-vision/lessons/21-video-understanding.md` |
| Tokenization (BPE, WordPiece) | Phase 09 | `09-nlp/lessons/02-tokenization.md` |
| Word embeddings | Phase 09 | `09-nlp/lessons/03-word-embeddings.md` |
| Language models | Phase 09 | `09-nlp/lessons/04-language-models.md` |
| RAG (retrieval augmented generation) | Phase 09 | `09-nlp/lessons/17-rag.md` |
| Prompt engineering | Phase 09 | `09-nlp/lessons/18-prompt-engineering.md` |
| Fine-tuning (LoRA, adapters) | Phase 09 | `09-nlp/lessons/10-efficient-finetuning.md` |
| Quantization (GPTQ, AWQ) | Phase 09 | `09-nlp/lessons/12-quantization.md` |
| LLM agents | Phase 09 | `09-nlp/lessons/27-agents.md` |
| RLHF / DPO / alignment | Phase 09 | `09-nlp/lessons/21-alignment.md` |
| LLM serving (vLLM, TGI) | Phase 09 | `09-nlp/lessons/29-llm-serving.md` |
| Q-Learning / DQN | Phase 10 | `10-reinforcement-learning/lessons/04-td-learning.md` |
| Policy gradients / PPO | Phase 10 | `10-reinforcement-learning/lessons/06-policy-gradient.md` |
| Actor-critic methods | Phase 10 | `10-reinforcement-learning/lessons/07-advanced-actor-critic.md` |
| MuZero / model-based RL | Phase 10 | `10-reinforcement-learning/lessons/08-model-based.md` |
| Multi-agent RL | Phase 10 | `10-reinforcement-learning/lessons/11-multi-agent.md` |
| Imitation learning | Phase 10 | `10-reinforcement-learning/lessons/12-imitation-learning.md` |
| Experiment tracking | Phase 11 | `11-mlops/lessons/01-experiment-tracking.md` |
| Model serving | Phase 11 | `11-mlops/lessons/05-model-serving.md` |
| Monitoring & drift detection | Phase 11 | `11-mlops/lessons/06-monitoring.md` |
| Distributed training | Phase 11 | `11-mlops/lessons/11-distributed-training.md` |
| A/B testing for ML | Phase 11 | `11-mlops/lessons/08-ab-testing.md` |
| Autograd from scratch | Phase 12 | `12-capstones/lessons/01-autograd-from-scratch.md` |
| Transformer from scratch | Phase 12 | `12-capstones/lessons/02-transformer-from-scratch.md` |
| Diffusion model from scratch | Phase 12 | `12-capstones/lessons/03-diffusion-model.md` |
| Mamba from scratch | Phase 12 | `12-capstones/lessons/04-mamba-from-scratch.md` |
| RAG system (full) | Phase 12 | `12-capstones/lessons/06-rag-system.md` |
| NumPy arrays | numpy-pandas | `lessons/01-arrays.md` |
| Pandas DataFrames | numpy-pandas | `lessons/11-series-dataframe.md` |
| Broadcasting | numpy-pandas | `lessons/04-broadcasting.md` |
| Train/test split | scikit-learn | `lessons/01-train-test-split.md` |
| Cross-validation | scikit-learn | `lessons/13-cross-validation.md` |
| PyTorch tensors | pytorch | `lessons/01-tensor-basics.md` |
| PyTorch autograd | pytorch | `lessons/04-autograd.md` |
| PyTorch DataLoader | pytorch | `lessons/13-dataset-dataloader.md` |
| PyTorch CNN | pytorch | `lessons/22-cnn-basics.md` |
| FastAPI for ML APIs | fastapi | `lessons/01-project-setup.md`, `lessons/04-response-models.md` |
| LangChain RAG | langchain | `lessons/10-retrieval-qa.md`, `lessons/20-integration-rag.md` |
| Airflow DAGs for ML | airflow | `lessons/01-dag-basics.md`, `lessons/20-capstone-pipeline.md` |
| Pydantic for ML configs | pydantic | `lessons/01-basics.md`, `lessons/10-integration-settings.md` |
| Celery for async ML tasks | celery | `lessons/01-celery-basics.md`, `lessons/15-integration-pipeline.md` |
| SQLAlchemy for ML metadata | sqlalchemy | `lessons/05-orm-declarative-models.md` |

---

## 6. Topic Index (Alphabetical)

A flat alphabetical index of major topics across all phases and frameworks.

- **A/B testing** → Phase 03 (17-hypothesis-testing), Phase 11 (08-ab-testing)
- **ABC (Approximate Bayesian Computation)** → Phase 03 (38-abc)
- **Activation functions** → Phase 06 (07-activations), pytorch (12-activations)
- **Active learning** → Phase 05 (35-active-learning)
- **Actor-critic methods** → Phase 10 (07-advanced-actor-critic)
- **Adam optimizer** → Phase 02 (09-adaptive-methods), Phase 06 (10-optimizer-zoo), pytorch (09-optimizers)
- **ADMM** → Phase 02 (19-admm)
- **Adversarial robustness** → Phase 08 (28-robustness)
- **Agents (LLM)** → Phase 09 (27-agents), langchain (12-agents, 13-agent-executor)
- **Airflow DAGs** → airflow (01-dag-basics, 20-capstone-pipeline)
- **Alignment (RLHF/DPO)** → Phase 09 (21-alignment), Phase 10 (16-rlhf), Phase 12 (05-rlhf-dpo)
- **Anomaly detection** → Phase 05 (31-anomaly)
- **ANOVA** → Phase 03 (20-anova)
- **Association rules** → Phase 05 (49-association-rules)
- **Attention mechanism** → Phase 06 (17-attention), Phase 07 (15-hybrid-ssm-attention), Phase 08 (07-vision-transformers), Phase 09 (08-efficient-attention)
- **Autograd** → Phase 06 (02-reverse-mode-autograd, 03-forward-mode-autograd, 04-full-autograd-framework), pytorch (04-autograd), Phase 12 (01-autograd-from-scratch)
- **AutoML** → Phase 05 (55-automl), Phase 12 (08-automl-system)
- **Autoregressive models** → Phase 07 (18-autoregressive)
- **Backpropagation** → Phase 06 (02-reverse-mode-autograd), Phase 12 (01-autograd-from-scratch)
- **Backprop through time (BPTT)** → Phase 06 (21-bptt)
- **Bandits (multi-armed)** → Phase 05 (34-bandits), Phase 10 (09-exploration)
- **Batch normalization** → Phase 06 (12-normalization-layers), pytorch (21-batch-norm)
- **Bayesian inference** → Phase 03 (16-bayesian-inference, 24-bayesian-linear-regression), Phase 05 (44-bayesian-opt)
- **Bayesian networks** → Phase 05 (27-bayesian-networks)
- **Bayesian nonparametrics** → Phase 03 (37-bayesian-nonparametrics)
- **Bayesian optimization** → Phase 02 (28-bayesian-optimization), Phase 05 (44-bayesian-opt)
- **Bayesian workflow** → Phase 03 (40-bayesian-workflow)
- **BFGS / L-BFGS** → Phase 02 (11-quasi-newton-bfgs)
- **Bias-variance tradeoff** → Phase 03 (05-expectation-variance-moments), Phase 05 (45-learning-theory)
- **Bilevel optimization** → Phase 02 (33-bilevel-optimization)
- **Bootstrapping** → Phase 03 (19-bootstrap)
- **Broadcasting (NumPy)** → numpy-pandas (04-broadcasting)
- **Calculus of variations** → Phase 02 (24-calculus-of-variations)
- **Calibration (probability)** → Phase 05 (40-calibration)
- **Capsule networks** → Phase 07 (10-capsule-networks)
- **Capstone projects** → Phase 12 (all)
- **Categorical data** → numpy-pandas (26-categorical)
- **Category theory** → Phase 04 (28-category-theory)
- **Causal inference** → Phase 03 (35-causal-inference, 36-causal-discovery)
- **Celery** → celery (all), Phase 11 (async tasks)
- **Chain-of-thought** → Phase 09 (18-prompt-engineering, 25-reasoning-math)
- **Cholesky decomposition** → Phase 01 (07-cholesky)
- **CLIP** → Phase 08 (27-open-vocabulary), Phase 07 (28-contrastive-learning)
- **Clustering** → Phase 05 (16-kmeans, 17-dbscan, 18-gmm, 19-hierarchical, 20-spectral), scikit-learn (08-kmeans, 24-clustering-advanced)
- **CNNs** → Phase 06 (15-convolutions, 24-cnn-backbones), Phase 08 (04-cnn-backbones), pytorch (22-cnn-basics, 23-cnn-image)
- **Code LLMs** → Phase 09 (26-code-llms)
- **Compositional optimization** → Phase 02 (34-compositional-optimization)
- **Computational graphs** → Phase 06 (01-computational-graphs)
- **Concentration inequalities** → Phase 03 (11-concentration-inequalities)
- **Conditional random fields (CRF)** → Phase 05 (29-crf)
- **Conformal prediction** → Phase 05 (41-conformal)
- **Conjugate gradient** → Phase 02 (12-conjugate-gradient)
- **Constitutional AI** → Phase 09 (22-constitutional-ai)
- **Constrained optimization** → Phase 02 (13-constrained-optimization)
- **Contrastive learning** → Phase 07 (28-contrastive-learning), Phase 08 (08-self-supervised-vision)
- **Control theory (optimal control)** → Phase 02 (25-optimal-control), Phase 10 (17-continuous-control)
- **Convolutions** → Phase 06 (15-convolutions), Phase 04 (18-signal-processing)
- **Convex analysis** → Phase 02 (17-convex-analysis)
- **Copulas** → Phase 03 (32-copulas)
- **Cross-validation** → Phase 05 (48-model-selection), scikit-learn (13-cross-validation)
- **Data augmentation** → Phase 06 (14-augmentation)
- **Data cleaning** → numpy-pandas (14-data-cleaning)
- **Data versioning** → Phase 11 (02-data-versioning)
- **DataLoaders** → pytorch (13-dataset-dataloader)
- **DBSCAN** → Phase 05 (17-dbscan)
- **Decision trees** → Phase 05 (06-decision-trees), scikit-learn (04-decision-trees)
- **Deep equilibrium models (DEQ)** → Phase 07 (05-deq), Phase 04 (27-fixed-point)
- **DeepSets** → Phase 07 (12-set-functions)
- **Depth estimation** → Phase 08 (13-depth-estimation)
- **Derivatives (calculus)** → Phase 02 (02-derivative-rules, 04-multivariable)
- **DETR** → Phase 08 (09-object-detection)
- **Differential geometry** → Phase 04 (21-differential-geometry)
- **Differentiable programming** → Phase 07 (25-differentiable-programming), Phase 02 (37-differentiable-optimization)
- **Diffusion models** → Phase 07 (19-diffusion, 20-latent-diffusion, 21-flow-matching), Phase 12 (03-diffusion-model)
- **Dimensionality reduction** → Phase 05 (21-pca, 22-tsne-umap, 23-manifold, 24-ica)
- **Distillation (knowledge)** → Phase 09 (11-distillation)
- **Distributed optimization** → Phase 02 (35-distributed-optimization)
- **Distributed training** → Phase 11 (11-distributed-training), pytorch (33-data-parallel), Phase 12 (07-distributed-training)
- **Divergences (KL, JS, f-divergences)** → Phase 04 (02-divergences)
- **Django** → django (all), Phase 11 (ML platforms), Phase 12 (deployment)
- **DPO (Direct Preference Optimization)** → Phase 10 (16-rlhf), Phase 12 (05-rlhf-dpo)
- **DQN / Deep Q-learning** → Phase 10 (05-function-approximation)
- **Dynamic programming** → Phase 10 (02-dynamic-programming)
- **Early stopping** → pytorch (17-early-stopping)
- **Efficient attention** → Phase 09 (08-efficient-attention), Phase 06 (20-transformer-variants)
- **Eigenvalues** → Phase 01 (08-eigenvalues), Phase 05 (21-pca)
- **EM algorithm** → Phase 05 (18-gmm)
- **Embeddings (word)** → Phase 09 (03-word-embeddings)
- **Empirical processes** → Phase 03 (30-empirical-processes)
- **Energy-based models** → Phase 07 (16-ebms), Phase 04 (29-stat-mech)
- **Ensemble methods** → Phase 05 (07-random-forest, 08-gradient-boosting, 42-stacking), scikit-learn (15-ensemble-methods)
- **Entropy** → Phase 04 (01-entropy), Phase 05 (06-decision-trees)
- **Experiment tracking** → Phase 11 (01-experiment-tracking), pytorch (29-tensorboard)
- **Exponential family** → Phase 03 (15-exponential-family)
- **Extreme value theory** → Phase 03 (31-extreme-value-theory)
- **FastAPI** → fastapi (all), Phase 09 (LLM serving), Phase 11 (model serving), Phase 12 (deployment)
- **Feature detection (CV)** → Phase 08 (02-feature-detection)
- **Feature engineering** → Phase 11 (03-feature-engineering), scikit-learn (11-feature-engineering)
- **Feature selection** → Phase 04 (36-feature-selection), scikit-learn (12-feature-selection)
- **Fine-tuning (efficient)** → Phase 09 (10-efficient-finetuning), pytorch (27-fine-tuning)
- **Fisher information** → Phase 04 (04-fisher-information)
- **Fixed-point iteration** → Phase 04 (27-fixed-point), Phase 07 (05-deq)
- **Flask** → flask (all), Phase 11 (model serving)
- **Flow matching** → Phase 07 (21-flow-matching)
- **Forward-mode autograd** → Phase 06 (03-forward-mode-autograd)
- **Fourier transforms** → Phase 04 (17-fourier-wavelet)
- **Game theory** → Phase 04 (33-game-theory), Phase 10 (11-multi-agent)
- **GANs** → Phase 07 (23-gans), Phase 08 (23-image-to-image)
- **Gaussian mixture models (GMM)** → Phase 05 (18-gmm)
- **Gaussian processes** → Phase 03 (25-gaussian-processes), Phase 05 (26-gp)
- **Generalized eigenvalues** → Phase 01 (20-generalized-eigenvalue)
- **Generalized linear models (GLMs)** → Phase 03 (22-glms), Phase 05 (03-glms)
- **Genetic algorithms** → Phase 02 (31-genetic-algorithms)
- **Gradient boosting** → Phase 05 (08-gradient-boosting, 09-xgboost, 10-lightgbm, 11-catboost), scikit-learn (16-gradient-boosting)
- **Gradient checkpointing** → Phase 06 (28-gradient-accumulation-checkpointing)
- **Gradient clipping** → Phase 06 (29-gradient-noise-clipping), pytorch (38-gradient-clipping)
- **Gradient descent** → Phase 02 (07-gradient-descent)
- **Graph Laplacians** → Phase 01 (21-graph-laplacians)
- **Graph theory** → Phase 04 (19-graph-theory)
- **Hamiltonian Monte Carlo** → Phase 02 (27-hamiltonian-monte-carlo), Phase 04 (14-riemannian-hmc)
- **Hessian** → Phase 02 (05-hessian)
- **Hidden Markov models (HMM)** → Phase 05 (28-hmm)
- **Hierarchical clustering** → Phase 05 (19-hierarchical)
- **Hierarchical RL** → Phase 10 (13-hierarchical-rl)
- **Hypernetworks** → Phase 07 (07-hypernetworks)
- **Hyperparameter tuning** → Phase 05 (55-automl), scikit-learn (14-hyperparameter-tuning)
- **Hypothesis testing** → Phase 03 (17-hypothesis-testing)
- **ICA (Independent Component Analysis)** → Phase 05 (24-ica)
- **Image processing** → Phase 08 (01-image-processing), Phase 04 (18-signal-processing)
- **Imbalanced learning** → Phase 05 (37-imbalanced), scikit-learn (19-imbalanced-data)
- **Imitation learning** → Phase 10 (12-imitation-learning)
- **Implicit differentiation** → Phase 02 (06-implicit-differentiation)
- **Implicit neural representations** → Phase 07 (06-implicit-neural), Phase 08 (17-neural-rendering)
- **Information geometry** → Phase 04 (08-information-geometry)
- **Initialization (weight)** → Phase 06 (08-initialization), pytorch (39-weight-init)
- **Inference optimization (LLM)** → Phase 09 (15-inference-optimization)
- **Instance segmentation** → Phase 08 (10-instance-segmentation)
- **Kalman filters** → Phase 03 (28-state-space-kalman), Phase 10 (robotics)
- **KAN (Kolmogorov-Arnold Networks)** → Phase 07 (01-kan)
- **Kernel methods** → Phase 04 (09-rkhs), Phase 05 (14-kernel-svm)
- **K-means** → Phase 05 (16-kmeans), scikit-learn (08-kmeans)
- **KNN** → Phase 05 (15-knn), scikit-learn (07-knn)
- **Krylov methods** → Phase 01 (18-krylov-methods)
- **LangChain** → langchain (all), Phase 09 (RAG, agents, chains)
- **Language models** → Phase 09 (04-language-models)
- **Latent diffusion** → Phase 07 (20-latent-diffusion)
- **Layer normalization** → Phase 06 (12-normalization-layers)
- **LDA / QDA** → Phase 05 (05-lda-qda)
- **Learning theory** → Phase 05 (45-learning-theory, 46-pac-bayes)
- **Lie groups** → Phase 04 (22-lie-groups)
- **Linear algebra (NumPy)** → numpy-pandas (05-linear-algebra)
- **Linear programming** → Phase 02 (14-linear-programming)
- **Linear regression** → Phase 03 (21-linear-regression), Phase 05 (01-linear-regression), scikit-learn (02-linear-regression)
- **LLM agents** → Phase 09 (27-agents), langchain (12-agents)
- **LLM evaluation** → Phase 09 (20-llm-evaluation)
- **LLM safety** → Phase 09 (23-safety)
- **LLM serving** → Phase 09 (29-llm-serving), Phase 11 (05-model-serving)
- **LoRA / QLoRA** → Phase 09 (10-efficient-finetuning)
- **Loss functions** → Phase 06 (09-loss-functions), pytorch (08-loss-functions)
- **Loss landscape** → Phase 02 (40-loss-landscape), Phase 06 (30-loss-symmetries)
- **Low-rank approximations** → Phase 01 (11-low-rank-approximations)
- **LR schedulers** → Phase 06 (11-lr-schedulers), pytorch (18-lr-scheduling)
- **LSTM / GRU** → Phase 06 (22-rnn-lstm-gru), pytorch (25-lstm-gru)
- **Mamba (SSM)** → Phase 07 (13-ssms, 14-ssm-variants, 15-hybrid-ssm-attention), Phase 12 (04-mamba-from-scratch)
- **Manifold learning** → Phase 05 (22-tsne-umap, 23-manifold)
- **MAP estimation** → Phase 03 (14-map)
- **Markov chains** → Phase 04 (11-markov-chains), Phase 05 (28-hmm)
- **Matrix completion** → Phase 01 (23-matrix-completion)
- **Matrix functions** → Phase 01 (19-matrix-functions)
- **Matrix norms** → Phase 01 (10-matrix-norms)
- **Maximum entropy** → Phase 04 (03-max-entropy), Phase 05 (30-maxent)
- **MCMC** → Phase 04 (13-mcmc), Phase 07 (24-mcmc)
- **MDP (Markov decision process)** → Phase 10 (01-mdp)
- **MDL / Kolmogorov complexity** → Phase 04 (07-mdll-kolmogorov)
- **Measure theory** → Phase 04 (26-measure-theory)
- **Measurement error** → Phase 03 (39-measurement-error)
- **Medical imaging** → Phase 08 (25-medical-imaging)
- **Meta-learning** → Phase 10 (14-multi-task-meta), Phase 02 (39-learn-to-optimize)
- **Mini-batch selection** → Phase 02 (38-minibatch-selection)
- **Missing data** → Phase 03 (34-missing-data), numpy-pandas (27-missing-data)
- **Mixed effects models** → Phase 03 (23-mixed-effects)
- **Mixed precision training** → Phase 06 (27-mixed-precision), pytorch (32-mixed-precision)
- **Mixture of experts** → Phase 09 (14-mixture-of-experts)
- **ML monitoring** → Phase 11 (06-monitoring), Phase 12 (09-ml-monitoring)
- **MLE (Maximum Likelihood Estimation)** → Phase 03 (13-mle)
- **MLOps** → Phase 11 (all), airflow (all), celery (all)
- **MLP (Multilayer Perceptron)** → Phase 06 (06-perceptron-mlp), pytorch (15-mlp-classification)
- **Model calibration** → scikit-learn (25-model-calibration)
- **Model governance** → Phase 11 (07-model-governance)
- **Model selection** → Phase 05 (48-model-selection)
- **Model serving** → Phase 11 (05-model-serving), fastapi, flask, pytorch (36-torchserve)
- **MoE (Mixture of Experts)** → Phase 09 (14-mixture-of-experts)
- **Momentum (optimization)** → Phase 02 (08-momentum-nesterov)
- **Monte Carlo methods** → Phase 04 (12-monte-carlo), Phase 10 (03-monte-carlo)
- **Multi-agent RL** → Phase 10 (11-multi-agent)
- **Multi-label classification** → Phase 05 (38-multi-label)
- **Multi-object tracking** → Phase 08 (20-multi-object-tracking)
- **Multi-objective optimization** → Phase 02 (29-multi-objective)
- **Multilingual NLP** → Phase 09 (06-multilingual)
- **Multivariate statistics** → Phase 03 (26-multivariate-methods)
- **MuZero** → Phase 10 (08-model-based)
- **Naive Bayes** → Phase 05 (04-naive-bayes), scikit-learn (23-naive-bayes)
- **NAS (Neural Architecture Search)** → Phase 07 (27-nas)
- **Natural gradient** → Phase 02 (23-natural-gradient)
- **NeRF** → Phase 08 (17-neural-rendering), Phase 07 (06-implicit-neural)
- **Neural face models** → Phase 08 (16-neural-face-models)
- **Neural ODEs** → Phase 07 (03-neural-odes)
- **Neural processes** → Phase 07 (11-neural-processes)
- **Neural rendering** → Phase 08 (17-neural-rendering)
- **Neural-symbolic AI** → Phase 07 (26-neural-symbolic)
- **Newton methods** → Phase 02 (10-newton-methods)
- **NMF (Non-negative Matrix Factorization)** → Phase 01 (14-nmf)
- **Normalization layers** → Phase 06 (12-normalization-layers, 26-normalization-alternatives), pytorch (21-batch-norm)
- **Normalizing flows** → Phase 07 (17-normalizing-flows)
- **NumPy arrays** → numpy-pandas (01-arrays, 02-operations, 03-indexing, 04-broadcasting)
- **Object detection** → Phase 08 (09-object-detection)
- **Offline RL** → Phase 10 (10-offline-rl)
- **Online learning** → Phase 05 (33-online-learning)
- **Open-vocabulary detection** → Phase 08 (27-open-vocabulary)
- **Operator splitting** → Phase 02 (20-operator-splitting)
- **Optimal control** → Phase 02 (25-optimal-control)
- **Optimal transport** → Phase 04 (10-optimal-transport)
- **Optimizers** → Phase 06 (10-optimizer-zoo), Phase 02 (36-optimizer-zoo), pytorch (09-optimizers)
- **PAC-Bayes** → Phase 05 (46-pac-bayes)
- **Pandas DataFrames** → numpy-pandas (11-series-dataframe, 12-reading-writing, 13-indexing-selection)
- **Panoptic segmentation** → Phase 08 (12-panoptic-segmentation)
- **PCA** → Phase 05 (21-pca), Phase 01 (08-eigenvalues, 09-svd, 29-pca-svd-pipeline), scikit-learn (09-pca)
- **Perceptron** → Phase 06 (06-perceptron-mlp)
- **Perturbation theory** → Phase 01 (12-perturbation-theory)
- **Physics-informed NNs (PINNs)** → Phase 07 (04-pinns)
- **Pipelines (ML)** → scikit-learn (17-pipeline)
- **Planning (RL)** → Phase 10 (18-planning)
- **Playwright** → playwright (all), Phase 11 (E2E testing of ML UIs)
- **Point clouds** → Phase 08 (18-point-cloud)
- **Policy gradients** → Phase 10 (06-policy-gradient)
- **Pooling** → Phase 06 (16-pooling)
- **Positional encodings** → Phase 06 (19-positional-encodings), Phase 09 (09-positional-encodings)
- **PPO** → Phase 10 (07-advanced-actor-critic)
- **Pruning (model)** → Phase 09 (13-pruning)
- **Pydantic** → pydantic (all), Phase 09 (19-structured-generation), Phase 11 (ML configs)
- **PyTorch** → pytorch (all), Phase 06–12
- **Q-learning** → Phase 10 (04-td-learning)
- **QR decomposition** → Phase 01 (06-qr-decomposition)
- **Quadratic programming** → Phase 02 (15-quadratic-programming)
- **Quantization** → Phase 09 (12-quantization)
- **RAG (Retrieval Augmented Generation)** → Phase 09 (17-rag), langchain (10-retrieval-qa, 20-integration-rag), Phase 12 (06-rag-system)
- **Random forests** → Phase 05 (07-random-forest), scikit-learn (05-random-forests)
- **Random matrix theory** → Phase 01 (16-random-matrix-theory)
- **Random graphs** → Phase 04 (31-random-graphs)
- **Rate-distortion theory** → Phase 04 (05-rate-distortion)
- **Reasoning (math, code)** → Phase 09 (25-reasoning-math)
- **Reinforcement Learning** → Phase 10 (all)
- **Relaxation (optimization)** → Phase 02 (32-relaxation)
- **Representation theory** → Phase 04 (23-representation-theory)
- **Reproducing kernel Hilbert spaces (RKHS)** → Phase 04 (09-rkhs)
- **Responsible AI** → Phase 11 (15-responsible-ai)
- **RLHF** → Phase 10 (16-rlhf), Phase 09 (21-alignment), Phase 12 (05-rlhf-dpo)
- **RNN** → Phase 06 (22-rnn-lstm-gru)
- **Robotics** → Phase 10 (19-robotics)
- **Robust statistics** → Phase 05 (52-robust-statistics)
- **Rule learning** → Phase 05 (51-rule-learning)
- **Safe RL** → Phase 10 (15-safe-rl)
- **scikit-learn pipelines** → scikit-learn (17-pipeline)
- **SDEs (stochastic differential equations)** → Phase 02 (26-sdes), Phase 04 (16-stochastic-calculus), Phase 07 (19-diffusion)
- **Segmentation (semantic)** → Phase 08 (11-semantic-segmentation)
- **Self-supervised learning** → Phase 08 (08-self-supervised-vision), Phase 07 (28-contrastive-learning)
- **Semidefinite programming** → Phase 02 (16-semidefinite-programming)
- **Semi-supervised learning** → Phase 05 (36-semi-supervised)
- **Seq2seq** → Phase 06 (23-seq2seq)
- **Signal processing** → Phase 04 (18-signal-processing)
- **Skip connections** → Phase 06 (25-skip-connections)
- **Sparse matrices** → Phase 01 (17-sparse-matrices)
- **Spectral clustering** → Phase 01 (21-graph-laplacians, 22-spectral-graph-theory), Phase 05 (20-spectral)
- **Spiking neural networks** → Phase 07 (08-spiking-nns)
- **SQLAlchemy** → sqlalchemy (all), Phase 11 (ML metadata storage)
- **SSMs (State Space Models)** → Phase 07 (13-ssms, 14-ssm-variants)
- **Stacking / blending** → Phase 05 (42-stacking), scikit-learn (29-stacking-blending)
- **Statistical mechanics** → Phase 04 (29-stat-mech, 30-stat-physics-learning)
- **Stochastic calculus** → Phase 04 (16-stochastic-calculus)
- **Stochastic processes** → Phase 04 (15-stochastic-processes)
- **Streaming ML** → Phase 05 (53-streaming)
- **Structured generation (LLM)** → Phase 09 (19-structured-generation), pydantic
- **Subgroup discovery** → Phase 05 (50-subgroup-discovery)
- **Super-resolution** → Phase 08 (24-super-resolution)
- **Survival analysis** → Phase 03 (29-survival-analysis)
- **SVD** → Phase 01 (09-svd), Phase 05 (21-pca)
- **SVM** → Phase 05 (13-svm, 14-kernel-svm), scikit-learn (06-svm)
- **Symplectic geometry** → Phase 04 (24-symplectic-geometry)
- **Taylor series** → Phase 02 (03-taylor-series)
- **Tensor decompositions** → Phase 01 (15-tensor-decompositions, 24-tensor-methods, 25-indscal-parafac2, 26-constrained-cp, 27-tensor-networks)
- **Tensor networks** → Phase 01 (27-tensor-networks)
- **Testing ML code** → Phase 11 (14-testing-for-ml), pytest-deep (all)
- **Time series** → Phase 03 (27-time-series), numpy-pandas (18-time-series)
- **Tokenization** → Phase 09 (02-tokenization)
- **Topological data analysis (TDA)** → Phase 04 (20-tda)
- **Transfer learning** → pytorch (26-transfer-learning)
- **Transformer** → Phase 06 (18-transformer-blocks, 20-transformer-variants), Phase 08 (07-vision-transformers), Phase 09 (05-encoder-decoder), Phase 12 (02-transformer-from-scratch)
- **t-SNE** → Phase 05 (22-tsne-umap)
- **U-Net** → Phase 08 (11-semantic-segmentation)
- **VAEs** → Phase 07 (22-vaes)
- **Variance-reduced SGD** → Phase 02 (21-variance-reduced-sgd)
- **Vector spaces** → Phase 01 (02-vector-spaces)
- **Video generation** → Phase 08 (22-video-generation)
- **Video understanding** → Phase 08 (21-video-understanding)
- **Vision Transformers (ViT)** → Phase 08 (07-vision-transformers)
- **Visual RL** → Phase 08 (29-visual-rl)
- **VQA (Visual Question Answering)** → Phase 08 (26-vqa-captioning)
- **Wasserstein distance** → Phase 04 (10-optimal-transport), Phase 07 (23-gans)
- **Watermarking (LLM)** → Phase 09 (24-watermarking)
- **Wavelet transforms** → Phase 04 (17-fourier-wavelet)
- **Weight initialization** → Phase 06 (08-initialization)
- **Word embeddings** → Phase 09 (03-word-embeddings)
- **XGBoost** → Phase 05 (09-xgboost)
- **YOLO** → Phase 08 (09-object-detection)
- **Zero-order optimization** → Phase 02 (30-zeroth-order)

---

*Generated from machine-learning/ (12 phases, ~391 lessons) and python-frameworks/ (13 frameworks, ~345 lessons)*
