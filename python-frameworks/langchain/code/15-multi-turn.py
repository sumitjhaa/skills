"""Multi-turn — simulate conversation with memory."""
from langchain_community.llms import FakeListLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory


print("=== Multi-Turn Conversations ===\n")

llm = FakeListLLM(responses=[
    "Hello Alice! Nice to meet you.",
    "You told me your name is Alice.",
    "3 + 5 equals 8.",
])

history = InMemoryChatMessageHistory()

prompt = PromptTemplate.from_template(
    "Previous conversation:\n{history}\n\nHuman: {input}\nAI:"
)

def format_history(messages):
    return "\n".join(f"{m.type}: {m.content}" for m in messages)

chain = prompt | llm | StrOutputParser()

inputs = [
    "Hi! My name is Alice.",
    "What's my name?",
    "What is 3 + 5?",
]

for inp in inputs:
    result = chain.invoke({"history": format_history(history.messages), "input": inp})
    history.add_user_message(inp)
    history.add_ai_message(result)
    print(f"Human: {inp}")
    print(f"AI:    {result}\n")

print("Memory enables follow-up questions.")
print("Each turn builds on the conversation history.")
