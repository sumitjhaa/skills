"""File handling & storage backends: file uploads, S3, image processing."""
from typing import Any, Optional
import os
import hashlib
import time
import json
from datetime import datetime


# ======================== Storage Backend Simulation ========================

class StorageBackend:
    """Base class for storage backends (simulates Django's storages)."""
    def save(self, name: str, content: bytes) -> str:
        raise NotImplementedError

    def open(self, name: str) -> Optional[bytes]:
        raise NotImplementedError

    def delete(self, name: str) -> bool:
        raise NotImplementedError

    def exists(self, name: str) -> bool:
        raise NotImplementedError

    def url(self, name: str) -> str:
        raise NotImplementedError

    def size(self, name: str) -> int:
        raise NotImplementedError


class LocalFileSystemStorage(StorageBackend):
    """Simulates Django's FileSystemStorage."""
    def __init__(self, base_dir: str = "/tmp/media"):
        self.base_dir = base_dir
        self._files: dict[str, bytes] = {}
        os.makedirs(base_dir, exist_ok=True)

    def save(self, name: str, content: bytes) -> str:
        self._files[name] = content
        return os.path.join(self.base_dir, name)

    def open(self, name: str) -> Optional[bytes]:
        return self._files.get(name)

    def delete(self, name: str) -> bool:
        if name in self._files:
            del self._files[name]
            return True
        return False

    def exists(self, name: str) -> bool:
        return name in self._files

    def url(self, name: str) -> str:
        return f"/media/{name}"

    def size(self, name: str) -> int:
        content = self._files.get(name)
        return len(content) if content else 0


class S3Storage(StorageBackend):
    """Simulates S3-compatible storage."""
    def __init__(self, bucket: str = "my-bucket", region: str = "us-east-1"):
        self.bucket = bucket
        self.region = region
        self._files: dict[str, bytes] = {}

    def save(self, name: str, content: bytes) -> str:
        self._files[name] = content
        return f"s3://{self.bucket}/{name}"

    def open(self, name: str) -> Optional[bytes]:
        return self._files.get(name)

    def delete(self, name: str) -> bool:
        if name in self._files:
            del self._files[name]
            return True
        return False

    def exists(self, name: str) -> bool:
        return name in self._files

    def url(self, name: str) -> str:
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{name}"

    def size(self, name: str) -> int:
        content = self._files.get(name)
        return len(content) if content else 0


# ======================== File Upload Handler ========================

class UploadedFile:
    """Simulates Django's UploadedFile."""
    def __init__(self, name: str, content: bytes, content_type: str = "application/octet-stream"):
        self.name = name
        self.content = content
        self.content_type = content_type
        self.size = len(content)

    def read(self) -> bytes:
        return self.content

    def chunks(self, chunk_size: int = 65536):
        for i in range(0, len(self.content), chunk_size):
            yield self.content[i:i + chunk_size]


# ======================== File Utilities ========================

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".docx", ".txt"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
UPLOADS: list[dict] = []


def validate_upload(uploaded_file: UploadedFile) -> tuple[bool, str]:
    """Validate file extension and size."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Extension '{ext}' not allowed"
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        return False, f"File too large ({uploaded_file.size} bytes, max {MAX_UPLOAD_SIZE})"
    return True, "OK"


def generate_filename(original_name: str) -> str:
    """Generate a unique filename to avoid collisions."""
    ext = os.path.splitext(original_name)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_suffix = hashlib.md5(original_name.encode() + str(time.time()).encode()).hexdigest()[:8]
    return f"{timestamp}_{hash_suffix}{ext}"


def handle_upload(uploaded_file: UploadedFile, storage: StorageBackend, upload_dir: str = "uploads") -> dict:
    """Process and store an uploaded file."""
    is_valid, message = validate_upload(uploaded_file)
    if not is_valid:
        return {"success": False, "error": message}

    filename = generate_filename(uploaded_file.name)
    path = f"{upload_dir}/{filename}"

    if isinstance(storage, LocalFileSystemStorage):
        storage_path = storage.save(path, uploaded_file.content)
    else:
        storage_path = storage.save(path, uploaded_file.content)

    record = {
        "original_name": uploaded_file.name,
        "stored_name": filename,
        "path": path,
        "storage_path": storage_path,
        "url": storage.url(path),
        "size": uploaded_file.size,
        "content_type": uploaded_file.content_type,
    }
    UPLOADS.append(record)
    return {"success": True, "file": record}


# ======================== Image Processing Simulation ========================

def create_thumbnail(content: bytes, size: tuple = (150, 150)) -> bytes:
    """Simulate thumbnail generation (in reality uses Pillow)."""
    # In a real app: from PIL import Image; img.thumbnail(size)
    return content[:100] + f"THUMBNAIL_{size[0]}x{size[1]}".encode()


# ======================== Demo ========================
print("=== File Handling & Storage Demo ===\n")

local_storage = LocalFileSystemStorage("/tmp/media")
s3_storage = S3Storage(bucket="my-django-app")

# --- Local file upload ---
print("1. Upload image (local storage):")
img = UploadedFile("photo.jpg", b"fake-image-content-12345", "image/jpeg")
result = handle_upload(img, local_storage, "uploads/images")
print(f"   Success: {result['success']}")
if result['success']:
    f = result['file']
    print(f"   Original: {f['original_name']}")
    print(f"   Stored as: {f['stored_name']}")
    print(f"   URL: {f['url']}")
    print(f"   Size: {f['size']} bytes")

# --- S3 upload ---
print("\n2. Upload PDF (S3 storage):")
pdf = UploadedFile("report.pdf", b"PDF-content-here-67890", "application/pdf")
result = handle_upload(pdf, s3_storage, "uploads/documents")
if result['success']:
    f = result['file']
    print(f"   Stored: {f['storage_path']}")
    print(f"   URL: {f['url']}")

# --- Invalid file ---
print("\n3. Invalid file (.exe):")
exe = UploadedFile("virus.exe", b"bad", "application/x-msdownload")
result = handle_upload(exe, local_storage)
print(f"   Success: {result['success']}, Error: {result.get('error', 'none')}")

# --- Thumbnail generation ---
print("\n4. Thumbnail generation:")
photo_content = b"FAKE_IMAGE_DATA_" * 100
thumb = create_thumbnail(photo_content, (300, 300))
print(f"   Original size: {len(photo_content)} bytes")
print(f"   Thumbnail size: {len(thumb)} bytes")

# --- File operations ---
print("\n5. File operations:")
name = "test.txt"
local_storage.save(name, b"hello world")
print(f"   Exists: {local_storage.exists(name)}")
print(f"   URL: {local_storage.url(name)}")
print(f"   Size: {local_storage.size(name)} bytes")
local_storage.delete(name)
print(f"   After delete - Exists: {local_storage.exists(name)}")

# --- Upload history ---
print(f"\n6. Total uploads handled: {len(UPLOADS)}")
for u in UPLOADS:
    print(f"   - {u['original_name']} → {u['url']}")
