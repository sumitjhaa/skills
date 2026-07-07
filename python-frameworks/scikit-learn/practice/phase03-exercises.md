# 📝 scikit-learn — Phase 03 Practice (Advanced Topics)

## Exercise 1: Polynomial vs Linear

Generate `y = sin(x) + noise` with 100 points. Compare `LinearRegression` vs `Pipeline([('poly', PolynomialFeatures(degree=5)), ('linear', LinearRegression())])`. Plot or print the MSE for both.

## Exercise 2: Ridge Path

Train `Ridge` on `load_diabetes()` for alpha values [0.001, 0.01, 0.1, 1, 10, 100]. Print the coefficient magnitudes for each alpha. Describe what happens as alpha increases.

## Exercise 3: Naive Bayes on Text

Use `load_digits()` (each pixel is a feature). Train `GaussianNB`, `MultinomialNB`, and `BernoulliNB`. Compare accuracy. Which one works best for pixel data and why?

## Exercise 4: Clustering Comparison

Generate `make_blobs(n_samples=500, centers=4)`. Run K-Means, DBSCAN (eps=0.5), and Agglomerative clustering. Compare adjusted Rand index and silhouette score for each against the true labels.

## Exercise 5: Probability Calibration

Train an uncalibrated `SVC` and a `CalibratedClassifierCV` on `make_classification(n_samples=500)`. Compare Brier scores and the mean predicted probabilities.

## Exercise 6: Learning Curve Diagnosis

Train a `DecisionTreeClassifier` (max_depth=20) on `make_classification(n_samples=300)`. Plot (or print) the learning curve. Is the model overfitting or underfitting? How can you tell?

## Exercise 7: Custom Transformer

Create a custom `FunctionTransformer` that applies a log transformation to positive features. Build a pipeline: log_transform → `StandardScaler` → `LinearRegression`. Test on `make_regression()`.

## Exercise 8: Stacking Ensemble

Create a `StackingClassifier` with `RandomForestClassifier`, `SVC`, and `KNeighborsClassifier` as base models and `LogisticRegression` as final estimator. Compare against each base model on `load_breast_cancer()`.

## Exercise 9: Full ML Pipeline

Design a pipeline for `load_wine()` that includes:
- Feature scaling
- Dimensionality reduction (PCA)
- Feature selection (SelectKBest)
- Classifier (RandomForest or GradientBoosting)
- Hyperparameter tuning with GridSearchCV
- Model persistence with joblib

Report the best params and all evaluation metrics.

## Exercise 10: Model Selection Study

For `load_breast_cancer()`, compare 6 models: LR, KNN, DT, RF, SVM, GB. Use cross_val_score with cv=5. Rank by mean accuracy. Then take the top 2 and create a stacking ensemble. Does stacking beat the single best model?
