"""Running shell commands, file operations, and archiving."""
import subprocess
import shutil
from pathlib import Path


def run_command(cmd: list) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"returncode": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}


def create_backup(source_dir: str, output_name: str) -> Path:
    base = Path(source_dir)
    output = Path(output_name)
    return Path(shutil.make_archive(str(output.with_suffix("")), "zip", base))


def disk_usage(path: str = "/") -> dict:
    usage = shutil.disk_usage(path)
    return {"total_gb": round(usage.total / (1024**3), 2), "used_gb": round(usage.used / (1024**3), 2), "free_gb": round(usage.free / (1024**3), 2), "percent_used": round(usage.used / usage.total * 100, 1)}


def git_status(directory: str) -> str:
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=directory)
    if result.returncode != 0:
        return f"Error: {result.stderr.strip()}"
    return result.stdout.strip() or "Clean working directory"


print("Disk usage:", disk_usage("/"))
result = run_command(["echo", "Hello from subprocess!"])
print(f"Command: {result['stdout']}")

tmp = Path("/tmp/backup_demo")
(tmp / "docs").mkdir(parents=True, exist_ok=True)
(tmp / "docs/readme.txt").write_text("Important data")
(tmp / "config.ini").write_text("[settings]\nversion=1.0")
archive = create_backup(tmp, "/tmp/project_backup")
print(f"Backup: {archive} ({archive.stat().st_size} bytes)")
shutil.rmtree(tmp)
archive.unlink()

print("Git status:", git_status("/tmp"))
