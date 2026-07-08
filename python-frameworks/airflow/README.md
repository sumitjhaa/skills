# Apache Airflow — Data Pipeline Orchestration

## Overview

20 lessons across 2 phases covering Apache Airflow for building and orchestrating data pipelines.

| Phase | Topic | Lessons | Code |
|-------|-------|---------|------|
| 01 | Core Concepts | 01–10 | 10 files |
| 02 | Advanced & Production | 11–20 | 10 files |

## Phase 01 — Core Concepts

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [DAG Basics](lessons/01-dag-basics.md) | [01-dag-basics.py](code/01-dag-basics.py) | DAG definition, PythonOperator |
| 02 | [Operators](lessons/02-operators.md) | [02-operators.py](code/02-operators.py) | Python, Bash, Empty operators |
| 03 | [Tasks](lessons/03-tasks.md) | [03-tasks.py](code/03-tasks.py) | Task instances, execution model |
| 04 | [Dependencies](lessons/04-dependencies.md) | [04-dependencies.py](code/04-dependencies.py) | Bit-shift operators, chain patterns |
| 05 | [Scheduling](lessons/05-scheduling.md) | [05-scheduling.py](code/05-scheduling.py) | Cron expressions, @presets, data intervals |
| 06 | [Sensors](lessons/06-sensors.md) | [06-sensors.py](code/06-sensors.py) | FileSensor, TimeDeltaSensor |
| 07 | [XComs](lessons/07-xcoms.md) | [07-xcom.py](code/07-xcom.py) | Push, pull, return values |
| 08 | [Branching](lessons/08-branching.md) | [08-branching.py](code/08-branching.py) | BranchPythonOperator, trigger rules |
| 09 | [Task Groups](lessons/09-task-groups.md) | [09-task-groups.py](code/09-task-groups.py) | TaskGroup context manager |
| 10 | [SubDAGs vs TaskGroups](lessons/10-subdags-vs-taskgroups.md) | [10-subdag-comparison.py](code/10-subdag-comparison.py) | Why TaskGroups are preferred |

## Phase 02 — Advanced & Production

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 11 | [Dynamic DAGs](lessons/11-dynamic-dags.md) | [11-dynamic-dags.py](code/11-dynamic-dags.py) | Programmatic DAG generation |
| 12 | [Custom Operators](lessons/12-custom-operator.md) | [12-custom-operator.py](code/12-custom-operator.py) | Subclass BaseOperator |
| 13 | [Hooks & Connections](lessons/13-hooks-connections.md) | [13-hooks-connections.py](code/13-hooks-connections.py) | BaseHook, connection management |
| 14 | [Pools](lessons/14-pools.md) | [14-pools.py](code/14-pools.py) | Limit concurrency, pool_slots |
| 15 | [SLAs & Timeouts](lessons/15-slas-timeouts.md) | [15-slas-timeouts.py](code/15-slas-timeouts.py) | execution_timeout, dagrun_timeout |
| 16 | [Triggers & Deferrable](lessons/16-triggers-deferrable.md) | [16-triggers.py](code/16-triggers.py) | Async execution pattern |
| 17 | [Testing DAGs](lessons/17-testing-dags.md) | [17-testing.py](code/17-testing.py) | DagBag validation, unit tests |
| 18 | [Production Patterns](lessons/18-production-patterns.md) | [18-production-patterns.py](code/18-production-patterns.py) | Retries, alerts, tags |
| 19 | [CI/CD for Airflow](lessons/19-cicd-airflow.md) | [19-cicd.py](code/19-cicd.py) | DAG validation in CI |
| 20 | [Capstone Pipeline](lessons/20-capstone-pipeline.md) | [20-capstone-pipeline.py](code/20-capstone-pipeline.py) | Full ETL with quality checks |

## Setup

```bash
# Install
pip install apache-airflow

# Initialize database
export AIRFLOW_HOME=~/airflow
airflow db migrate

# Run a DAG
cp code/01-dag-basics.py $AIRFLOW_HOME/dags/
airflow dags test 01_dag_basics 2024-01-01
```

## Notes

- Written for **Airflow 3.x**. Uses modern provider import paths (`airflow.providers.standard.*`).
- All DAGs have `schedule=None` for manual testing and `catchup=False`.
- DAG verification is done via `DagBag` import check (industry standard for CI).
- `airflow dags test <dag_id> <logical_date>` is the recommended way to run individual DAGs.

## Practice

- [Phase 01 Exercises](practice/phase01-exercises.md)
- [Phase 02 Exercises](practice/phase02-exercises.md)
