# 📝 Forms & WTForms
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Create form classes, validate input, CSRF protection, render forms.

## Install

```bash
pip install flask-wtf
```

## Form Classes

Define forms as classes with typed fields and validators.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(3, 20)])
    email = StringField("Email", [DataRequired(), Email()])
    age = IntegerField("Age", [NumberRange(13, 120)])
    agree = BooleanField("Agree to terms")
```

## Handling Form Submission

```python
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user(form.data)
        return redirect(url_for("profile"))
    return render_template("register.html", form=form)
```

## Rendering Forms in Templates

```html
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.username.label }} {{ form.username() }}
    {% for error in form.username.errors %}
        <span style="color:red">{{ error }}</span>
    {% endfor %}
    {{ form.submit() }}
</form>
```

## CSRF Protection

Flask-WTF includes CSRF protection automatically. Include `{{ form.hidden_tag() }}` in every form.

```python
app.config["SECRET_KEY"] = "your-secret-key"
app.config["WTF_CSRF_ENABLED"] = True
```

## Custom Validators

```python
from wtforms.validators import ValidationError

def unique_username(form, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError("Username already taken")
```

<!-- 🧠 Always validate on the server side — never trust client-side validation alone. -->

## Run the Code

```bash
python code/05-forms-wtf.py
```
