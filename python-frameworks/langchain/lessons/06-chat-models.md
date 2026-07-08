# 🏗️ Chat Models
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Use chat models with message types.

## Message Types

```python
from langchain_core.messages import (
    SystemMessage,      # system instructions
    HumanMessage,       # user input
    AIMessage,          # AI response
    FunctionMessage,    # function result
)
```

## Chat Model

```python
from langchain_community.chat_models import FakeListChatModel

model = FakeListChatModel(responses=["Hello! I'm an AI assistant."])
messages = [
    SystemMessage(content="You are helpful."),
    HumanMessage(content="Say hello"),
]
result = model.invoke(messages)
```

## Streaming

```python
for chunk in model.stream(messages):
    print(chunk.content, end="", flush=True)
```

<!-- 🤔 Chat models work with message objects, not raw strings. Use them for conversational interfaces. -->

## Run the Code

```bash
python code/06-chat-models.py
```
