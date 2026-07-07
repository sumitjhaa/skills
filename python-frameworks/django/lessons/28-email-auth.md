# 📘 Django Phase 03 — Lesson 08: Email Authentication

> 🎯 **Goal**: Let users log in with email instead of username.

## 📖 Concepts

### Why Email Auth?
- Users forget usernames but remember emails
- Cleaner signup (one less field)
- Matches most SaaS platforms

### Approach 1: Custom Auth Backend
Keep the default User model but add email-based authentication.

```python
# authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(ModelBackend):
    """Authenticate by email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get('email') or username
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
```

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'myapp.authentication.EmailAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

### Approach 2: Custom User Model (AbstractBaseUser)
Complete replacement — no username field at all.

```python
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['display_name']
```

### Login Form for Email Auth
```python
class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(request=self.request, email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password")
        self.user = user
        return self.cleaned_data
```

### Signup Form (No Username)
```python
class EmailSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'display_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

### Template Changes
```html
<form method="post">
    {% csrf_token %}
    {{ form.email.label }}: {{ form.email }}
    {{ form.password.label }}: {{ form.password }}
    <button type="submit">Log in with email</button>
</form>
```

### Best Practices
- Validate email format at signup
- Handle duplicate email on registration
- Allow users to change email (with verification)
- Consider email verification flow

### ADHD-Friendly Summary
```
Option 1: Custom backend (keep User model, add email login)
Option 2: Custom User (AbstractBaseUser, USERNAME_FIELD='email')

Both work. Option 2 is cleaner for new projects.
```

## 🛠️ Code

```python
# Custom backend for email auth
class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email') or username
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and user.is_active:
            return user
        return None

# Usage
user = authenticate(email='alice@example.com', password='secret')
```

## 🧪 Practice

1. Create a custom `EmailAuthBackend` that authenticates by email
2. Add it to `AUTHENTICATION_BACKENDS`
3. Create a login view that uses email instead of username
4. Create a signup form without a username field
5. Test: login with email, wrong password, nonexistent email

## 🧠 Key Takeaways

- Custom `EmailAuthBackend` works with the default User model
- Set `USERNAME_FIELD = 'email'` on custom User models
- Always update login forms and templates to use email
- Handle duplicate email at registration
- Email auth + social auth = complete auth solution
