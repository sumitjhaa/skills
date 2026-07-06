# 📊 Data Engineering — Baby Style (8 weeks)

**For:** Some basics. Like data. Want high salary without managing people.

**Time:** 3 hrs/day | **Goal:** Junior Data Engineer

**Pay:** $80-110k | **Difficulty:** Medium-Hard

---

## What is Data Engineering?

- Data comes from many places (apps, databases, APIs, files)
- Data Engineers collect it, clean it, store it, make it accessible
- Without data engineers, data analysts and data scientists have nothing to work with
- Pays very well. Growing fast. Less competition than web dev.

---

## 🗓️ Week 1 — Python for Data (quick version)

### Day 1: Python basics
- Variables, loops, if/else, functions, lists, dicts
- See 02-express-python.md Week 1 if stuck

**Do:** Write a script that reads a list of numbers and prints the average.

### Day 2: File I/O
- `open("file.csv")`, `read()`, `write()`
- Read CSV files line by line

**Do:** Read a CSV file. Print each row.

### Day 3: pandas
- `import pandas as pd`
- `df = pd.read_csv("data.csv")`
- `df.head()`, `df.info()`, `df.describe()`
- `df["column"]`, `df[df["age"] > 30]`

**Do:** Load a CSV. Clean missing values. Find average of a column.

### Day 4: Data cleaning
- `df.dropna()`, `df.fillna()`, `df.drop_duplicates()`
- Fix data types: `df["date"] = pd.to_datetime(df["date"])`

**Do:** Take a messy dataset. Clean it. Document every fix.

### Day 5: APIs + JSON
- `requests.get("https://api.example.com/data")`
- `data.json()` — convert to Python dict
- Flatten nested JSON

**Do:** Fetch data from a public API. Convert to DataFrame. Save as CSV.

### Day 6-7: pandas practice
- Group data, merge datasets, create pivot tables

**Do:** Take 2 CSV files. Merge them. Find insights.

---

## 🗓️ Week 2 — SQL (deep)

### Day 1: SQL basics
- SELECT, WHERE, ORDER BY, LIMIT
- COUNT, SUM, AVG, MAX, MIN

**Do:** Run 10 queries on a sample database.

### Day 2: JOINs
- INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN
- Joining multiple tables

**Do:** Join 3 tables: users → orders → products. Show user name + product name.

### Day 3: Subqueries + CTEs
- Subquery = query inside a query
- CTE = WITH clause (reusable query)

**Do:** Write a query with a CTE. Find users who spent more than average.

### Day 4: Window functions
- ROW_NUMBER(), RANK(), LAG(), LEAD()
- Running totals, moving averages

**Do:** Find the top 3 products by sales in each category.

### Day 5: Query performance
- Indexes = speed up queries
- EXPLAIN ANALYZE = see how query runs
- Avoid SELECT *, use proper filters

**Do:** Create an index. Compare query speed with and without it.

### Day 6-7: SQL project
- Download a large dataset (millions of rows)
- Write 10 queries: aggregations, joins, window functions, CTEs

---

## 🗓️ Week 3 — Databases + Cloud

### Day 1: PostgreSQL
- Install PostgreSQL. Create database, tables, insert data.
- psql command line

**Do:** Create a database with 3 tables. Insert 100 records.

### Day 2: Database design
- Normalization = avoid duplicate data
- Primary keys, foreign keys, indexes
- Schema design patterns

**Do:** Design a schema for an e-commerce platform (users, products, orders, order_items).

### Day 3: Cloud databases
- AWS RDS = managed PostgreSQL
- Google Cloud SQL
- Cloud = don't manage the server yourself

**Do:** Create a free RDS instance. Connect to it from Python.

### Day 4: Data warehousing
- OLTP = transaction database (for apps)
- OLAP = analytics database (for reporting)
- Columnar storage (Snowflake, BigQuery, Redshift)

**Do:** Read about Snowflake vs PostgreSQL. What's different?

### Day 5: BigQuery (Google's warehouse)
- Load data, run SQL queries, analyze billions of rows instantly
- Free tier available

**Do:** Create a BigQuery account. Load a CSV. Run a query on 1 million rows.

### Day 6-7: Cloud project
- Load data into BigQuery. Write 5 analytical queries. Visualize results.

---

## 🗓️ Week 4 — ETL Pipelines

### Day 1: What is ETL?
- Extract (get data from source)
- Transform (clean, change format)
- Load (put it in database)
- The core of data engineering

**Do:** Write a Python script that: reads CSV → cleans data → saves to database. That's ETL.

### Day 2: Extract from APIs
- `requests.get()` → `response.json()` → clean → save to DB
- Schedule it to run daily

**Do:** Build a pipeline that fetches weather data daily and stores it in PostgreSQL.

### Day 3: Extract from databases
- `pd.read_sql("SELECT * FROM source", source_conn)`
- Transform → Load into target database

