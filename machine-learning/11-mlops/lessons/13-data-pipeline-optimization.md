# Lesson 11.13: Data Pipeline Optimization

## Learning Objectives
- Understand data pipeline performance bottlenecks
- Implement parallel processing and caching
- Apply data quality monitoring and alerting

## Pipeline Bottlenecks

### Common Issues
- **I/O bound**: Slow disk/network reads
- **CPU bound**: Expensive transformations
- **Memory bound**: Large data in RAM
- **Network bound**: Data transfer between services

## Parallel Processing

### Ray
```python
import ray

ray.init()

@ray.remote
def process_shard(shard):
    result = transform(shard)
    return result

def parallel_pipeline(data, num_shards=16):
    shards = np.array_split(data, num_shards)
    futures = [process_shard.remote(shard) for shard in shards]
    results = ray.get(futures)
    return np.concatenate(results)
```

### Dask
```python
import dask.dataframe as dd

# Lazy evaluation
df = dd.read_parquet("s3://bucket/data/*.parquet")
result = df.groupby("category").agg({"value": "mean"})
result = result.compute()  # Triggers parallel execution
```

## Caching

### Multi-Level Cache
```python
import joblib
import hashlib

class PipelineCache:
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def key(self, func_name, args, kwargs):
        content = f"{func_name}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, key):
        path = self.cache_dir / key
        if path.exists():
            return joblib.load(path)
        return None

    def set(self, key, value):
        path = self.cache_dir / key
        joblib.dump(value, path)

cache = PipelineCache()

@cache_decorator
def expensive_transform(data, param=1):
    # Cached computation
    return transformed_data
```

## Data Quality

### Validation Checks
```python
import pandera as pa

class DataSchema(pa.DataFrameModel):
    customer_id: pa.typing.String = pa.Field(nullable=False)
    amount: pa.typing.Float64 = pa.Field(in_range={"min_value": 0, "max_value": 100000})
    transaction_date: pa.typing.DateTime = pa.Field()
    category: pa.typing.String = pa.Field(isin=["food", "transport", "entertainment"])
    is_valid: pa.typing.Bool = pa.Field()

def validate_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    schema = DataSchema
    validated_df = schema.validate(df)
    return validated_df
```

## Code: Optimized Pipeline

```python
import pandas as pd
import numpy as np
from typing import Callable, List
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

class OptimizedPipeline:
    def __init__(self, steps: List[tuple[str, Callable, dict]]):
        self.steps = steps  # [(name, function, params), ...]

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        for name, func, params in self.steps:
            print(f"Running step: {name}")
            data = func(data, **params)
        return data

    def run_parallel(self, data: pd.DataFrame, n_jobs=4) -> pd.DataFrame:
        shards = np.array_split(data, n_jobs)
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = list(executor.map(self.run, shards))
        return pd.concat(results, ignore_index=True)

    def lazy_run(self, data_source):
        """Stream processing for large datasets"""
        chunk_size = 10000
        for chunk in pd.read_csv(data_source, chunksize=chunk_size):
            yield self.run(chunk)


class DataPipelineMonitor:
    def __init__(self, pipeline: OptimizedPipeline):
        self.pipeline = pipeline
        self.metrics = {name: [] for name, _, _ in pipeline.steps}

    def run_with_monitoring(self, data: pd.DataFrame):
        for name, func, params in self.pipeline.steps:
            start = time.time()
            data = func(data, **params)
            elapsed = time.time() - start
            self.metrics[name].append({
                "time": elapsed,
                "input_rows": len(data),
                "timestamp": datetime.now(),
            })
        return data

    def get_bottlenecks(self):
        bottlenecks = []
        for name, times in self.metrics.items():
            avg_time = np.mean([m["time"] for m in times])
            bottlenecks.append((name, avg_time))
        bottlenecks.sort(key=lambda x: x[1], reverse=True)
        return bottlenecks
```

## Monitoring & Alerting

```python
class DataPipelineAlert:
    def __init__(self):
        self.alerts = []

    def check_latency(self, step_name, duration, threshold=60):
        if duration > threshold:
            self.alerts.append({
                "type": "latency",
                "step": step_name,
                "duration": duration,
                "threshold": threshold,
                "timestamp": datetime.now(),
            })

    def check_data_volume(self, step_name, row_count, expected_range):
        if not (expected_range[0] <= row_count <= expected_range[1]):
            self.alerts.append({
                "type": "volume",
                "step": step_name,
                "rows": row_count,
                "expected": expected_range,
                "timestamp": datetime.now(),
            })

    def check_null_rate(self, step_name, df, max_null_rate=0.05):
        null_rates = df.isnull().mean()
        high_null_cols = null_rates[null_rates > max_null_rate]
        if len(high_null_cols) > 0:
            self.alerts.append({
                "type": "null_rate",
                "step": step_name,
                "columns": high_null_cols.to_dict(),
                "timestamp": datetime.now(),
            })

    def send_alerts(self):
        if self.alerts:
            for alert in self.alerts:
                print(f"ALERT: {alert['type']} in {alert['step']}")
```

## References
- Ray: https://docs.ray.io/
- Dask: https://docs.dask.org/
- Pandera: https://pandera.readthedocs.io/
- Polak, "Optimizing Data Pipelines: A Practical Guide", 2023
- Kreps, "Questioning the Lambda Architecture", 2014
