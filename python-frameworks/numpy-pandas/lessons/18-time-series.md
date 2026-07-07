# 📅 Time Series
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Datetime handling, resampling, shifting, rolling windows.

## Datetime Basics

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

# Access date parts
df.index.year
df.index.month
df.index.day_of_week
```

## Resampling

```python
# Downsample
df.resample("ME").mean()   # Monthly mean
df.resample("W").sum()     # Weekly sum
df.resample("QE").max()    # Quarterly max

# Upsample
df.resample("D").ffill()   # Fill daily
```

## Shifting

```python
df["prev_day"] = df["value"].shift(1)    # Previous row
df["next_day"] = df["value"].shift(-1)   # Next row
df["daily_change"] = df["value"].diff()  # Change from previous
df["pct_change"] = df["value"].pct_change()
```

## Rolling Windows

```python
df["rolling_mean"] = df["value"].rolling(window=7).mean()
df["rolling_std"] = df["value"].rolling(window=30).std()
df["expanding"] = df["value"].expanding().mean()
```

<!-- 🤔 Set your datetime column as index for resample to work. -->

## Run the Code

```bash
python code/18-time-series.py
```
