# Lesson 11.07: Model Governance

## Learning Objectives
- Understand model governance frameworks
- Implement model versioning, approval, and audit trails
- Apply compliance requirements (GDPR, CCPA) for ML

## Model Governance Components

### Lifecycle Stages
```
Development → Validation → Approval → Deployment → Monitoring → Retirement
```

## Model Registry

### MLflow Model Registry
```python
import mlflow
from mlflow.tracking.client import MlflowClient

client = MlflowClient()

# Register model
result = mlflow.register_model(
    "runs:/<run_id>/model",
    "fraud_detection_model"
)

# Transition stage
client.transition_model_version_stage(
    name="fraud_detection_model",
    version=1,
    stage="Staging"  # None, Staging, Production, Archived
)

# Add description
client.update_model_version(
    name="fraud_detection_model",
    version=1,
    description="XGBoost with 200 features, trained on Q1 2024 data"
)
```

## Approval Workflow

```python
from enum import Enum
from datetime import datetime

class ModelStage(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"
    REJECTED = "rejected"

class ModelApproval:
    def __init__(self):
        self.approvals = []

    def submit_for_review(self, model_id, model_card, metrics):
        self.approvals.append({
            "model_id": model_id,
            "model_card": model_card,
            "metrics": metrics,
            "stage": ModelStage.STAGING,
            "submitted_at": datetime.now(),
            "reviewers": [],
            "status": "pending",
        })

    def approve(self, model_id, reviewer):
        for a in self.approvals:
            if a["model_id"] == model_id:
                a["stage"] = ModelStage.PRODUCTION
                a["reviewers"].append(reviewer)
                a["approved_at"] = datetime.now()
                a["status"] = "approved"

    def reject(self, model_id, reviewer, reason):
        for a in self.approvals:
            if a["model_id"] == model_id:
                a["stage"] = ModelStage.REJECTED
                a["reviewers"].append(reviewer)
                a["rejected_at"] = datetime.now()
                a["reason"] = reason
                a["status"] = "rejected"
```

## Audit Trail

```python
import json
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file

    def log_event(self, event_type, model_id, user, details):
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "model_id": model_id,
            "user": user,
            "details": details,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")

    def query_events(self, model_id=None, event_type=None):
        events = []
        with open(self.log_file) as f:
            for line in f:
                event = json.loads(line)
                if model_id and event["model_id"] != model_id:
                    continue
                if event_type and event["event_type"] != event_type:
                    continue
                events.append(event)
        return events

# Usage
audit = AuditLogger()
audit.log_event("deploy", "model-v1", "alice", {
    "stage": "production",
    "version": 3,
    "reason": "Passed all validation tests",
})
```

## Compliance Requirements

### GDPR for ML
| Requirement | Implementation |
|------------|---------------|
| Right to explanation | SHAP/LIME explanations |
| Data deletion | Retrain without user data |
| Data access | Log all training data sources |
| Consent tracking | Store consent records |

### Model Documentation
```python
MODEL_CARD_TEMPLATE = {
    "model_name": "",
    "version": "",
    "author": "",
    "date": "",
    "model_type": "",
    "training_data": {
        "source": "",
        "size": 0,
        "features": [],
        "date_range": "",
    },
    "evaluation": {
        "metrics": {},
        "test_data": "",
        "bias_analysis": {},
    },
    "intended_use": "",
    "limitations": [],
    "ethical_considerations": [],
    "approval": {
        "reviewer": "",
        "date": "",
        "status": "",
    },
}
```

## Code: Model Governance System

```python
import yaml
from datetime import datetime
from typing import Dict, List

class ModelGovernor:
    def __init__(self):
        self.models = {}

    def register_model(self, name, version, metadata):
        model_id = f"{name}:{version}"
        self.models[model_id] = {
            **metadata,
            "id": model_id,
            "created_at": datetime.now(),
            "versions": [],
        }

    def validate_for_deployment(self, model_id: str) -> bool:
        model = self.models.get(model_id)
        if not model:
            return False
        checks = [
            model.get("accuracy", 0) > model.get("threshold", 0),
            model.get("bias_test_passed", False),
            model.get("privacy_reviewed", False),
            len(model.get("limitations", [])) > 0,
            model.get("approval_status") == "approved",
        ]
        return all(checks)

    def log_inference(self, model_id: str, input_hash: str, output: str, latency: float):
        self.models[model_id].setdefault("inference_logs", []).append({
            "timestamp": datetime.now(),
            "input_hash": input_hash,
            "output": output,
            "latency_ms": latency,
        })

    def get_model_card(self, model_id: str) -> Dict:
        return self.models.get(model_id, {})
```

## References
- MLflow Model Registry: https://mlflow.org/docs/latest/model-registry.html
- GDPR: https://gdpr-info.eu/
- Mitchell, Wu, et al., "Model Cards for Model Reporting", FAT 2019
- Gebru, Morgenstern, et al., "Datasheets for Datasets", 2018
- Raji, Gebru, et al., "Saving Face: Investigating the Ethical Concerns of Facial Recognition Auditing", AAAI 2020
