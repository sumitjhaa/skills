"""Chains — LCEL pipeline with prompt | llm | parser."""
from langchain_community.llms import FakeListLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


print("=== Chains ===\n")

llm = FakeListLLM(responses=["Bonjour", "Hola", "Ciao"])

prompt = PromptTemplate.from_template(
    "Translate {text} to {language}."
)

chain = prompt | llm | StrOutputParser()

result1 = chain.invoke({"text": "Hello", "language": "French"})
print(f"Translate 'Hello' to French: {result1}")

result2 = chain.invoke({"text": "Hello", "language": "Spanish"})
print(f"Translate 'Hello' to Spanish: {result2}")

result3 = chain.invoke({"text": "Hello", "language": "Italian"})
print(f"Translate 'Hello' to Italian: {result3}")

print("\nTwo-step chain:")
prompt1 = PromptTemplate.from_template("Tell me about {topic}.")
prompt2 = PromptTemplate.from_template("Summarize this: {text}")

llm1 = FakeListLLM(responses=["Python is a versatile programming language."])
llm2 = FakeListLLM(responses=["Python is versatile."])

chain2 = prompt1 | llm1 | StrOutputParser()
chain3 = prompt2 | llm2 | StrOutputParser()
combined = chain2 | chain3

result4 = combined.invoke({"topic": "Python"})
print(f"  Combined: {result4}")

print("\nLCEL: chain = prompt | llm | parser")
