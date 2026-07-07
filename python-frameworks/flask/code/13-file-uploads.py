"""File uploads: multipart forms, validation, secure filenames, storage."""
from typing import Any, Optional
from datetime import datetime
import json
import os
import hashlib
import uuid


# ======================== File Upload System ========================

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "csv", "json"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


class UploadedFile:
    def __init__(self, filename: str, content: bytes, content_type: str = "application/octet-stream"):
        self.filename = filename
        self.content = content
        self.content_type = content_type
        self.size = len(content)
        self.uploaded_at = datetime.now()

    @property
    def extension(self) -> str:
        return self.filename.rsplit(".", 1)[-1].lower() if "." in self.filename else ""

    @property
    def safe_filename(self) -> str:
        ext = self.extension
        name = hashlib.md5(f"{self.filename}{uuid.uuid4()}".encode()).hexdigest()[:12]
        return f"{name}.{ext}" if ext else name


class FileValidator:
    @staticmethod
    def validate(file: UploadedFile, allowed: set[str] = None, max_size: int = MAX_CONTENT_LENGTH) -> list[str]:
        errors = []
        allowed = allowed or ALLOWED_EXTENSIONS
        if file.extension not in allowed:
            errors.append(f"Extension '{file.extension}' not allowed. Allowed: {', '.join(sorted(allowed))}")
        if file.size > max_size:
            errors.append(f"File too large: {file.size} bytes (max: {max_size})")
        return errors


class FileStorage:
    def __init__(self):
        self._files: dict[str, dict] = {}

    def save(self, file: UploadedFile, directory: str = "uploads") -> dict:
        safe_name = file.safe_filename
        path = f"{directory}/{safe_name}"
        record = {
            "original_name": file.filename,
            "saved_as": safe_name,
            "path": path,
            "size": file.size,
            "content_type": file.content_type,
            "uploaded_at": file.uploaded_at.isoformat(),
        }
        self._files[safe_name] = record
        return record

    def list(self) -> list[dict]:
        return list(self._files.values())

    def get(self, filename: str) -> Optional[dict]:
        return self._files.get(filename)

    def delete(self, filename: str) -> bool:
        if filename in self._files:
            del self._files[filename]
            return True
        return False

    def total_size(self) -> int:
        return sum(f["size"] for f in self._files.values())


storage = FileStorage()


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Routes ========================

@app.route("/upload", methods=["POST"])
def upload_file(**kw):
    filename = kw.get("filename", "")
    content = kw.get("content", "")
    content_type = kw.get("content_type", "application/octet-stream")

    file = UploadedFile(filename, content.encode() if isinstance(content, str) else content, content_type)

    errors = FileValidator.validate(file)
    if errors:
        return {"error": "validation_failed", "details": errors}

    record = storage.save(file)
    return {
        "message": "Upload successful",
        "file": record,
        "url": f"/files/{record['saved_as']}",
    }


@app.route("/upload/image", methods=["POST"])
def upload_image(**kw):
    filename = kw.get("filename", "")
    content = kw.get("content", "")

    file = UploadedFile(filename, content.encode(), "image/png")
    errors = FileValidator.validate(file, allowed={"png", "jpg", "jpeg", "gif", "webp"}, max_size=5 * 1024 * 1024)
    if errors:
        return {"error": "validation_failed", "details": errors}

    return {"message": "Image uploaded", "file": storage.save(file)}


@app.route("/upload/document", methods=["POST"])
def upload_document(**kw):
    filename = kw.get("filename", "")
    content = kw.get("content", "")

    file = UploadedFile(filename, content.encode(), "application/pdf")
    errors = FileValidator.validate(file, allowed={"pdf", "doc", "docx", "txt"}, max_size=10 * 1024 * 1024)
    if errors:
        return {"error": "validation_failed", "details": errors}

    return {"message": "Document uploaded", "file": storage.save(file)}


@app.route("/files")
def list_files():
    return {"files": storage.list(), "total": len(storage.list()), "total_size": storage.total_size()}


@app.route("/files/<filename>")
def get_file(filename: str):
    record = storage.get(filename)
    if not record:
        return {"error": "File not found"}
    return {"file": record}


@app.route("/files/<filename>", methods=["DELETE"])
def delete_file(filename: str):
    if storage.delete(filename):
        return {"message": "Deleted", "filename": filename}
    return {"error": "File not found"}


@app.route("/upload/multiple", methods=["POST"])
def upload_multiple(**kw):
    results = []
    for key, value in kw.items():
        if key.startswith("file_"):
            filename = key[5:]
            content = value
            file = UploadedFile(filename, content.encode())
            errors = FileValidator.validate(file)
            if errors:
                results.append({"filename": filename, "error": errors})
            else:
                results.append({"filename": filename, "status": "uploaded", "file": storage.save(file)})
    return {"results": results, "count": len(results)}


# ======================== Demo ========================
print("=== File Uploads Demo ===\n")

print("1. Upload valid image:")
r = app("POST", "/upload/image", filename="photo.png", content="fake_png_data_here")
print(f"   {json.dumps(r['data'], indent=2)}\n")

print("2. Upload valid document:")
r = app("POST", "/upload/document", filename="report.pdf", content="PDF content here")
print(f"   {json.dumps(r['data'], indent=2)}\n")

print("3. Upload invalid extension:")
r = app("POST", "/upload/image", filename="script.exe", content="bad")
print(f"   {r['data']}\n")

print("4. Upload oversized:")
large = "x" * (6 * 1024 * 1024)
r = app("POST", "/upload/image", filename="large.png", content=large)
print(f"   {r['data']}\n")

print("5. Multiple files:")
r = app("POST", "/upload/multiple", file_a="content_a", file_b="content_b")
for res in r["data"]["results"]:
    print(f"   {res['filename']}: {res.get('status', 'error')}")

print("\n6. List all files:")
r = app("GET", "/files")
for f in r["data"]["files"]:
    print(f"   - {f['original_name']} ({f['size']} bytes)")
print(f"   Total: {r['data']['total']} files, {r['data']['total_size']} bytes")

print("\n7. Delete file:")
r = app("DELETE", "/files/list_files_0")
print(f"   {json.dumps(r['data'])}")
