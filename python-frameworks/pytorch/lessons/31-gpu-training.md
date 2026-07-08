# 🏗️ GPU Training
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Write device-agnostic code that runs on CPU or GPU.

## Device-Agnostic Pattern

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = MyModel().to(device)
X = X.to(device)
y = y.to(device)
```

## Checking GPU

```python
torch.cuda.is_available()   # True if CUDA GPU exists
torch.cuda.device_count()   # number of GPUs
torch.cuda.get_device_name(0)  # GPU name
```

## Common Pitfall

```python
# WRONG: model and data on different devices
model = MyModel().to("cuda")
loss = criterion(model(X), y)  # ERROR if X is on CPU

# RIGHT: move everything to the same device
X, y = X.to(device), y.to(device)
```

<!-- 🤔 Always use device-agnostic code. It costs nothing and makes your code portable. -->

## Run the Code

```bash
python code/31-gpu-training.py
```
