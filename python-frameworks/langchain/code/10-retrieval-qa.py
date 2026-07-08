"""Retrieval QA — answer questions using LCEL."""
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough


print("=== Retrieval QA ===\n")

embeddings = FakeEmbeddings(size=384)

docs = [
    Document(page_content="Python was created by Guido van Rossum in 1991."),
    Document(page_content="Python is used for web development, data science, and AI."),
    Document(page_content="Python has a large standard library with many modules."),
    Document(page_content="Python is dynamically typed and garbage-collected."),
]

vectorstore = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = FakeListLLM(responses=[
    "Python was created by Guido van Rossum in 1991."
])

prompt = PromptTemplate.from_template(
    "Answer using this context:\n{context}\n\nQuestion: {question}"
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("Who created Python?")
print(f"Question: Who created Python?")
print(f"Answer:   {result}")

print("\nRetrieved docs:")
retrieved = retriever.invoke("Who created Python?")
for i, doc in enumerate(retrieved):
    print(f"  [{i}] {doc.page_content}")
