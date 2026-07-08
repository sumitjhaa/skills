# 🏗️ TorchScript
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Export PyTorch models to TorchScript for production.

## Tracing vs Scripting

```python
# Tracing — records operations on example input
traced = torch.jit.trace(model, example_input)

# Scripting — compiles the model code
scripted = torch.jit.script(model)
```

## Save & Load

```python
torch.jit.save(traced, 'model.pt')
loaded = torch.jit.load('model.pt')
loaded.eval()
```

## When to Use

- **C++ deployment** (libtorch)
- **Mobile** (iOS/Android)
- **No Python dependency**
- **Model optimization** (fusion, constant folding)

<!-- 🤔 Tracing is simpler but scripting handles control flow better. Start with trace. -->

## Run the Code

```bash
python code/34-torchscript.py
```
