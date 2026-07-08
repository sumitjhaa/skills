"""Streaming — stream LLM responses token by token."""
from langchain_community.llms import FakeListLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


print("=== Streaming ===\n")

llm = FakeListLLM(responses=["Hello! I am a helpful AI assistant."])

prompt = PromptTemplate.from_template("Say hello nicely.")

chain = prompt | llm | StrOutputParser()

print("Streaming response:")
for chunk in chain.stream({"input": "Say hello"}):
    print(f"  Chunk: '{chunk}'")

print("\nFakeListLLM returns the full response at once.")
print("Real models stream tokens one by one for better UX.")

print("\nStreaming with real LLMs:")
print("  for chunk in chain.stream({'input': 'Tell me a story'}):")
print("      print(chunk, end='', flush=True)")
