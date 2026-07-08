"""Agent executor — run agent with config."""
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.tools import tool


print("=== Agent Executor ===\n")

class MockChatModel(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="The result is 8."))])
    def bind_tools(self, tools, **kwargs):
        return self
    @property
    def _llm_type(self):
        return "mock"

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

tools = [add]
model = MockChatModel()

agent = create_react_agent(model, tools)
result = agent.invoke({"messages": [HumanMessage("What is 3+5?")]})

final = result["messages"][-1]
print(f"Input: What is 3+5?")
print(f"Output: {final.content}")

print("\nagent.invoke() handles the full loop:")
print("  - Formats the tool prompt")
print("  - Calls the LLM")
print("  - Parses tool call requests")
print("  - Executes tools")
print("  - Returns the final result")
