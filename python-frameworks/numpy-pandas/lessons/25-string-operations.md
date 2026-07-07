# 📝 String Operations
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Vectorized string methods, regex, extracting patterns.

## String Methods

```python
df["name"].str.lower()
df["name"].str.strip()
df["name"].str.len()
df["name"].str.contains("alice", case=False)
```

## Splitting & Replacing

```python
df["full_name"].str.split(" ", expand=True)  # Split into columns
df["phone"].str.replace(r"\D", "", regex=True)  # Keep only digits
```

## Extracting Patterns

```python
df["email"].str.extract(r"(\w+)@(\w+)\.(\w+)")
df["email"].str.extractall(r"(\w+)@(\w+)\.(\w+)")
```

## Checking Conditions

```python
df["email"].str.startswith("alice")
df["email"].str.endswith(".com")
df["email"].str.match(r"^\w+@\w+\.\w+$")
```

## Categorizing with str

```python
df["domain"] = df["email"].str.split("@").str[1]
df["domain_category"] = df["domain"].str.extract(r"(\w+)")
```

<!-- 🤔 Use `.str` accessor for vectorized string ops — much faster than loop. -->

## Run the Code

```bash
python code/25-string-operations.py
```
