# 09.11 Distillation

## Learning Objectives
- Understand knowledge distillation for model compression
- Implement logit-based and feature-based distillation
- Apply distillation for transformer models (DistilBERT, TinyBERT)
- Analyze trade-offs between speed and accuracy

## Knowledge Distillation

### Teacher-Student Framework
```
Teacher (large)  →  Soft labels  →  Student (small, trained)
```

### Logit Distillation (Hinton 2015)
$$\mathcal{L} = \alpha \cdot \mathcal{L}_{\text{CE}}(y_{\text{true}}, y_{\text{student}}) + \beta \cdot \mathcal{L}_{\text{KL}}(y_{\text{teacher}}, y_{\text{student}})$$

- $y_{\text{teacher}}$: softmax with temperature $T$:
  $$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$
- $T > 1$: softer distribution, more information about class relationships

## DistilBERT

### Student Architecture
- Same architecture as BERT but 40% fewer layers (6 vs 12)
- Same hidden dimension (768)
- DistilBERT: 66M params (vs BERT-base 110M)

### Training
1. **Distillation loss**: Match teacher logits
2. **Masked LM loss**: Standard MLM objective
3. **Cosine embedding loss**: Align hidden states
   $$\mathcal{L}_{\text{cos}} = 1 - \cos(h_{\text{student}}, h_{\text{teacher}})$$

### Results
- Retains 97% of BERT performance
- 60% faster inference
- 40% fewer parameters

## TinyBERT

### Two-Stage Distillation
1. **General distillation**: Pretrain student on teacher's behaviour
2. **Task-specific distillation**: Fine-tune on downstream data

### Layer Mapping
```
Teacher: L1  L2  L3  L4  L5  L6  L7  L8  L9  L10 L11 L12
Student: L1  L2  L3  L4
```

### Multi-Head Attention Transfer
Student learns teacher's attention patterns:
$$\mathcal{L}_{\text{attn}} = \frac{1}{h} \sum_{i=1}^h \|A_i^{\text{student}} - A_i^{\text{teacher}}\|_2^2$$

## Task-Specific Distillation

### Classification
Match logits + hidden states between teacher and student.

### QA (BERT→TinyBERT for SQuAD)
Match logits + attention matrices + hidden states.

## Code: Distillation Loss

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DistillationLoss(nn.Module):
    def __init__(self, temperature=4.0, alpha=0.7):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha

    def forward(self, student_logits, teacher_logits, true_labels):
        # Soft target loss (KL divergence)
        soft_student = F.log_softmax(student_logits / self.temperature, dim=-1)
        soft_teacher = F.softmax(teacher_logits / self.temperature, dim=-1)
        kl_loss = F.kl_div(soft_student, soft_teacher, reduction='batchmean')
        kl_loss *= self.temperature ** 2
        
        # Hard target loss (cross-entropy)
        ce_loss = F.cross_entropy(student_logits, true_labels)
        
        return self.alpha * kl_loss + (1 - self.alpha) * ce_loss


class FeatureDistillationLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse = nn.MSELoss()

    def forward(self, student_hidden, teacher_hidden):
        # Align hidden states
        return self.mse(student_hidden, teacher_hidden)


class AttentionDistillationLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.mse = nn.MSELoss()

    def forward(self, student_attn, teacher_attn):
        # Align attention patterns
        return self.mse(student_attn, teacher_attn)
```

## Distillation Results

| Student Model | Teacher | Params | Speedup | GLUE Score |
|--------------|---------|--------|---------|-----------|
| DistilBERT | BERT-base | 66M (60%) | 1.6x | 77.0 (vs 78.9) |
| TinyBERT (4-layer) | BERT-base | 14.5M (13%) | 9.4x | 74.5 (vs 78.9) |
| MiniLM (6-layer) | BERT-large | 66M (17%) | 2.0x | 78.0 (vs 80.7) |
| DistilGPT2 | GPT-2 (124M) | 82M (66%) | 1.3x | Perplexity: 36.5 (vs 35.2) |

## Practical Considerations
- **Temperature**: T=4-8 works well for NLP tasks
- **Alpha**: 0.5-0.8 for distillation vs CE loss balance
- **Teacher quality**: Better teacher = better student (up to a point)
- **Data augmentation**: Using unlabeled data helps student generalise
- **Quantization**: Combine distillation + quantization for maximum compression

## References
- Hinton, Vinyals, Dean, "Distilling the Knowledge in a Neural Network", NeurIPS 2014 Workshop
- Sanh, Debut, Chaumond, Wolf, "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter", NeurIPS 2019 Workshop
- Jiao, Yin, et al., "TinyBERT: Distilling BERT for Natural Language Understanding", EMNLP 2020
- Wang, Wei, et al., "MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers", NeurIPS 2020
- Gou, Yu, Maybank, Tao, "Knowledge Distillation: A Survey", IJCV 2021
