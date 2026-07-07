"""Deployment & Monitoring — FastAPI app with structured logging, health, metrics.
Run: uvicorn 10-09-deployment-monitoring:app --reload
or:  python 10-09-deployment-monitoring.py
"""

import time
import logging
import random
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger("social_api")

app = FastAPI(title="Social Analytics API")
METRICS: dict[str, float | int] = {
    "http_requests_total": 0,
    "http_request_duration_seconds": 0.0,
    "errors_total": 0,
}


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    METRICS["http_requests_total"] += 1
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    METRICS["http_request_duration_seconds"] = duration
    logger.info("request", extra={
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2),
    })
    return response


@app.get("/health")
async def health():
    db_ok = random.choice([True, True, True, False])
    redis_ok = True
    if not db_ok:
        logger.error("health_check_failed", extra={"component": "database"})
        return JSONResponse(
            status_code=503,
            content={"status": "DOWN", "database": "unreachable", "redis": "ok"},
        )
    return {"status": "UP", "database": "ok", "redis": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/metrics")
async def metrics():
    return {
        "http_requests_total": METRICS["http_requests_total"],
        "http_request_duration_seconds": METRICS["http_request_duration_seconds"],
        "errors_total": METRICS["errors_total"],
    }


@app.get("/analyze")
async def analyze(text: str = "default"):
    METRICS["http_requests_total"] += 1
    result = {
        "text": text,
        "word_count": len(text.split()),
        "char_count": len(text),
        "sentiment": random.choice(["positive", "neutral", "negative"]),
    }
    logger.info("analyze_complete", extra={"text": text[:20], "result": result})
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
