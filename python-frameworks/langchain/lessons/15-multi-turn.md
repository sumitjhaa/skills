# 🏗️ Multi-Turn Conversations
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Full conversational agent with memory and retrieval.

## Memory + Agent

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
)
```

## Conversation Loop

```python
executor.invoke({"input": "Hi, my name is Alice"})
executor.invoke({"input": "What's my name?"})  # remembers Alice
```

<!-- 🤔 Memory lets agents maintain context across turns. Always use with conversational agents. -->

## Run the Code

```bash
python code/15-multi-turn.py
```
