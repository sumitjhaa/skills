"""LLM basics — invoke, stream, batch with FakeListLLM."""
from langchain_community.llms import FakeListLLM


print("=== LLM Basics ===\n")

responses = [
    "Python is a programming language.",
    "The capital of France is Paris.",
    "Machine learning is a subset of AI.",
]
llm = FakeListLLM(responses=responses)

result = llm.invoke("What is Python?")
print(f"invoke(): {result}")

results = llm.batch(["What is Python?", "What is the capital of France?"])
print(f"batch(): {results}")

results = llm.batch(responses[:3])
print(f"batch(3): {results}")

print("\nFakeListLLM returns predefined responses in order.")
print("Use for testing without API keys.")
