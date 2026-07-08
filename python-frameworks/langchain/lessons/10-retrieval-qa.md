# 🏗️ Retrieval QA
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Answer questions using retrieved documents.

## RetrievalQA Chain

```python
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
)
result = qa.invoke("What is Python?")
```

## With Sources

```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True,
)
result = qa.invoke("What is Python?")
result['result']         # the answer
result['source_documents']  # chunks used
```

## Custom Prompt

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Answer using ONLY this context:\n{context}\n\nQuestion: {question}"
)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type_kwargs={"prompt": prompt})
```

<!-- 🤔 RetrievalQA is the simplest way to build a RAG system. Start here. -->

## Run the Code

```bash
python code/10-retrieval-qa.py
```
