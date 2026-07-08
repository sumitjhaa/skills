# Phase 09 — Natural Language Processing

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 09 — Natural Language Processing |
| **Lessons** | 30 |
| **Core topics** | Text processing, tokenization, word embeddings, language models, encoder-decoder, multilingual, long-range contexts, efficient attention, positional encodings, efficient finetuning (LoRA, etc.), distillation, quantization, pruning, mixture of experts, inference optimization, long-context, RAG, prompt engineering, structured generation, LLM evaluation, alignment (RLHF, DPO), constitutional AI, safety, watermarking, reasoning/math, code LLMs, agents, AI governance, LLM serving, LLM applications |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (embeddings as vectors, attention as inner products), [Phase 03](../03-probability-statistics/INDEX.md) (language models as probability distributions), [Phase 06](../06-deep-learning/INDEX.md) (transformers, attention, autograd, seq2seq)
- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (model building), [`../../python-frameworks/langchain/`](../../python-frameworks/langchain/) (LLM orchestration), [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (data processing)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Text Processing | Regex, stemming, lemmatization, stop words | [lesson](lessons/01-text-processing.md) | [code](code/01-text-processing.py) | Used in: Phase 11 (data pipelines) |
| 02 | Tokenization | BPE, WordPiece, Unigram, SentencePiece | [lesson](lessons/02-tokenization.md) | [code](code/02-tokenization.py) | Used in: Phase 06 (tokenization for transformers) |
| 03 | Word Embeddings | Word2Vec, GloVe, FastText, subword | [lesson](lessons/03-word-embeddings.md) | [code](code/03-word-embeddings.py) | Used in: Phase 01 (SVD connections) |
| 04 | Language Models | N-gram, neural LM, transformer LM | [lesson](lessons/04-language-models.md) | [code](code/04-language-models.py) | Used in: Phase 05 (HMM, CRF) |
| 05 | Encoder-Decoder | BERT, T5, BART, encoder-decoder architectures | [lesson](lessons/05-encoder-decoder.md) | [code](code/05-encoder-decoder.py) | Used in: Phase 06 (seq2seq) |
| 06 | Multilingual | XLM-R, mBERT, cross-lingual transfer | [lesson](lessons/06-multilingual.md) | [code](code/06-multilingual.py) | Used in: Phase 12 (novel contribution) |
| 07 | Long-Range | Longformer, BigBird, Sparse Transformers | [lesson](lessons/07-long-range.md) | [code](code/07-long-range.py) | Used in: Phase 06 (efficient attention) |
| 08 | Efficient Attention | Flash Attention, linear attention, AFT | [lesson](lessons/08-efficient-attention.md) | [code](code/08-efficient-attention.py) | Used in: Phase 11 (GPU optimization) |
| 09 | Positional Encodings | RoPE, ALiBi, YaRN, NTK-aware | [lesson](lessons/09-positional-encodings.md) | [code](code/09-positional-encodings.py) | Used in: Phase 06 (positional encodings) |
| 10 | Efficient Finetuning | LoRA, QLoRA, AdaLoRA, prefix tuning | [lesson](lessons/10-efficient-finetuning.md) | [code](code/10-efficient-finetuning.py) | Used in: Phase 11 (model deployment) |
| 11 | Distillation | Knowledge distillation, token-level, on-policy | [lesson](lessons/11-distillation.md) | [code](code/11-distillation.py) | Used in: Phase 11 (model optimization) |
| 12 | Quantization | INT8, GPTQ, AWQ, bitsandbytes | [lesson](lessons/12-quantization.md) | [code](code/12-quantization.py) | Used in: Phase 11 (serving) |
| 13 | Pruning | Magnitude, SparseGPT, Wanda | [lesson](lessons/13-pruning.md) | [code](code/13-pruning.py) | Used in: Phase 11 (optimization) |
| 14 | Mixture of Experts | MoE, routing, load balancing | [lesson](lessons/14-mixture-of-experts.md) | [code](code/14-mixture-of-experts.py) | Used in: Phase 07 (sparse models) |
| 15 | Inference Optimization | KV cache, continuous batching, speculation | [lesson](lessons/15-inference-optimization.md) | [code](code/15-inference-optimization.py) | Used in: Phase 11 (model serving) |
| 16 | Long Context | Context extension, positional interpolation | [lesson](lessons/16-long-context.md) | [code](code/16-long-context.py) | Used in: Phase 12 (RAG capstone) |
| 17 | RAG | Retrieval-augmented generation, dense retrieval | [lesson](lessons/17-rag.md) | [code](code/17-rag.py) | Used in: Phase 12 (RAG system capstone) |
| 18 | Prompt Engineering | Few-shot, chain-of-thought, instruction tuning | [lesson](lessons/18-prompt-engineering.md) | [code](code/18-prompt-engineering.py) | Used in: Phase 12 (LLM application) |
| 19 | Structured Generation | Grammar-guided, JSON mode, constrained decoding | [lesson](lessons/19-structured-generation.md) | [code](code/19-structured-generation.py) | Used in: Phase 11 (MLOps) |
| 20 | LLM Evaluation | Benchmarks, automated eval, human eval | [lesson](lessons/20-llm-evaluation.md) | [code](code/20-llm-evaluation.py) | Used in: Phase 11 (monitoring) |
| 21 | Alignment | RLHF, DPO, KTO, preference optimization | [lesson](lessons/21-alignment.md) | [code](code/21-alignment.py) | Used in: Phase 10 (RLHF), Phase 12 (RLHF capstone) |
| 22 | Constitutional AI | Self-critique, red-teaming, principles | [lesson](lessons/22-constitutional-ai.md) | [code](code/22-constitutional-ai.py) | Used in: Phase 12 (safety) |
| 23 | Safety | Prompt injection, jailbreaking, guardrails | [lesson](lessons/23-safety.md) | [code](code/23-safety.py) | Used in: Phase 11 (responsible AI) |
| 24 | Watermarking | Text watermarking, detection, robustness | [lesson](lessons/24-watermarking.md) | [code](code/24-watermarking.py) | Used in: Phase 11 (governance) |
| 25 | Reasoning & Math | Chain-of-thought, program-aided, tool use | [lesson](lessons/25-reasoning-math.md) | [code](code/25-reasoning-math.py) | Used in: Phase 07 (neuro-symbolic) |
| 26 | Code LLMs | Code generation, execution, Codex, AlphaCode | [lesson](lessons/26-code-llms.md) | [code](code/26-code-llms.py) | Used in: Phase 12 (agent systems) |
| 27 | Agents | ReAct, tool use, planning, multi-agent | [lesson](lessons/27-agents.md) | [code](code/27-agents.py) | Used in: Phase 10 (multi-agent RL) |
| 28 | AI Governance | Regulation, ethics, bias, transparency | [lesson](lessons/28-ai-governance.md) | [code](code/28-ai-governance.py) | Used in: Phase 11 (responsible AI) |
| 29 | LLM Serving | vLLM, TGI, Triton, batching | [lesson](lessons/29-llm-serving.md) | [code](code/29-llm-serving.py) | Used in: Phase 11 (model serving) |
| 30 | LLM Application | Full-stack LLM app development | [lesson](lessons/30-llm-application.md) | [code](code/30-llm-application.py) | Used in: Phase 12 (capstone) |

## 4. Builds Toward

- **Phase 10** (RLHF — RL with human feedback)
- **Phase 11** (LLM serving, monitoring, responsible AI, cost optimization)
- **Phase 12** (all capstones: transformer, RAG, RLHF, reasoning, novel contribution)

## 5. Quick Start

```bash
python3 code/01-text-processing.py
```
