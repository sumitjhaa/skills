# 09.30 LLM Application Design

## Learning Objectives
- Understand end-to-end LLM application architecture
- Implement RAG pipelines, chatbots, and agents
- Apply evaluation and monitoring for production
- Optimise cost, latency, and quality trade-offs

## Application Architecture

### Full-Stack LLM App
```
Frontend (React) → API Gateway → LLM Service → Backend Services
                                     ↓
                              Vector Database
                                     ↓
                              Cache (Redis)
```

## Chatbot Design

### Conversation State Management
```python
class ConversationManager:
    def __init__(self, max_history=10):
        self.sessions = {}  # session_id → messages

    def add_message(self, session_id, role, content):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({
            "role": role, "content": content,
            "timestamp": time.time()
        })
        self._truncate(session_id)

    def get_context(self, session_id):
        messages = self.sessions[session_id]
        return [{"role": m["role"], "content": m["content"]}
                for m in messages[-self.max_history:]]
```

### Prompt Template
```python
SYSTEM_PROMPT = """You are a helpful assistant. You answer questions accurately and concisely.
If you don't know the answer, say so. Do not make up information.

Guidelines:
- Be helpful, harmless, and honest
- Cite sources when possible
- Ask clarifying questions when needed
- Use {language} for responses"""

def build_chat_prompt(system_prompt, messages, user_input):
    prompt = f"<|system|>{system_prompt}</s>"
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        prompt += f"<|{role}|>{content}</s>"
    prompt += f"<|user|>{user_input}</s><|assistant|>"
    return prompt
```

## RAG Application

### Query Processing Pipeline
```python
class RAGChatbot:
    def __init__(self, retriever, generator, memory):
        self.retriever = retriever
        self.generator = generator
        self.memory = memory

    def query(self, user_input, top_k=3):
        # 1. Retrieve relevant documents
        docs = self.retriever.search(user_input, k=top_k)
        
        # 2. Build context
        context = "\n".join([doc["text"] for doc in docs])
        
        # 3. Generate with RAG prompt
        prompt = f"""Use the following context to answer:
Context: {context}
Question: {user_input}
Answer (cite sources with [1], [2], etc.):"""
        
        # 4. Generate response
        response = self.generator.generate(prompt)
        
        # 5. Store in memory
        self.memory.add((user_input, response))
        
        return {"response": response, "sources": docs}
```

## Cost Optimisation

### Strategies
| Strategy | Cost Reduction | Quality Impact | Complexity |
|----------|---------------|---------------|------------|
| Prompt caching | 30-50% | None | Low |
| Response caching | 50-80% (for repeat queries) | None | Low |
| Model routing | 40-60% | Low | Medium |
| Smaller model for simple tasks | 50-90% | Task-dependent | Medium |
| Streaming | Perceived speed | None | Low |

### Model Routing
```python
class ModelRouter:
    def __init__(self, models):
        # models: {"small": fast_model, "large": powerful_model}
        self.models = models

    def select_model(self, query):
        if len(query) < 50:
            return "small"  # Simple query
        if "code" in query or "math" in query:
            return "large"  # Complex reasoning
        return "small"  # Default

    def query(self, user_input):
        model_key = self.select_model(user_input)
        return self.models[model_key].generate(user_input)
```

## Monitoring

### Key Metrics
```python
METRICS = {
    "latency_p50": 0.05,    # 50ms
    "latency_p95": 0.2,     # 200ms
    "latency_p99": 0.5,     # 500ms
    "throughput": 100,       # requests/sec
    "error_rate": 0.01,      # 1%
    "token_usage": 0,        # tokens/sec
    "cost_per_query": 0.001, # $0.001
}
```

### Logging
```python
import logging
import json

class QueryLogger:
    def __init__(self):
        self.logger = logging.getLogger("llm_app")
    
    def log_query(self, user_id, query, response, latency, model):
        self.logger.info(json.dumps({
            "user_id": user_id,
            "query": query,
            "response_length": len(response),
            "latency_ms": latency,
            "model": model,
            "timestamp": time.time(),
        }))
```

## Production Checklist

### Pre-Deployment
- [ ] Safety guardrails tested
- [ ] Rate limiting configured
- [ ] Real-time monitoring dashboard
- [ ] Fallback model for high availability
- [ ] A/B testing pipeline
- [ ] User feedback collection
- [ ] Data privacy compliance (GDPR, CCPA)
- [ ] PII detection and redaction
- [ ] CORS and authentication

### Ongoing
- [ ] Model performance drift monitoring
- [ ] User satisfaction tracking
- [ ] Cost optimisation reviews
- [ ] Security penetration testing
- [ ] Model updates and deployment

## Code: Complete Application

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

class QueryRequest(BaseModel):
    text: str
    session_id: str = None

class QueryResponse(BaseModel):
    text: str
    sources: list = []

class LLMApplication:
    def __init__(self):
        self.cache = {}
        self.conversations = {}
        self.load_models()

    def generate_response(self, request: QueryRequest):
        # Check cache
        cache_key = hashlib.md5(request.text.encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Get conversation context
        session_id = request.session_id or "default"
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        # Generate
        response = self.query_model(request.text, self.conversations[session_id])
        
        # Store in conversation
        self.conversations[session_id].append(request.text)
        self.conversations[session_id].append(response["text"])
        
        # Cache
        self.cache[cache_key] = response
        return response

llm_app = LLMApplication()

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        return llm_app.generate_response(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## References
- Zaharia, Chen, et al., "The Shift from Models to Compound AI Systems", 2024
- Khattab, Santhanam, et al., "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines", 2023
- Chase, "LangChain: Building applications with LLMs through composability", 2022
- Li, Wang, et al., "InferCept: A Comprehensive Benchmark for LLM Inference Serving", 2024
- HuggingFace, "Practical Guides for Building LLM Applications", 2024
