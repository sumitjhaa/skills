"""Form validation — pure Python simulation."""
from dataclasses import dataclass, field
import re
from typing import Optional


@dataclass
class FormField:
    name: str
    field_type: str
    required: bool = True
    max_length: Optional[int] = None
    errors: list = field(default_factory=list)

    def validate(self, value):
        self.errors = []
        if self.required and not value:
            self.errors.append(f"{self.name} is required")
            return
        if self.max_length and len(str(value)) > self.max_length:
            self.errors.append(f"{self.name} must be at most {self.max_length} characters")


class ContactForm:
    def __init__(self, data: dict = None):
        self.data = data or {}
        self.fields = [
            FormField('name', 'CharField', max_length=100),
            FormField('email', 'EmailField'),
            FormField('message', 'TextField'),
        ]
        self.cleaned_data = {}
        self.errors = {}

    def is_valid(self) -> bool:
        valid = True
        for field in self.fields:
            value = self.data.get(field.name, '')
            field.validate(value)
            if field.errors:
                self.errors[field.name] = field.errors
                valid = False
            elif field.name == 'email':
                if not re.match(r'[^@]+@[^@]+\.[^@]+', str(value)):
                    self.errors[field.name] = ['Invalid email format']
                    valid = False
            else:
                self.cleaned_data[field.name] = value
        return valid


# Test
form = ContactForm({'name': 'Alice', 'email': 'alice@example.com', 'message': 'Hello!'})
print(f"Form valid: {form.is_valid()}")
print(f"Cleaned data: {form.cleaned_data}")

form2 = ContactForm({'name': '', 'email': 'not-an-email', 'message': ''})
print(f"\nForm valid: {form2.is_valid()}")
print(f"Errors: {form2.errors}")
