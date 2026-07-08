# 11.10 Infrastructure as Code

## Objective
Provision and manage ML infrastructure reproducibly with **Terraform** and **Kubernetes**.

## Terraform for ML
Declarative infrastructure: GPUs, storage, networking, IAM.

```hcl
resource "aws_sagemaker_notebook_instance" "ml_dev" {
  name          = "ml-dev-notebook"
  role_arn      = aws_iam_role.ml_role.arn
  instance_type = "ml.p3.2xlarge"
}

resource "aws_ecr_repository" "model_repo" {
  name = "ml-models"
}
```

## Kubernetes + Kubeflow
- Pods / Deployments for model serving.
- Kubeflow Pipelines for end-to-end ML workflows.
- Horizontal Pod Autoscaler (HPA) for inference.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: triton
        image: nvcr.io/nvidia/tritonserver:23.10-py3
        resources:
          limits:
            nvidia.com/gpu: 1
```

## Immutable Infrastructure
- Build golden AMIs / container images with baked-in dependencies.
- Never patch running servers — redeploy with new image.
- Use Terraform workspaces for dev / staging / prod.

## Best Practices
1. Store Terraform state in remote backend (S3 + DynamoDB lock).
2. Tag all resources (project, owner, environment, cost-center).
3. Use modules to standardize GPU clusters, VPCs, monitoring.
4. Run `terraform plan` in CI; require approval for `apply` in prod.
