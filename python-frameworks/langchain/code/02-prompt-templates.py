"""Prompt templates — PromptTemplate, ChatPromptTemplate, FewShot."""
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate


print("=== Prompt Templates ===\n")

template = PromptTemplate.from_template(
    "Translate {text} to {language}."
)
result = template.format(text="Hello", language="French")
print(f"PromptTemplate: {result}")

template2 = PromptTemplate.from_template(
    "Write a {length} poem about {topic} in the style of {author}."
)
result2 = template2.format(length="short", topic="coding", author="Dr. Seuss")
print(f"Complex template: {result2}")

chat = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("human", "My question is: {question}"),
    ("ai", "Let me think about that..."),
    ("human", "Please answer concisely."),
])
result3 = chat.format_messages(
    role="Python",
    question="What is a decorator?",
)
print(f"\nChatPromptTemplate:")
for msg in result3:
    print(f"  {msg.type}: {msg.content[:60]}...")

examples = [
    {"input": "happy", "output": "joyful"},
    {"input": "sad", "output": "melancholy"},
]
example_template = PromptTemplate.from_template("Input: {input} -> Output: {output}")
few_shot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    suffix="Input: {input} -> Output:",
    input_variables=["input"],
)
result4 = few_shot.format(input="angry")
print(f"\nFewShot: {result4}")
