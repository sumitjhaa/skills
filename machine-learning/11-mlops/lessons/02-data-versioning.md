# Lesson 11.02: Data Versioning

## Learning Objectives
- Understand data versioning for ML pipelines
- Implement DVC (Data Version Control) for datasets
- Apply data lineage and reproducibility

## Why Data Versioning?

### Problems Without Versioning
- Which dataset version was used for this model?
- Can I reproduce old results?
- How did the data change between experiments?

## DVC (Data Version Control)

### Setup
```bash
pip install dvc
dvc init              # Initialize DVC in repo
dvc remote add myremote s3://mybucket/dvcstore  # Configure remote
```

### Track Data
```bash
dvc add data/dataset.csv          # Track dataset (creates .dvc file)
git add data/dataset.csv.dvc      # Version track metadata
git commit -m "Add dataset v1"

# Push data to remote
dvc push

# Switch to different version
git checkout <commit>
dvc checkout                      # Restore data version
```

### Pipeline
```bash
dvc run -n train -d data/train.csv -d src/train.py -o models/model.pth \
    python src/train.py
```

## Data Lineage

### Tracking Data Sources
```python
class DataVersion:
    def __init__(self, source, version, preprocess_version):
        self.source = source
        self.version = version
        self.preprocess_version = preprocess_version
        self.timestamp = datetime.now().isoformat()

    def log(self, run_id):
        wandb.log({
            "data_source": self.source,
            "data_version": self.version,
            "preprocess_version": self.preprocess_version,
        })
```

## Code: DVC Integration

```python
import subprocess
import yaml
from pathlib import Path

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.metadata_file = self.data_dir / "metadata.yaml"

    def add_version(self, dataset_name, description=""):
        cmd = f"dvc add {self.data_dir / dataset_name}"
        subprocess.run(cmd, shell=True, check=True)
        
        metadata = {
            "name": dataset_name,
            "version": self.get_current_version(),
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "files": list((self.data_dir / dataset_name).rglob("*")),
        }
        with open(self.metadata_file, "w") as f:
            yaml.dump(metadata, f)

    def get_current_version(self):
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True
        )
        return result.stdout.strip()

    def checkout(self, git_commit):
        subprocess.run(f"git checkout {git_commit}", shell=True, check=True)
        subprocess.run("dvc checkout", shell=True, check=True)

    def verify_integrity(self, dataset_name):
        result = subprocess.run(
            ["md5sum", str(self.data_dir / dataset_name)],
            capture_output=True, text=True
        )
        checksum = result.stdout.split()[0]
        with open(self.metadata_file) as f:
            metadata = yaml.safe_load(f)
        return checksum == metadata.get("checksum")
```

## Dataset Registry

### Simple Registry
```python
DATASET_REGISTRY = {
    "imagenet-100-v1": {
        "path": "s3://bucket/imagenet-100-v1",
        "checksum": "abc123...",
        "preprocessing": "resize 256, center crop 224",
        "num_samples": 100000,
        "classes": 100,
    },
    "imagenet-100-v2": {
        "path": "s3://bucket/imagenet-100-v2",
        "checksum": "def456...",
        "preprocessing": "random resize crop 224",
        "num_samples": 110000,
        "classes": 100,
    },
}

def load_dataset(name, version):
    config = DATASET_REGISTRY[f"{name}-{version}"]
    return Dataset(config["path"], config["preprocessing"])
```

## Comparison

| Tool | Storage | Versioning | Pipeline | Best For |
|------|---------|-----------|----------|----------|
| DVC | S3/GCS/local | Git-based DVC files | Yes | ML projects |
| Git LFS | Git remote | Git blob | No | Large binary files |
| LakeFS | S3-compatible | Git-like branches | Yes | Data lakes |
| Quilt | S3 | Package versions | No | Data packages |

## Best Practices
- **Do not commit data to Git**: Use DVC/LFS for large files
- **Hash verification**: Store checksums with each version
- **Immutable datasets**: Once created, datasets should not be modified
- **Document preprocessing**: Track preprocessing code version alongside data
- **Automated validation**: Validate dataset integrity before training

## References
- DVC documentation: https://dvc.org/doc
- Git LFS: https://git-lfs.com/
- LakeFS: https://docs.lakefs.io/
- Alla, Aditya, et al., "Data Versioning at Scale: A Survey", 2022
