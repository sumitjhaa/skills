# 📘 Django Phase 05 — Lesson 07: File Handling & Storage Backends

> 🎯 **Goal**: Handle file uploads, image processing, and pluggable storage backends (local, S3, GCS).

## 📖 Concepts

### File Upload Flow
```
Browser → multipart form → request.FILES['file'] → UploadedFile
  → validate (type, size)
  → generate safe filename
  → save to storage backend
  → store path in model field
```

### FileField / ImageField
```python
class Post(models.Model):
    image = models.ImageField(upload_to='posts/%Y/%m/%d/')
    document = models.FileField(upload_to='documents/')
```

`upload_to` can be:
- String with `strftime` formatting: `posts/%Y/%m/%d/`
- Callable: `def user_path(instance, filename): return f"user_{instance.id}/{filename}"`

### Storage Backends

| Backend | Package | URL Pattern |
|---------|---------|-------------|
| `FileSystemStorage` | Built-in | `/media/file.jpg` |
| `S3Boto3Storage` | `django-storages` | `https://bucket.s3.amazonaws.com/file.jpg` |
| `GoogleCloudStorage` | `django-storages` | `https://storage.googleapis.com/bucket/file.jpg` |
| `AzureStorage` | `django-storages` | `https://account.blob.core.windows.net/file.jpg` |

### Settings
```python
# Local dev
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Production (S3)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'my-bucket'
```

### Image Processing (Pillow)
```python
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def create_thumbnail(image_field, size=(300, 300)):
    img = Image.open(image_field)
    img.thumbnail(size)
    thumb_io = BytesIO()
    img.save(thumb_io, format='JPEG', quality=85)
    return ContentFile(thumb_io.getvalue(), name='thumb_' + image_field.name)
```

### ADHD-Friendly Summary
```
request.FILES['file'] → UploadedFile object
model.FileField(upload_to='path/') → auto save + delete
upload_to with strftime → posts/%Y/%m/%d/
django-storages → S3/GCS/Azure in one line
Pillow → ImageField, thumbnail creation
```

## 🛠️ Code

```python
# models.py
class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/%H/')
    thumbnail = models.ImageField(upload_to='posts/thumbs/', blank=True)
    document = models.FileField(upload_to='documents/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        img = Image.open(self.image)
        img.thumbnail((300, 300))
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        self.thumbnail.save(
            f'thumb_{self.image.name}',
            ContentFile(thumb_io.getvalue()),
            save=False,
        )
        super().save(update_fields=['thumbnail'])

# forms.py
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'document']
```

## 🧪 Practice

1. Add an `ImageField` to a model with `upload_to='photos/%Y/%m/'`
2. Create a form with `FileField` and handle upload in a view
3. Generate a thumbnail on save using Pillow
4. Configure S3 storage with `django-storages`
5. Add file type validation (only images < 5MB)

## 🧠 Key Takeaways

- `request.FILES` contains uploaded files in a dict
- `FileField` stores the path, not the file content
- Use `upload_to` with date formatting for organized storage
- Always validate file type and size server-side
- Pillow is required for `ImageField`
- Use `django-storages` for production cloud storage
