# 🔄 Middleware & CORS
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Custom middleware, request/response processing, CORS configuration.

## Custom Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

<!-- ⏱️ Middleware wraps every request — perfect for timing, logging, rate limiting. -->

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

| Setting | Value | Effect |
|---------|-------|--------|
| `allow_origins` | `["*"]` | Any origin (dev only) |
| `allow_origins` | `["https://myapp.com"]` | Specific origin |
| `allow_methods` | `["*"]` | All HTTP methods |
| `allow_headers` | `["*"]` | All headers |

<!-- 🌐 Frontend on a different port? Add CORS middleware or the browser blocks the request. -->

## Middleware Order

Middleware runs in the order they're added. First added = outermost (runs first on request, last on response).

```python
app.add_middleware(LoggingMiddleware)  # Runs first
app.add_middleware(CORSMiddleware)     # Runs second
```

## Run the Code

```bash
python code/07-middleware-cors.py
```
