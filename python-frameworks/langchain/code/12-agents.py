"""Agents — create agent using LangGraph."""
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.tools import tool


print("=== Agents ===\n")

class MockChatModel(BaseChatModel):
    """Minimal chat model that supports tool binding."""
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="The answer is 8."))])
    def bind_tools(self, tools, **kwargs):
        return self
    @property
    def _llm_type(self):
        return "mock"

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [add, multiply]
print(f"Tools: {[t.name for t in tools]}")

model = MockChatModel()
agent = create_react_agent(model, tools)
result = agent.invoke({"messages": [HumanMessage("What is 3+5?")]})

print(f"\nAgent response ({len(result['messages'])} messages):")
for msg in result["messages"]:
    c = msg.content if hasattr(msg, "content") else str(msg)
    print(f"  [{msg.type}] {str(c)[:80]}")

print("\ncreate_react_agent builds a ReAct loop:")
print("  1. Reason about the question")
print("  2. Decide which tool to call")
print("  3. Observe tool output")
print("  4. Generate final answer")
