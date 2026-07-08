"""
09.17 RAG — Dense Retrieval with Chunking and Cosine Similarity
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class DocumentStore:
    """Simple embedding-based document store."""

    def __init__(self, embedding_dim=16):
        self.embeddings = []
        self.documents = []
        self.embedding_dim = embedding_dim

    def add_documents(self, docs):
        for doc in docs:
            # Simulate embedding with random vectors
            emb = np.random.randn(self.embedding_dim)
            emb = emb / np.linalg.norm(emb)
            self.embeddings.append(emb)
            self.documents.append(doc)

    def retrieve(self, query_embedding, k=3):
        query_emb = query_embedding / np.linalg.norm(query_embedding)
        emb_matrix = np.array(self.embeddings)
        scores = emb_matrix @ query_emb
        top_k = np.argsort(-scores)[:k]
        return [(self.documents[i], scores[i]) for i in top_k]


def chunk_document(text, chunk_size=50, overlap=10):
    """Simple sliding-window chunking."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def embed_text(text, embedding_dim=16):
    """Simple bag-of-characters embedding (for demonstration)."""
    emb = np.zeros(embedding_dim)
    for i, ch in enumerate(text):
        emb[i % embedding_dim] += ord(ch) * 0.001
    return emb / (np.linalg.norm(emb) + 1e-10)


if __name__ == "__main__":
    documents = [
        "The cat sat on the mat near the fireplace. It was warm and cozy.",
        "Dogs are known as man's best friend. They are loyal and protective.",
        "Natural language processing is a field of AI concerned with text.",
        "Transformers use attention mechanisms to process sequences.",
        "Retrieval augmented generation combines search with language models.",
        "The quick brown fox jumps over the lazy dog near the bank.",
        "Machine learning models learn patterns from data without explicit programming.",
        "Python is a popular programming language for data science and AI.",
    ]
    chunks = []
    for doc in documents:
        chunks.extend(chunk_document(doc, chunk_size=10, overlap=2))

    store = DocumentStore(embedding_dim=16)
    for chunk in chunks:
        emb = embed_text(chunk)
        store.embeddings.append(emb)
        store.documents.append(chunk)

    query = "How do transformers work?"
    query_emb = embed_text(query)
    results = store.retrieve(query_emb, k=3)

    print(f"Query: '{query}'\n")
    print("Top retrieved chunks:")
    for i, (doc, score) in enumerate(results):
        print(f"  {i+1}. (score={score:.4f}) '{doc[:80]}...'")

    # Simulate RAG generation: add retrieved context
    context = " ".join(doc for doc, _ in results)
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer: Based on the context, "
    print(f"\nRAG prompt length: {len(prompt)} chars")
    print(f"Context includes {len(results)} relevant chunks")
