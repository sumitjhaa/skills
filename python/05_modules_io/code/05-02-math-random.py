"""Game probability, statistical sampling, and Monte Carlo simulation."""
import math
import random


def dice_probability(target: int, dice: int = 2, sides: int = 6) -> float:
    trials = 100_000
    hits = sum(1 for _ in range(trials) if sum(random.randint(1, sides) for _ in range(dice)) >= target)
    return hits / trials


def sample_statistics(population: list, sample_size: int) -> dict:
    sample = random.sample(population, min(sample_size, len(population)))
    mean = sum(sample) / len(sample)
    variance = sum((x - mean) ** 2 for x in sample) / (len(sample) - 1)
    return {"sample_mean": round(mean, 2), "sample_std": round(math.sqrt(variance), 2), "min": min(sample), "max": max(sample)}


random.seed(42)
print(f"Probability of 7+ with 2d6: {dice_probability(7):.1%}")
print(f"Sample stats: {sample_statistics(list(range(1000)), 50)}")
print(f"Pi: {math.pi:.4f}")
print(f"Sin(π/2): {math.sin(math.pi / 2)}")
