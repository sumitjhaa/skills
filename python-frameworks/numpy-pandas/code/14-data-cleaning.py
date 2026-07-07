"""Data cleaning — missing values, duplicates, type conversion."""
import pandas as pd
import numpy as np


print("=== Data Cleaning ===")

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", None, "Frank"],
    "age": [25, None, 35, 28, 30, None],
    "email": ["alice@a.com", "bob@b.com", None, "diana@d.com", "eve@e.com", None],
    "salary": [70000, 120000, 90000, None, None, 85000],
})
print(f"Raw data:\n{df}")

print(f"\nMissing values:\n{df.isna().sum()}")
print(f"\nDrop rows with any NaN:\n{df.dropna()}")
print(f"Drop if email is NaN:\n{df.dropna(subset=['email'])}")

df_clean = df.copy()
df_clean["age"].fillna(df_clean["age"].median(), inplace=True)
df_clean["salary"].fillna(df_clean["salary"].mean(), inplace=True)
df_clean["email"].fillna("unknown@unknown.com", inplace=True)
df_clean["name"].fillna("UNKNOWN", inplace=True)
print(f"\nAfter filling:\n{df_clean}")

print(f"\nDuplicates:")
df_dup = pd.concat([df_clean, df_clean.iloc[[0]]], ignore_index=True)
print(f"  Rows: {len(df_dup)}, Duplicates: {df_dup.duplicated().sum()}")
print(f"  Drop duplicates:\n{df_dup.drop_duplicates()}")

print(f"\nType conversion:")
df["age"] = df["age"].astype(float)
print(f"  age dtype: {df['age'].dtype}")

print(f"\nString cleaning:")
df["email_lower"] = df["email"].str.lower().str.strip()
print(email_lower := df["email_lower"].tolist())
