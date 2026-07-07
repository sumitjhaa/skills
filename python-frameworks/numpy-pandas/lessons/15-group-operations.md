# 📊 Group Operations
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** groupby, aggregation, transform, filter.

## Basic GroupBy

```python
df.groupby("city")["age"].mean()
df.groupby("city").agg({"age": ["mean", "std"], "salary": "sum"})
```

## Named Aggregations

```python
df.groupby("city").agg(
    avg_age=("age", "mean"),
    max_salary=("salary", "max"),
    count=("name", "count"),
)
```

## Transform

```python
df["age_rank"] = df.groupby("city")["age"].rank()
df["age_centered"] = df.groupby("city")["age"].transform(lambda x: x - x.mean())
```

## Filter

```python
df.groupby("city").filter(lambda x: len(x) >= 3)
```

## Multiple Group Keys

```python
df.groupby(["city", "department"]).agg({"salary": "mean"})
```

<!-- 🤔 `transform` returns same shape as input — great for feature engineering. -->

## Run the Code

```bash
python code/15-group-operations.py
```
