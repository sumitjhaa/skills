"""File organization tools — backup script and directory cleanup."""
from pathlib import Path
import shutil
from datetime import datetime


def organize_by_extension(directory: str) -> dict:
    base = Path(directory)
    groups = {}
    for f in base.iterdir():
        if f.is_file():
            ext = f.suffix.lower() or "no_extension"
            groups.setdefault(ext, []).append(f.name)
    return groups


def backup_file(path: str, backup_dir: str = "/tmp/backups") -> Path:
    src = Path(path)
    backup = Path(backup_dir)
    backup.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup / f"{src.stem}_{timestamp}{src.suffix}"
    shutil.copy2(src, dest)
    return dest


tmp = Path("/tmp/organize_demo")
(tmp / "sub").mkdir(parents=True, exist_ok=True)
(tmp / "doc.txt").write_text("hello")
(tmp / "data.csv").write_text("a,b,c")
(tmp / "script.py").write_text("print('hi')")

print("Groups:", organize_by_extension(tmp))
backup = backup_file(tmp / "doc.txt")
print(f"Backup: {backup}")
shutil.rmtree(tmp)
backup.unlink()
