"""Chat models — SystemMessage, HumanMessage, AIMessage."""
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_models import FakeListChatModel


print("=== Chat Models ===\n")

model = FakeListChatModel(responses=[
    "I'm doing great, thanks!",
    "Python is awesome!",
])

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="How are you?"),
]
result = model.invoke(messages)
print(f"System + Human:")
for m in messages:
    print(f"  {m.type}: {m.content}")
print(f"  ai: {result.content}")

messages2 = [
    SystemMessage(content="You are a Python expert."),
    HumanMessage(content="What's your favorite language?"),
    AIMessage(content="I love all languages!"),
    HumanMessage(content="Which is best for data science?"),
]
result2 = model.invoke(messages2)
print(f"\nMulti-turn:")
for m in messages2:
    print(f"  {m.type}: {m.content}")
print(f"  ai: {result2.content}")

print("\nStreaming:")
for chunk in model.stream(messages):
    print(f"  Chunk: '{chunk.content}'")
