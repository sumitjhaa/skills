"""Conversational retrieval — RAG with chat history."""
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough


print("=== Conversational Retrieval ===\n")

embeddings = FakeEmbeddings(size=384)
docs = [
    Document(page_content="Python was created by Guido van Rossum in 1991."),
    Document(page_content="Python is used for web development, data science, and AI."),
    Document(page_content="Python has a large standard library."),
]
vectorstore = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = FakeListLLM(responses=["Python was created by Guido van Rossum."])

history = InMemoryChatMessageHistory()
history.add_user_message("Tell me about Python.")
history.add_ai_message("Python is a programming language created in 1991.")

prompt = PromptTemplate.from_template(
    "History: {history}\n"
    "Context: {context}\n"
    "Question: {question}\n"
    "Answer:"
)

def format_docs(docs):
    return "\n".join(d.page_content for d in docs)

def format_history(messages):
    return "\n".join(f"{m.type}: {m.content}" for m in messages)

chain = (
    {
        "context": RunnablePassthrough() | (lambda x: format_docs(retriever.invoke(x))),
        "question": RunnablePassthrough(),
        "history": RunnablePassthrough() | (lambda _: format_history(history.messages)),
    }
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("Who created it?")
print(f"Question: Who created it?")
print(f"Answer:   {result}")
