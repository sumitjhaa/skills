# 📂 Reading & Writing Data
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Read CSV, Excel, JSON; write to various formats.

## CSV

```python
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", index_col=0)
df = pd.read_csv("data.csv", usecols=["name", "age"])
df.to_csv("output.csv", index=False)
```

## Excel

```python
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", sheet_name="Results", index=False)
```

## JSON

```python
df = pd.read_json("data.json")
df.to_json("output.json", orient="records", indent=2)
```

## Other Formats

```python
df = pd.read_parquet("data.parquet")
df = pd.read_sql("SELECT * FROM users", engine)
df = pd.read_html("https://example.com/table")
```

## Options

```python
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 50)
pd.set_option("display.precision", 2)
```

<!-- 🤔 Use `index_col=0` when your CSV has a row index column. -->

## Run the Code

```bash
python code/12-reading-writing.py
```
