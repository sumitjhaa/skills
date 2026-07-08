"""Integration: full async pipeline with routing, workflows, error handling."""
from celery import Celery, chain, group
from celery.schedules import crontab


print("=" * 55)
print("  FULL CELERY PIPELINE")
print("=" * 55, "\n")

app = Celery('pipeline', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

app.conf.task_queues = {
    'default': {'exchange': 'default', 'routing_key': 'default'},
    'high': {'exchange': 'high', 'routing_key': 'high'},
    'batch': {'exchange': 'batch', 'routing_key': 'batch'},
}

app.conf.beat_schedule = {
    'cleanup-hourly': {
        'task': 'tasks.cleanup_temp_files',
        'schedule': 3600.0,
    },
}

@app.task(queue='high', bind=True, max_retries=3)
def fetch_data(self, source_id):
    print(f"  [FETCH]  source={source_id}")
    return {"source": source_id, "raw": f"data_from_{source_id}"}

@app.task(queue='batch')
def validate_data(data):
    is_valid = len(data['raw']) > 0
    print(f"  [VALIDATE] {data['source']}: {'✓' if is_valid else '✗'}")
    return {**data, "valid": is_valid}

@app.task(queue='batch')
def transform_data(data):
    transformed = data['raw'].upper()
    print(f"  [TRANSFORM] {data['source']}: {transformed}")
    return {**data, "transformed": transformed}

@app.task(queue='default')
def store_result(data):
    print(f"  [STORE]  {data['source']}: stored successfully")
    return f"stored_{data['source']}"

@app.task(queue='default')
def cleanup_temp_files():
    print(f"  [CLEANUP] Temp files removed")
    return "cleaned"

sources = [101, 102, 103]
print("Running parallel pipeline:\n")

pipeline = group(
    chain(fetch_data.s(s) | validate_data.s() | transform_data.s() | store_result.s())
    for s in sources
)
results = pipeline.delay()
print(f"\nPipeline results:")
for r in results.get():
    print(f"  - {r}")

cleanup_temp_files.delay()
print(f"\nPipeline: parallel fetch → validate → transform → store")
print(f"Queues:    high (fetch), batch (validate/transform), default (store)")
