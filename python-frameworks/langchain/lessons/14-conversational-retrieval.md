# 🏗️ Conversational Retrieval
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Add chat history to RAG.

## With History

```python
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain

# Rewrite question based on history
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, prompt
)

# Answer using retrieved context
qa_chain = create_retrieval_chain(
    history_aware_retriever, document_chain
)
```

## How It Works

1. User asks "Who created it?"
2. LLM rewrites with history: "Who created Python?"
3. Retrieval finds relevant docs
4. LLM generates answer from context

<!-- 🤔 History-aware retrieval is key for follow-up questions in RAG. -->

## Run the Code

```bash
python code/14-conversational-retrieval.py
```
