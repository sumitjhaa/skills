"""
Mock DVC Pipeline — demonstrates data versioning concepts by simulating
a DVC-like pipeline that tracks dataset hashes, stages, and reproduces results.
"""

import hashlib
import json
import os
import tempfile
from pathlib import Path


class MockDvcPipeline:
    """A minimal DVC-inspired data versioning system."""

    def __init__(self, repo_root: str | Path):
        self.root = Path(repo_root)
        self.dvc_dir = self.root / ".mockdvc"
        self.dvc_dir.mkdir(parents=True, exist_ok=True)
        self.stages: dict = {}
        self._load_state()

    def _state_path(self):
        return self.dvc_dir / "state.json"

    def _load_state(self):
        if self._state_path().exists():
            with open(self._state_path()) as f:
                data = json.load(f)
                self.stages = data.get("stages", {})
        else:
            self.stages = {}

    def _save_state(self):
        (self.dvc_dir).mkdir(parents=True, exist_ok=True)
        with open(self._state_path(), "w") as f:
            json.dump({"stages": self.stages}, f, indent=2)

    def _hash_file(self, path: str | Path) -> str:
        path = Path(path)
        if not path.exists():
            return ""
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()

    def add(self, path: str | Path) -> str:
        path = Path(path)
        file_hash = self._hash_file(path)
        entry = {"path": str(path), "md5": file_hash, "size": path.stat().st_size}
        dvc_file = self.root / f"{path.name}.dvc"
        with open(dvc_file, "w") as f:
            json.dump(entry, f, indent=2)
        print(f"Tracked {path.name} (hash={file_hash[:8]}...)")
        return file_hash

    def run_stage(self, name: str, cmd: str, deps: list, outs: list) -> None:
        dep_hashes = {str(d): self._hash_file(d) for d in deps}
        self.stages[name] = {
            "cmd": cmd,
            "deps": dep_hashes,
            "outs": outs,
        }
        self._save_state()
        print(f"Stage '{name}' recorded.")

    def reproduce(self, name: str) -> bool:
        stage = self.stages.get(name)
        if not stage:
            print(f"Stage '{name}' not found.")
            return False

        changed = False
        for dep_path, dep_hash in stage["deps"].items():
            current = self._hash_file(dep_path)
            if current != dep_hash:
                print(f"Dependency {dep_path} has changed! Re-running...")
                changed = True
                stage["deps"][dep_path] = current

        if changed:
            self._save_state()
            print(f"Re-running stage '{name}': {stage['cmd']}")
            return True
        else:
            print(f"Stage '{name}' is up-to-date.")
            return False


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        pipeline = MockDvcPipeline(tmp)

        # Simulate data versioning
        data_file = tmp / "train.csv"
        data_file.write_text("feature_1,feature_2,label\n1.0,2.0,0\n2.0,3.0,1\n")

        pipeline.add(data_file)

        pipeline.run_stage(
            name="preprocess",
            cmd="python preprocess.py --input train.csv --output clean.parquet",
            deps=[str(data_file)],
            outs=["clean.parquet"],
        )

        pipeline.reproduce("preprocess")

        # Simulate data change
        data_file.write_text(data_file.read_text() + "3.0,4.0,0\n")
        print("\n--- After data change ---")
        pipeline.reproduce("preprocess")
