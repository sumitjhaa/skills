# 🧹 Data Cleaning
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Handle missing values, duplicates, string cleaning, type conversion.

## Missing Values

```python
df.isna().sum()           # Count missing per column
df.dropna()               # Drop rows with any NaN
df.dropna(subset=["email"])  # Drop if email is NaN
df.fillna(0)              # Fill with value
df.fillna({"age": df["age"].median()})  # Fill with median
df.ffill()                # Forward fill
df.bfill()                # Backward fill
```

## Duplicates

```python
df.duplicated().sum()     # Count duplicates
df.drop_duplicates()      # Drop exact duplicates
df.drop_duplicates(subset=["email"])  # Drop by column
```

## Type Conversion

```python
df["age"] = df["age"].astype(int)
df["date"] = pd.to_datetime(df["date"])
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

## String Cleaning

```python
df["name"] = df["name"].str.strip()
df["name"] = df["name"].str.lower()
df["phone"] = df["phone"].str.replace(r"\D", "", regex=True)
```

<!-- 🤔 Use `errors="coerce"` to turn invalid entries into NaN instead of crashing. -->

## Run the Code

```bash
python code/14-data-cleaning.py
```
