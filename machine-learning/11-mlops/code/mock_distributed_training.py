"""
Mock Distributed Training — demonstrates DDP, FSDP, and DeepSpeed concepts
by simulating multi-GPU training with mock communication.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class DistributedConfig:
    world_size: int = 4
    backend: str = "nccl"
    zero_stage: int = 2
    use_fp16: bool = True


class MockProcessGroup:
    """Simulates a distributed process group with all-reduce."""

    def __init__(self, rank: int, world_size: int):
        self.rank = rank
        self.world_size = world_size

    def all_reduce(self, tensor: np.ndarray) -> np.ndarray:
        """Simulate gradient all-reduce across 'GPUs'."""
        noise = np.random.uniform(-0.01, 0.01, tensor.shape)
        aggregated = tensor * self.world_size + noise
        return aggregated / self.world_size


@dataclass
class MockModel:
    """A tiny model with fake parameters."""
    params: int = 100_000
    size_mb: float = 0.4


class MockTrainer:
    """Simulates distributed training loop."""

    def __init__(self, config: DistributedConfig, rank: int = 0):
        self.config = config
        self.rank = rank
        self.pg = MockProcessGroup(rank, config.world_size)
        self.model = MockModel()
        self.loss_history = []

    def train_step(self, step: int) -> float:
        local_loss = float(np.random.exponential(0.5))
        grad = np.array([local_loss])

        synced = self.pg.all_reduce(grad)
        avg_loss = float(synced[0])

        self.loss_history.append(avg_loss)
        return avg_loss

    def estimate_memory_savings(self) -> dict:
        """Estimate memory savings from FSDP / DeepSpeed."""
        base_memory = self.model.size_mb

        if self.config.zero_stage == 0:
            sharded = base_memory
        elif self.config.zero_stage == 1:
            # optimizer states sharded
            sharded = base_memory * (1 + 1 / self.config.world_size)
        elif self.config.zero_stage == 2:
            # optimizer + gradients sharded
            sharded = base_memory * (1 + 2 / self.config.world_size)
        elif self.config.zero_stage == 3:
            # parameters + optimizer + gradients sharded
            sharded = base_memory * 3 / self.config.world_size
        else:
            sharded = base_memory

        return {
            "model_size_mb": base_memory,
            "estimated_per_gpu_mb": round(sharded, 2),
            "savings_pct": round((1 - sharded / (base_memory * 3)) * 100, 1),
            "zero_stage": self.config.zero_stage,
        }


if __name__ == "__main__":
    config = DistributedConfig(world_size=8, zero_stage=2, use_fp16=True)
    trainer = MockTrainer(config, rank=3)

    print(f"Distributed training: world_size={config.world_size}, rank={trainer.rank}")
    print(f"Backend: {config.backend}, ZeRO stage: {config.zero_stage}, FP16: {config.use_fp16}")

    print("\nTraining 10 steps...")
    for step in range(10):
        loss = trainer.train_step(step)
        print(f"  Step {step+1:2d} | loss = {loss:.4f}")

    print(f"\nFinal loss: {trainer.loss_history[-1]:.4f}")

    mem = trainer.estimate_memory_savings()
    print(f"\nMemory estimate per GPU (ZeRO-{mem['zero_stage']}):")
    print(f"  Model size: {mem['model_size_mb']} MB")
    print(f"  Per GPU:    {mem['estimated_per_gpu_mb']} MB")
    print(f"  Savings:    {mem['savings_pct']}% vs. naive DDP")
