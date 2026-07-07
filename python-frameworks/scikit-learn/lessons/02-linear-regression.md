# 📈 Linear Regression
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Fit a linear model, interpret coefficients, evaluate with R² and MSE.

## Training

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

## Coefficients

```python
model.coef_       # Feature weights
model.intercept_  # Bias term
```

## Prediction & Evaluation

```python
from sklearn.metrics import mean_squared_error, r2_score

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

## Assumptions

- Linear relationship between features and target
- No multicollinearity among features
- Homoscedasticity (constant variance of errors)
- Normally distributed residuals

<!-- 🤔 R² close to 1 = good fit. R² near 0 = model no better than mean. -->

## Run the Code

```bash
python code/02-linear-regression.py
```
