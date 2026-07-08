# 📝 Airflow — Phase 02 Practice (Advanced & Production)

## Exercise 1: Dynamic DAG Factory

Write a function `create_dag(team_name, schedule)` that generates a DAG with team-specific tasks (extract, transform, load). Call it to generate DAGs for "data", "ml", and "analytics" teams.

## Exercise 2: Custom CSVReaderOperator

Create a custom operator `CSVReaderOperator` that takes a `filepath` and reads a CSV into a list of dicts, returned via XCom.

## Exercise 3: Connection Inspector

Create a DAG with a PythonOperator that lists all connections (IDs only) from `BaseHook`, prints their type and host (masked password), and reports total count.

## Exercise 4: Pool Contention

Create a DAG with 10 identical PythonOperator tasks all using `pool="test_pool"` with `pool_slots=2`. Show that only 2 run concurrently. Create the pool via `airflow pools set test_pool 2 "test"`.

## Exercise 5: SLA Monitor

Create a DAG where one task has an `sla=timedelta(seconds=1)` and `execution_timeout=timedelta(seconds=3)`. The task should `time.sleep(5)` to trigger both.

## Exercise 6: Deferrable Pattern

Create a DAG that simulates a deferrable pattern: start → wait (sensor) → process → end. Set the sensor to use `mode="reschedule"` with `poke_interval=3`.

## Exercise 7: DAG Unit Tests

Write a Python script (not a DAG) that:
1. Uses `DagBag` to load your DAGs
2. Asserts each DAG has at least 1 task
3. Asserts no import errors
4. Validates task dependency chains aren't circular

## Exercise 8: Production Config

Create a DAG configured for production with:
- `retries=3`, `retry_delay=timedelta(minutes=5)`
- `email_on_retry=True`, `email_on_failure=True`
- Tags for discovery
- `max_active_runs=2`
- A description

## Exercise 9: CI Validation Script

Write a CI-ready script that:
1. Checks all DAGs import cleanly
2. Runs `flake8` on DAG files (or simulates with `ast` parsing)
3. Reports total tasks per DAG
4. Exits with code 1 if any error found

## Exercise 10: Full Production Pipeline

Combine everything into a single pipeline DAG that:
- Uses a custom operator
- Has TaskGroups for modularity
- Uses XCom for data flow
- Has proper retry and SLA config
- Has at least 8 tasks
- Validates data quality at the end
