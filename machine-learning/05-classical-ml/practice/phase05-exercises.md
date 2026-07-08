# Phase 05 Exercises: Classical Machine Learning

## About
These ~20 exercises reinforce the 55 lessons. Implement or analyze algorithms from scratch.

## Exercises

### 1. Linear Regression — Normal Equations
Derive the normal equation for ridge regression. Implement a `RidgeClosedForm` class that:
- Uses `np.linalg.solve` instead of `lstsq`
- Supports fit_intercept parameter
- Test with `make_regression` and compare to sklearn

### 2. Logistic Regression — Multinomial
Extend the logistic regression code (`02-logistic-regression.py`) to handle multiclass using softmax and cross-entropy. Compare to `sklearn.linear_model.LogisticRegression(multi_class='multinomial')`.

### 3. Naive Bayes — Text Classification
Implement a `MultinomialNB` for text: use bag-of-words features from 20 Newsgroups. Add Laplace smoothing and log-space computation. Compare to sklearn.

### 4. Decision Tree — Pruning
Add cost-complexity pruning to the Decision Tree implementation. Implement a function that finds the optimal $\alpha$ subtree using validation data. Plot accuracy vs $\alpha$.

### 5. Random Forest — Feature Importance
Extend the RF implementation to track feature importance via mean decrease in impurity and permutation importance. Compare the rankings.

### 6. Gradient Boosting — Huber Loss
Modify the gradient boosting code to use Huber loss (mixed L1/L2) for robustness. Compare MSE with standard L2 boosting on data with outliers.

### 7. SVM — Visualize Decision Boundary
Use the SMO-based SVM on 2D data (`make_moons`, `make_circles`). Visualize the decision boundary and support vectors. Use linear and RBF kernels.

### 8. k-Means — Elbow & Silhouette
Implement the elbow method and silhouette score from scratch. Compute both for k=1..10 on `make_blobs` and identify the optimal k.

### 9. DBSCAN — Parameter Sensitivity
Run DBSCAN on `make_moons` with different `eps` values (0.1, 0.2, 0.5, 1.0) and min_samples values (2, 5, 10). Visualize and discuss the results.

### 10. PCA — Eigenfaces
Apply the PCA implementation to the Olivetti faces dataset (from sklearn). Visualize the top 10 eigenfaces. Plot cumulative explained variance vs components.

### 11. t-SNE — Parameter Effects
Run the t-SNE implementation on `make_swiss_roll` with perplexity values 5, 30, 50. Visualize and discuss how perplexity changes the embedding.

### 12. Gaussian Processes — Kernel Design
Implement a periodic kernel and a Matérn kernel. Compare GP regression with RBF, periodic, and Matérn kernels on a periodic function `sin(2x) + sin(5x)`.

### 13. HMM — Part-of-Speech Tagging
Use the HMM implementation for a simplified POS tagging task. Define 3 states (NOUN, VERB, DET) and emission probabilities. Run Viterbi decoding on a test sentence.

### 14. Anomaly Detection — Outlier Detection
Compare Isolation Forest, LOF (implement simple version), and Z-score on synthetic data with outliers. Report precision and recall.

### 15. Bandits — Regret Analysis
Simulate epsilon-greedy (eps=0.01, 0.1, 0.3), UCB, and Thompson sampling on 5-armed bandit for 10,000 rounds. Plot cumulative regret curves.

### 16. SMOTE — Visualization
Apply SMOTE to 2D imbalanced data (10:1 ratio). Visualize the original and synthetic points. Train a classifier before and after SMOTE and compare decision boundaries.

### 17. Apriori — Market Basket Analysis
Run Apriori on the `groceries` dataset (from mlxtend or create synthetic). Find rules with lift > 2. Report interesting rules.

### 18. Model Selection — AIC vs BIC
Simulate polynomial regression with degrees 1-15. Compute AIC, BIC, and CV error. Find the degree selected by each criterion. Discuss.

### 19. Bayesian Optimization — Hyperparameter Tuning
Use the Bayesian optimization code to tune `C` and `gamma` of an RBF SVM on a classification dataset. Compare to random search over the same budget.

### 20. Stacking — Ensemble Design
Build a stacking ensemble with base models: DecisionTree, SVM, k-NN, and meta-model: LogisticRegression. Compare the stacking performance to each individual model and to a simple voting ensemble.

### 21. Robust Statistics — Breakdown Point
Demonstrate the breakdown point of mean, median, and Huber estimator by gradually increasing contamination from 0% to 50%. Plot the estimated value vs contamination fraction.

### 22. Streaming — Count-Min Sketch Accuracy
Insert 10,000 items into Count-Min Sketch. Query 100 items and measure the estimation error. Vary the width (50, 100, 500) and depth (3, 5, 10). Plot error vs parameters.

## How to Submit
Complete each exercise in a separate `.py` or `.ipynb` file. Include:
- Implementation
- Test on synthetic/real data
- Comparison against scikit-learn (where applicable)
- Visualization (where applicable)
- Brief discussion of results
