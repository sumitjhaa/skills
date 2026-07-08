"""Integration: full RAG pipeline — ingest, retrieve, answer."""
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough


print("=" * 55)
print("  FULL RAG PIPELINE")
print("=" * 55, "\n")

source_docs = [
    Document(page_content="""Python is a high-level programming language.
It was created by Guido van Rossum and first released in 1991.
Python emphasizes code readability and simplicity.
It supports multiple programming paradigms."""),

    Document(page_content="""Python has a large standard library.
The standard library includes modules for file I/O, networking, and more.
Python's philosophy is 'batteries included'."""),

    Document(page_content="""Python is used in many domains:
web development (Django, Flask), data science (NumPy, Pandas),
machine learning (scikit-learn, PyTorch), and automation."""),
]

print("Phase 1: Ingest")
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_documents(source_docs)
print(f"  {len(source_docs)} docs → {len(chunks)} chunks")

embeddings = FakeEmbeddings(size=384)
vectorstore = InMemoryVectorStore.from_documents(chunks, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
print(f"  Stored in vector store\n")

print("Phase 2: Build Chain")
llm = FakeListLLM(responses=[
    "Python was created by Guido van Rossum in 1991 for general-purpose programming."
])

prompt = PromptTemplate.from_template(
    "Answer using context:\n{context}\n\nQuestion: {question}"
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("Phase 3: Query")
questions = [
    "Who created Python and when?",
    "What is in Python's standard library?",
    "What is Python used for?",
]

for q in questions:
    answer = chain.invoke(q)
    print(f"\n  Q: {q}")
    print(f"  A: {answer}")

print(f"\n{'=' * 55}")
print("  RAG PIPELINE COMPLETE")
print("=" * 55)
