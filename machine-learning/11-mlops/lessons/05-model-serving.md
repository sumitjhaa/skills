# Lesson 11.05: Model Serving

## Learning Objectives
- Understand model serving architectures
- Implement REST/gRPC model endpoints
- Apply batching, caching, and autoscaling

## Serving Architecture

### Options
```
Model → API Server (FastAPI/Triton) → Client
Model → Serverless (AWS Lambda) → Client
Model → Edge (ONNX/TFLite) → Mobile/Browser
```

## REST vs gRPC

| Aspect | REST | gRPC |
|--------|------|------|
| Protocol | HTTP/1.1 | HTTP/2 |
| Serialisation | JSON | Protobuf |
| Speed | Slower | 2-5x faster |
| Streaming | Limited | Bidirectional |
| Client support | Universal | Limited for web |

## FastAPI Serving

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch

app = FastAPI()
model = load_model()
tokenizer = load_tokenizer()

class PredictRequest(BaseModel):
    text: str
    max_length: int = 100
    temperature: float = 0.7

class PredictResponse(BaseModel):
    generated_text: str
    tokens_used: int
    latency_ms: float

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    import time
    start = time.time()
    
    inputs = tokenizer(request.text, return_tensors='pt')
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=request.max_length, 
                                temperature=request.temperature)
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    latency = (time.time() - start) * 1000
    
    return PredictResponse(
        generated_text=generated[len(request.text):],
        tokens_used=outputs.shape[-1],
        latency_ms=latency,
    )

@app.get("/health")
async def health():
    return {"status": "ok", "model": model.config.model_type}
```

## Batching

```python
from fastapi import BackgroundTasks
from collections import deque
import asyncio

class BatchProcessor:
    def __init__(self, model, max_batch_size=32, max_wait=0.1):
        self.model = model
        self.max_batch_size = max_batch_size
        self.max_wait = max_wait
        self.queue = deque()
        self.lock = asyncio.Lock()

    async def process(self, request):
        future = asyncio.Future()
        async with self.lock:
            self.queue.append((request, future))
            if len(self.queue) >= self.max_batch_size:
                asyncio.create_task(self._process_batch())
        return await future

    async def _process_batch(self):
        async with self.lock:
            batch = [self.queue.popleft() for _ in range(min(len(self.queue), self.max_batch_size))]
        
        if not batch:
            return
        
        texts = [r.text for r, _ in batch]
        inputs = tokenizer(texts, padding=True, return_tensors='pt')
        outputs = self.model.generate(**inputs)
        results = [tokenizer.decode(o, skip_special_tokens=True) for o in outputs]
        
        for (_, future), result in zip(batch, results):
            future.set_result(result)

batch_processor = BatchProcessor(model)

@app.post("/batch_predict")
async def batch_predict(request: PredictRequest):
    result = await batch_processor.process(request)
    return {"generated_text": result}
```

## Caching

```python
import hashlib
import json
from functools import lru_cache
import redis

class ModelCache:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.ttl = 3600  # 1 hour

    def key(self, request):
        return f"model:{hashlib.md5(json.dumps(request, sort_keys=True).encode()).hexdigest()}"

    def get(self, request):
        return self.redis.get(self.key(request))

    def set(self, request, response):
        self.redis.setex(self.key(request), self.ttl, json.dumps(response))

    @lru_cache(maxsize=1000)
    def get_cached(self, request):
        # Hot cache for most frequent requests
        return super().get(request)
```

## Autoscaling

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: model-server
  template:
    spec:
      containers:
      - name: server
        image: myregistry/model-server:latest
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "16Gi"
            cpu: "8"
        ports:
        - containerPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-server
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## References
- FastAPI: https://fastapi.tiangolo.com/
- NVIDIA Triton Inference Server: https://developer.nvidia.com/triton-inference-server
- TorchServe: https://pytorch.org/serve/
- Hibernate, "Scaling ML Model Serving: A Comprehensive Guide", 2023
