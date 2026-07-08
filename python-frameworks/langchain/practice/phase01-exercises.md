# 📝 LangChain — Phase 01 Practice (LLM Foundations)

## Exercise 1: Custom Prompt Templates

Create a prompt template for a code reviewer. It should take `code`, `language`, and `style_guide` as variables. Test it with a sample Python function and a mock LLM (FakeListLLM).

## Exercise 2: Chain Variants

Implement three chains using the same prompt and LLM:
- `LLMChain` (legacy)
- LCEL pipe (`|`) operator
- `RunnableSequence`

Compare the API for each.

## Exercise 3: Output Parser for Sentiment

Create a custom output parser that takes LLM output and returns a dict `{"sentiment": "positive" | "negative" | "neutral", "confidence": float}`. Use `FakeListLLM` to test parsing logic.

## Exercise 4: Conversation Memory

Build a chatbot with `InMemoryChatMessageHistory` that:
- Remembers user name after first interaction
- Can answer "What's my name?" in follow-ups
- Stores at least 3 turns of history

## Exercise 5: Chat Model Temperature

Create a `FakeListChatModel` with 3 different response lists simulating what different temperature settings might produce. Pass the same prompt and show how responses vary.

## Exercise 6: Document Loader from Files

Without reading a real file, create a `TextLoader` instance. Show how you'd configure the loader and what attributes it exposes. Then simulate loading by manually creating Document objects.

## Exercise 7: Custom Text Splitter

Write a function that splits text by paragraph (double newline) instead of by character count. Compare your chunks to `RecursiveCharacterTextSplitter` output on the same text.

## Exercise 8: Similarity Search Comparison

Using `InMemoryVectorStore` and `FakeEmbeddings`, store 5 different documents. Search with 3 different queries. Show the distance scores for each result.

## Exercise 9: Retriever with Custom Prompt

Build a retrieval QA chain with a custom prompt that instructs the model to answer in exactly 3 sentences. Test it with a question about a known document.

## Exercise 10: End-to-End RAG Pipeline

Combine all Phase 01 components:
1. Ingest 3 documents
2. Split into chunks
3. Embed and store in vector store
4. Build a retrieval chain
5. Query with 2 questions
6. Show both the answer and the source chunks
