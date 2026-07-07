# 📝 NumPy & Pandas — Phase 02 Practice (Pandas Basics)

## Exercise 1: DataFrame Construction

Create a DataFrame from a list of 50 dicts (each with: name, age, city, salary, department). Add a column for salary after a 10% raise. Filter to employees over 30 in Engineering. Find the average salary per city.

## Exercise 2: Data Cleaning

Load a CSV (or create a DataFrame with intentional mess): missing values, duplicate rows, mixed date formats, string whitespace. Clean it:
- Fill missing numeric with median
- Drop duplicate rows
- Standardize dates to YYYY-MM-DD
- Strip whitespace from strings

## Exercise 3: Sales Analysis

Given a DataFrame with columns: date, product, region, units_sold, price. Compute:
- Total revenue per region
- Monthly revenue trend
- Top 3 products by revenue
- Each product's contribution % to total revenue

## Exercise 4: Merge Challenge

Create `customers` (id, name, signup_date) and `orders` (id, customer_id, amount, date). Answer:
- Which customers haven't ordered in the last 90 days?
- What's the average time between signup and first order?
- Which customers have spent more than the median?

## Exercise 5: Time Series

Generate 2 years of daily temperature data (seasonal pattern + noise). Compute:
- Monthly average temperature
- Day-of-year with highest/lowest average
- Number of days above a threshold
- Rolling 7-day mean

## Exercise 6: EDA Report

Find a dataset (or create one) with 500+ rows, 8+ columns, mix of numeric and categorical. Write a function that produces a complete EDA report: shape, dtypes, missing %, summary stats, correlation heatmap, top category values, and 3 key insights.
