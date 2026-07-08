"""Output parsers — StrOutputParser, CommaSeparatedList, Pydantic."""
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field


print("=== Output Parsers ===\n")

str_parser = StrOutputParser()
result = str_parser.invoke("Hello world")
print(f"StrOutputParser: '{result}' (type: {type(result).__name__})")

list_parser = CommaSeparatedListOutputParser()
result = list_parser.parse("apple, banana, cherry, date")
print(f"CommaSeparatedList: {result} (type: {type(result).__name__})")

class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    city: str = Field(description="The person's city of residence")

pydantic_parser = PydanticOutputParser(pydantic_object=Person)
json_str = '{"name": "Alice Smith", "age": 30, "city": "New York"}'
person = pydantic_parser.parse(json_str)
print(f"\nPydanticOutputParser:")
print(f"  Person: {person}")
print(f"  Name: {person.name}")
print(f"  Age: {person.age}")
print(f"  City: {person.city}")

print(f"\nParsers convert LLM text to structured data.")
