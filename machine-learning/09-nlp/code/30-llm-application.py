"""
09.30 End-to-End LLM Application — Full Stack with RAG, Streaming, Guardrails
Built with only numpy, scipy, matplotlib.
"""
import numpy as np
import time


class EmbeddingModel:
    def embed(self, text):
        return np.random.randn(32)


class SimpleVectorDB:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add(self, doc, emb):
        self.documents.append(doc)
        self.embeddings.append(emb)

    def search(self, query_emb, k=3):
        scores = [np.dot(query_emb, e) for e in self.embeddings]
        top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(self.documents[i], scores[i]) for i in top]


class LLMBackend:
    def generate(self, prompt, stream=False):
        response = f"Based on the context provided, here is the answer to your question."
        if stream:
            for word in response.split():
                yield word + " "
                time.sleep(0.05)
        else:
            return response


class Guardrail:
    def check(self, text):
        blocked = ["hack", "exploit", "illegal"]
        for b in blocked:
            if b in text.lower():
                return False
        return True


class FullStackApp:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.vector_db = SimpleVectorDB()
        self.llm = LLMBackend()
        self.guardrail = Guardrail()

    def ingest(self, documents):
        for doc in documents:
            emb = self.embedder.embed(doc)
            self.vector_db.add(doc, emb)

    def query(self, question, stream=False):
        if not self.guardrail.check(question):
            return "I cannot process this request.", []

        query_emb = self.embedder.embed(question)
        retrieved = self.vector_db.search(query_emb, k=2)
        context = "\n".join([doc for doc, _ in retrieved])
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer: "

        if stream:
            return self.llm.generate(prompt, stream=True), retrieved
        response = self.llm.generate(prompt)
        return response, retrieved


if __name__ == "__main__":
    app = FullStackApp()

    app.ingest([
        "Natural language processing is a subfield of AI.",
        "Transformers use attention mechanisms for sequence processing.",
        "RAG combines retrieval with generation for grounded outputs.",
    ])

    questions = [
        "What is natural language processing?",
        "How do I hack into a system?",
    ]

    for question in questions:
        print(f"\nQ: {question}")
        response, sources = app.query(question)
        print(f"A: {response}")
        if sources:
            print(f"Sources: {[s[:40] for s, _ in sources]}")
