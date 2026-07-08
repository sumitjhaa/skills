"""Document loaders — load documents from various sources."""
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
import tempfile
import os


print("=== Document Loaders ===\n")

tmpdir = tempfile.mkdtemp()
file_path = os.path.join(tmpdir, "sample.txt")
with open(file_path, "w") as f:
    f.write("Python is a high-level programming language.\n")
    f.write("It was created by Guido van Rossum in 1991.\n")
    f.write("Python emphasizes code readability.\n")

loader = TextLoader(file_path)
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")
print(f"Content: {docs[0].page_content}")
print(f"Metadata: {docs[0].metadata}")

docs_from_list = [
    Document(page_content="LangChain is a framework for LLM apps."),
    Document(page_content="It provides chains, agents, and retrieval."),
    Document(page_content="You can build RAG systems with it."),
]
print(f"\nIn-memory documents:")
for i, doc in enumerate(docs_from_list):
    print(f"  [{i}] {doc.page_content}")

os.remove(file_path)
os.rmdir(tmpdir)
