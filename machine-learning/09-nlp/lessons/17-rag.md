# 09.17 Retrieval-Augmented Generation (RAG)

## Learning Objectives
- Understand RAG architecture for knowledge-grounded generation
- Implement dense passage retrieval (DPR, Contriever)
- Apply chunking strategies and reranking
- Evaluate RAG systems on open-domain QA

## RAG Architecture

### Pipeline
```
Query → Retriever → (Documents) → Generator → Answer
```

### Components
1. **Retriever**: Search relevant documents from corpus
2. **Generator**: Condition on query + retrieved docs → generate answer

### RAG-Sequence vs RAG-Token
- **RAG-Sequence**: Same documents for all output tokens
- **RAG-Token**: Different documents per token

## Dense Passage Retrieval (DPR)

### Encoders
$$E_Q(q) \in \mathbb{R}^d, \quad E_P(p) \in \mathbb{R}^d$$

- BERT encoders (separate for query and passage)
- 768-dimensional embeddings

### Training
$$\mathcal{L} = -\log \frac{e^{\text{sim}(q, p^+)}}{\sum_{p_i \in \text{batch}} e^{\text{sim}(q, p_i)}}$$

- In-batch negatives: use other passages in batch as negatives
- Hard negatives: retrieved from BM25

## Contriever

### Unsupervised Dense Retrieval
Train without labeled data using:

1. **Contrastive learning**: Crop two spans from same document → positive pair
2. **InfoNCE loss**: Maximize similarity of same-document spans

### Performance
- No labeled data needed for training
- 95% of supervised DPR performance

## Chunking Strategies

| Strategy | Size | Overlap | Pros | Cons |
|----------|------|---------|------|------|
| Fixed token | 256 | 0 | Simple | May split sentences |
| Sentence | ~20 tokens | 1-2 sentences | Semantic units | Variable length |
| Recursive | Varies | 10-20% | Context preservation | Complex |
| Semantic | Varies | None | Natural boundaries | Expensive |

## Reranking

### Two-Stage Pipeline
1. **Retriever**: Retrieve top-K (K=100) with fast embedding search
2. **Reranker**: Score top-K with cross-encoder (slower but more accurate)

### Cross-Encoder
$$s(q, p) = W \cdot \text{BERT}([CLS] q [SEP] p [SEP])_{[CLS]}$$

- Full attention between query and passage
- More accurate than bi-encoder
- Too slow for large-scale retrieval

## Code: RAG Pipeline

```python
import torch
from transformers import AutoModel, AutoTokenizer

class DPR:
    def __init__(self, model_name='facebook/dpr-question_encoder-multiset-base'):
        self.encoder = AutoModel.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def encode(self, texts):
        encoded = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        output = self.encoder(**encoded)
        return output.pooler_output  # (B, D)

class RAGGenerator:
    def __init__(self, retriever, generator, passage_store):
        self.retriever = retriever
        self.generator = generator
        self.passage_store = passage_store

    def retrieve(self, query, top_k=5):
        q_emb = self.retriever.encode([query])
        scores = q_emb @ self.passage_store.embeddings.T
        idxs = scores.topk(top_k).indices[0]
        return [self.passage_store.passages[i] for i in idxs]

    def generate(self, query, max_length=200):
        passages = self.retrieve(query)
        context = " ".join(passages)
        prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
        inputs = self.generator.tokenizer(prompt, return_tensors='pt')
        outputs = self.generator.model.generate(**inputs, max_length=max_length)
        return self.generator.tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## RAG Evaluation

| Dataset | Split | Metric | DPR + BART | FiD | Atlas |
|---------|-------|--------|-----------|-----|-------|
| Natural Questions | Test | EM | 43.6 | 48.2 | 51.2 |
| TriviaQA | Test | EM | 66.8 | 69.3 | 71.3 |
| HotpotQA | Distractor | F1 | 55.3 | 59.2 | 61.8 |
| FEVER | Test | Acc | 75.3 | 78.5 | 80.1 |

## Practical Considerations
- **Index size**: FAISS (GPU) or ScaNN; billions of passages feasible
- **Query rewriting**: Use LLM to rewrite ambiguous queries for retrieval
- **Hybrid search**: Combine dense + sparse (BM25) for better recall
- **Chunking**: 256-512 tokens balanced for retrieval quality
- **Self-RAG**: LLM decides when to retrieve and whether retrieved docs are useful

## References
- Lewis, Perez, et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020
- Karpukhin, Oguz, et al., "Dense Passage Retrieval for Open-Domain Question Answering", EMNLP 2020
- Izacard, Lewis, et al., "Atlas: Few-shot Learning with Retrieval Augmented Language Models", JMLR 2023
- Izacard, Gravier, et al., "Unsupervised Dense Information Retrieval with Contrastive Learning (Contriever)", TMLR 2022
- Asai, Wu, Wang, et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection", ICLR 2024
