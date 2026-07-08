"""Tools — create and invoke tools with @tool decorator."""
from langchain_core.tools import tool


print("=== Tools ===\n")

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def word_count(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

print(f"add.invoke({{'a': 3, 'b': 5}}): {add.invoke({'a': 3, 'b': 5})}")
print(f"multiply.invoke({{'a': 4, 'b': 7}}): {multiply.invoke({'a': 4, 'b': 7})}")
print(f"word_count.invoke({{'text': 'hello world'}}): {word_count.invoke({'text': 'hello world'})}")

print(f"\nTool name:        {add.name}")
print(f"Tool description: {add.description}")
print(f"Tool args:        {add.args}")

tools = [add, multiply, word_count]
print(f"\nTool list ({len(tools)} tools):")
for t in tools:
    print(f"  - {t.name}: {t.description}")
