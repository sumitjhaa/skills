# 📝 Celery Practice

## Exercise 1: Task Result Pattern

Create a Celery app with a `multiply` task. Call it with `apply_async` including a `countdown=3`. Check `.ready()`, `.status`, `.successful()`, and `.get(timeout=5)`.

## Exercise 2: Task Configuration

Define a task with `bind=True`, `max_retries=5`, `acks_late=True`. Inside the task, print `self.request.id`, `self.request.args`, and `self.request.retries`.

## Exercise 3: Multiple Tasks

Create three tasks: `validate_email`, `send_email`, and `log_email`. Route them to `high`, `default`, and `slow` queues respectively. Call each and verify they run.

## Exercise 4: Partial Signatures

Create a `scale` task that multiplies a number by a factor. Use partial signatures to create `double = scale.s(2)` and `triple = scale.s(3)`. Test both.

## Exercise 5: Chain Pipeline

Build a text processing chain: `clean_text.s(raw)` | `tokenize.s()` | `count_words.s()`. Each task passes its result to the next. Print the final output.

## Exercise 6: Group + Chord

Create a `square` task and a `summarize` task. Use a chord to square all numbers in a list, then sum the results. Compare the group intermediate results vs the chord final result.

## Exercise 7: Retry with Backoff

Implement a `flaky_api_call` task that fails on the first 3 attempts (in eager mode, simulate with a counter) and succeeds on the 4th. Use exponential backoff.

## Exercise 8: Base Task Class

Create a `DatabaseTask` base class that logs task start/end in `on_success` and `on_failure` hooks. Derive a `query_users` task from it.

## Exercise 9: Signal Monitor

Use `task_prerun`, `task_success`, and `task_failure` signals to build a simple monitoring system that counts success/failure per task name.

## Exercise 10: Workflow Router

Create tasks for an order processing workflow: `validate_order` → `charge_payment` → `send_confirmation` → `update_inventory`. Route `charge_payment` to a `payments` queue. Build the full chain.

## Exercise 11: Beat Scheduler

Configure beat tasks: `heartbeat` every 10 seconds, `daily_digest` at 6 AM weekdays, `weekly_report` on Monday at 3 AM. Print the schedule definitions.

## Exercise 12: Django-Style Setup

Recreate the Django Celery setup pattern: set a default Django settings module, configure from an object with namespace, and simulate autodiscovery.

## Exercise 13: FastAPI Report API

Simulate a FastAPI pattern: submit a `generate_report` task with a user ID, check its status (simulate with a short sleep), then retrieve the result.

## Exercise 14: Error Handling Strategy

Create tasks for each error pattern:
- Retry 3 times then fail permanently
- Retry with exponential backoff (2^retry seconds)
- No retry (fail immediately)
- Validate input and reject bad data without retry

## Exercise 15: Integration Pipeline

Build a data pipeline: `fetch_data` (3 parallel sources) | `validate` each | `merge` results | `store` final output. Use group + chain. Add error handling. Add a cleanup task to beat schedule.
