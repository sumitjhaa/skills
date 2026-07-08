# 📝 Airflow — Phase 01 Practice (Core Concepts)

## Exercise 1: Multi-Step DAG

Create a DAG with 6 tasks in a diamond pattern: `start → [a, b] → c → [d, e] → end`. Use EmptyOperator for all tasks.

## Exercise 2: Bash + Python Combo

Create a DAG with a `BashOperator` that writes a timestamp to a file, a `PythonOperator` that reads and prints it, and an `EmptyOperator` as the start. Verify the data flows correctly.

## Exercise 3: Custom Schedule

Create a DAG that runs every 2 hours on weekdays (Monday–Friday) using a cron expression. Set `catchup=True` and `max_active_runs=3`.

## Exercise 4: Two Sensors

Create a DAG with a `FileSensor` waiting for file `/tmp/trigger_a` and a `TimeDeltaSensor` waiting 10 seconds. Both must succeed before a final PythonOperator runs.

## Exercise 5: XCom Pipeline

Build a 3-task pipeline: task1 generates a random number and pushes it, task2 receives it, multiplies by 2, pushes the result, task3 receives and prints it.

## Exercise 6: Branch on Value

Create a DAG with a `BranchPythonOperator` that checks if `x > 10`. If yes, run `high` path; if no, run `low` path. Both paths merge to a common `end` task.

## Exercise 7: Task Group ETL

Create a DAG with two TaskGroups: `load` (download, unzip) and `process` (validate, transform, analyze). Wire them sequentially.

## Exercise 8: Multi-Branch with Trigger Rules

Create a DAG where task_a branches to [b, c, d]. Task b and c can fail, but d must succeed for task_e to run. Use appropriate trigger rules.

## Exercise 9: File Monitor with XCom

Create a DAG where a FileSensor waits for a file, then a PythonOperator reads the filename and pushes it via XCom, then another task logs it.

## Exercise 10: Complex DAG Structure

Design a DAG that represents an order processing workflow with TaskGroups for checkout, payment, shipping, and notification. Include at least 12 tasks across 4 groups.
