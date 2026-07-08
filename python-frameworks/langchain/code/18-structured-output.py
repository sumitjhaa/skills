"""Structured output — extract structured data with Pydantic."""
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


print("=== Structured Output ===\n")

class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="Person's age in years")
    occupation: str = Field(description="Person's job title")

parser = PydanticOutputParser(pydantic_object=Person)

prompt = PromptTemplate.from_template(
    "Extract information from:\n{text}\n\n{format_instructions}",
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

text = "Alice Johnson is a 32-year-old software engineer from San Francisco."
formatted_prompt = prompt.format(text=text)
print(f"Formatted prompt:\n{formatted_prompt}\n")

person = parser.parse(
    '{"name": "Alice Johnson", "age": 32, "occupation": "software engineer"}'
)
print(f"Parsed Person:")
print(f"  Name:       {person.name}")
print(f"  Age:        {person.age}")
print(f"  Occupation: {person.occupation}")

print("\nUse with_structured_output for function-calling models:")
print("  structured_llm = llm.with_structured_output(Person)")
