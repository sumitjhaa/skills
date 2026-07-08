# 🏗️ Random Tensors & Seeding
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create random tensors and control reproducibility with seeds.

## Random Functions

```python
torch.rand(3, 3)           # uniform [0, 1)
torch.randn(3, 3)          # standard normal
torch.randint(0, 10, (3,)) # random integers
torch.randperm(10)         # permutation
```

## Seeding for Reproducibility

```python
torch.manual_seed(42)
t1 = torch.randn(3)  # deterministic

torch.manual_seed(42)
t2 = torch.randn(3)  # same as t1

assert torch.equal(t1, t2)  # True
```

## Distributions

```python
# Uniform
torch.empty(3, 3).uniform_(0, 1)
# Normal with mean/std
torch.normal(mean=0, std=2, size=(3, 3))
```

<!-- 🤔 Always seed at the start of training scripts for reproducibility. -->

## Run the Code

```bash
python code/03-random-tensors.py
```
