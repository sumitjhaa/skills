# 📤 File Uploads
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Handle file uploads, validate extensions, secure filenames, store files.

## Basic File Upload

```python
from flask import request
from werkzeug.utils import secure_filename

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file.filename == "":
        return {"error": "No file selected"}

    filename = secure_filename(file.filename)
    file.save(f"uploads/{filename}")
    return {"message": "File uploaded", "filename": filename}
```

## File Validation

```python
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not allowed_file(file.filename):
        return {"error": "File type not allowed"}, 400
    filename = secure_filename(file.filename)
    file.save(f"uploads/{filename}")
    return {"message": "OK", "filename": filename}
```

## Secure Filenames

```python
from werkzeug.utils import secure_filename

filename = secure_filename("../../../etc/passwd")
# Result: etc_passwd — path traversal is blocked
```

## Multiple File Upload

```python
@app.route("/upload/multiple", methods=["POST"])
def upload_multiple():
    files = request.files.getlist("files")
    results = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"uploads/{filename}")
            results.append(filename)
    return {"uploaded": results, "count": len(results)}
```

## Serving Uploaded Files

```python
from flask import send_from_directory

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
```

<!-- 🧠 Never trust user-provided filenames. Always use `secure_filename()` and consider hashed/stored filenames for production. -->

## Run the Code

```bash
python code/13-file-uploads.py
```
