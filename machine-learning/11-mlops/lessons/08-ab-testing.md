# Lesson 11.08: A/B Testing

## Learning Objectives
- Understand A/B testing for ML models
- Implement online evaluation frameworks
- Apply statistical significance testing

## A/B Testing in ML

### Compared to Offline Evaluation
| Aspect | Offline | Online (A/B) |
|--------|---------|--------------|
| Data | Historical | Live users |
| Metrics | Accuracy, F1 | Revenue, engagement |
| Cost | Low | High |
| Risk | None | User-facing |
| Setup | Simple | Complex |

## Traffic Splitting

### Random Assignment
```python
import hashlib

def assign_variant(user_id: str, experiment_name: str, variants: list) -> str:
    """Deterministic variant assignment based on user_id"""
    hash_input = f"{user_id}:{experiment_name}"
    hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    idx = hash_val % len(variants)
    return variants[idx]
```

### Ramping
```python
def should_serve_variant(user_id: str, rollout_percentage: float) -> bool:
    hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return (hash_val % 100) < rollout_percentage * 100
```

## Experiment Pipeline

```python
class ABTest:
    def __init__(self, experiment_name, control_model, treatment_model, metric_fn):
        self.name = experiment_name
        self.control = control_model
        self.treatment = treatment_model
        self.metric_fn = metric_fn
        self.results = {"control": [], "treatment": []}

    def predict(self, user_id, features):
        variant = assign_variant(user_id, self.name, ["control", "treatment"])
        model = self.control if variant == "control" else self.treatment
        prediction = model.predict(features)
        return variant, prediction

    def log_result(self, variant, user_id, prediction, actual):
        metric_value = self.metric_fn(prediction, actual)
        self.results[variant].append(metric_value)

    def analyze(self):
        import scipy.stats as stats
        control_metrics = self.results["control"]
        treatment_metrics = self.results["treatment"]
        
        t_stat, p_value = stats.ttest_ind(control_metrics, treatment_metrics)
        effect_size = (np.mean(treatment_metrics) - np.mean(control_metrics)) / \
                      np.std(control_metrics)
        
        return {
            "experiment": self.name,
            "control_mean": np.mean(control_metrics),
            "treatment_mean": np.mean(treatment_metrics),
            "improvement_pct": (np.mean(treatment_metrics) - np.mean(control_metrics)) / 
                               np.mean(control_metrics) * 100,
            "p_value": p_value,
            "effect_size": effect_size,
            "significant": p_value < 0.05,
            "sample_size": len(control_metrics) + len(treatment_metrics),
        }
```

## Statistical Significance

### Metrics
| Metric | When to Use | Formula |
|--------|-------------|---------|
| Conversion rate | Binary outcomes | z-test for proportions |
| Average value | Continuous metrics | t-test |
| Revenue | Skewed distribution | Bootstrap |
| CTR | Rare events | Chi-squared test |

### Sample Size Calculation
```python
def required_sample_size(effect_size=0.01, alpha=0.05, power=0.8):
    from statsmodels.stats.power import NormalIndPower
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size, power=power, alpha=alpha)
    return int(n * 2)  # Two groups
```

## Multi-Armed Bandit

### Thompson Sampling for A/B
```python
class BanditAB:
    def __init__(self, variants):
        self.variants = variants
        self.alpha = {v: 1 for v in variants}  # Successes
        self.beta = {v: 1 for v in variants}   # Failures

    def select_variant(self):
        samples = {v: np.random.beta(self.alpha[v], self.beta[v]) 
                   for v in self.variants}
        return max(samples, key=samples.get)

    def update(self, variant, reward):
        if reward > 0:
            self.alpha[variant] += 1
        else:
            self.beta[variant] += 1

    def get_win_probability(self):
        # Probability treatment is better than control
        samples_control = np.random.beta(self.alpha["control"], self.beta["control"], 10000)
        samples_treatment = np.random.beta(self.alpha["treatment"], self.beta["treatment"], 10000)
        return (samples_treatment > samples_control).mean()
```

## Platform Integration

```python
from fastapi import FastAPI, Request

app = FastAPI()
experiments = {}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    
    for exp_name, experiment in experiments.items():
        variant, prediction = experiment.predict(user_id, data["features"])
        data[f"exp_{exp_name}"] = variant
    
    return data

@app.post("/feedback")
async def feedback(request: Request):
    data = await request.json()
    for exp_name, experiment in experiments.items():
        variant = data.get(f"exp_{exp_name}")
        if variant:
            experiment.log_result(variant, data["user_id"], 
                                  data["prediction"], data["actual"])
    return {"status": "ok"}
```

## References
- Kohavi, Tang, Xu, "Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing", 2020
- Google, "Overlapping Experiment Infrastructure: More, Better, Faster Experimentation", KDD 2010
- Scott, "A Modern Bayesian Look at the Multi-Armed Bandit", 2010
- Deng, Xu, et al., "Online Controlled Experiments at Large Scale", KDD 2013
