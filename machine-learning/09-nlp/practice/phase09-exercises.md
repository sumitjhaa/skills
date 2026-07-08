# Phase 09 Exercises — Natural Language Processing

## Guidelines
- Implement from scratch using only numpy, scipy, matplotlib unless otherwise noted.
- Each exercise builds on concepts from specific lessons.
- Test your implementations on small synthetic datasets.

---

## Exercise 1: Text Normalization Pipeline (09.01)
Implement a text normalization pipeline that:
1. Converts text to lowercase and strips punctuation
2. Implements a Porter stemmer (at least 4 suffix rules)
3. Implements a simple lemmatizer with noun/verb inflection rules
4. Evaluate on 10 test sentences comparing stemmed vs. lemmatized output

**Data:** Create 10 varied sentences with different verb forms, plurals, and possessives.

---

## Exercise 2: BPE Tokenizer (09.02)
Build a BPE tokenizer from scratch:
1. Implement pair statistics and merging
2. Train on a corpus of 5,000 English sentences (or create synthetic data)
3. Encode 10 test words and visualize the merge tree
4. Compare vocabulary size vs. compression ratio

**Deliverable:** Show tokenized output and learned merges for "unhappiness", "transformer", "tokenization".

---

## Exercise 3: Word2Vec Skip-gram (09.03)
Implement Word2Vec with negative sampling:
1. Build a Skip-gram model with embedding dimension 50
2. Implement negative sampling with unigram distribution (^0.75)
3. Train on a small corpus (min. 50 sentences)
4. Compute cosine similarity for 5 word pairs
5. Visualize embeddings using t-SNE (from sklearn or write simple PCA)

**Deliverable:** Similarity matrix for 10 semantically related words.

---

## Exercise 4: N-gram LM with Smoothing (09.04)
Implement an n-gram language model:
1. Support configurable n (2, 3, 4)
2. Implement Kneser-Ney smoothing with discount parameter
3. Compute perplexity on a held-out test set
4. Generate sentences of 15-20 tokens from each n-gram model
5. Compare perplexity across n values

**Deliverable:** Table of perplexity for n=2,3,4 and 5 generated sentences per model.

---

## Exercise 5: Transformer Block (09.05)
Implement a single transformer encoder and decoder block:
1. Multi-head self-attention with causal masking
2. Cross-attention for decoder
3. Layer normalization and feed-forward network
4. Forward pass with random data: B=4, T=16, d=64, H=8
5. Verify the causal mask is working correctly

**Deliverable:** Verify output shapes and that causal mask prevents future token leakage.

---

## Exercise 6: Flash Attention Tiling (09.08)
Implement tiled attention with online softmax:
1. Process Q, K, V in blocks of size B (variable)
2. Implement safe online softmax with rescaling
3. Compare numerical accuracy with standard attention
4. Profile memory savings (simulate with virtual memory tracking)
5. Test with block sizes B=2, 4, 8, 16

**Deliverable:** Max error vs. standard attention for each block size.

---

## Exercise 7: LoRA Finetuning (09.10)
Implement LoRA for a 2-layer MLP classifier:
1. Create a synthetic binary classification dataset (d=20, N=1000)
2. Implement LoRA with configurable rank r
3. Train only LoRA parameters (freeze base weights)
4. Compare accuracy with full finetuning
5. Plot accuracy vs. rank r = [1, 2, 4, 8, 16]

**Deliverable:** Graph showing LoRA accuracy vs. full finetuning across ranks.

---

## Exercise 8: Mixture of Experts (09.14)
Implement a sparse MoE layer:
1. Create 4 expert FFNs with d=32, d_ff=64
2. Implement top-2 routing with softmax gating
3. Add load balancing loss (auxiliary loss)
4. Compare output quality and expert utilization
5. Visualize token-to-expert assignments

**Deliverable:** Histogram of tokens per expert showing balanced routing.

---

## Exercise 9: ReAct Agent (09.27)
Implement a ReAct agent with 3 tools:
1. Calculator (arithmetic operations)
2. Web search (simulated with a local knowledge base)
3. Code interpreter (execute Python expressions)
4. The agent should interleave Thought, Action, Observation
5. Test on 5 multi-step queries

**Deliverable:** Full transcript of agent reasoning for "What is 25 * 4 + 10?" and "Find the capital of France and multiply its population by 0.01".

---

## Exercise 10: RAG System (09.17)
Build a complete RAG system:
1. Create a document store with 20 documents
2. Implement chunking (with overlap), embedding, and retrieval
3. Implement hybrid search (dense + BM25-style sparse)
4. Add a re-ranker (cross-encoder style scoring)
5. Evaluate on 10 questions with and without RAG

**Deliverable:** Table comparing answer quality (1-5 scale) with/without RAG for 10 questions.

---

## Exercise 11: DPO Alignment (09.21)
Implement DPO training:
1. Create a preference dataset of 100 chosen/rejected pairs
2. Implement DPO loss with β parameter
3. Train a simple 2-layer model with DPO
4. Compare with supervised finetuning on chosen answers only
5. Sweep β = [0.01, 0.05, 0.1, 0.5, 1.0]

**Deliverable:** Plot of DPO loss vs. β and final preference accuracy.

---

## Exercise 12: Statistical Watermarking (09.24)
Implement a red-green list watermark:
1. Implement watermark generation with configurable green ratio γ
2. Implement detection with z-score test
3. Evaluate on 100 watermarked and 100 non-watermarked sequences
4. Compute ROC curve (TPR vs FPR) for different z thresholds
5. Test robustness against simulated attack (replace 10%, 20% of tokens)

**Deliverable:** ROC curve and AUC score.

---

## Bonus Challenge: End-to-End LLM App (09.30)
Build a minimal LLM application integrating:
- RAG retrieval from a document store
- Guardrails (input/output filtering)
- Streaming response generation
- Conversation memory (last 5 turns)
- Run 3 example queries showing the full pipeline

**Deliverable:** Working script with interactive query loop.
