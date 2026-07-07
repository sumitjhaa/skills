"""pathlib patterns: file operations, glob, log rotation — real dev workflows"""
from pathlib import Path
import tempfile, os, shutil

# Set up temp workspace simulating a real app's log directory
tmp = Path(tempfile.mkdtemp())
(tmp / "logs" / "2024" / "01").mkdir(parents=True)  # Creates all missing dirs

# write_text: concise file writing vs open/close boilerplate
(tmp / "logs" / "2024" / "01" / "app.log").write_text("[INFO] Started\n[ERROR] timeout\n")
(tmp / "logs" / "2024" / "01" / "db.log").write_text("[INFO] Connected\n")

# rglob: recursive glob to find ALL .log files in subtree
log_files = list(tmp.rglob("*.log"))
print(f"  Found {len(log_files)} log files")

# with_suffix: rename extension (e.g., .csv → .csv.bak before processing)
for f in log_files:
    backup = f.with_suffix(".log.bak")  # Only changes extension
    shutil.copy2(f, backup)  # Preserves metadata (mtime, etc.)

# stat: file size & mtime for log rotation / cleanup decisions
for f in log_files:
    st = f.stat()
    print(f"  {f.name}: {st.st_size}B, modified {st.st_mtime:.0f}")

# relative_to: get relative path from a base directory
for f in tmp.rglob("*"):
    if f.is_file():
        print(f"  Relative: {f.relative_to(tmp)}")

# resolve: get absolute path (resolves symlinks, ., ..)
print(f"  Abs: {tmp.resolve()}")

# Cleanup
shutil.rmtree(tmp)
print("  Cleanup done")