**Do:** Copy data from one database to another. Transform it in between.

### Day 4: Airflow basics
- Airflow = schedule + monitor pipelines
- DAG = Directed Acyclic Graph (pipeline definition)
- Tasks = steps in the pipeline

**Do:** Install Airflow. Create a simple DAG with 3 tasks.

### Day 5: Airflow operators
- PythonOperator = run Python function
- PostgresOperator = run SQL
- EmailOperator = send email on failure

**Do:** Build a DAG that: extracts data → transforms → loads to DB → sends success email.

### Day 6-7: Airflow project
**Do:** Build a DAG that runs daily:
1. Fetch data from API
2. Clean + transform
3. Load to PostgreSQL
4. Send summary email

---

## 🗓️ Week 5 — Big Data Tools

### Day 1: What is big data?
- When data is too big for one computer
- Distributed processing = split across many computers
- Hadoop vs Spark

**Do:** Read about MapReduce concept (5 min). Watch a video.

### Day 2: Spark basics
- PySpark = Python + Spark
- Process data across many computers at once
- `spark.read.csv("file.csv")`, `.filter()`, `.groupBy()`, `.agg()`

**Do:** Install Spark locally. Load a CSV. Count rows. Filter. Group.

### Day 3: Spark DataFrames
- Similar to pandas but distributed
- `df.select("name"), df.filter(col("age") > 30)`
- `.join()`, `.union()`, `.withColumn()`

**Do:** Load a large dataset. Run transformations. Save results.

### Day 4: Spark SQL
- Run SQL queries on Spark DataFrames
- `spark.sql("SELECT * FROM table WHERE age > 30")`

**Do:** Register a DataFrame as a temp view. Run 5 SQL queries on it.

### Day 5: Data formats
- Parquet = compressed columnar format (faster than CSV)
- Avro = row-based format (good for streaming)
- JSON = flexible but slower

**Do:** Convert a CSV to Parquet. Compare file size. Compare query speed.

### Day 6-7: Spark project
**Do:** Process 1GB+ of data with Spark:
- Read CSV → clean → transform → aggregate → save as Parquet → query

---

## 🗓️ Week 6 — Streaming + Orchestration

### Day 1: Batch vs streaming
- Batch = process data daily/hourly (Airflow)
- Streaming = process data in real-time (Kafka)
- Most pipelines are batch. Streaming is advanced.

**Do:** Read about when to use batch vs streaming.

### Day 2: Kafka basics
- Kafka = message queue. Apps send data, other apps read it.
- Producer = sends messages. Consumer = reads messages.
- Topic = category of messages

**Do:** Install Kafka. Start producer. Start consumer. Send and read messages.

### Day 3: dbt (data build tool)
- dbt = transform data in your warehouse using SQL
- Write SQL SELECT statements. dbt handles CREATE TABLE/VIEW
- Version control for your data transformations

**Do:** Install dbt. Create a model. Run it. See the table created.

### Day 4: dbt deeper
- Models, tests, documentation, snapshots
- dbt docs = auto-generated documentation site

**Do:** Build 3 dbt models. Add tests. Generate docs.

### Day 5: Data quality
- Test your data: null checks, uniqueness, referential integrity
- dbt tests, Great Expectations

**Do:** Write 5 data quality tests. See them fail. Fix the data.

### Day 6-7: Full pipeline project
**Do:** End-to-end:
1. Source data (API or CSV)
2. Python ETL → PostgreSQL
3. dbt transforms → clean tables
4. Airflow schedules it daily
5. Tests run automatically

---

## 🗓️ Week 7 — Certifications + Portfolio

### Day 1-3: Portfolio projects
- GitHub with 3 projects:
  1. ETL pipeline (Python + PostgreSQL + Airflow)
  2. Big data processing (Spark + Parquet)
  3. dbt transformation project

### Day 4-5: Resume
- 1 page. Keywords: Python, SQL, PostgreSQL, Airflow, Spark, dbt, ETL, data pipelines, cloud (AWS/GCP)

### Day 6-7: Cert prep
- **AWS Certified Data Analytics — Specialty** (advanced)
- **Google Professional Data Engineer** (well recognized)
- **dbt Fundamentals Certification** (free)
- Or just focus on projects + applications

---

## 🗓️ Week 8 — Job Hunt

- Roles: Junior Data Engineer, Data Engineer, Analytics Engineer
- LinkedIn, Indeed — 10 apps/day
- Salary expectations: $80-110k (entry), $120-150k (2-3 years)

**Interview prep:**
- "What's the difference between OLTP and OLAP?"
- "Explain an ETL pipeline you built"
- "How do you handle data quality issues?"
- "What's your experience with Airflow / Spark / dbt?"

---

> ✅ **Data Engineering = high pay, high demand, less competition.** Every company needs data engineers. After 2-3 years: $120k+. Remote jobs are common.
