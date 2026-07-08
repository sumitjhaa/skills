"""
09.29 LLM Serving — Continuous Batching Scheduler
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class ContinuousBatchingScheduler:
    """
    Iteration-level continuous batching.
    New requests join after current iteration; finished requests leave.
    """

    def __init__(self, max_batch_size=8):
        self.max_batch_size = max_batch_size
        self.active_requests = []
        self.completed = []

    def add_request(self, request_id, num_tokens):
        self.active_requests.append({
            "id": request_id,
            "remaining": num_tokens,
            "total": num_tokens,
        })

    def step(self):
        """Simulate one decode iteration."""
        if not self.active_requests:
            return [], []

        # Process current batch
        batch = self.active_requests[:self.max_batch_size]
        generated = []

        for req in batch:
            req["remaining"] -= 1
            if req["remaining"] <= 0:
                self.active_requests.remove(req)
                self.completed.append(req)
                generated.append(req["id"])

        return [r["id"] for r in batch], generated

    def simulate(self, arrival_rate=0.5, max_steps=20):
        requests_scheduled = 0
        req_id = 0

        for step in range(max_steps):
            # New requests arrive
            if np.random.rand() < arrival_rate:
                tokens = np.random.randint(2, 10)
                self.add_request(f"req_{req_id}", tokens)
                print(f"Step {step:2d}: req_{req_id} arrived ({tokens} tokens)")
                req_id += 1
                requests_scheduled += 1

            # Process step
            batch, completed = self.step()
            if batch:
                print(f"Step {step:2d}: batch={batch}, completed={completed}")
            else:
                print(f"Step {step:2d}: idle")

        print(f"\nTotal requests: {requests_scheduled}, Completed: {len(self.completed)}")
        return self.completed


class SimpleServingSimulation:
    """Compare continuous vs. static batching."""

    @staticmethod
    def static_batch_time(requests, batch_size, time_per_token=1.0):
        num_batches = int(np.ceil(len(requests) / batch_size))
        max_tokens = max(r["tokens"] for r in requests)
        return num_batches * max_tokens * time_per_token

    @staticmethod
    def continuous_batch_time(requests, time_per_token=1.0):
        remaining = [r["tokens"] for r in requests]
        total_time = 0
        while any(r > 0 for r in remaining):
            active = [r for r in remaining if r > 0]
            if active:
                total_time += time_per_token
                remaining = [r - 1 for r in remaining]
        return total_time


if __name__ == "__main__":
    scheduler = ContinuousBatchingScheduler(max_batch_size=4)
    scheduler.simulate(arrival_rate=0.6, max_steps=15)

    print("\n--- Batching comparison ---")
    requests = [{"tokens": np.random.randint(2, 10)} for _ in range(20)]
    static_time = SimpleServingSimulation.static_batch_time(requests, batch_size=4)
    continuous_time = SimpleServingSimulation.continuous_batch_time(requests)
    print(f"Static batching:    {static_time:.0f} time units")
    print(f"Continuous batching: {continuous_time:.0f} time units")
    print(f"Speedup: {static_time / continuous_time:.2f}x")
