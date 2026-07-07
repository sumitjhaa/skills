"""Config files, log reading, and CSV export — data pipeline foundations."""
from pathlib import Path


def load_config(path: str) -> dict:
    config = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    return config


def write_log(path: str, entries: list) -> None:
    with open(path, "a") as f:
        for entry in entries:
            f.write(f"{entry}\n")


with open("/tmp/config.txt", "w") as f:
    f.write("# App config\ndb_host=localhost\ndb_port=5432\ndebug=true\n")
print(load_config("/tmp/config.txt"))

write_log("/tmp/app.log", ["[INFO] Started", "[INFO] Connected"])
print(Path("/tmp/app.log").read_text())
Path("/tmp/config.txt").unlink()
Path("/tmp/app.log").unlink()
