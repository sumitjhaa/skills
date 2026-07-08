# 09.06 Multilingual NLP

## Learning Objectives
- Understand multilingual embeddings and cross-lingual transfer
- Implement Sentence-BERT for bitext retrieval
- Apply XLM-R for zero-shot cross-lingual classification
- Analyze challenges in low-resource language modelling

## Multilingual Embeddings

### Aligned Embeddings
Map monolingual embeddings to shared space:

$$W^* = \arg\min_W \|W X - Y\|_F$$

- $X$: source embeddings
- $Y$: target embeddings (bilingual dictionary pairs)
- Procrustes alignment (orthogonal constraint)

### LASER (Language-Agnostic SEntence Representations)
Single BiLSTM encoder trained on 93 languages:

- Shared BPE vocabulary (200K)
- Training: parallel data, max-margin loss
- Zero-shot transfer possible

## Multilingual BERT (mBERT)

### Architecture
Same as BERT-Base (12 layers, 768 hidden) but trained on 104 languages with shared WordPiece vocabulary.

### Cross-Lingual Transfer
- Fine-tune on English, evaluate on target language
- Works for high-resource languages (French, German, Spanish)
- Fails for low-resource or typologically distant languages (Japanese, Korean)

## XLM-R (XLM-RoBERTa)

### Improvements over mBERT
- Trained on 100 languages with 2.5TB CommonCrawl data
- 250K SentencePiece vocabulary (larger = better coverage)
- XLM-R XL: 3.5B parameters

### Results
| Task | mBERT | XLM-R | XLM-R XL |
|------|-------|-------|----------|
| XNLI (avg 15 languages) | 69.8 | 79.2 | 82.3 |
| MLQA (cross-lingual QA) | 61.4 | 70.5 | 74.0 |
| NER (cross-lingual) | 58.0 | 75.0 | 78.5 |

## Code: Sentence-BERT for Bitext Retrieval

```python
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class SentenceBERT(nn.Module):
    def __init__(self, model_name='xlm-roberta-base'):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)

    def mean_pooling(self, token_embeds, attention_mask):
        mask = attention_mask.unsqueeze(-1)
        return (token_embeds * mask).sum(dim=1) / mask.sum(dim=1)

    def forward(self, sentences):
        tokenizer = AutoTokenizer.from_pretrained(self.encoder.config._name_or_path)
        encoded = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        outputs = self.encoder(**encoded)
        embeddings = self.mean_pooling(outputs.last_hidden_state, encoded['attention_mask'])
        return nn.functional.normalize(embeddings, p=2, dim=1)

def retrieve_bitext(source_sents, target_sents, query, model, top_k=5):
    src_emb = model(source_sents)
    tgt_emb = model(target_sents)
    q_emb = model([query])
    scores = q_emb @ src_emb.T
    idxs = scores.topk(top_k).indices[0]
    return [(source_sents[i], target_sents[i]) for i in idxs]
```

## Challenges

### Low-Resource Languages
- Data scarcity: less than 1M tokens available
- Cognate sharing: benefits related languages (Spanish/Italian)
- Script variation: 25% of languages use non-Latin scripts

### Vocabulary Overlap
- mBERT: 30% tokens shared across languages
- XLM-R: larger vocab helps but still biased toward high-resource languages

### Typological Diversity
- Word order: SOV (Japanese), VSO (Arabic), free order (Latin)
- Morphology: agglutinative (Turkish), fusional (Russian), isolating (Chinese)

## Multilingual Benchmarks
- XNLI: 15 languages, natural language inference
- MLQA: 7 languages, extractive QA
- XQuAD: 13 languages, SQuAD-style QA
- TyDiQA: 11 languages, typologically diverse QA

## References
- Conneau, Lample, et al., "XNLI: Evaluating Cross-lingual Sentence Representations", EMNLP 2018
- Conneau, Khandelwal, et al., "Unsupervised Cross-lingual Representation Learning at Scale (XLM-R)", ACL 2020
- Artetxe & Schwenk, "Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond (LASER)", TACL 2019
- Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks", EMNLP 2019
- Hu, Ruder, et al., "XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalisation", ICML 2020
