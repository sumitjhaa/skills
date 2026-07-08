# Phase 09: Natural Language Processing

> From text preprocessing to production LLM applications.

## Overview

| # | Lesson | Topic | Description |
|---|--------|-------|-------------|
| 09.01 | [Text Processing](lessons/01-text-processing.md) | Normalization, Stemming, Lemmatization | Clean and normalize text, reduce words to root forms |
| 09.02 | [Tokenization](lessons/02-tokenization.md) | BPE, WordPiece, SentencePiece | Subword tokenization algorithms for modern NLP |
| 09.03 | [Word Embeddings](lessons/03-word-embeddings.md) | Word2Vec, GloVe, FastText | Dense vector representations of words |
| 09.04 | [Language Models](lessons/04-language-models.md) | N-gram, GPT, Llama | Statistical and neural language modeling |
| 09.05 | [Encoder-Decoder](lessons/05-encoder-decoder.md) | T5, BART | Sequence-to-sequence transformer architectures |
| 09.06 | [Multilingual NLP](lessons/06-multilingual.md) | mT5, BLOOM, NLLB | Cross-lingual models and translation |
| 09.07 | [Long-Range](lessons/07-long-range.md) | Transformer-XL, Longformer, S4 | Architectures for long document processing |
| 09.08 | [Efficient Attention](lessons/08-efficient-attention.md) | Flash Attention | IO-aware exact attention algorithms |
| 09.09 | [Positional Encodings](lessons/09-positional-encodings.md) | RoPE, ALiBi | Relative position representations |
| 09.10 | [Efficient Finetuning](lessons/10-efficient-finetuning.md) | LoRA, Adapters | Parameter-efficient transfer learning |
| 09.11 | [Distillation](lessons/11-distillation.md) | Knowledge Distillation | Compress large models into smaller ones |
| 09.12 | [Quantization](lessons/12-quantization.md) | INT8, GPTQ, AWQ | Reduce model precision for faster inference |
| 09.13 | [Pruning](lessons/13-pruning.md) | Magnitude, SparseGPT | Remove redundant weights from networks |
| 09.14 | [Mixture of Experts](lessons/14-mixture-of-experts.md) | Switch Transformer, Mixtral | Conditional computation with expert routing |
| 09.15 | [Inference Optimization](lessons/15-inference-optimization.md) | PagedAttention, Speculative Decoding | Speed up LLM text generation |
| 09.16 | [Long-Context](lessons/16-long-context.md) | StreamingLLM, Ring Attention | Extend context windows beyond pretrained limits |
| 09.17 | [RAG](lessons/17-rag.md) | Retrieval-Augmented Generation | Ground LLMs with external knowledge |
| 09.18 | [Prompt Engineering](lessons/18-prompt-engineering.md) | CoT, DSPy | Systematic prompt design and optimization |
| 09.19 | [Structured Generation](lessons/19-structured-generation.md) | Grammar-guided, JSON-mode | Constrain LLM outputs to formal schemas |
| 09.20 | [LLM Evaluation](lessons/20-llm-evaluation.md) | Benchmarks, Metrics | Systematic assessment of model capabilities |
| 09.21 | [Alignment](lessons/21-alignment.md) | RLHF, DPO | Human-preference tuning of LLMs |
| 09.22 | [Constitutional AI](lessons/22-constitutional-ai.md) | Self-supervised Safety | Train models with constitutional principles |
| 09.23 | [Safety](lessons/23-safety.md) | Red Teaming, Guardrails | Robustness against misuse and harmful outputs |
| 09.24 | [Watermarking](lessons/24-watermarking.md) | Statistical, Cryptographic | Detect and prove AI-generated text |
| 09.25 | [Reasoning & Math](lessons/25-reasoning-math.md) | o1, DeepSeek R1 | Chain-of-thought and mathematical reasoning |
| 09.26 | [Code LLMs](lessons/26-code-llms.md) | CodeLlama, StarCoder | Models specialized for code generation |
| 09.27 | [Agents](lessons/27-agents.md) | ReAct, AutoGen | LLM-driven autonomous agents |
| 09.28 | [AI Governance](lessons/28-ai-governance.md) | Policy, Standards | Regulatory and ethical frameworks |
| 09.29 | [LLM Serving](lessons/29-llm-serving.md) | vLLM, TGI | Production deployment of language models |
| 09.30 | [End-to-End App](lessons/30-llm-application.md) | Full Stack | Build and deploy a complete LLM application |

## Code

Each `code/` directory contains a standalone Python implementation for the corresponding lesson, built with only numpy, scipy, and matplotlib.

## Quick Start

```bash
# Run any lesson's code
python code/01-text-processing.py

# Read a lesson
cat lessons/01-text-processing.md

# Practice exercises
code practice/phase09-exercises.md
```

**Dependencies:** `numpy`, `scipy`, `matplotlib`

## Practice

[Phase 09 Exercises](practice/phase09-exercises.md) — 12 hands-on exercises covering the full pipeline.
