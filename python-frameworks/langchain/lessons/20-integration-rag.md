# 🏗️ Integration: Full RAG Pipeline
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Complete RAG system with ingestion, retrieval, and QA.

## Pipeline

```
1. Load documents          → Document Loaders
2. Split into chunks       → Text Splitters
3. Create embeddings       → Embeddings
4. Store in vector DB      → Vector Store
5. Create retriever        → Retriever
6. Build QA chain          → LCEL chain
7. Query with context      → invoke()
```

## Code

```python
# Ingest
chunks = splitter.split_documents(docs)
vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)

# Retrieve + Answer
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)
result = chain.invoke("Your question")
```

<!-- 🤔 This is the core RAG pattern. Every production system builds on this. -->

## Run the Code

```bash
python code/20-integration-rag.py
```
