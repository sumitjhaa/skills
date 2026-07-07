# 📘 Django Phase 03 — Lesson 06: Social Authentication (OAuth)

> 🎯 **Goal**: Add "Login with Google/GitHub" using django-allauth.

## 📖 Concepts

### OAuth2 Flow
```
1. User clicks "Login with Google"
2. Redirect to Google → user approves → redirect back with code
3. Server exchanges code for access token
4. Server fetches user info with token
5. Find or create local user → login
```

### django-allauth
The standard library for social auth in Django. Supports 50+ providers.

```bash
pip install django-allauth
```

### Setup
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Provider-specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
        }
    }
}

LOGIN_REDIRECT_URL = '/'
```

```python
# urls.py
urlpatterns += [
    path('accounts/', include('allauth.urls')),
]
```

### Templates
```html
{% load socialaccount %}

<!-- Login button -->
<a href="{% provider_login_url 'google' %}">Login with Google</a>
<a href="{% provider_login_url 'github' %}">Login with GitHub</a>
```

### Callback URLs
Add these in your Google/GitHub OAuth app settings:
```
http://localhost:8000/accounts/google/login/callback/
http://localhost:8000/accounts/github/login/callback/
```

### Social Account Model
```python
from allauth.socialaccount.models import SocialAccount

# Get user's social accounts
accounts = request.user.socialaccount_set.all()
for account in accounts:
    print(account.provider)  # 'google' or 'github'
    print(account.uid)       # provider's user ID
```

### Customizing Social Login
```python
# signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):
    # Auto-create profile
    Profile.objects.get_or_create(user=user)
    # Set default avatar from social provider
    ...
```

### Connecting Multiple Providers
Users can connect multiple social accounts to one Django user:
```
/accounts/social/connections/   → manage connected accounts
```

### ADHD-Friendly Summary
```
django-allauth → 50+ providers

Install → add INSTALLED_APPS → add urls
→ add provider client_id/secret
→ {% provider_login_url 'google' %}

Callbacks: /accounts/<provider>/login/callback/
```

## 🛠️ Code

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# urls.py
urlpatterns += [path('accounts/', include('allauth.urls'))]

# template
<a href="{% provider_login_url 'google' %}">Sign in with Google</a>
```

## 🧪 Practice

1. Install and configure django-allauth with Google as a provider
2. Create a "Login with GitHub" button
3. Access user's social account info after login
4. Customize the signup signal to create a user profile
5. Test the OAuth flow locally (requires provider credentials)

## 🧠 Key Takeaways

- django-allauth handles OAuth complexity — don't build it yourself
- Each provider needs its own `client_id` and `secret` from the provider's developer console
- Social accounts are linked to Django users via `SocialAccount` model
- Users can connect multiple social accounts to one Django account
- `SOCIALACCOUNT_PROVIDERS` config in settings.py controls provider behavior
