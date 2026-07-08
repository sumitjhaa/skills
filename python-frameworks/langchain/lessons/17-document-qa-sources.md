# 🏗️ Document QA with Sources
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Return sources alongside answers.

## With Sources

```python
doc_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, doc_chain)

result = rag_chain.invoke({"input": "Your question"})
result['answer']          # generated answer
result['context']         # retrieved documents
```

## Source Metadata

```python
for doc in result['context']:
    print(f"From: {doc.metadata.get('source', 'unknown')}")
    print(f"Page: {doc.metadata.get('page', 'N/A')}")
    print(f"Content: {doc.page_content[:100]}...")
```

<!-- 🤔 Returning sources builds trust and enables verification. Critical for production RAG. -->

## Run the Code

```bash
python code/17-document-qa-sources.py
```
