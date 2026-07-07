# 📝 Django Forms
<!-- ⏱️ 12 min | 🟡 Applied -->

**What You'll Learn:** Build forms, validate input, handle submissions, and integrate with models.

## Creating Forms

```python
# blog/forms.py
from django import forms
from .models import Post

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    subscribe = forms.BooleanField(required=False)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'category', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
```

## Using Forms in Views

```python
# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm, PostForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data has validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Send email, save to DB, etc.
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()  # ModelForm saves automatically
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
```

## Template Rendering

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}  <!-- Renders all fields as <p> elements -->
  <button type="submit">Submit</button>
</form>
```

## Code Example

```python
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
```

## Field Types

| Field | HTML Widget | Validation |
|-------|-------------|------------|
| `CharField` | `<input type="text">` | Max length, min length |
| `EmailField` | `<input type="email">` | Email format |
| `IntegerField` | `<input type="number">` | Integer, min/max values |
| `BooleanField` | `<input type="checkbox">` | True/False |
| `DateField` | `<input type="date">` | Date format |
| `ChoiceField` | `<select>` | Value in choices |

## Key Points
- Always include `{% csrf_token %}` in forms — prevents CSRF attacks
- `request.method == 'POST'` checks if form was submitted
- `form.is_valid()` runs all validators; use `form.cleaned_data` afterward
- `ModelForm` automatically creates form fields from model fields
- Custom validators: add `clean_<fieldname>()` or `clean()` methods
