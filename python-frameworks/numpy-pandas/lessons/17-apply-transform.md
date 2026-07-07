# ⚡ Apply & Transform
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Apply functions to rows/columns, map, vectorized operations.

## Applying Functions

```python
df["age_sq"] = df["age"].apply(lambda x: x ** 2)
df["name_len"] = df["name"].apply(len)
```

## Apply to Rows

```python
df["full_label"] = df.apply(
    lambda row: f"{row['name']} ({row['city']})", axis=1
)
```

## Map

```python
city_pop = {"NYC": 8.4e6, "SF": 0.9e6, "LA": 3.8e6}
df["city_pop"] = df["city"].map(city_pop)
```

## Transform vs Apply

```python
# transform — same shape
df.groupby("city")["age"].transform("mean")

# apply — flexible return shape
df.groupby("city")["age"].apply(list)
```

## Vectorized (Fastest)

```python
df["age_group"] = "adult"
df.loc[df["age"] < 18, "age_group"] = "minor"
df.loc[df["age"] > 60, "age_group"] = "senior"
```

<!-- 🤔 Vectorized operations are fastest. `apply` is slower. Loop is slowest. -->

## Run the Code

```bash
python code/17-apply-transform.py
```
