"""Group operations — groupby, agg, transform, filter."""
import pandas as pd
import numpy as np


print("=== Group Operations ===")

rng = np.random.default_rng(42)
df = pd.DataFrame({
    "department": rng.choice(["Engineering", "Sales", "Marketing"], 20),
    "team": rng.choice(["Alpha", "Beta", "Gamma"], 20),
    "salary": rng.integers(50000, 150000, 20),
    "experience": rng.integers(1, 15, 20),
    "name": [f"Employee_{i}" for i in range(20)],
})
print(f"Data (first 5):\n{df.head()}")

print(f"\nMean salary by department:\n{df.groupby('department')['salary'].mean()}")

print(f"\nMultiple aggregations:\n{df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    std_salary=('salary', 'std'),
    max_exp=('experience', 'max'),
    count=('name', 'count'),
)}")

print(f"\nGroupby multiple keys:")
print(df.groupby(['department', 'team'])['salary'].mean())

print(f"\nTransform (centering):")
df['salary_centered'] = df.groupby('department')['salary'].transform(
    lambda x: x - x.mean()
)
print(df[['department', 'salary', 'salary_centered']].head())

print(f"\nFilter (departments with >= 5 employees):")
filtered = df.groupby('department').filter(lambda x: len(x) >= 5)
print(filtered['department'].value_counts())
