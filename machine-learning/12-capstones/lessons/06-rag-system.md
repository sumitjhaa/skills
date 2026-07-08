# Lesson 12.06: Full RAG System with Evaluation

## Project Architecture

Build a complete Retrieval-Augmented Generation pipeline with document ingestion, chunking, embedding, retrieval, generation, and evaluation.

```
Document Ingestion
  ├── Loader: PDF, TXT, HTML → raw text
  ├── Chunker: recursive character splitting
  │    ├── chunk_size=512, chunk_overlap=50
  │    └── Strategy: sentence, paragraph, semantic
  ├── Embedder: sentence-transformers (mini-LM)
  └── Vector Store: FAISS / numpy index

Retrieval
  ├── Query encoding (same embedder)
  ├── Similarity search (cosine / dot product)
  │    ├── Top-K retrieval
  │    └── Optional: MMR diversification
  └── Context assembly

Generation
  ├── Prompt template: context + question
  ├── Language model (distilgpt2 / custom)
  └── Response generation with citations

Evaluation
  ├── Retrieval: Recall@K, MRR, NDCG
  ├── Generation: BLEU, ROUGE, BERTScore
  ├── End-to-end: Faithfulness (NLI), Answer Relevance
  └── Ablation: chunk size, top-K, embedding model
```

## Design Decisions

### Chunking
- RecursiveCharacterTextSplitter: split on paragraph → sentence → token
- Overlap ensures context isn't lost at boundaries
- Metadata tracking (source, page, chunk index)

### Embedding
- Use a small sentence-transformer model (e.g., `all-MiniLM-L6-v2`) or implement a simple TF-IDF baseline
- Fallback: average of word2vec embeddings

### Vector store
- Flat index (brute force) for small corpora; FAISS IVF for larger
- Cosine similarity on normalized embeddings

### Retrieval
- Dense retrieval with optional Hybrid (BM25 + dense) via weighted sum
- MMR (Maximal Marginal Relevance) to diversify results

### Generation
- Use the transformer from project 12.02 as the generator
- Prompt: "Answer based on: {context}\nQuestion: {question}\nAnswer:"

### Evaluation pipeline
- Create synthetic QA pairs from documents (gold context + question + answer)
- Measure retrieval metrics independent of generation
- Measure end-to-end metrics

## Implementation Guide

1. **Implement document loading and chunking**
2. **Implement embedding** (sentence-transformers or TF-IDF baseline)
3. **Implement vector store** (numpy-based with cosine similarity)
4. **Implement retrieval** (top-K with optional MMR)
5. **Implement prompt construction and generation**
6. **Create synthetic evaluation dataset** from documents
7. **Implement retrieval metrics** (Recall@K, MRR)
8. **Implement generation metrics** (BLEU, ROUGE-L)
9. **Run ablation studies** (chunk size, top-K, embedding choice)
10. **Plot results** and summarize findings

## Key Insights

- RAG quality is bounded by retrieval quality + generation quality
- Chunk size and overlap are critical hyperparameters
- Hybrid retrieval (dense + sparse) often outperforms either alone
- Evaluation requires gold-standard QA pairs for meaningful metrics
- Citation generation improves trustworthiness but is hard to evaluate
