# Lesson 11.01: Experiment Tracking

## Learning Objectives
- Understand experiment tracking for ML pipelines
- Implement logging with Weights & Biases and MLflow
- Apply hyperparameter search and result analysis

## Why Track Experiments?

### Key Information
- Hyperparameters: learning rate, batch size, architecture
- Metrics: loss, accuracy, F1 score over training
- Artifacts: model weights, predictions, visualisations
- Environment: Python version, GPU model, library versions

## Experiment Tracking Tools

| Tool | Features | Best For |
|------|----------|----------|
| MLflow | Open-source, local/cloud | Teams needing self-hosted |
| Weights & Biases | Cloud, collaboration | Research teams |
| TensorBoard | Built into TF/PyTorch | Quick visualisation |
| Neptune | Paid, advanced tracking | Enterprise |
| DVC | Git-based experiment tracking | Version control centric |

## MLflow

### Setup
```bash
mlflow ui  # Start tracking server at localhost:5000
```

### Code
```python
import mlflow

mlflow.set_experiment("my_experiment")
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 64)
    mlflow.log_param("model", "resnet50")
    
    # Log metrics during training
    for epoch in range(10):
        loss = train_one_epoch()
        mlflow.log_metric("loss", loss, step=epoch)
    
    # Log artifacts
    mlflow.log_artifact("model.pth")
    mlflow.pytorch.log_model(model, "model")
```

## Weights & Biases

### Setup
```bash
wandb login  # Login with API key
```

### Code
```python
import wandb

wandb.init(project="my_project", config={
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 10,
})

config = wandb.config  # Access config
for epoch in range(config.epochs):
    loss = train_one_epoch()
    wandb.log({"loss": loss, "epoch": epoch})
    wandb.log({"gradients": wandb.Histogram(grads)})

wandb.finish()
```

## Hyperparameter Search

### Grid Search
```python
param_grid = {
    "lr": [1e-4, 1e-3, 1e-2],
    "batch_size": [32, 64, 128],
}
for lr in param_grid["lr"]:
    for bs in param_grid["batch_size"]:
        run_experiment(lr=lr, batch_size=bs)
```

### Bayesian Optimisation (with W&B Sweep)
```python
sweep_config = {
    "method": "bayes",
    "metric": {"name": "val_loss", "goal": "minimize"},
    "parameters": {
        "learning_rate": {"min": 1e-5, "max": 1e-1},
        "dropout": {"min": 0.1, "max": 0.5},
        "num_layers": {"values": [2, 4, 6]},
    }
}

sweep_id = wandb.sweep(sweep_config, project="my_sweep")
wandb.agent(sweep_id, function=train_model)
```

## Code: Trainer with Logging

```python
import torch
import wandb
from tqdm import tqdm

class TrackedTrainer:
    def __init__(self, model, train_loader, val_loader, config):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config
        self.optimizer = torch.optim.Adam(
            model.parameters(), lr=config.learning_rate
        )
        wandb.init(project=config.project, config=config)

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        for batch in tqdm(self.train_loader):
            inputs, targets = batch
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = torch.nn.functional.cross_entropy(outputs, targets)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(), self.config.max_grad_norm
            )
            self.optimizer.step()
            total_loss += loss.item()
        return total_loss / len(self.train_loader)

    def validate(self):
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in self.val_loader:
                outputs = self.model(inputs)
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()
        return 100.0 * correct / total

    def run(self):
        for epoch in range(self.config.epochs):
            train_loss = self.train_epoch()
            val_acc = self.validate()
            
            wandb.log({
                "epoch": epoch,
                "train_loss": train_loss,
                "val_accuracy": val_acc,
                "learning_rate": self.optimizer.param_groups[0]["lr"],
            })
            
            print(f"Epoch {epoch}: loss = {train_loss:.4f}, acc = {val_acc:.2f}%")
        
        wandb.finish()
```

## Best Practices
- **Reproducibility**: Log all parameters, seeds, and environment details
- **Naming**: Use descriptive experiment names
- **Tagging**: Add tags for easy filtering (e.g., "resnet50", "baseline")
- **Dashboards**: Create custom dashboards for key metrics
- **Compare**: Use parallel coordinate plots for hyperparameter analysis

## References
- MLflow documentation: https://mlflow.org/docs/latest/index.html
- Weights & Biases: https://docs.wandb.ai/
- TensorBoard: https://www.tensorflow.org/tensorboard
- Liaw, Liang, et al., "Tune: A Research Platform for Distributed Model Selection and Training", 2018
