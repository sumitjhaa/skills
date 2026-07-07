# 📊 Data Science Introduction
<!-- ⏱️ 18 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** SQLite for embedded databases, NumPy for numerical arrays, Pandas for data analysis, Matplotlib for plotting, and a taste of scikit-learn for ML.

> 💡 **TL;DR — The whole point:** SQLite stores structured data without a server. NumPy gives fast numerical arrays. Pandas makes tabular data analysis feel like SQL + Excel. Matplotlib turns data into charts.

## 🔗 Why This Matters
Social-media analytics generates terabytes of data — posts, likes, shares, comments, user profiles. SQLite stores it, NumPy processes it, Pandas analyzes it, Matplotlib visualizes it. These four tools form the backbone of data science in Python.

## The Concept
- **SQLite:** embedded SQL database (zero config, file-based)
- **NumPy:** `numpy.ndarray` — fast fixed-type arrays with vectorized operations
- **Pandas:** `pandas.DataFrame` — labeled 2D data with groupby, merge, filter
- **Matplotlib:** comprehensive plotting (line, bar, scatter, histogram)
- **scikit-learn:** ML toolkit built on NumPy/Pandas

## Code Example
```python
"""Social-media analytics: SQLite → Pandas → Matplotlib pipeline."""

import sqlite3
from pathlib import Path


# ─── SQLite: store social-media posts ───
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        content TEXT,
        likes INTEGER,
        shares INTEGER,
        created_at TEXT
    )
""")
sample_posts = [
    (1, 101, "Python is amazing!", 150, 30, "2025-01-15"),
    (2, 102, "Just learned async/await", 200, 45, "2025-01-16"),
    (3, 101, "Threading vs asyncio?", 89, 12, "2025-01-17"),
    (4, 103, "Data science with Python", 312, 78, "2025-01-18"),
    (5, 101, "Pandas is life", 175, 40, "2025-01-19"),
]
cur.executemany("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)", sample_posts)
conn.commit()


# ─── NumPy: analyze likes/shares ───
try:
    import numpy as np
    likes = np.array([row[3] for row in cur.execute("SELECT * FROM posts")])
    print(f"Mean likes: {likes.mean():.1f}, Median: {np.median(likes):.1f}")
    print(f"Max likes: {likes.max()}, Min: {likes.min()}")
except ImportError:
    print("NumPy not installed (pip install numpy)")


# ─── Pandas: DataFrame operations ───
try:
    import pandas as pd
    df = pd.read_sql("SELECT * FROM posts", conn)
    print(f"\nDataFrame: {len(df)} rows, {list(df.columns)}")
    popular = df[df["likes"] > 150]
    print(f"Popular posts (>150 likes): {len(popular)}")
    per_user = df.groupby("user_id")["likes"].mean()
    print(f"Avg likes per user:\n{per_user}")
except ImportError:
    print("Pandas not installed (pip install pandas)")


# ─── Matplotlib: bar chart ───
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    user_avg = df.groupby("user_id")["likes"].mean()
    plt.bar(user_avg.index.astype(str), user_avg.values)
    plt.title("Average Likes per User")
    plt.xlabel("User ID")
    plt.ylabel("Avg Likes")
    plt.savefig("user_likes.png")
    print("Chart saved to user_likes.png")
except Exception:
    pass
```

## 🔍 How It Works
- `sqlite3.connect(":memory:")` — in-memory DB (use a filename for persistent storage)
- `?` placeholders — prevent SQL injection (never use f-strings for SQL)
- `np.array(list)` — converts Python list to NumPy array; enables fast vector math
- `pd.read_sql(query, conn)` — load SQL query results directly into a DataFrame
- `df[df["likes"] > 150]` — filter rows with a boolean mask
- `df.groupby("user_id")["likes"].mean()` — SQL-like GROUP BY + aggregation
- `plt.savefig("file.png")` — save chart to file (use `plt.show()` in notebooks)

## ⚠️ Common Pitfall
Using Python loops on NumPy arrays or Pandas DataFrames. `for row in df:` is almost always the wrong approach. Use vectorized operations: `df["likes"].mean()`, `df.groupby()`, `np.where()`.

## 🧠 Memory Aid
"SQLite = file-based SQL. NumPy = fast arrays. Pandas = DataFrame = Excel on steroids. Matplotlib = chart everything. Vectorize, don't loop."

## 🏃 Try It
Create a SQLite database for a movie watchlist (title, year, rating, watched). Load it into a Pandas DataFrame. Plot a bar chart of average rating by year.

## 🔗 Related
- [SQLAlchemy Deep](07-sqlalchemy-deep.md) — production ORM
- [NumPy & Pandas Deep](08-numpy-pandas-deep.md) — advanced data analysis

## ➡️ Next
[Asyncio Deep](05-asyncio-deep.md)
