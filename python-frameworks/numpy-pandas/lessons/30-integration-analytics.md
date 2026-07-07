# 🏁 Integration: Full Analysis Project
<!-- ⏱️ 30 min | 🔴 Advanced -->

**What You'll Learn:** End-to-end data analysis combining all skills.

## Project: Customer Analytics

1. **Generate** synthetic customer dataset (transactions, demographics)
2. **Clean** (missing values, outliers, type fixes)
3. **Explore** (group summaries, correlations, distributions)
4. **Feature engineer** (cohorts, RFM, behavioral metrics)
5. **Aggregate** (segment summaries, trends)
6. **Report** (key findings as DataFrame + text)

## Concepts Used

- MultiIndex for customer × month
- Pivot tables for segment × metric
- Rolling windows for trends
- GroupBy with custom aggs for RFM
- Categorical dtypes for segments

## Key Outputs

| Metric | Method |
|--------|--------|
| Customer lifetime value | GroupBy sum + percentile rank |
| Monthly active users | Date resample + nunique |
| Segment profiles | Pivot table with means |
| Spending trends | Rolling mean per cohort |

<!-- 🧠 This integration ties everything together — run it and inspect the output. -->

## Run the Code

```bash
python code/30-integration-analytics.py
```
