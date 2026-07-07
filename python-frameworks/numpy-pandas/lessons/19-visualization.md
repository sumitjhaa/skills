# 📈 Visualization
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Quick plots with pandas, matplotlib basics.

## Basic Plotting

```python
df["value"].plot()              # Line
df.plot(kind="bar")             # Bar
df.plot(kind="hist", bins=30)   # Histogram
df.plot(kind="scatter", x="x", y="y")  # Scatter
df.boxplot(column="value")      # Boxplot
```

## Line Plot

```python
df.set_index("date")["price"].plot(
    title="Price Over Time",
    figsize=(10, 5),
    grid=True,
)
```

## Subplots

```python
fig, axes = plt.subplots(2, 2)
df.plot(ax=axes[0, 0], kind="line")
df.plot(ax=axes[1, 0], kind="bar")
```

## Style

```python
plt.style.use("ggplot")        # Alternative style
# Styles: "default", "seaborn-v0_8", "ggplot", "fivethirtyeight"
```

<!-- 🤔 Pandas `.plot()` uses matplotlib under the hood. Call `plt.show()` or `plt.savefig()`. -->

## Run the Code

```bash
python code/19-visualization.py
```
