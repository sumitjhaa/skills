"""Document QA with sources — return context with answers."""
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough


print("=== Document QA With Sources ===\n")

embeddings = FakeEmbeddings(size=384)
docs = [
    Document(page_content="Python was created by Guido van Rossum in 1991.", metadata={"source": "history.txt", "page": 1}),
    Document(page_content="Python is dynamically typed and garbage-collected.", metadata={"source": "guide.txt", "page": 5}),
    Document(page_content="Python supports OOP, functional, and procedural programming.", metadata={"source": "guide.txt", "page": 10}),
]
vectorstore = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = FakeListLLM(responses=["Python was created by Guido van Rossum in 1991."])

prompt = PromptTemplate.from_template(
    "Answer based ONLY on:\n{context}\n\nQuestion: {question}"
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("Who created Python?")
print(f"Answer: {result}")

print(f"\nSource documents:")
retrieved = retriever.invoke("Who created Python?")
for i, doc in enumerate(retrieved):
    print(f"  [{i}] {doc.page_content}")
    print(f"       Source: {doc.metadata}")
