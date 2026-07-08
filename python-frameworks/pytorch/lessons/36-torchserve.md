# 🏗️ TorchServe
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Serve PyTorch models via REST API with TorchServe.

## Model Archiver

```bash
torch-model-archiver --model-name my_model --version 1.0 \
  --model-file model.pt --handler handler.py \
  --export-path model_store
```

## Start Server

```bash
torchserve --start --model-store model_store --models my_model.mar
```

## Inference Request

```bash
curl -X POST http://localhost:8080/predictions/my_model \
  -T input.json
```

## Handler Structure

```python
class ModelHandler:
    def initialize(self, context):    # load model
    def preprocess(self, data):       # prepare input
    def inference(self, data):        # run model
    def postprocess(self, data):      # format output
```

<!-- 🤔 TorchServe handles batching, scaling, logging out of the box. -->

## Run the Code

```bash
python code/36-torchserve.py
```
