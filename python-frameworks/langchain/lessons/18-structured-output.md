# 🏗️ Structured Output
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Extract structured data from LLM outputs.

## with_structured_output

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str
    age: int

# Only works with function-calling models
structured_llm = llm.with_structured_output(Person)
result = structured_llm.invoke("Alice is 30 years old")
# Person(name="Alice", age=30)
```

## Via PydanticOutputParser

```python
parser = PydanticOutputParser(pydantic_object=Person)
prompt = PromptTemplate.from_template(
    "Extract: {text}\n{format_instructions}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

<!-- 🤔 with_structured_output is cleaner but requires function-calling models. Fall back to parser for text models. -->

## Run the Code

```bash
python code/18-structured-output.py
```
