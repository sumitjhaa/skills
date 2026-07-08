"""Vector stores & embeddings — store and search documents."""
from langchain_core.documents import Document
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore


print("=== Vector Stores & Embeddings ===\n")

embeddings = FakeEmbeddings(size=384)

docs = [
    Document(page_content="Python is a programming language created in 1991."),
    Document(page_content="Java is a compiled programming language for enterprise."),
    Document(page_content="JavaScript is used for web development."),
    Document(page_content="C is a low-level systems programming language."),
    Document(page_content="Machine learning uses algorithms to learn from data."),
]

vectorstore = InMemoryVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
)

print("Searching for 'programming language':")
results = vectorstore.similarity_search("programming language", k=3)
for i, doc in enumerate(results):
    print(f"  [{i}] {doc.page_content}")

print(f"\nSearch with score:")
results_scored = vectorstore.similarity_search_with_score("web development", k=2)
for i, (doc, score) in enumerate(results_scored):
    print(f"  [{i}] (score={score:.4f}) {doc.page_content}")

print(f"\nEmbedding dimension: {len(embeddings.embed_query('test'))}")
