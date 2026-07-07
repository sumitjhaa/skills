# 📝 scikit-learn — Phase 02 Practice (Modeling Workflow)

## Exercise 1: Feature Engineering

Create a dataset with 3 numeric features and 2 categorical features. Use `PolynomialFeatures(degree=2)` and `OneHotEncoder` in a `ColumnTransformer`. Train a ridge regression and compare R² with and without feature engineering.

## Exercise 2: Feature Selection

Load `load_diabetes()`. Compare `SelectKBest` (k=3), `RFE` (n_features_to_select=3), and `SelectFromModel` (using Lasso) for feature selection. Report which features each method selects and the resulting R².

## Exercise 3: Cross-Validation

Compare 5-fold CV scores for `LinearRegression`, `Ridge`, and `Lasso` on `load_diabetes()`. Report mean ± std for each. Identify the most stable model.

## Exercise 4: Grid vs Random Search

Use both `GridSearchCV` and `RandomizedSearchCV` to tune `RandomForestClassifier` on `load_breast_cancer()`. Compare the best params found and total search time.

## Exercise 5: Ensemble Voting

Create a voting classifier with `LogisticRegression`, `RandomForestClassifier`, and `GradientBoostingClassifier` on `make_classification(n_samples=1000)`. Compare accuracy of each individual model vs the ensemble (hard and soft voting).

## Exercise 6: Gradient Boosting Tuning

Train a `GradientBoostingClassifier` on `load_wine()`. Tune `learning_rate` (0.01, 0.1, 0.2), `n_estimators` (50, 100, 200), and `max_depth` (2, 3, 4) with GridSearchCV. Report best params and test accuracy.

## Exercise 7: Pipeline Export

Build a pipeline: `StandardScaler` → `PCA(n_components=5)` → `LogisticRegression`. Fit on `load_breast_cancer()`, save with `joblib`, load it back, and verify predictions match.

## Exercise 8: Model Evaluation

Train 3 classifiers on `load_breast_cancer()`. Plot (or print as table) their:
- Accuracy, precision, recall, F1, ROC-AUC
- Confusion matrix
- Classification report

Rank models by F1 score.

## Exercise 9: Imbalanced Data

Generate `make_classification(n_samples=2000, weights=[0.9])`. Compare a baseline `LogisticRegression` with one using `class_weight='balanced'`. Report accuracy, balanced accuracy, and recall for the minority class.

## Exercise 10: Regression Pipeline

Build a full regression pipeline for `load_diabetes()`:
1. Scale features
2. Select top 4 features with SelectKBest
3. Train a Ridge regressor
4. Tune alpha with GridSearchCV
5. Report R², MAE, RMSE on test set
