# 🏗️ Result Backend
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Store and retrieve task results.

## Backend Options

```python
# Redis
app = Celery('tasks', backend='redis://localhost:6379/0')

# Database (SQLAlchemy)
app = Celery('tasks', backend='db+sqlite:///results.db')

# Cache (Memcached, Redis)
app = Celery('tasks', backend='cache+redis://localhost:6379/1')
```

## Using Results

```python
result = add.delay(4, 5)
result.ready()   # True if complete
result.get()     # 9 (blocks until ready)
result.status    # PENDING, STARTED, SUCCESS, FAILURE
result.successful()  # True/False
result.failed()     # True/False
```

## Timeouts

```python
result.get(timeout=10)      # raise if not done in 10s
result.get(propagate=False)  # return error instead of raising
```

<!-- 🤔 Always set a timeout on `get()` to avoid blocking forever. -->

## Run the Code

```bash
python code/04-result-backend.py
```
