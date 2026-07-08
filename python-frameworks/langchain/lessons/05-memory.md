# 🏗️ Memory
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Add conversation memory to chains.

## ConversationBufferMemory

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("Hi!")
memory.chat_memory.add_ai_message("Hello!")
memory.load_memory_variables({})
# {'history': 'Human: Hi!\nAI: Hello!'}
```

## With Chain

```python
from langchain.chains import ConversationChain

chain = ConversationChain(llm=llm, memory=memory)
chain.invoke("My name is Alice")
chain.invoke("What's my name?")  # Remembers: Alice
```

## Other Memory Types

```python
ConversationBufferWindowMemory(k=2)  # last 2 turns only
ConversationSummaryMemory()          # summarized history
ConversationKGMemory()               # entity-based graph
```

<!-- 🤔 Start with BufferMemory. Switch to WindowMemory for long conversations. -->

## Run the Code

```bash
python code/05-memory.py
```
