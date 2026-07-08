# 🏗️ Agents
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Create agents that use tools.

## Create Agent

```python
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({"input": "Add 5 and 3"})
```

## Agent Types

```python
create_react_agent          # ReAct: Reason + Act
create_tool_calling_agent   # OpenAI function calling
create_structured_chat_agent  # Multi-turn structured
```

## Agent Executor

```python
from langchain.agents import AgentExecutor

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)
```

<!-- 🤔 Start with create_react_agent. Switch to tool_calling for function-calling models. -->

## Run the Code

```bash
python code/12-agents.py
```
