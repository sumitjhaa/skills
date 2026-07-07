# 📝 scikit-learn — Phase 01 Practice (Classification)

## Exercise 1: Train/Test Split

Load `load_diabetes()` from sklearn. Split 80/20 with `random_state=42`. Scale features with `StandardScaler`. Train a `LinearRegression` and report R² on test set.

## Exercise 2: Logistic Regression

Generate a classification dataset with `make_classification(n_samples=500, n_features=5, random_state=42)`. Train a `LogisticRegression` and compute accuracy, precision, recall, F1, and a confusion matrix.

## Exercise 3: Decision Tree Depth

Train a `DecisionTreeClassifier` on `load_iris()`. Vary `max_depth` from 1 to 10 and plot (or print) train vs test accuracy for each depth. Identify the optimal depth.

## Exercise 4: Random Forest vs Single Tree

Compare a single `DecisionTreeClassifier` (max_depth=10) with a `RandomForestClassifier` (n_estimators=100, max_depth=10) on `make_classification(n_samples=1000)`. Report accuracy and training time for each.

## Exercise 5: SVM Kernel Comparison

Train SVMs with linear, poly, and RBF kernels on `load_breast_cancer()`. Compare accuracy and number of support vectors for each kernel.

## Exercise 6: KNN Parameter Sweep

Train `KNeighborsClassifier` on `load_wine()` with `n_neighbors` from 1 to 20. Find the best k. Report test accuracy.

## Exercise 7: K-Means Evaluation

Generate 4 well-separated blobs with `make_blobs()`. Run K-Means with k=2..8, compute inertia and silhouette score for each. Identify the optimal k.

## Exercise 8: PCA Visualization

Load `load_digits()`. Reduce to 2 components with PCA. Plot the resulting 2D projection colored by digit label. Report explained variance ratio for each component.

## Exercise 9: Full Classification Pipeline

Build a pipeline: `StandardScaler` → `SelectKBest(k=5)` → `RandomForestClassifier`. Tune `n_estimators` and `max_depth` with GridSearchCV on `load_breast_cancer()`. Report best params and test accuracy.

## Exercise 10: Fraud Detection

Generate `make_classification(n_samples=2000, weights=[0.95], flip_y=0.01)` for imbalanced data. Split, scale, train a `LogisticRegression`. Compare accuracy vs balanced accuracy. Check if the model predicts any positives.
