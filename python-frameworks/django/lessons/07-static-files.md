# 🎨 Static Files & Media
<!-- ⏱️ 8 min | 🟢 Core -->

**What You'll Learn:** Serve CSS, JavaScript, images, and user-uploaded files.

## Static Files (CSS, JS, Images)

```python
# settings.py
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # For project-wide static files
STATIC_ROOT = BASE_DIR / 'staticfiles'     # Collected in production
```

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## Media Files (User Uploads)

```python
# settings.py
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# models.py
class Post(models.Model):
    image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    file = models.FileField(upload_to='files/', blank=True)

# urls.py (development only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Management Command

```bash
python manage.py collectstatic  # Copy all static files to STATIC_ROOT
```

## Code Example

```python
"""Static files — pure Python simulation."""
from dataclasses import dataclass, field
from pathlib import Path
import hashlib


@dataclass
class StaticFile:
    path: Path
    content: str = ''

    def url(self) -> str:
        return f"/static/{self.path}"


class StaticFileStorage:
    def __init__(self):
        self.files: dict[str, StaticFile] = {}

    def add(self, path: str, content: str):
        self.files[path] = StaticFile(Path(path), content)

    def collect(self, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        for path, sf in self.files.items():
            dest = output_dir / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(sf.content)
            print(f"  Collected: {dest}")

    def get(self, path: str):
        sf = self.files.get(path)
        if sf:
            return {'url': sf.url(), 'size': len(sf.content), 'type': path.split('.')[-1]}
        return None


storage = StaticFileStorage()
storage.add('css/style.css', 'body { font-family: sans-serif; }')
storage.add('js/main.js', 'console.log("Hello!");')
storage.add('images/logo.png', 'FAKE-PNG-BINARY-DATA')

for path in ['css/style.css', 'js/main.js', 'images/logo.png']:
    info = storage.get(path)
    print(f"  {path:20s} → url={info['url']:30s} size={info['size']}")

print("\n  Collecting static files:")
storage.collect(Path('/tmp/staticfiles'))
```

## Key Points
- `{% static %}` template tag generates the correct URL for static files
- `collectstatic` gathers files from all apps into one directory for production
- `ImageField` requires `Pillow` library: `pip install Pillow`
- Never serve media files from Django in production — use S3 or Nginx
- Use `STATICFILES_DIRS` for project-level static files (logo, global CSS)
