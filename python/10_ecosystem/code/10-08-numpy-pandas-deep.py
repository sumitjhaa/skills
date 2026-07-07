"""NumPy & Pandas Deep — broadcasting, groupby, merge, rolling, pivot.
Run: python 10-08-numpy-pandas-deep.py
"""

import numpy as np
import pandas as pd

likes = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
boost = np.array([1.0, 1.5, 2.0])
boosted = likes * boost
print(f"Broadcasting:\n{boosted}")

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

weekly = df.groupby("week").agg(
    total_likes=("likes", "sum"),
    avg_shares=("shares", "mean"),
    total_comments=("comments", "sum"),
    post_count=("likes", "count"),
).reset_index()
print(f"\nWeekly stats:\n{weekly.head()}")

df_sorted = df.sort_values("date").set_index("date")
df_sorted["likes_ma7"] = df_sorted["likes"].rolling(7).mean()
print(f"\n7-day moving average (first 10):")
print(df_sorted[["likes", "likes_ma7"]].head(10))

pivot = df.pivot_table(values="likes", index="month", columns="user_id", aggfunc="mean")
print(f"\nPivot table (month x user): {pivot.shape}")


def engagement_ratio(group: pd.DataFrame) -> float:
    return group["likes"].sum() / max(group["shares"].sum(), 1)


top_users = df.groupby("user_id").apply(engagement_ratio).sort_values(ascending=False)
print(f"Top 3 users by engagement ratio:\n{top_users.head(3)}")

users_df = pd.DataFrame({
    "user_id": range(1000),
    "region": np.random.choice(["NA", "EU", "APAC", "LATAM"], size=1000),
})
merged = df.merge(users_df, on="user_id")
region_stats = merged.groupby("region")["likes"].describe()
print(f"\nRegion stats:\n{region_stats}")
