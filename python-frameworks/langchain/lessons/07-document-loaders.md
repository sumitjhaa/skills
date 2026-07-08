# 🏗️ Document Loaders
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Load documents from various sources.

## Text Loader

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("file.txt")
documents = loader.load()  # list of Document objects
```

## Other Loaders

```python
from langchain_community.document_loaders import (
    CSVLoader,         # CSV files
    PyPDFLoader,       # PDFs
    JSONLoader,        # JSON
    DirectoryLoader,   # All files in a directory
    WebBaseLoader,     # Web pages
)

# Documents have: page_content, metadata
doc = documents[0]
doc.page_content  # the text
doc.metadata      # source, page, etc.
```

<!-- 🤔 Document loaders convert external data into a uniform Document format. -->

## Run the Code

```bash
python code/07-document-loaders.py
```
