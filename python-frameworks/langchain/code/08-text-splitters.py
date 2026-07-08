"""Text splitters — splitting documents into chunks."""
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents import Document


print("=== Text Splitters ===\n")

text = """Python is a high-level programming language.
Its design philosophy emphasizes code readability.
Python supports multiple programming paradigms.
It has a large standard library.
Python is used in web development, data science, and AI.
The language is dynamically typed and garbage-collected.
Python has a rich ecosystem of third-party packages.
It runs on Windows, macOS, Linux, and more."""

print(f"Original text ({len(text)} chars):")
print(f"  {text[:80]}...\n")

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", ".", " ", ""],
)

recursive_chunks = recursive_splitter.split_text(text)
print(f"RecursiveCharacterTextSplitter: {len(recursive_chunks)} chunks")
for i, chunk in enumerate(recursive_chunks):
    print(f"  [{i}] ({len(chunk):3d} chars): {chunk[:60]}...")

print()
char_splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    separator=" ",
)

docs = [Document(page_content=text)]
char_chunks = char_splitter.split_documents(docs)
print(f"CharacterTextSplitter: {len(char_chunks)} chunks on documents")
for i, chunk in enumerate(char_chunks[:3]):
    print(f"  [{i}] ({len(chunk.page_content):3d} chars): {chunk.page_content[:50]}...")
