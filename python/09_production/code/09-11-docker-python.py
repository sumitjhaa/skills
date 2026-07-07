"""Docker for Python — FastAPI health endpoint & Dockerfile demo.
Run: python 09-11-docker-python.py
Build: docker build -f Dockerfile -t my-api .
"""

from fastapi import FastAPI

app = FastAPI(title="E-Commerce API")


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/")
def root():
    return {"message": "E-Commerce API running in Docker"}


# --- Dockerfile content shown for reference ---
DOCKERFILE = """
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
CMD ["uvicorn", "09-11-docker-python:app", "--host", "0.0.0.0", "--port", "8000"]
"""

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI app... Open http://localhost:8000/health")
    print("Dockerfile:\n" + DOCKERFILE.strip())
    uvicorn.run(app, host="0.0.0.0", port=8000)
