# 08.26 VQA & Captioning

## Learning Objectives
- Understand multimodal fusion for visual question answering
- Implement Bottom-Up Top-Down attention for VQA
- Apply image captioning with encoder-decoder architecture
- Evaluate with BLEU, ROUGE, METEOR, CIDEr, SPICE

## Visual Question Answering (VQA)

### Problem Definition
Given image $I$ and question $Q$, predict answer $A$:

$$A = \arg\max_{a \in \mathcal{A}} p(a | I, Q; \theta)$$

### Bottom-Up Top-Down Attention

#### Bottom-Up (Visual)
Object detection features (Faster R-CNN with ResNet-101):

$$V = \{v_1, \dots, v_k\}, \quad v_i \in \mathbb{R}^{2048}$$

- $k$ = 36 regions (NMS-filtered)
- Pretrained on Visual Genome

#### Top-Down (Question-Guided)
Attention over visual features conditioned on question:

$$a = \text{softmax}((W_q q) \odot (W_v V))$$
$$\hat{v} = \sum_i a_i v_i$$

#### Multimodal Fusion
$$\begin{aligned}
z &= \text{ReLU}(W_z (\hat{v} \odot W_q q + \text{ReLU}(W_v \hat{v} + W_q q))) \\
p &= \text{softmax}(W_o z)
\end{aligned}$$

### VQA Datasets
| Dataset | Size | Answer Types | Notes |
|---------|------|-------------|-------|
| VQA v2 | 1.1M Q/A | Open-ended | Balanced pairs |
| CLEVR | 999K Q/A | Synthetic | Compositional reasoning |
| GQA | 22M Q/A | Open-ended | Scene graph-based |
| VizWiz | 32K Q/A | Open-ended | Blind users' photos |

## Image Captioning

### Encoder-Decoder

**Encoder (CNN)**:
$$V = \text{CNN}(I) \in \mathbb{R}^{H \times W \times D}$$

**Decoder (LSTM/Transformer)**:

$$p(y_t | y_{<t}, V) = \text{softmax}(W_h h_t)$$

### Show, Attend and Tell
Spatial attention at each decoding step:

$$e_{ti} = f_{\text{att}}(h_{t-1}, v_i)$$
$$\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_j \exp(e_{tj})}$$
$$c_t = \sum_i \alpha_{ti} v_i$$

### Transformer Decoder
Self-attention over text + cross-attention over image:

$$h_t = \text{Transformer}(y_{<t}, V)$$

### ClipCap
CLIP image embedding → prefix (mapped via MLP) → GPT-2 fine-tuned:

1. CLIP encodes image → $f_I \in \mathbb{R}^{512}$
2. MLP maps $f_I$ → prefix embeddings (10 tokens)
3. GPT-2 generates caption conditioned on prefix

## Code: Bottom-Up Top-Down Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class BottomUpTopDown(nn.Module):
    def __init__(self, v_dim=2048, q_dim=512, hidden=1024, num_answers=3129):
        super().__init__()
        self.q_proj = nn.Linear(q_dim, hidden)
        self.v_proj = nn.Linear(v_dim, hidden)
        self.attn = nn.Linear(hidden, 1)
        self.fusion = nn.Sequential(
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, num_answers),
        )

    def forward(self, v, q):
        # v: (B, K, 2048), q: (B, 512)
        q_emb = self.q_proj(q).unsqueeze(1)      # (B, 1, H)
        v_emb = self.v_proj(v)                    # (B, K, H)
        attn = self.attn(torch.tanh(v_emb + q_emb)).squeeze(-1)  # (B, K)
        alpha = F.softmax(attn, dim=1)
        v_att = (alpha.unsqueeze(-1) * v_emb).sum(dim=1)  # (B, H)
        return self.fusion(v_att * q_emb.squeeze(1))
```

## Evaluation Metrics

### BLEU (Bilingual Evaluation Understudy)
n-gram precision with brevity penalty:

$$\text{BLEU-N} = \text{BP} \cdot \exp\left(\sum_{n=1}^N \frac{1}{N} \log p_n\right)$$

### ROUGE-L
Longest Common Subsequence (LCS) based:
$$\text{ROUGE-L} = \frac{(1+\beta^2) \cdot \text{Precision} \cdot \text{Recall}}{\beta^2 \cdot \text{Precision} + \text{Recall}}$$

### METEOR
Unigram matching with synonymy (WordNet) + fragmentation penalty.

### CIDEr
TF-IDF weighted n-gram similarity:

$$\text{CIDEr}_n = \frac{1}{M} \sum_j \frac{g^n(c_i) \cdot g^n(s_{ij})}{\|g^n(c_i)\| \|g^n(s_{ij})\|}$$

### SPICE
Scene graph-based: parses caption to semantic tuples (objects, relations, attributes).

## Benchmark Results

| Model | BLEU-4 | CIDEr | METEOR | SPICE |
|-------|--------|-------|--------|-------|
| Show & Tell | 27.7 | 85.5 | 23.7 | — |
| Show, Attend & Tell | 30.0 | 95.5 | 25.1 | — |
| Bottom-Up Top-Down | 36.2 | 113.5 | 27.0 | 20.3 |
| ClipCap | 33.5 | 108.4 | 25.8 | 19.6 |
| GIT (Generative Image-to-text) | 40.5 | 138.2 | 29.8 | 23.4 |

## Practical Considerations
- **Answer space**: VQA uses 3,129 most frequent answers (covers ~82% of questions)
- **Balancing**: VQA v2 balances yes/no questions by collecting complementary images
- **Object detection**: Faster R-CNN features are better than grid features for fine-grained VQA
- **Visual grounding**: Attention maps should align with relevant image regions

## References
- Antol, Agrawal, et al., "VQA: Visual Question Answering", ICCV 2015
- Anderson, He, et al., "Bottom-Up and Top-Down Attention for Image Captioning and Visual Question Answering", CVPR 2018
- Xu, Ba, Kiros, et al., "Show, Attend and Tell: Neural Image Caption Generation with Visual Attention", ICML 2015
- Mokady, Hertz, Bermano, "ClipCap: CLIP Prefix for Image Captioning", 2021
- Lin, "METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments", ACL 2005
