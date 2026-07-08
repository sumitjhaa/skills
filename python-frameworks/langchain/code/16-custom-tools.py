"""Custom tools — @tool decorator and BaseTool subclass."""
from langchain_core.tools import tool, BaseTool


print("=== Custom Tools ===\n")

@tool
def reverse_text(text: str) -> str:
    """Reverse the input text."""
    return text[::-1]

@tool
def count_vowels(text: str) -> int:
    """Count vowels in text."""
    vowels = "aeiouAEIOU"
    return sum(1 for c in text if c in vowels)

@tool
def calculator(expression: str) -> float:
    """Evaluate a math expression."""
    return eval(expression)

class RepeatTool(BaseTool):
    name: str = "repeat"
    description: str = "Repeat text multiple times"

    def _run(self, text: str, times: int = 2) -> str:
        return (text + " ") * times

print(f"reverse_text: {reverse_text.invoke({'text': 'hello'})}")
print(f"count_vowels: {count_vowels.invoke({'text': 'hello world'})}")
print(f"calculator:   {calculator.invoke({'expression': '2 + 3 * 4'})}")

repeat = RepeatTool()
print(f"repeat:       {repeat.invoke({'text': 'hi', 'times': 3})}")

custom_tools = [reverse_text, count_vowels, calculator, repeat]
print(f"\nCustom tools ({len(custom_tools)}):")
for t in custom_tools:
    print(f"  - {t.name}: {t.description}")
