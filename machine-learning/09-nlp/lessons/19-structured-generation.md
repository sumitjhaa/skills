# 09.19 Structured Generation

## Learning Objectives
- Understand constrained decoding for structured outputs
- Implement JSON mode and grammar-based generation
- Apply structured generation for tool calling
- Compare approaches: constrained decoding vs post-hoc parsing

## Problem

### Unstructured Output
```
Model: Sure, here are the top 5... (free-form text)
```

### Desired Output
```json
{"name": "John", "age": 30, "city": "New York"}
```

## Constrained Decoding

### Approach
Modify token probabilities to enforce constraints:

```python
# At each decoding step:
logits = model(next_token)
mask = compute_allowed_tokens(partial_output, grammar)
logits[~mask] = -inf
next_token = sample(logits)
```

## JSON Mode

### Implementation
```python
import json

class JSONConstraint:
    def __init__(self, schema):
        self.schema = schema  # dict of {"field": type}

    def get_allowed_tokens(self, partial):
        # Parse partial to understand current state
        if partial.strip() == "":
            return [ord('{')]
        try:
            obj = json.loads(partial)
            # Determine which field to write next
            return self._allowed_for_next_field(obj)
        except json.JSONDecodeError:
            # Incomplete JSON — continue current field/string
            return self._allowed_for_incomplete(partial)

    def _allowed_for_next_field(self, obj):
        # Return tokens for next field key or closing brace
        ...
```

### Libraries
- **lm-format-enforcer**: Define schema via JSON Schema
- **Outlines**: Regex-based grammar constraints
- **Guidance**: Programmatic control over generation

## Grammar-Based Generation

### Regex Grammar
```python
from outlines import generate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
    },
    "required": ["name", "age"],
}

generator = generate.json(model, schema)
result = generator(prompt)
```

### CFG (Context-Free Grammar)
Speech acts and structured dialogue:

```
greeting ::= "Hello" | "Hi" | "Hey"
farewell ::= "Goodbye" | "See you" | "Bye"
response ::= greeting (name)? farewell
```

## Tool Calling (Function Calling)

### OpenAI Function Calling
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "unit": {"type": "string", "enum": ["c", "f"]}
            },
            "required": ["city"]
        }
    }
]
response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

### How It Works
1. Model generates JSON matching function schema
2. System parses JSON, validates, executes function
3. Function result fed back to model

## Code: JSON Constrained Decoding

```python
import torch
import json
from typing import Set

class StructuredDecoder:
    def __init__(self, model, tokenizer, schema):
        self.model = model
        self.tokenizer = tokenizer
        self.schema = schema

    def _compute_allowed_tokens(self, prefix_ids: list) -> torch.Tensor:
        prefix_text = self.tokenizer.decode(prefix_ids)
        allowed = set(range(self.tokenizer.vocab_size))
        
        # Basic JSON structural constraints
        text_stripped = prefix_text.strip()
        if not text_stripped:
            allowed = {ord('{')}
        elif not text_stripped.endswith('"'):
            # Inside a string: allow all valid string chars
            pass
        else:
            # After a value or key
            allowed = {ord(','), ord('}')}
            
        mask = torch.zeros(self.tokenizer.vocab_size, dtype=torch.bool)
        mask[list(allowed)] = True
        return mask

    def generate(self, prompt, max_tokens=500):
        input_ids = self.tokenizer(prompt, return_tensors='pt').input_ids
        prefix_ids = input_ids[0].tolist()
        
        for _ in range(max_tokens):
            with torch.no_grad():
                outputs = self.model(input_ids)
                logits = outputs.logits[0, -1]
                
                mask = self._compute_allowed_tokens(prefix_ids)
                logits[~mask] = float('-inf')
                
                probs = torch.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, 1).item()
                prefix_ids.append(next_token)
                input_ids = torch.tensor([prefix_ids])
                
                if next_token == self.tokenizer.eos_token_id:
                    break
                    
        return self.tokenizer.decode(prefix_ids)
```

## Comparison of Approaches

| Method | Flexibility | Speed | Accuracy | Use Case |
|--------|------------|-------|----------|----------|
| Post-hoc parsing | Arbitrary | Fast | 85-95% | Simple formats |
| Prompt engineering | Moderate | Fast | 90-98% | Common formats |
| Constrained decoding | Limited | Slow | 99.9% | Safety-critical |
| Grammar | Moderate | Moderate | 99.9% | Complex schemas |
| Function calling | Predefined | Fast | 99% | Tool use |

## Practical Considerations
- **Tokenisation alignment**: Constraints must operate on token IDs, not characters
- **Speed overhead**: Constrained decoding adds 10-50% latency
- **Stack conflicts**: Model wants to output natural language but constrained to JSON
- **Fallback strategy**: Retry generation or fall back to post-hoc parsing on failure
- **Escaping**: Handle special characters in strings (quotes, newlines)

## References
- Lundberg, "Guidance: A guidance language for controlling large language models", 2023
- Willard & Louf, "Efficient Guided Generation for Large Language Models (Outlines)", 2023
- OpenAI, "Function Calling and Tool Use", 2023
- Geng, Joshi, et al., "lm-format-enforcer: Enforce the Output Format of Language Models", 2023
- Beurer-Kellner, Fischer, Vechev, "Guiding Language Models with Structured Prompts", 2023
