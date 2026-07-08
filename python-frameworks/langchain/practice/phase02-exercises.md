# 📝 LangChain — Phase 02 Practice (Agents & Advanced)

## Exercise 1: Tool Registry

Create a registry of 5 tools (calculator, weather lookup, web search stub, translation, file read). Register them in a dict keyed by name, then write a function that routes a query string to the correct tool based on keyword matching.

## Exercise 2: Agent with Custom Mock Model

Using the `MockChatModel` pattern from lesson 12, create an agent that answers questions about a library of 3+ tools. Use `create_react_agent`. Add a tool that reverses a string.

## Exercise 3: Multi-Query Retrieval

Given a user query, generate 3 rephrased versions using `FakeListLLM`. Run each through the retriever from Phase 01, deduplicate the results, and show the combined set of documents.

## Exercise 4: Conversation Chain with Summary Memory

Using `InMemoryChatMessageHistory`, build a chain that:
1. Stores the full conversation
2. Before answering, formats all previous messages into the prompt
3. Handles at least 5 back-and-forth turns

## Exercise 5: Custom Tool with State

Create a tool that maintains state (e.g., a counter). Use a closure or class to track how many times it's been called. Invoke it multiple times and print the count.

## Exercise 6: QA with Source Metadata

Build a document QA system that, for each answer, also prints:
- Which document(s) provided the evidence
- The relevant excerpt from each source
- A relevance score (distance)

## Exercise 7: Pydantic Structured Output

Define a Pydantic model `Movie` with fields: `title`, `year`, `director`, `rating`. Use `FakeListLLM` + output parser to extract structured data from a text review.

## Exercise 8: Streaming with Callbacks

Implement a callback handler that logs:
- When each chunk is received
- Timing between chunks
- Total response time

## Exercise 9: Hybrid Search

Combine keyword search (simple word matching) with vector similarity search (using `InMemoryVectorStore`). Create a function `hybrid_search(query, docs, alpha=0.5)` that interpolates scores.

## Exercise 10: Full RAG with Filters

Extend the Phase 02 RAG pipeline to support metadata filters. Index documents with tags like `['python', 'tutorial']`. Add a query filter so the retriever only returns documents matching certain tags.
