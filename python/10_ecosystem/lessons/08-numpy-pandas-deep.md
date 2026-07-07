# 📈 NumPy & Pandas Deep
<!-- ⏱️ 20 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** NumPy broadcasting, vectorization, advanced indexing; Pandas groupby, merge/join, pivot tables, rolling windows, datetime handling, and custom aggregations.

> 💡 **TL;DR — The whole point:** NumPy broadcasting eliminates loops. Pandas groupby + agg = SQL GROUP BY on steroids. Merge/join combine DataFrames. Rolling windows compute moving averages. Vectorized operations beat Python loops by 100×.

## 🔗 Why This Matters
A social-media analytics dashboard processes daily metrics for 10K users over 3 years — that's 11M data points. Computing weekly average engagement, comparing cohorts, and finding trends requires vectorized operations. Python loops would take hours; NumPy/Pandas does it in seconds.

## The Concept
- **Broadcasting:** NumPy automatically expands dimensions for element-wise operations
- **Vectorization:** apply operations to entire arrays without explicit loops
- **`groupby` + `agg`:** split-apply-combine with multiple aggregations
- **`merge`/`join`:** SQL-like joins between DataFrames
- **`pivot_table`:** spreadsheets-style cross-tabulation
- **`rolling`:** sliding window operations (moving average, etc.)
- **`dt` accessor:** datetime components (year, month, day, weekday)

## Code Example
```python
"""Social-media analytics: advanced NumPy/Pandas patterns."""

import numpy as np
import pandas as pd

# ─── NumPy Broadcasting ───
likes = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
boost = np.array([1.0, 1.5, 2.0])  # per-day boost factor
boosted = likes * boost  # broadcasting: (3,3) * (3,) = (3,3)
print(f"Broadcasting:\n{boosted}")

# ─── Vectorized condition ───
np.where(boosted > 100, "viral", "normal")

# ─── Pandas: time series ───
dates = pd.date_range("2025-01-01", periods=365, freq="D")
np.random.seed(42)
df = pd.DataFrame({
    "date": dates,
    "user_id": np.random.choice(range(1000), size=365),
    "likes": np.random.poisson(lam=50, size=365),
    "shares": np.random.poisson(lam=10, size=365),
    "comments": np.random.poisson(lam=5, size=365),
})
df["week"] = df["date"].dt.isocalendar().week.astype(int)
df["month"] = df["date"].dt.month
print(f"\nDataFrame: {len(df)} rows")

# ─── Groupby + agg ───
weekly = df.groupby("week").agg(
    total_likes=("likes", "sum"),
    avg_shares=("shares", "mean"),
    total_comments=("comments", "sum"),
    post_count=("likes", "count"),
).reset_index()
print(f"\nWeekly stats:\n{weekly.head()}")

# ─── Rolling window ───
df_sorted = df.sort_values("date").set_index("date")
df_sorted["likes_ma7"] = df_sorted["likes"].rolling(7).mean()
print(f"\n7-day moving average (first 10):")
print(df_sorted[["likes", "likes_ma7"]].head(10))

# ─── Pivot table ───
pivot = df.pivot_table(
    values="likes",
    index="month",
    columns="user_id",
    aggfunc="mean",
)
print(f"\nPivot table (month × user): {pivot.shape}")

# ─── Custom aggregation ───
def engagement_ratio(group: pd.DataFrame) -> float:
    return group["likes"].sum() / max(group["shares"].sum(), 1)

top_users = df.groupby("user_id").apply(engagement_ratio).sort_values(ascending=False)
print(f"\nTop 3 users by engagement ratio:\n{top_users.head(3)}")

# ─── Merge (simulated user metadata) ───
users_df = pd.DataFrame({
    "user_id": range(1000),
    "region": np.random.choice(["NA", "EU", "APAC", "LATAM"], size=1000),
})
merged = df.merge(users_df, on="user_id")
region_stats = merged.groupby("region")["likes"].describe()
print(f"\nRegion stats:\n{region_stats}")
```

## 🔍 How It Works
- Broadcasting: `arr * np.array([1, 2, 3])` — NumPy aligns shapes, expanding the smaller array
- `df.groupby("week").agg(total_likes=("likes", "sum"))` — name the output column, pick the source column, pick the aggregation function
- `df.rolling(7).mean()` — sliding window of 7 rows, computes mean at each position
- `pivot_table(index="month", columns="user_id", values="likes", aggfunc="mean")` — spreadsheet-style cross-tab
- `df.merge(users_df, on="user_id")` — SQL INNER JOIN by default (use `how="left"` for LEFT JOIN)
- `df["date"].dt.month` — extract month from datetime column

## ⚠️ Common Pitfall
Using `apply()` with a Python loop function on large DataFrames. `apply` is syntactic sugar for a for-loop and can be 100× slower than vectorized operations. Prefer `groupby().agg()` with built-in functions (`sum`, `mean`, `std`) over `apply`.

## 🧠 Memory Aid
"Broadcasting = auto dimension expansion. Vectorized = no loops. groupby + agg = split+apply+combine. merge = SQL join. rolling = moving window. pivot = Excel cross-tab."

## 🏃 Try It
Load a CSV of daily website visits (date, page, visits, unique_visitors). Compute weekly total visits per page. Find the page with the highest average weekly visits. Plot a 7-day rolling average for that page.

## 🔗 Related
- [Data Science Introduction](04-data-science-intro.md) — NumPy/Pandas basics
- [FastAPI Deep](06-fastapi-deep.md) — serve analytics via API

## ➡️ Next
[Deployment & Monitoring](09-deployment-monitoring.md)
