"""
Mock Terraform for ML — demonstrates Infrastructure-as-Code concepts
by generating Terraform-like HCL for SageMaker notebooks, ECR repos,
and GPU instances, plus a plan/apply workflow.
"""

import json
from dataclasses import dataclass, field


@dataclass
class Resource:
    resource_type: str
    name: str
    properties: dict = field(default_factory=dict)
    _provisioned: bool = False

    def to_hcl(self) -> str:
        """Generate pseudo-HCL output."""
        props = "\n".join(f"    {k} = {json.dumps(v)}" for k, v in self.properties.items())
        return f'resource "{self.resource_type}" "{self.name}" {{\n{props}\n}}'


class MockTerraform:
    """Minimal Terraform-like state manager."""

    def __init__(self):
        self.resources: list[Resource] = []
        self.state: dict = {}

    def add(self, resource: Resource):
        self.resources.append(resource)

    def plan(self) -> list[str]:
        """Dry-run: show what will be created."""
        changes = []
        for res in self.resources:
            if not res._provisioned:
                changes.append(f"+ create {res.resource_type}.{res.name}")
            else:
                changes.append(f"~ update {res.resource_type}.{res.name}")
        return changes

    def apply(self):
        """Apply: 'provision' all unprovisioned resources."""
        for res in self.resources:
            if not res._provisioned:
                res._provisioned = True
                key = f"{res.resource_type}.{res.name}"
                self.state[key] = res.properties
                print(f"  Provisioned {key}")

    def destroy(self):
        self.resources = []
        self.state = {}
        print("  All resources destroyed.")


def build_ml_infra() -> MockTerraform:
    tf = MockTerraform()

    tf.add(Resource("aws_sagemaker_notebook_instance", "ml_dev", {
        "name": "ml-dev-notebook",
        "instance_type": "ml.p3.2xlarge",
        "role_arn": "arn:aws:iam::123456789012:role/sagemaker-role",
    }))

    tf.add(Resource("aws_ecr_repository", "model_repo", {
        "name": "ml-models",
        "image_tag_mutability": "MUTABLE",
    }))

    tf.add(Resource("aws_iam_role", "ml_role", {
        "name": "ml-service-role",
        "managed_policy_arns": [
            "arn:aws:iam::aws:policy/AmazonS3FullAccess",
            "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
        ],
    }))

    tf.add(Resource("aws_spot_instance_request", "training_gpu", {
        "instance_type": "p4d.24xlarge",
        "spot_price": "3.00",
        "spot_type": "persistent",
        "wait_for_fulfillment": True,
    }))

    return tf


if __name__ == "__main__":
    tf = build_ml_infra()

    print("=== Terraform Plan ===")
    for change in tf.plan():
        print(f"  {change}")

    print("\n=== Terraform Apply ===")
    tf.apply()

    print(f"\nState contains {len(tf.state)} resources:")
    for key in tf.state:
        print(f"  ✓ {key}")

    print("\n=== HCL Output Preview ===")
    for res in tf.resources:
        print()
        print(res.to_hcl())
