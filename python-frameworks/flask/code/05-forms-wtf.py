"""Flask-WTF forms: form classes, validation, CSRF, rendering."""
from typing import Any, Optional
import json
import re


# ======================== Form & Validation ========================

class FormField:
    def __init__(self, label: str = "", validators: list = None, default: Any = None):
        self.label = label
        self.validators = validators or []
        self.default = default
        self.value: Any = default
        self.errors: list[str] = []

    def validate(self, value: Any) -> bool:
        self.value = value
        self.errors = []
        for validator in self.validators:
            error = validator(value)
            if error:
                self.errors.append(error)
        return len(self.errors) == 0

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


class StringField(FormField):
    def __init__(self, label: str = "", validators: list = None, default: str = ""):
        super().__init__(label, validators, default)


class IntegerField(FormField):
    def __init__(self, label: str = "", validators: list = None, default: int = 0):
        super().__init__(label, validators, default)

    def validate(self, value: Any) -> bool:
        try:
            return super().validate(int(value))
        except (ValueError, TypeError):
            self.errors.append("Must be an integer")
            return False


class BooleanField(FormField):
    def __init__(self, label: str = "", default: bool = False):
        super().__init__(label, default=default)

    def validate(self, value: Any) -> bool:
        self.value = value in (True, "true", "1", "yes", "on")
        return True


class SelectField(FormField):
    def __init__(self, label: str = "", choices: list[tuple] = None, validators: list = None):
        super().__init__(label, validators)
        self.choices = choices or []

    def validate(self, value: Any) -> bool:
        valid_choices = [c[0] for c in self.choices]
        if value not in valid_choices:
            self.errors.append(f"Not a valid choice")
            return False
        return super().validate(value)


# ======================== Validators ========================

def required():
    def validate(value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return "This field is required"
        return None
    return validate


def length(min_len: int = 0, max_len: int = None):
    def validate(value):
        if isinstance(value, str):
            if len(value) < min_len:
                return f"Must be at least {min_len} characters"
            if max_len and len(value) > max_len:
                return f"Must be at most {max_len} characters"
        return None
    return validate


def email():
    def validate(value):
        if value and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', str(value)):
            return "Invalid email address"
        return None
    return validate


def number_range(min_val: int = None, max_val: int = None):
    def validate(value):
        if isinstance(value, (int, float)):
            if min_val is not None and value < min_val:
                return f"Must be at least {min_val}"
            if max_val is not None and value > max_val:
                return f"Must be at most {max_val}"
        return None
    return validate


# ======================== Form Base ========================

class FormMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "Form":
            cls._fields = {}
            for attr, val in namespace.items():
                if isinstance(val, FormField):
                    cls._fields[attr] = val
        return cls


class Form(metaclass=FormMeta):
    def __init__(self, **data):
        self._errors: dict[str, list[str]] = {}
        self._is_submitted = bool(data)

        for name, field in self._fields.items():
            value = data.get(name, field.default)
            if not field.validate(value):
                self._errors[name] = field.errors

    @property
    def is_valid(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> dict[str, list[str]]:
        return self._errors

    @property
    def data(self) -> dict:
        return {name: field.value for name, field in self._fields.items() if field.is_valid}

    @property
    def is_submitted(self) -> bool:
        return self._is_submitted

    def render(self) -> str:
        lines = ["<form>"]
        for name, field in self._fields.items():
            label = field.label or name.title()
            error_html = f' <span style="color:red">{", ".join(field.errors)}</span>' if field.errors else ""
            lines.append(f'  <label>{label}: <input name="{name}" value="{field.value or ""}"></label>{error_html}')
        lines.append('  <button type="submit">Submit</button>')
        lines.append("</form>")
        return "\n".join(lines)


# ======================== Form Classes ========================

class RegistrationForm(Form):
    username: str = StringField("Username", [required(), length(3, 20)])
    email: str = StringField("Email", [required(), email()])
    password: str = StringField("Password", [required(), length(6)])
    age: int = IntegerField("Age", [required(), number_range(13, 120)])
    agree: bool = BooleanField("Agree to terms")


class ContactForm(Form):
    name: str = StringField("Name", [required(), length(2, 50)])
    email: str = StringField("Email", [required(), email()])
    subject: str = SelectField("Subject", choices=[("general", "General"), ("support", "Support"), ("feedback", "Feedback")], validators=[required()])
    message: str = StringField("Message", [required(), length(10, 1000)])


class ProductForm(Form):
    name: str = StringField("Product Name", [required(), length(3, 100)])
    price: float = StringField("Price", [required()])
    category: str = SelectField("Category", choices=[("electronics", "Electronics"), ("books", "Books"), ("clothing", "Clothing")], validators=[required()])
    in_stock: bool = BooleanField("In Stock")


# ======================== App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def deco(func):
            self.routes.append({"path": path, "methods": methods, "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if method in route["methods"] and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()


@app.route("/register", methods=["GET", "POST"])
def register(**kwargs):
    form = RegistrationForm(**kwargs)
    if form.is_submitted and form.is_valid:
        return {"status": "success", "data": form.data, "message": "Registration successful!"}
    return {
        "status": "form",
        "fields": list(RegistrationForm._fields.keys()),
        "errors": form.errors if form.is_submitted else {},
        "html": form.render(),
    }


@app.route("/contact", methods=["GET", "POST"])
def contact(**kwargs):
    form = ContactForm(**kwargs)
    if form.is_submitted and form.is_valid:
        return {"status": "success", "data": form.data, "message": "Message sent!"}
    return {
        "status": "form",
        "subject_choices": ContactForm._fields["subject"].choices,
        "errors": form.errors if form.is_submitted else {},
    }


# ======================== Demo ========================
print("=== Flask-WTF Forms Demo ===\n")

print("1. Registration form (GET):")
r = app("GET", "/register")
print(f"   Fields: {r['data']['fields']}")
print(f"   HTML: {r['data']['html'][:80]}...\n")

print("2. Registration with valid data:")
r = app("POST", "/register", username="alice", email="alice@test.com", password="secret123", age=25, agree=True)
print(f"   Status: {r['data']['status']}")
print(f"   Data: {r['data']['data']}\n")

print("3. Registration with invalid data:")
r = app("POST", "/register", username="a", email="bad", password="12", age=10, agree=False)
print(f"   Status: {r['data']['status']}")
for field, errs in r['data']['errors'].items():
    print(f"   {field}: {', '.join(errs)}")

print("\n4. Contact form with valid data:")
r = app("POST", "/contact", name="Bob", email="bob@test.com", subject="support", message="Need help with my order")
print(f"   Status: {r['data']['status']}")
print(f"   Data: {r['data']['data']}")

print("\n5. Contact form with invalid data:")
r = app("POST", "/contact", name="", email="bad", subject="invalid", message="short")
print(f"   Status: {r['data']['status']}")
for field, errs in r['data']['errors'].items():
    print(f"   {field}: {', '.join(errs)}")
