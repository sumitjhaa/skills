# 09.26 Code LLMs

## Learning Objectives
- Understand code generation and infilling models
- Implement Codex, CodeLlama, and StarCoder
- Apply code benchmarks (HumanEval, MBPP, SWE-bench)
- Analyze training data strategies for code models

## Code Generation

### Models
| Model | Base | Architecture | Size | Training Data |
|-------|------|-------------|------|--------------|
| Codex (GPT-3) | GPT-3 | Decoder-only | 12B | 159GB code |
| CodeLlama | LLaMA-2 | Decoder-only | 7B-34B | Code + natural language |
| StarCoder | - | Decoder-only | 15.5B | 1TB code (The Stack) |
| CodeGemma | Gemma | Decoder-only | 2B-7B | 500B code tokens |
| DeepSeek-Coder | DeepSeek | Decoder-only | 1.3B-33B | 2T code tokens |

### Fill-in-the-Middle (FIM)
```python
# Standard: prefix → suffix
# FIM: prefix → middle ← suffix

# Training format
<p>function hello() {<s>  console.log("hello");<m>...original middle...</m>}
# At inference:
<p>function hello() {<s>  console.log("hello");<m>
# Model fills middle:   console.log("world"); }
```

## Code Benchmarks

### HumanEval
- 164 hand-written Python programming problems
- Metric: pass@k (functional correctness)
- GPT-4: pass@1 = 67.0%, pass@100 = 90.2%

### MBPP (Mostly Basic Python Programming)
- 974 Python tasks
- CodeLlama-34B: 62.0%
- StarCoder: 51.7%

### SWE-bench
- 2,294 real GitHub issues from 12 Python repos
- Requires: understand issue → edit code → pass tests
- Current SOTA: ~30% (SWE-agent + GPT-4)

## Code Infilling

### Span Masking
Mask continuous spans in code:

```python
def add(a, b):
    <mask>
    return result
```

### Causal Masking with FIM
Two configurations:
1. **PSM**: Prefix → Suffix → Middle (causal)
2. **SPM**: Suffix → Prefix → Middle (bidirectional context)

## Repository-Level Code Generation

### Cross-File Context
```python
# Model needs to know imports, types, and functions from other files
# Solution: include related file contents in context window

context = read_related_files(file_path, imports)
prompt = f"Context:\n{context}\n\nContinue:\n{code_before_cursor}"
```

## Code: FIM Training

```python
import torch
from transformers import AutoTokenizer

def fim_transform(tokens, tokenizer, fim_rate=0.5):
    """Apply Fill-in-the-Middle transformation"""
    if torch.rand(1) < (1 - fim_rate):
        return tokens  # Keep original
    
    seq_len = len(tokens)
    split = torch.randint(1, seq_len - 1, (1,))
    
    prefix = tokens[:split]
    middle = tokens[split:split + seq_len // 3]
    suffix = tokens[split + seq_len // 3:]
    
    # PSM format
    fim_tokens = (
        [tokenizer.fim_prefix_id] + prefix.tolist() +
        [tokenizer.fim_suffix_id] + suffix.tolist() +
        [tokenizer.fim_middle_id] + middle.tolist()
    )
    return torch.tensor(fim_tokens)

class CodeGenModel:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def complete_code(self, prefix, suffix=None, max_new=100):
        if suffix:
            prompt = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
        else:
            prompt = prefix
        
        inputs = self.tokenizer(prompt, return_tensors='pt')
        outputs = self.model.generate(**inputs, max_new_tokens=max_new, 
                                     pad_token_id=self.tokenizer.eos_token_id)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def explain_code(self, code):
        prompt = f"Explain this code:\n```python\n{code}\n```\nExplanation:"
        return self.model.generate(prompt)
```

## Practical Considerations
- **Tokenization**: Treat code tokens (indentation, newlines) properly
- **Comment preservation**: Keep docstrings/comments for context
- **Multi-language**: Shared tokenizer for different languages
- **Max length**: Repository-level tasks need 8K-32K context
- **Agent tools**: Code LLMs + execution + iteration = powerful coding assistants

## References
- Chen, Tworek, et al., "Evaluating Large Language Models Trained on Code (Codex)", NeurIPS 2021
- Li, Choi, et al., "StarCoder: May the Source Be with You!", 2023
- Rozière, Gehring, et al., "Code Llama: Open Foundation Models for Code", 2023
- Austin, Odena, et al., "Program Synthesis with Large Language Models (MBPP)", 2021
- Jimenez, Yang, et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", ICLR 2024
