# LangChain — LLM Applications

## Overview

20 lessons across 2 phases covering the LangChain ecosystem for building LLM-powered applications.

| Phase | Topic | Lessons | Code |
|-------|-------|---------|------|
| 01 | LLM Foundations | 01–10 | 10 files |
| 02 | Agents & Advanced | 11–20 | 10 files |

## Phase 01 — LLM Foundations

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [LLM Basics](lessons/01-llm-basics.md) | [01-llm-basics.py](code/01-llm-basics.py) | FakeListLLM, invoke, batch, stream |
| 02 | [Prompt Templates](lessons/02-prompt-templates.md) | [02-prompt-templates.py](code/02-prompt-templates.py) | PromptTemplate, ChatPromptTemplate, MessagesPlaceholder |
| 03 | [Output Parsers](lessons/03-output-parsers.md) | [03-output-parsers.py](code/03-output-parsers.py) | StrOutputParser, CommaSeparatedListOutputParser |
| 04 | [Chains](lessons/04-chains.md) | [04-chains.py](code/04-chains.py) | LCEL pipe operator, RunnableSequence, RunnableParallel |
| 05 | [Memory](lessons/05-memory.md) | [05-memory.py](code/05-memory.py) | InMemoryChatMessageHistory, history-aware prompts |
| 06 | [Chat Models](lessons/06-chat-models.md) | [06-chat-models.py](code/06-chat-models.py) | ChatMessage history, FakeListChatModel |
| 07 | [Document Loaders](lessons/07-document-loaders.md) | [07-document-loaders.py](code/07-document-loaders.py) | Document class, metadata, InMemoryVectorStore |
| 08 | [Text Splitters](lessons/08-text-splitters.md) | [08-text-splitters.py](code/08-text-splitters.py) | RecursiveCharacterTextSplitter, chunking strategies |
| 09 | [Vector Stores](lessons/09-vector-stores.md) | [09-vector-stores.py](code/09-vector-stores.py) | FakeEmbeddings, InMemoryVectorStore, similarity search |
| 10 | [Retrieval QA](lessons/10-retrieval-qa.md) | [10-retrieval-qa.py](code/10-retrieval-qa.py) | RetrievalQA chain with source documents |

## Phase 02 — Agents & Advanced

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 11 | [Tools](lessons/11-tools.md) | [11-tools.py](code/11-tools.py) | `@tool` decorator, tool metadata, tool registry |
| 12 | [Agents](lessons/12-agents.md) | [12-agents.py](code/12-agents.py) | create_react_agent, ReAct loop |
| 13 | [Agent Executor](lessons/13-agent-executor.md) | [13-agent-executor.py](code/13-agent-executor.py) | Running and configuring agents |
| 14 | [Conversational Retrieval](lessons/14-conversational-retrieval.md) | [14-conversational-retrieval.py](code/14-conversational-retrieval.py) | Chat history + document retrieval |
| 15 | [Multi-Turn](lessons/15-multi-turn.md) | [15-multi-turn.py](code/15-multi-turn.py) | Multi-turn conversations with memory |
| 16 | [Custom Tools](lessons/16-custom-tools.md) | [16-custom-tools.py](code/16-custom-tools.py) | Custom tool patterns |
| 17 | [Document QA](lessons/17-document-qa-sources.md) | [17-document-qa-sources.py](code/17-document-qa-sources.py) | QA with source attribution |
| 18 | [Structured Output](lessons/18-structured-output.md) | [18-structured-output.py](code/18-structured-output.py) | JSON output, pydantic parsing |
| 19 | [Streaming](lessons/19-streaming.md) | [19-streaming.py](code/19-streaming.py) | Stream LLM responses |
| 20 | [RAG Pipeline](lessons/20-rag-pipeline.md) | [20-rag-pipeline.py](code/20-rag-pipeline.py) | Full end-to-end RAG system |

## Key Libraries

```txt
langchain            — core framework
langchain-community  — community integrations (FakeListLLM, FakeEmbeddings, InMemoryVectorStore)
langchain-core       — base classes (prompts, parsers, memory)
langchain-text-splitters — text chunking utilities
langgraph            — agent framework (create_react_agent)
```

## Notes

- All code runs **offline** with `FakeListLLM` / `FakeListChatModel` / `FakeEmbeddings` — no API keys needed
- Agent lessons use `MockChatModel` (custom subclass) because `FakeListChatModel` doesn't support `bind_tools`
- Use `langchain_community.*` imports for community components, `langchain_core.*` for core abstractions
- Always set `pip install langchain langchain-community langchain-core langchain-text-splitters langgraph` before running

## Practice

- [Phase 01 Exercises](practice/phase01-exercises.md)
- [Phase 02 Exercises](practice/phase02-exercises.md)
