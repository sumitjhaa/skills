# 🏗️ Custom Tools
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Create custom tools with complex logic.

## Tool with Args

```python
@tool
def fetch_weather(city: str, units: str = "celsius") -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 22°{units[0].upper()}"
```

## Tool Class

```python
from langchain_core.tools import BaseTool

class DatabaseQuery(BaseTool):
    name = "db_query"
    description = "Query the database"

    def _run(self, query: str) -> str:
        return execute_sql(query)

    async def _arun(self, query: str) -> str:
        raise NotImplementedError
```

<!-- 🤔 Use the @tool decorator for simple functions, BaseTool for complex initialization. -->

## Run the Code

```bash
python code/16-custom-tools.py
```
