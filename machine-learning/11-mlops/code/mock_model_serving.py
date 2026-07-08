"""
Mock Model Serving — demonstrates TorchServe / vLLM / Triton concepts
with a lightweight HTTP server that loads a "model" and serves predictions.
"""

import json
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any

import numpy as np


class MockLinearModel:
    """A trivial linear model for demonstration."""

    def __init__(self):
        self.coef_ = np.array([0.5, -0.3, 1.2])
        self.intercept_ = 0.1

    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.coef_ + self.intercept_


class ModelServerHandler(BaseHTTPRequestHandler):
    model = MockLinearModel()

    def do_GET(self):
        if self.path == "/ping":
            self._respond(200, {"status": "healthy", "model": "LinearModel v1"})
        elif self.path == "/metrics":
            self._respond(200, {"requests_served": getattr(self.server, "request_count", 0)})
        else:
            self._respond(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/predict":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            X = np.array(data["instances"], dtype=float)
            t0 = time.perf_counter()
            preds = self.model.predict(X)
            latency = time.perf_counter() - t0

            self.server.request_count = getattr(self.server, "request_count", 0) + 1

            self._respond(200, {
                "predictions": preds.tolist(),
                "latency_ms": round(latency * 1000, 2),
            })
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code: int, body: dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def log_message(self, format, *args):
        pass  # suppress logs


def run_server(host="localhost", port=8080):
    server = HTTPServer((host, port), ModelServerHandler)
    server.request_count = 0
    print(f"Serving on http://{host}:{port}")
    print("Endpoints: GET /ping, POST /predict, GET /metrics")
    print("Send Ctrl+C to stop.")

    import threading
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    # Demonstrate a few requests
    import urllib.request

    time.sleep(0.2)
    req = urllib.request.Request(
        f"http://{host}:{port}/predict",
        data=json.dumps({"instances": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    print("Response:", json.loads(resp.read()))

    # Health check
    resp = urllib.request.urlopen(f"http://{host}:{port}/ping")
    print("Health:", json.loads(resp.read()))

    server.shutdown()
    print("Server stopped.")


if __name__ == "__main__":
    run_server()
