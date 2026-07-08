# 08.31 End-to-End CV System

## Learning Objectives
- Understand production CV pipeline design
- Implement distributed training and mixed precision
- Optimise inference with ONNX/TensorRT
- Deploy with TorchServe and Triton Inference Server

## Pipeline Design

### High-Level Architecture
```
Input → Preprocess → Backbone → Task Head → Postprocess → Output
```

### Multi-Stage Pipelines
```
Camera → Detection → Crop → Classification (e.g., face detection → recognition)
Camera → Detection → Tracking → Re-ID (e.g., multi-object tracking)
```

### Streaming vs Batch
| Aspect | Streaming | Batch |
|--------|-----------|-------|
| Latency | Low (ms) | High (min) |
| Throughput | Moderate | High |
| Use case | Real-time detection | Offline processing |
| Buffer | Single frame | Large batch |

## Data Module

### Data Ingestion
- **TFRecord / RecordIO**: Serialised binary format (TensorFlow)
- **LMDB**: Key-value store for image data
- **WebDataset**: Sharded tar files with streaming
- **S3/GCS**: Cloud storage with prefetching

### Augmentation Pipeline (NVIDIA DALI)
GPU-accelerated data augmentation:

```python
# DALI pipeline example
pipeline = dali.Pipeline(batch_size=64, num_threads=4, device_id=0)
pipeline.add_operator(dali.ops.FileReader(file_root="/data"))
pipeline.add_operator(dali.ops.ImageDecoder())
pipeline.add_operator(dali.ops.RandomResizedCrop(size=(224, 224)))
pipeline.add_operator(dali.ops.CoinFlip(probability=0.5))
pipeline.add_operator(dali.ops.Flip(horizontal=dali.ops.Flip.FlipType.HORIZONTAL))
pipeline.add_operator(dali.ops.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]))
```

## Model Zoo

### Standardised Backbones
| Backbone | Parameters | ImageNet Top-1 | FLOPs | Notes |
|----------|-----------|---------------|-------|-------|
| ResNet-50 | 25.6M | 76.1% | 4.1G | Classic, widely available |
| ResNeXt-101 | 83.5M | 79.3% | 16.5G | Group convolution |
| EfficientNet-B4 | 19.3M | 82.9% | 4.2G | Compound scaling |
| ConvNeXt-B | 88.6M | 84.0% | 15.4G | Modern ConvNet |
| ViT-B/16 | 86.6M | 81.1% | 17.6G | Transformer-based |
| Swin-B | 87.8M | 83.5% | 15.4G | Hierarchical ViT |

### Task Heads (Detectron2 / MMDetection)
- **Detection**: Faster R-CNN, RetinaNet, DETR
- **Segmentation**: Mask R-CNN, Panoptic FPN
- **Pose**: Keypoint R-CNN, HRNet
- **Tracking**: FairMOT, QDTrack

## Training Pipeline

### Distributed Training
```bash
# PyTorch DDP
torchrun --nproc_per_node=8 train.py --batch_size 256 --lr 0.1

# FSDP (Fully Sharded Data Parallel)
torchrun --nproc_per_node=8 train_fsdp.py --sharding_strategy hybrid
```

### Mixed Precision (AMP)
```python
with torch.cuda.amp.autocast():
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### Checkpointing
- Resume from checkpoint
- Keep best model (validation loss/accuracy)
- Exponential Moving Average (EMA) of weights
- Early stopping with patience=10

### Logging
- **W&B**: Training curves, hyperparameters, model graphs
- **TensorBoard**: Scalars, histograms, images, PR curves
- **MLflow**: Experiment tracking, model registry, deployment

## Inference Optimisation

### ONNX Export
```python
torch.onnx.export(model, dummy_input, "model.onnx",
                  input_names=["input"], output_names=["output"],
                  dynamic_axes={"input": {0: "batch"}})
```

### TensorRT
- Graph optimisation (layer fusion, constant folding)
- FP16/INT8 quantisation (calibration with representative data)
- TensorRT plugin for custom ops (NMS, RoI Align)

### Deployment Targets
| Platform | Format | Hardware | Optimisation |
|----------|--------|---------|-------------|
| Server | ONNX/TensorRT | NVIDIA GPU | FP16, INT8 |
| Mobile | TFLite / CoreML | ARM CPU/GPU | INT8, Weight quant |
| Edge | OpenVINO | Intel CPU/GPU | FP16, INT8 |
| Web | WebGL / WebNN | Browser | FP16 |

### GPU-Accelerated NMS
```python
# Torchvision NMS (GPU)
from torchvision.ops import nms
keep = nms(boxes, scores, iou_threshold=0.5)
```

## Serving

### TorchServe
- REST/gRPC endpoints
- Multi-model serving
- Model versioning (A/B tests)
- Custom handlers for preprocessing/postprocessing

### Triton Inference Server
- Framework agnostic (PyTorch, TF, ONNX, TensorRT)
- Dynamic batching
- Concurrent model execution
- GPU resource scheduling

### Performance Metrics
- **Latency**: p50, p95, p99 (target: p99 < 100ms)
- **Throughput**: Requests per second (QPS)
- **Error rate**: 5XX responses (target: < 0.1%)
- **Model load time**: Cold start (target: < 30s)

## Monitoring

### Model Drift Detection
- **Data drift**: KL divergence of input distribution
- **Prediction drift**: Distribution of model outputs
- **Feature drift**: Per-feature distribution comparison

### Explainability
```python
# Grad-CAM
grads = torch.autograd.grad(class_score, feature_maps, retain_graph=True)
weights = grads.mean(dim=(2, 3), keepdim=True)
cam = (weights * feature_maps).sum(dim=1).relu()
```

### Alerting
- Latency spikes
- Error rate increase
- Memory usage
- Model accuracy degradation (requires labels)

## References
- Paszke, Gross, et al., "PyTorch: An Imperative Style, High-Performance Deep Learning Library", NeurIPS 2019
- Vanhoucke, Mao, "The Design of a Production-Level Computer Vision Pipeline", 2020
- NVIDIA, "Triton Inference Server: An Optimized Cloud and Edge Inferencing Solution"
- PyTorch, "TorchServe: A flexible and easy to use tool for serving PyTorch models"
- Wu, Kirillov, Massa, Lo, Girshick, "Detectron2", 2019
