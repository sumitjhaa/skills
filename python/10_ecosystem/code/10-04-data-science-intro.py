"""Data Science Introduction — SQLite, NumPy, Pandas, Matplotlib.
Run: python 10-04-data-science-intro.py
"""

import sqlite3

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

try:
    import numpy as np
    likes = np.array([row[3] for row in cur.execute("SELECT * FROM posts")])
    print(f"Mean likes: {likes.mean():.1f}, Median: {np.median(likes):.1f}")
    print(f"Max likes: {likes.max()}, Min: {likes.min()}")
except ImportError:
    print("NumPy not installed (pip install numpy)")

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
