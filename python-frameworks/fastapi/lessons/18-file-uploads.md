# 📁 File Uploads
<!-- ⏱️ 10 min | 🟢 Supplement -->

**What You'll Learn:** UploadFile, form data, file validation, storage backends.

## UploadFile

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }
```

<!-- 📤 `UploadFile` is async. Always `await file.read()`. Don't read huge files into memory without streaming. -->

## Multiple Files

```python
@app.post("/upload/multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return [{"filename": f.filename, "size": len(await f.read())} for f in files]
```

## File Validation

```python
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file(file: UploadFile):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid extension: {ext}")
    # Read in chunks for real validation
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, f"File too large: {len(content)} bytes")
    return content
```

## Save to Disk

```python
import aiofiles

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    async with aiofiles.open(path, "wb") as f:
        await f.write(await file.read())
    return {"url": f"/static/{file.filename}"}
```

## Storage Backends

| Backend | When to Use |
|---------|-------------|
| Local disk | Development |
| S3 (boto3) | Production |
| Memory | Testing |

## Run the Code

```bash
python code/18-file-uploads.py
```
