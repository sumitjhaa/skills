# 🏗️ Text Splitters
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Split documents into chunks for embedding and retrieval.

## RecursiveCharacterTextSplitter

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=["\n\n", "\n", ".", " ", ""],
)
chunks = splitter.split_documents(documents)
```

## Other Splitters

```python
CharacterTextSplitter        # split by character count
RecursiveCharacterTextSplitter  # split by natural boundaries (recommended)
TokenTextSplitter           # split by token count
MarkdownHeaderTextSplitter  # split by markdown headers
```

## Why Split?

- LLMs have context limits
- Embeddings work better on focused chunks
- Retrieval finds relevant passages

<!-- 🤔 Start with chunk_size=500, chunk_overlap=50. Adjust based on your content. -->

## Run the Code

```bash
python code/08-text-splitters.py
```
