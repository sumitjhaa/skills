# 09.27 Agents

## Learning Objectives
- Understand LLM agents and tool use
- Implement ReAct (Reasoning + Acting) framework
- Apply multi-agent systems and agent orchestration
- Analyze planning, memory, and tool integration

## Agent Architecture

### Components
```
Agent = LLM Core + Tools + Memory + Planning
```

### Loop
```
Observe → Think → Act → Observe → ...
```

## ReAct (Reasoning + Acting)

### Framework
```
Thought: I need to find the weather in Tokyo.
Action: search("Tokyo weather")
Observation: Tokyo is 22°C with clear skies.
Thought: I have the weather information.
Action: respond("The weather in Tokyo is 22°C and clear.")
```

### Implementation
```python
def react_agent(task, max_steps=10):
    context = f"Task: {task}\n"
    for step in range(max_steps):
        # Think
        thought = llm(f"{context}What should I do next?")
        context += f"Thought: {thought}\n"
        
        # Act
        if "Action:" in thought:
            action = parse_action(thought)
            result = execute_tool(action)
            context += f"Observation: {result}\n"
        else:
            return parse_final_answer(thought)
    return "Max steps reached"
```

## Tools

### Tool Registry
```python
tools = {
    "search": search_function,
    "calculator": calculate,
    "code_executor": run_python,
    "file_reader": read_file,
    "database": query_db,
}
```

### Tool Description
```python
tool_descriptions = {
    "search": {
        "description": "Search the web for information",
        "parameters": {"query": "string"}
    },
    "calculator": {
        "description": "Evaluate mathematical expressions",
        "parameters": {"expression": "string"}
    }
}
```

## Memory Systems

### Short-Term Memory
- Conversation history (within context window)
- Typically 4K-128K tokens

### Long-Term Memory
- External vector database
- Store past experiences, facts, and learnings

```python
class AgentMemory:
    def __init__(self, embedding_model, vector_store):
        self.embedder = embedding_model
        self.store = vector_store

    def add(self, experience):
        emb = self.embedder(experience)
        self.store.add(emb, experience)

    def query(self, question, k=5):
        q_emb = self.embedder(question)
        return self.store.search(q_emb, k)
```

## Multi-Agent Systems

### Example: ChatDev
- **CEO Agent**: Plans tasks, assigns to other agents
- **CTO Agent**: Designs architecture
- **Programmer Agent**: Writes code
- **Reviewer Agent**: Reviews and tests

### Agent Communication
```python
class Agent:
    def __init__(self, name, role, model):
        self.name = name
        self.role = role
        self.model = model

    def send_message(self, recipient, message):
        recipient.receive_message(self.name, message)

    def receive_message(self, sender, content):
        response = self.model.generate(f"{sender}: {content}\n{self.name}:")
        return response
```

## Code: Simple Agent

```python
import json
from typing import Dict, Callable

class ToolCallingAgent:
    def __init__(self, llm, tools: Dict[str, Callable]):
        self.llm = llm
        self.tools = tools
        self.tool_descriptions = self._describe_tools()
        self.memory = []

    def _describe_tools(self):
        desc = ""
        for name, func in self.tools.items():
            desc += f"- {name}: {func.__doc__}\n"
        return desc

    def run(self, task: str, max_steps=10):
        prompt = f"""You are an agent with tools:
{self.tool_descriptions}

Task: {task}

Respond in this format:
Thought: (your reasoning)
Action: tool_name(params)
Observation: (tool result)
... (repeat) ...
Answer: (final answer)

Let me start."""
        context = prompt
        
        for _ in range(max_steps):
            response = self.llm.generate(context)
            context += response + "\n"
            
            if "Action:" in response:
                action_str = response.split("Action:")[1].split("\n")[0].strip()
                tool_name, params_str = action_str.split("(", 1)
                params = json.loads("{" + params_str.replace(")", "}"))
                
                if tool_name in self.tools:
                    result = self.tools[tool_name](**params)
                    context += f"Observation: {result}\n"
            
            if "Answer:" in response:
                return response.split("Answer:")[1].strip()
        
        return "Failed to complete task"
```

## Agent Benchmarks

| Benchmark | Task | Metric | GPT-4 | Claude 3 |
|-----------|------|--------|-------|----------|
| WebShop | Online shopping | Success rate | 62% | 58% |
| ALFWorld | Embodied tasks | Success rate | 37% | 34% |
| AgentBench | Various agent tasks | Score | 87% | 82% |
| ToolBench | Tool use | Pass rate | 75% | 71% |
| SWE-bench | Code fixes | Resolved rate | 16% | 18% |

## Practical Considerations
- **Error recovery**: Agent should handle tool failures gracefully
- **Cost**: Each tool call costs tokens and time
- **Security**: Sandbox tool execution (isolated environment)
- **Hallucination**: Agent may fabricate tool outputs
- **Planning depth**: Complex tasks need hierarchical planning

## References
- Yao, Zhao, et al., "ReAct: Synergizing Reasoning and Acting in Language Models", ICLR 2023
- Schick, Dwivedi-Yu, et al., "Toolformer: Language Models Can Teach Themselves to Use Tools", 2023
- Qin, Hu, et al., "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs", ICLR 2024
- Qian, Cong, et al., "ChatDev: Communicative Agents for Software Development", ACL 2024
- Liu, Ning, et al., "AgentBench: Evaluating LLMs as Agents", ICLR 2024
