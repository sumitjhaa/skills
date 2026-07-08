# 11.16 Cost Optimization

## Objective
Reduce ML infrastructure costs without sacrificing performance.

## Compute Cost Strategies

### 1. Spot / Preemptible Instances
- 60–90 % discount vs. on-demand.
- Use for training, batch inference, hyperparameter sweeps.
- Design fault-tolerant: checkpoint + resume.

```hcl
resource "aws_spot_instance_request" "training" {
  instance_type     = "p4d.24xlarge"
  spot_price        = "3.00"
  spot_type         = "persistent"
  wait_for_fulfillment = true
}
```

### 2. Autoscaling
- Scale to zero when not in use (development notebooks).
- HPA for inference — scale on CPU/memory/latency.
- Karpenter (Kubernetes) for just-in-time GPU provisioning.

### 3. Reserved / Savings Plans
- 1-year / 3-year commitment for predictable workloads.
- Mix spot + reserved for baseline + elastic demand.

## Storage Cost Strategies
- **Lifecycle policies**: hot → cold → archive (S3 Intelligent-Tiering).
- **Compression**: Parquet + Zstd vs. CSV (10× reduction).
- **Data retention**: delete stale training artifacts after N days.

## Monitoring Cost
```python
# Track cost per experiment
labels = {"experiment": exp_id, "user": user, "instance": instance_type}
aws_metric = boto3.client("cloudwatch")
aws_metric.put_metric_data(
    Namespace="ML/Experiments",
    MetricData=[{"MetricName": "Cost", "Value": estimated_cost, "Unit": "USD", "Dimensions": labels}],
)
```

## Optimization Checklist
| Area | Action | Savings |
|------|--------|---------|
| Compute | Spot instances | 60–70 % |
| Compute | Right-size instance family | 20–40 % |
| Storage | Parquet + Zstd | 4–10× |
| Storage | Lifecycle to Glacier after 30 d | 70 % |
| Training | Early stopping + HP tuning | 30–50 % |
| Serving | Batch instead of real-time | 50–80 % |
| Idle | Shut down dev notebooks after-hours | 40–60 % |

## Best Practices
1. Tag every resource with cost-center, project, and owner.
2. Use spot instances for training; keep on-demand for critical serving.
3. Set budgets and alerts in AWS Budgets / GCP Billing.
4. Review cost allocation reports weekly and optimize top 5 spenders.
