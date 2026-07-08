# 🏗️ Streaming
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Stream LLM responses token by token.

## Basic Streaming

```python
for chunk in chain.stream({"input": "Tell me a story"}):
    print(chunk, end="", flush=True)
```

## Stream Events

```python
async for event in chain.astream_events(...):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

## With Agents

```python
async for chunk in agent_executor.astream({"input": "Hello"}):
    if "output" in chunk:
        print(chunk["output"], end="")
```

<!-- 🤔 Streaming provides better UX. Always stream in production chatbots. -->

## Run the Code

```bash
python code/19-streaming.py
```
