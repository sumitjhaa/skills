# 09.29 LLM Serving

## Learning Objectives
- Understand LLM serving infrastructure and challenges
- Implement batching, caching, and streaming for LLMs
- Apply TensorRT-LLM, vLLM, and text-generation-inference
- Analyze latency, throughput, and cost trade-offs

## Serving Challenges

### Autoregressive Bottleneck
- Generating 100 tokens requires 100 sequential forward passes
- Each pass is ~10ms → 1 second for 100 tokens
- Parallelisation limited by causal attention

### Memory
- Model weights: 7B model = 14GB (fp16)
- KV cache: 32GB for 128K context at fp16
- Total: 46GB per model instance

## Batching

### Dynamic Batching
```python
class RequestQueue:
    def __init__(self, max_batch_size=64):
        self.queue = []
        self.max_batch_size = max_batch_size

    def add_request(self, request):
        self.queue.append(request)

    def get_batch(self):
        batch = []
        while self.queue and len(batch) < self.max_batch_size:
            batch.append(self.queue.pop(0))
        return batch

    def process_batch(self):
        batch = self.get_batch()
        if not batch:
            return
        padded_inputs = self.pad_to_same_length(batch)
        outputs = model.generate(padded_inputs)
        self.dispatch_results(batch, outputs)
```

### Continuous Batching (vLLM)
- Process tokens at different positions in the same batch
- No padding waste
- PagedAttention for KV cache management

## Streaming

### Token-by-Token Output
```python
async def stream_generate(prompt, model):
    inputs = tokenizer(prompt, return_tensors='pt')
    for _ in range(max_length):
        outputs = model(**inputs)
        next_token = outputs.logits[0, -1].argmax()
        yield tokenizer.decode(next_token)
        inputs = torch.cat([inputs, next_token.unsqueeze(0)], dim=-1)
```

## Server Configuration

### Hardware
| Model Size | GPU | Memory | Batch Size | Throughput |
|-----------|-----|--------|-----------|-----------|
| 7B | 1xA100-80GB | 14GB | 64 | 2000 tok/s |
| 13B | 1xA100-80GB | 26GB | 32 | 1200 tok/s |
| 70B | 4xA100-80GB | 140GB | 128 | 4000 tok/s |
| 175B | 8xA100-80GB | 350GB | 64 | 2000 tok/s |

### Quantization
| Precision | 7B Memory | 70B Memory | Speedup |
|-----------|----------|-----------|---------|
| FP16 | 14GB | 140GB | 1x |
| INT8 | 7GB | 70GB | 1.5-2x |
| INT4 | 3.5GB | 35GB | 2-3x |

## Framework Comparison

| Framework | Technique | Max Throughput | Latency (p50) | Features |
|-----------|----------|---------------|---------------|----------|
| Text-Generation-Inference (TGI) | Continuous batching | 2000 tok/s | 50ms | HF native, streaming |
| vLLM | PagedAttention | 2400 tok/s | 40ms | Memory efficient, fast |
| TensorRT-LLM | Custom kernels | 3000 tok/s | 30ms | Fastest, NVIDIA only |
| Llama.cpp | CPU/edge inference | 500 tok/s | 100ms | Runs on CPU |

## Code: Basic LLM Server

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    stream: bool = False

class GenerateResponse(BaseModel):
    text: str
    tokens_generated: int
    time_ms: float

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer.pad_token = tokenizer.eos_token

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    import time
    start = time.time()
    
    inputs = tokenizer(request.prompt, return_tensors='pt').to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_tokens,
            temperature=request.temperature,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    text = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    elapsed = (time.time() - start) * 1000
    
    return GenerateResponse(
        text=text,
        tokens_generated=outputs.shape[-1] - inputs.input_ids.shape[-1],
        time_ms=elapsed,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Practical Considerations
- **Cold start**: Model loading takes 1-5 minutes
- **Concurrent users**: Use request queue + load balancing
- **Cost**: GPU instances cost $1-10/hr for inference
- **Monitoring**: Token throughput, latency percentiles, error rates
- **Fallback**: Serve smaller model during peak load

## References
- Kwon, Li, et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023
- NVIDIA, "TensorRT-LLM: A TensorRT Toolset for Optimizing LLM Inference", 2023
- HuggingFace, "Text Generation Inference (TGI)", 2023
- Gerganov, "Llama.cpp: LLM Inference in C/C++", 2023
- Zhu, Pulijala, et al., "LLM Inference Performance Engineering: Best Practices", 2024
