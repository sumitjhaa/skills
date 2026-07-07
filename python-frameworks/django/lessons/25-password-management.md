# 📘 Django Phase 03 — Lesson 05: Password Management

> 🎯 **Goal**: Implement password change and password reset flows.

## 📖 Concepts

### Password Change
User is logged in and wants to change their password.

```python
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})
```

### Password Reset (Not Logged In)
A 4-step flow:

```
1. User enters email → send_email → token generated
2. Email with link → /reset/<uidb64>/<token>/
3. User enters new password → form validates
4. Password saved → redirect to login
```

Django provides this out of the box:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
```

### Token Security
- Tokens are **time-limited** (default: 3 days)
- Tokens are **single-use** (consumed on successful reset)
- Token generated via `django.contrib.auth.tokens.PasswordResetTokenGenerator`

### Customizing Reset Emails
```python
# settings.py
PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes (in seconds)

# Templates to create:
# registration/password_reset_subject.txt
# registration/password_reset_email.html
```

### update_session_auth_hash
When a logged-in user changes password, their session hash changes → they get logged out.

**Fix**: Call `update_session_auth_hash(request, user)` after `form.save()`.

### Best Practices
- Require **old password** for password change
- Show password strength requirements
- Rate-limit password reset requests
- Never send the new password in plain text via email
- Use HTTPS everywhere

### ADHD-Friendly Summary
```
Password Change  : logged in → old + new + confirm → save
Password Reset   : email → token → link → new password
update_session_auth_hash → keeps user logged in after change
Tokens are time-limited + single-use
```

## 🛠️ Code

```python
# Password change (views.py)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def password_change(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed!')
        return redirect('profile')
    return render(request, 'password_change.html', {'form': form})

# URLs for password reset (use built-in views)
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns += [
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
```

## 🧪 Practice

1. Build a password change view with `PasswordChangeForm`
2. Add `update_session_auth_hash` — verify user stays logged in
3. Wire up the built-in password reset URLs
4. Customize the password reset email template
5. Set `PASSWORD_RESET_TIMEOUT` to 30 minutes

## 🧠 Key Takeaways

- `PasswordChangeForm` requires old password; `PasswordResetForm` does not
- Always call `update_session_auth_hash` after admin changes a user's password
- Password reset tokens are cryptographically signed and time-limited
- Django ships with ready-to-use password reset views
- Customize email templates in `registration/` directory
