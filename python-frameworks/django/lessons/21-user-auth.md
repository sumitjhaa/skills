# 📘 Django Phase 03 — Lesson 01: User Model & Authentication

> 🎯 **Goal**: Understand Django's built-in auth — `authenticate()`, `login()`, `logout()`, and the `User` model.

## 📖 Concepts

### The User Model
Django ships with a `User` model in `django.contrib.auth.models`:

| Field | Type | Purpose |
|-------|------|---------|
| `username` | CharField | Unique login name |
| `password` | CharField | Hashed password |
| `email` | EmailField | Email address |
| `first_name` | CharField | First name |
| `last_name` | CharField | Last name |
| `is_active` | Boolean | Can this user log in? |
| `is_staff` | Boolean | Can access admin? |
| `is_superuser` | Boolean | All permissions |
| `date_joined` | DateTime | Registration date |
| `last_login` | DateTime | Last login time |

### Auth Flow
```
Login form → authenticate() → login() → session created → request.user
Logout     → logout()       → session destroyed
```

### `authenticate()`
Checks credentials against all `AUTHENTICATION_BACKENDS`. Returns `User` or `None`.

```python
from django.contrib.auth import authenticate

user = authenticate(username='alice', password='secret123')
if user is not None:
    # credentials valid
    pass
```

### `login()`
Attaches user to session. Sets `request.user` and creates session data.

```python
from django.contrib.auth import login

login(request, user)
# Now request.user is the authenticated user
```

### `logout()`
Flushes session. Sets `request.user` to `AnonymousUser`.

### `request.user`
Always available. Either a `User` instance or `AnonymousUser`.

```python
if request.user.is_authenticated:
    # logged in
else:
    # anonymous
```

### Common Patterns
```python
# login_required decorator
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# LoginRequiredMixin (CBV)
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
```

### ADHD-Friendly Summary
```
authenticate(usern, pw) → User or None
login(req, user)       → session created
logout(req)            → session destroyed
request.user           → User or AnonymousUser
@login_required        → redirects if not logged in
```

## 🛠️ Code

```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Protected view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })
```

## 🧪 Practice

1. Create a login view with `authenticate()` and `login()`
2. Create a logout view
3. Protect 3 views with `@login_required`
4. Show different nav items based on `request.user.is_authenticated`
5. Handle the case where `authenticate()` returns `None` (wrong password)

## 🧠 Key Takeaways

- `authenticate()` verifies credentials; `login()` creates the session
- `logout()` clears the session
- `request.user.is_authenticated` checks login status everywhere
- `@login_required` is the quickest way to protect a view
- Never store passwords in plain text — Django hashes them for you
