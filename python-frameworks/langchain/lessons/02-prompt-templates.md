# 🏗️ Prompt Templates
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create reusable prompt templates.

## PromptTemplate

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Translate {text} to {language}."
)
prompt = template.format(text="Hello", language="French")
# "Translate Hello to French."
```

## ChatPromptTemplate

```python
from langchain.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("human", "{question}"),
])
messages = template.format_messages(
    role="translator",
    question="How do you say hello in French?"
)
```

## FewShotPromptTemplate

```python
examples = [
    {"input": "happy", "output": "joyful"},
    {"input": "big", "output": "large"},
]
# Uses examples to guide LLM responses
```

<!-- 🤔 Prompt templates separate prompt logic from code. Always use them. -->

## Run the Code

```bash
python code/02-prompt-templates.py
```
