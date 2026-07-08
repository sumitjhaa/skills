# 🏗️ Agent Executor
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Configure and run an agent executor.

## Configuration

```python
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,            # print reasoning steps
    max_iterations=10,       # max thought-action cycles
    max_execution_time=30,   # seconds
    early_stopping_method="generate",  # or "force"
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)
```

## Intermediate Steps

```python
result = executor.invoke({"input": "Calculate 2+2 and 5*3"})
result['output']               # final answer
result['intermediate_steps']   # list of (action, output) pairs
```

<!-- 🤔 Use return_intermediate_steps=True for debugging agent behavior. -->

## Run the Code

```bash
python code/13-agent-executor.py
```
