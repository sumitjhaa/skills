# 🏗️ Tools
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create and use tools for LLMs.

## Tool Decorator

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

result = add.invoke({"a": 3, "b": 5})  # 8
```

## Tool Properties

- **name**: function name (auto)
- **description**: docstring (auto)
- **args**: type-hinted parameters (auto)
- **return type**: type-hinted return

## Built-in Tools

```python
from langchain_community.tools import (
    DuckDuckGoSearchRun,  # web search
    WikipediaQueryRun,    # wikipedia
)
```

<!-- 🤔 Tools are the building blocks for agents. One function = one tool. -->

## Run the Code

```bash
python code/11-tools.py
```
