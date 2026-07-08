# 🏗️ Vector Stores & Embeddings
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Store and retrieve document chunks using embeddings.

## Embeddings

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings

# For testing (no API key needed)
embeddings = FakeEmbeddings(size=384)

# Real
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector = embeddings.embed_query("Hello world")
```

## Vector Store

```python
from langchain_community.vectorstores import InMemoryVectorStore

vectorstore = InMemoryVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
)
```

## Similarity Search

```python
results = vectorstore.similarity_search("your question", k=3)
# Returns top 3 most relevant Document chunks
```

<!-- 🤔 InMemoryVectorStore is great for dev. Use Chroma, FAISS, or Pinecone in production. -->

## Run the Code

```bash
python code/09-vector-stores.py
```
