# 📊 Data Analytics — Baby Style (6 weeks)

**For:** No coding experience. Like numbers. Want to analyze things.

**Time:** 3 hrs/day | **Goal:** Junior Data Analyst

**Pay:** $55-80k | **Difficulty:** Easy

---

## What is Data Analytics?

- Companies have data (sales, users, clicks). They need someone to understand it.
- You use SQL + Python + charts to find answers
- "Which products sell best?" "Why are users leaving?" "Show me a dashboard."

---

## 🗓️ Week 1 — SQL (just the questions)

### Day 1: What is SQL?
- SQL = talks to databases
- Database = giant Excel in the cloud
- `SELECT * FROM users` — get all users

**Do:** Open a free SQL practice site (sql-practice.com or similar). Run `SELECT * FROM patients`.

### Day 2: Filtering
- `WHERE` = filter rows
- `SELECT * FROM users WHERE age > 30`
- `AND`, `OR`, `IN`, `LIKE`

**Do:** Find all patients older than 50. Then find all from a specific city.

### Day 3: Grouping
- `GROUP BY` = group similar rows
- `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`

**Do:** Count how many users are in each city. Find average age.

### Day 4: JOINs
- Tables link together (users table + orders table)
- `JOIN` = combine them
- `SELECT users.name, orders.total FROM users JOIN orders ON users.id = orders.user_id`

**Do:** Join patients with admissions. Show patient name + admission date.

### Day 5: Practice
- Solve 10 SQL problems on LeetCode (free ones)

### Day 6-7: SQL project
- Download a sample dataset (Kaggle: "Superstore Sales")
- Write 10 queries: total sales, top products, sales by region, monthly trends

---

## 🗓️ Week 2 — Python for Data

### Day 1: Python basics
- Variables, print, lists, loops, if/else
- See 04-express-python.md Week 1 if stuck

### Day 2: pandas (Excel on steroids)
- `import pandas as pd`
- `df = pd.read_csv("file.csv")` — load data
- `df.head()` — see first 5 rows
- `df["column"].mean()` — average of a column

**Do:** Load a CSV. Find average, max, min of a column.

### Day 3: Filtering + Grouping in pandas
- `df[df["age"] > 30]` — filter rows
- `df.groupby("city")["sales"].sum()` — group and sum

**Do:** Group your data. Find totals per category.

### Day 4: Data cleaning
- Real data is messy: missing values, wrong types, duplicates
- `df.dropna()` — remove empty rows
- `df["column"].fillna(0)` — fill empty with 0

**Do:** Take a messy dataset. Clean it. Document what you fixed.

### Day 5-6: Combining SQL + Python
- Connect Python to a database
- `pd.read_sql("SELECT * FROM orders", connection)`

**Do:** Pull data from SQL into pandas. Analyze it. Find insights.

### Day 7: Mini project
- Find a dataset on Kaggle
- Load, clean, analyze, write 5 findings

---

## 🗓️ Week 3 — Charts + Dashboards

### Day 1: Why visualize?
- A chart is worth 1000 numbers
- Bar chart = compare categories. Line chart = trends over time. Pie = parts of whole.

**Do:** Look at 10 good charts online. Notice what makes them clear.

### Day 2: Charts in Python (matplotlib + seaborn)
- `import matplotlib.pyplot as plt`
- `plt.bar(categories, values)` — bar chart
- `plt.plot(dates, sales)` — line chart

**Do:** Make 3 charts from your project data. Save them as images.

### Day 3: Tableau (industry standard)
- Tableau = drag-and-drop charts (no code)
- Free version: Tableau Public
- Connect to data → drag fields → instant chart

**Do:** Download Tableau Public. Connect to a CSV. Make a dashboard.

### Day 4: Tableau dashboard
- Combine multiple charts on one page
- Add filters (dropdown to filter by region, date, etc.)

**Do:** Build a sales dashboard: total sales, sales by region, monthly trend, top products.

### Day 5: Power BI (alternative)
- Microsoft's version of Tableau
- Similar concept. Many companies use it.

**Do:** Try Power BI. Make the same dashboard. Compare.

### Day 6-7: Dashboard project
- Pick a topic (COVID data, movie ratings, sports stats)
- Clean the data → explore → build dashboard → write findings

---

## 🗓️ Week 4 — Statistics (just the basics)

### Day 1-2: Basic stats
- Mean (average), median (middle value), mode (most common)
- Standard deviation (how spread out is the data)
- Percentiles (top 10%, bottom 25%)

**Do:** Calculate these on your project data.

### Day 3-4: Correlation
- Do two things relate? (ice cream sales ↑, temperature ↑)
- Correlation = -1 to 1. 0 = no relationship.

**Do:** Find a correlation in your dataset. Make a scatter plot.

### Day 5: A/B testing basics
- Two versions of something. Which is better?
- "Does red button get more clicks than blue button?"

**Do:** Design an A/B test. Write out: hypothesis, test plan, success metric.

### Day 6-7: Full case study
Pick a business question and answer it:
- "What factors increase customer spending?"
- "Which marketing channel brings best customers?"
- "When do users churn?"

**Do:** Write a 1-page report: question → data → analysis → answer → chart

---

## 🗓️ Week 5 — Portfolio + Resume

### Day 1-2: Portfolio setup
- GitHub with 3 projects (each with README)
- Tableau Public profile with your dashboards

### Day 3: Resume
- 1 page. Keywords: SQL, Python, pandas, Tableau, data cleaning, dashboards, statistics

**Do:** Write your resume. Use ChatGPT to make bullet points stronger.

### Day 4: LinkedIn
- Headline: "Data Analyst" or "Junior Data Analyst"
- Add projects. Set Open to Work.

### Day 5-7: Apply
- Roles: Data Analyst, Business Intelligence Analyst, Reporting Analyst
- LinkedIn, Indeed — 10 apps/day
- Many data analyst roles are remote

---

## 🗓️ Week 6 — Interview + Keep going

### Day 1-3: SQL interview prep
- LeetCode SQL: medium problems
- Window functions (ROW_NUMBER, RANK)
- You'll be tested on SQL in interviews. This is the most important skill.

### Day 4-5: Behavioral prep
- "Tell me about a time you found an insight from data"
- "How do you explain technical findings to non-technical people?"

### Day 6-7: Apply more
- 10 apps/day. Follow up on old ones.
- r/dataanalysis for community + job posts

---

> ✅ **Data analytics = easiest path if you like patterns and questions.** After 1-2 years, you can move into data engineering ($100k+) or data science ($120k+).
