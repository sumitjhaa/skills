# 📘 Django Phase 03 — Lesson 02: Registration & User Profiles

> 🎯 **Goal**: Build signup flows and extend users with profile data.

## 📖 Concepts

### Signup View Pattern
```
GET  /signup/ → show form
POST /signup/ → validate → create User → login → redirect
```

### Two Approaches for Extra User Data

#### 1. Profile Model (OneToOneField)
Recommended for third-party apps or when you don't want to touch the User model.

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
```

#### 2. Custom User Model (AbstractUser)
Recommended for new projects. Add fields directly to the User model.

```python
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
```

**Set before first migration**: `AUTH_USER_MODEL = 'myapp.User'`

### Registration Form
Always use a `UserCreationForm` or custom `ModelForm`:

```python
from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username taken")
        return username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords don't match")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
```

### Signal-Based Profile Auto-Creation
```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### ADHD-Friendly Summary
```
Signup: form → validate → User.objects.create_user() → login → redirect
Profile: OneToOne → signal auto-create → per-user data
Custom User: AUTH_USER_MODEL = 'app.User' (before first migrate!)
```

## 🛠️ Code

```python
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
```

## 🧪 Practice

1. Create a `SignUpForm` with username, email, password, confirm_password
2. Create a signup view that creates user + profile, then logs in
3. Create a profile edit view (bio, location, avatar)
4. Auto-create Profile via signal when User is created
5. Add `@login_required` to the profile edit view

## 🧠 Key Takeaways

- Always use `User.objects.create_user()` (not `create()`) to hash passwords
- Signals are the cleanest way to auto-create profiles
- Profile with `OneToOneField` = no risk of breaking auth internals
- Custom User (`AbstractUser`) is cleaner for new projects
- Never store user data on the User model itself unless it's auth-related
