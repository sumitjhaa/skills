"""Memory — in-memory chat history for conversations."""
from langchain_core.chat_history import InMemoryChatMessageHistory


print("=== Memory ===\n")

history = InMemoryChatMessageHistory()

history.add_user_message("Hi, my name is Alice.")
history.add_ai_message("Hi Alice! Nice to meet you.")
history.add_user_message("What's my name?")
history.add_ai_message("Your name is Alice!")

print(f"Full history ({len(history.messages)} messages):")
for msg in history.messages:
    print(f"  {msg.type}: {msg.content}")

print(f"\nWindowed (last 2):")
window = history.messages[-2:]
for msg in window:
    print(f"  {msg.type}: {msg.content}")

history2 = InMemoryChatMessageHistory()
history2.add_user_message("Hello!")
history2.add_ai_message("How can I help you today?")
print(f"\nNew conversation ({len(history2.messages)} messages):")
for msg in history2.messages:
    print(f"  {msg.type}: {msg.content}")
