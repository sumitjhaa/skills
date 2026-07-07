# 📝 NumPy & Pandas — Phase 03 Practice (Advanced)

## Exercise 1: MultiIndex Stock Data

Create a MultiIndex DataFrame with (ticker, date) as index. Columns: open, high, low, close, volume for 3 tickers over 100 days. Compute:
- Monthly return per ticker
- Correlation between tickers
- Rolling 20-day volatility per ticker
- Best/worst performing ticker each month

## Exercise 2: Pivot Table Dashboard

Create a sales dataset with: year, quarter, region, product_category, salesperson, amount. Build a pivot table dashboard:
- Year × Region (sum of sales)
- Product Category × Quarter (mean of sales)
- Salesperson ranking with totals

## Exercise 3: Missing Data Strategy

Create a dataset with 30% missing values in 3 patterns: MCAR, MAR, MNAR. Compare imputation strategies: mean, median, forward fill, linear interpolation, group median. Measure which gives the closest to true values.

## Exercise 4: Performance Optimization

Start with a DataFrame of 1M rows and 10 columns. Measure and improve:
- Memory usage (optimize dtypes)
- Filtering speed (query vs mask)
- GroupBy speed (category vs object)
- Apply vs vectorized operations
Report improvements as a table.

## Exercise 5: Customer Analytics

Use the Phase 03 integration project concepts to analyze a new dataset:
- Compute RFM scores
- Segment customers into quartiles
- Build a churn prediction feature set
- Profile each segment with mean/median stats

## Exercise 6: Full Pipeline

Build a complete analysis pipeline for a dataset of your choice:
1. Load & inspect
2. Clean & validate
3. Feature engineer (at least 5 new features)
4. Aggregate & summarize
5. Visualize (at least 3 plots)
6. Export cleaned data + summary report
