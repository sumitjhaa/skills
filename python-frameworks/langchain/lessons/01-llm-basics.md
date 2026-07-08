# 🏗️ LLM Basics
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Call LLMs with LangChain.

## Basic LLM Call

```python
from langchain.llms import FakeListLLM

responses = ["Hello! How can I help you?"]
llm = FakeListLLM(responses=responses)
result = llm.invoke("Say hello")
print(result)  # "Hello! How can I help you?"
```

## Real LLM (requires API key)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)
result = llm.invoke("What is Python?")
```

## Key Concepts

- **LLM**: text-in, text-out
- **ChatModel**: messages-in, message-out
- **invoke()**: single call
- **stream()**: streaming response
- **batch()**: multiple inputs

<!-- 🤔 Use FakeListLLM for testing. Switch to real model with an API key. -->

## Run the Code

```bash
python code/01-llm-basics.py
```
