# 🏗️ Output Parsers
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Parse LLM output into structured formats.

## StrOutputParser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
result = parser.invoke("Hello world")  # "Hello world"
```

## CommaSeparatedListOutputParser

```python
parser = CommaSeparatedListOutputParser()
result = parser.invoke("apple, banana, cherry")
# ["apple", "banana", "cherry"]
```

## PydanticOutputParser

```python
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class Person(BaseModel):
    name: str = Field(description="person's name")
    age: int = Field(description="person's age")

parser = PydanticOutputParser(pydantic_object=Person)
result = parser.parse('{"name": "Alice", "age": 30}')
```

<!-- 🤔 Output parsers convert string responses to usable data structures. -->

## Run the Code

```bash
python code/03-output-parsers.py
```
