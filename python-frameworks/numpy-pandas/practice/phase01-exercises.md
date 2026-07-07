# 📝 NumPy & Pandas — Phase 01 Practice (NumPy)

## Exercise 1: Array Creation

Create a 5×5 array of random integers between 0 and 100. Find the min, max, mean, and standard deviation of each row and each column.

## Exercise 2: Boolean Masking

Generate a 10×4 array of random normal values. Find values > 2 standard deviations from the mean. Replace them with the column mean.

## Exercise 3: Broadcasting

Create a 2D array of shape (5, 3) and a 1D array of shape (3,). Use broadcasting to:
- Add the 1D array to each row
- Compute the Euclidean distance of each row from the origin
- Normalize each row to unit length

## Exercise 4: Linear Algebra

Generate a 3×3 random matrix. Compute:
- Its determinant and inverse
- Eigenvalues and eigenvectors
- Verify that A @ inv(A) ≈ identity

## Exercise 5: Simulation

Simulate a stock price over 252 trading days using: `price[t] = price[t-1] * (1 + normal(0, 0.01))`. Start at $100. Compute daily returns, rolling 20-day volatility, and max drawdown.

## Exercise 6: Data Pipeline

Create a pipeline that:
1. Generates 1000 samples with 5 features (mix of normal, uniform, categorical)
2. Removes outliers (any row with Z-score > 3)
3. Normalizes to [0, 1]
4. Computes correlation matrix
5. Saves the cleaned data to a .npz file
