# 08.27 Open-Vocabulary Understanding

## Learning Objectives
- Understand CLIP's contrastive pretraining for zero-shot transfer
- Implement open-vocabulary detection with GLIP
- Apply SAM for promptable segmentation
- Evaluate zero-shot and few-shot visual recognition

## CLIP (Contrastive Language-Image Pre-training)

### Architecture
```
Image:  ViT/ResNet → I ∈ ℝ^d
Text:   Transformer → T ∈ ℝ^d
```

### Contrastive Loss
$$\mathcal{L} = -\frac{1}{2N}\sum_{i=1}^N \left[\log\frac{e^{\text{sim}(I_i,T_i)/\tau}}{\sum_j e^{\text{sim}(I_i,T_j)/\tau}} + \log\frac{e^{\text{sim}(I_i,T_i)/\tau}}{\sum_j e^{\text{sim}(I_j,T_i)/\tau}}\right]$$

- $N$: batch size (32768 in CLIP)
- $\text{sim}(I, T) = I^\top T / \|I\| \|T\|$ (cosine similarity)
- $\tau$: learned temperature

### Zero-Shot Classification
```
p(y = c | I) ∝ exp(sim(I, T_c) / τ)
T_c = text_encoder("a photo of a {class_name}")
```

### Prompt Engineering
- Ensembling: "a photo of a {c}", "a blurry photo of a {c}", "a {c}"
- Template matters: "a photo of a {c}" vs "{c}"

### CLIP Variants
| Model | Parameters | Image Encoder | Zero-shot ImageNet Top-1 |
|-------|-----------|---------------|-------------------------|
| CLIP RN50 | 38M | ResNet-50 | 58.2% |
| CLIP ViT-L/14 | 428M | ViT-L/14 | 76.2% |
| CLIP ViT-H/14 | 630M | ViT-H/14 | 78.0% |
| OpenCLIP ViT-G/14 | 1.2B | ViT-G/14 | 80.1% |

## Open-Vocabulary Detection

### GLIP (Grounded Language-Image Pre-training)
Unify detection + phrase grounding:

**Training**: $$\mathcal{L} = \mathcal{L}_{\text{det}} + \mathcal{L}_{\text{grounding}}$$

- Detection loss: class-specific (closed set)
- Grounding loss: phrase-region alignment (open set)

**Inference**: Match region features to arbitrary text queries:
$$p(\text{obj}_i = \text{phrase}_j) \propto \exp(\text{sim}(f_i^{\text{region}}, f_j^{\text{text}}) / \tau)$$

### OV-DETR
- DETR-based detector with vision-language alignment
- Object queries attend to both visual features and text features

### Grounding DINO
- DINO (DETR with improved denoising) + grounding
- Text features injected into encoder and decoder cross-attention

## SAM (Segment Anything)

### Architecture
```
Image encoder (ViT-H) → Image embedding
Prompt encoder (points, boxes, text) → Prompt embedding
Mask decoder (lightweight Transformer) → Masks
```

### Prompt Types
- **Points**: Positive/negative clicks
- **Bounding boxes**: Region of interest
- **Text**: CLIP-based text embedding
- **Ambiguous**: Multiple valid masks (3 output masks per prompt)

### Data Engine
1. **Model-assisted**: SAM trained on 1.1B masks from 11M images
2. **Interactive**: Annotators use SAM to label new images
3. **Fully automatic**: Mask generation from grid prompts

### Zero-Shot Segmentation
SAM generalises to novel objects without fine-tuning.

## Code: CLIP Zero-Shot Classifier

```python
import torch
import torch.nn.functional as F

class CLIPZeroShot:
    def __init__(self, clip_model, class_names, templates):
        self.model = clip_model
        self.class_names = class_names
        self.templates = templates
        
        # Precompute text features
        text_features = []
        for c in class_names:
            texts = [t.format(c) for t in templates]
            text_tokens = self.model.tokenize(texts)
            text_feat = self.model.encode_text(text_tokens)
            text_feat = F.normalize(text_feat, dim=-1)
            text_feat = text_feat.mean(dim=0)  # ensemble templates
            text_feat = F.normalize(text_feat, dim=0)
            text_features.append(text_feat)
        self.text_features = torch.stack(text_features, dim=0).T

    def classify(self, images):
        image_features = self.model.encode_image(images)
        image_features = F.normalize(image_features, dim=-1)
        logits = 100 * (image_features @ self.text_features)
        return logits.softmax(dim=-1)
```

## Evaluation Benchmarks

| Benchmark | Task | Metric | CLIP ViT-L | Best |
|-----------|------|--------|-----------|------|
| ImageNet | Classification | Top-1 | 76.2% | 92.3% (specialised) |
| LVIS | Open-vocab detection | mAP | 16.4 | 30.2 (GLIP) |
| COCO | Zero-shot detection | mAP | — | 23.4 (GLIP) |
| DAVIS | Zero-shot segmentation | mIoU | — | 75.0 (SAM) |
| 13 datasets | Distribution shift | Avg accuracy | 72.3% | — |

## Practical Considerations
- **Template ensemble**: Using 80+ templates improves by 2-5% over single template
- **CLIP biases**: Underperforms on fine-grained classes, biased toward web data
- **Detection vs classification**: Open-vocabulary detection is harder — needs region-text alignment
- **SAM limits**: Can produce over-segmentation; needs prompt filtering

## References
- Radford, Kim, Hallacy, et al., "Learning Transferable Visual Models From Natural Language Supervision", ICML 2021
- Li, Zhang, et al., "Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection", 2023
- Kirillov, Mintun, Ravi, et al., "Segment Anything", ICCV 2023
- Li, Li, Xiong, Hoi, "GLIP: Grounded Language-Image Pre-training", CVPR 2022
- Jia, Yang, et al., "OpenCLIP: Open-Source Implementation of CLIP", 2021
