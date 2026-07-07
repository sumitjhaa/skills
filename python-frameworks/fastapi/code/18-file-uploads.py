"""File uploads: multipart form data, file validation, storage backends."""
from typing import Any, Optional
from datetime import datetime
import json
import hashlib
import os


# ======================== Simulated Upload ========================

class UploadFile:
    """Simulates FastAPI's UploadFile."""
    def __init__(self, filename: str, content: bytes, content_type: str = "application/octet-stream"):
        self.filename = filename
        self.content = content
        self.content_type = content_type
        self.size = len(content)

    async def read(self) -> bytes:
        return self.content

    async def write(self, path: str):
        with open(path, "wb") as f:
            f.write(self.content)

    @property
    def extension(self) -> str:
        return self.filename.rsplit(".", 1)[-1].lower() if "." in self.filename else ""


class FormData:
    """Simulates multipart form data parsing."""
    def __init__(self, **fields):
        self.fields = fields
        self.files: dict[str, UploadFile] = {}


class StorageBackend:
    """Abstract storage backend."""
    def save(self, file: UploadFile, path: str) -> str:
        raise NotImplementedError

    def delete(self, path: str):
        raise NotImplementedError

    def url(self, path: str) -> str:
        raise NotImplementedError


class LocalStorage(StorageBackend):
    """Store files on local filesystem."""
    def __init__(self, base_path: str = "uploads"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save(self, file: UploadFile, subdir: str = "") -> str:
        dir_path = os.path.join(self.base_path, subdir)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, file.filename)
        # In real app: file.write(file_path)
        return file_path

    def url(self, path: str) -> str:
        return f"/static/{path}"

    def exists(self, path: str) -> bool:
        return os.path.exists(path)


class MemoryStorage(StorageBackend):
    """Store files in memory (for testing)."""
    def __init__(self):
        self._files: dict[str, bytes] = {}

    def save(self, file: UploadFile, subdir: str = "") -> str:
        path = f"{subdir}/{file.filename}" if subdir else file.filename
        self._files[path] = file.content
        return path

    def url(self, path: str) -> str:
        return f"/files/{path}"

    def list_files(self) -> list[dict]:
        return [{"path": k, "size": len(v)} for k, v in self._files.items()]


class FileValidator:
    """Validate uploaded files."""
    ALLOWED_IMAGES = {"jpg", "jpeg", "png", "gif", "webp"}
    ALLOWED_DOCUMENTS = {"pdf", "doc", "docx", "txt", "md"}
    ALLOWED_VIDEOS = {"mp4", "mov", "avi"}
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def validate(cls, file: UploadFile, allowed_extensions: set[str], max_size: int) -> list[str]:
        errors = []
        if file.extension not in allowed_extensions:
            errors.append(f"Invalid extension '{file.extension}'. Allowed: {', '.join(sorted(allowed_extensions))}")
        if file.size > max_size:
            errors.append(f"File too large: {file.size} bytes (max: {max_size} bytes)")
        return errors


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.storage = MemoryStorage()

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.post("/upload/image")
def upload_image(
    filename: str = "",
    content: str = "",
    content_type: str = "image/png",
    alt_text: str = "",
    author: str = "",
    category: str = "general",
):
    """Upload an image file."""
    file_bytes = content.encode() if content else b""
    upload_file = UploadFile(filename=filename or "unnamed.png", content=file_bytes, content_type=content_type)

    errors = FileValidator.validate(upload_file, FileValidator.ALLOWED_IMAGES, FileValidator.MAX_IMAGE_SIZE)
    if errors:
        return {"error": "validation_failed", "details": errors}

    path = app.storage.save(upload_file, subdir="images")
    return {
        "filename": upload_file.filename,
        "size": upload_file.size,
        "content_type": upload_file.content_type,
        "url": app.storage.url(path),
        "alt_text": alt_text or upload_file.filename,
        "author": author or "anonymous",
        "category": category,
    }


@app.post("/upload/document")
def upload_document(
    filename: str = "",
    content: str = "",
    content_type: str = "application/pdf",
    title: str = "",
    author: str = "",
):
    """Upload a document."""
    file_bytes = content.encode() if content else b""
    upload_file = UploadFile(filename=filename or "document.txt", content=file_bytes, content_type=content_type)

    errors = FileValidator.validate(upload_file, FileValidator.ALLOWED_DOCUMENTS, FileValidator.MAX_DOCUMENT_SIZE)
    if errors:
        return {"error": "validation_failed", "details": errors}

    path = app.storage.save(upload_file, subdir="documents")
    return {
        "filename": upload_file.filename,
        "size": upload_file.size,
        "content_type": upload_file.content_type,
        "url": app.storage.url(path),
        "title": title or upload_file.filename,
        "author": author or "anonymous",
    }


@app.get("/files")
def list_files():
    """List all uploaded files."""
    return {"files": app.storage.list_files(), "total": len(app.storage.list_files())}


# ======================== Demo ========================
print("=== File Upload Demo ===\n")

print("1. Upload valid image:")
result = app("POST", "/upload/image",
    filename="photo.png",
    content="fake_image_binary_data",
    content_type="image/png",
    alt_text="A photo",
    author="alice",
)
print(f"   {json.dumps(result['data'], indent=2)}\n")

print("2. Upload valid document:")
result = app("POST", "/upload/document",
    filename="report.pdf",
    content="fake_pdf_content",
    content_type="application/pdf",
    title="Annual Report",
    author="bob",
)
print(f"   {json.dumps(result['data'], indent=2)}\n")

print("3. Upload invalid extension:")
result = app("POST", "/upload/image",
    filename="script.exe",
    content="bad",
    content_type="application/x-msdownload",
)
print(f"   {result['data']}\n")

print("4. Upload oversized file:")
large_content = "x" * (6 * 1024 * 1024)  # 6MB (exceeds 5MB limit)
result = app("POST", "/upload/image",
    filename="large.png",
    content=large_content,
    content_type="image/png",
)
print(f"   {result['data']}\n")

print("5. Upload another image:")
result = app("POST", "/upload/image",
    filename="avatar.jpg",
    content="avatar_data",
    content_type="image/jpeg",
    author="charlie",
)
print(f"   {result['data']}\n")

print("6. List all files:")
result = app("GET", "/files")
print(f"   {json.dumps(result['data'], indent=2)}\n")

# Allowed extensions summary
print("7. Allowed extensions:")
print(f"   Images:    {', '.join(sorted(FileValidator.ALLOWED_IMAGES))}")
print(f"   Documents: {', '.join(sorted(FileValidator.ALLOWED_DOCUMENTS))}")
print(f"   Videos:    {', '.join(sorted(FileValidator.ALLOWED_VIDEOS))}")
