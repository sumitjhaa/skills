"""Static files — pure Python simulation."""
from dataclasses import dataclass
from pathlib import Path


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
