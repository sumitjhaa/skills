"""Apply and transform — vectorized ops, map, apply."""
import pandas as pd
import numpy as np


print("=== Apply & Transform ===")

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [25, 30, 35, 28],
    "city": ["NYC", "SF", "LA", "NYC"],
    "salary": [70000, 120000, 90000, 85000],
})

print(f"Data:\n{df}")

print(f"\nApply on column:")
df["age_bucket"] = df["age"].apply(
    lambda x: "young" if x < 30 else ("mid" if x < 35 else "senior")
)
print(df[["name", "age", "age_bucket"]])

print(f"\nApply on rows:")
df["label"] = df.apply(
    lambda row: f"{row['name']} - {row['city']} (${row['salary']:,})", axis=1
)
print(df[["name", "label"]])

print(f"\nMap:")
city_rank = {"NYC": "A", "SF": "A", "LA": "B"}
df["city_tier"] = df["city"].map(city_rank)
print(df[["name", "city", "city_tier"]])

print(f"\nVectorized (fastest):")
df["salary_class"] = "mid"
df.loc[df["salary"] < 80000, "salary_class"] = "low"
df.loc[df["salary"] > 100000, "salary_class"] = "high"
print(df[["name", "salary", "salary_class"]])

print(f"\nTransform with groupby:")
df["city_avg_salary"] = df.groupby("city")["salary"].transform("mean")
df["salary_diff"] = df["salary"] - df["city_avg_salary"]
print(df[["name", "city", "salary", "salary_diff"]])
