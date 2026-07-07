# 📘 Django Phase 03 — Lesson 09: Session Management & Security

> 🎯 **Goal**: Understand Django sessions, CSRF protection, and security best practices.

## 📖 Concepts

### How Django Sessions Work
```
1. User logs in → session data created on server
2. Session ID sent as cookie (sessionid)
3. On each request, Django looks up session by ID
4. Data available as request.session dict
```

### Session Engines
```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'         # default (DB)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'      # Redis/Memcached
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # cache + DB fallback
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'  # all in cookie
```

### Session Configuration
```python
# settings.py
SESSION_COOKIE_AGE = 1209600        # 2 weeks (default, in seconds)
SESSION_COOKIE_HTTPONLY = True      # not accessible via JS
SESSION_COOKIE_SECURE = True        # HTTPS only
SESSION_COOKIE_SAMESITE = 'Lax'     # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False  # saves only when modified
```

### Session Fixation Protection
Django **automatically** rotates session ID on login:
```python
# This happens automatically:
# 1. Old session flushed
# 2. New session created with same data
# 3. Cookie updated with new session ID
```

### CSRF Protection
Cross-Site Request Forgery prevention.

```python
# In every POST form:
<form method="post">
    {% csrf_token %}
    ...
</form>

# For AJAX:
fetch('/api/data/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
    },
})
```

### Security Headers
```python
# settings.py
SECURE_SSL_REDIRECT = True          # HTTP → HTTPS
SECURE_HSTS_SECONDS = 31536000      # HSTS (1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True  # X-Content-Type-Options
SECURE_BROWSER_XSS_FILTER = True    # X-XSS-Protection
CSRF_COOKIE_SECURE = True           # CSRF cookie only over HTTPS
SESSION_COOKIE_SECURE = True         # Session cookie only over HTTPS
X_FRAME_OPTIONS = 'DENY'            # Clickjacking protection
```

### Common Security Pitfalls
| Issue | Fix |
|-------|-----|
| Session not saved | `request.session.modified = True` |
| CSRF cookie missing | Use `{% csrf_token %}` in forms |
| Session fixation | Handled automatically by Django |
| HTTP-only session | Set `SESSION_COOKIE_SECURE = True` |
| Session data too large | Store in DB, not session |

### ADHD-Friendly Summary
```
Session: request.session['key'] = value  (dict-like)
CSRF: {% csrf_token %} in every POST form
Security: SECURE flags in settings.py

Session engines: db (default), cache, cached_db, signed_cookies
```

## 🛠️ Code

```python
# Storing in session
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    request.session.modified = True

# Session security settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # in production
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF in templates
<form method="post">
    {% csrf_token %}
    <input type="submit" value="Submit">
</form>
```

## 🧪 Practice

1. Store a user preference in the session (e.g., `theme: 'dark'`)
2. Test that session persists across requests
3. Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`
4. Add a form with `{% csrf_token %}` and test CSRF protection
5. Switch session backend to `signed_cookies` and verify it works

## 🧠 Key Takeaways

- Sessions store per-user data across requests (cart, preferences, etc.)
- CSRF tokens prevent cross-site request forgery — always use `{% csrf_token %}`
- Security settings should be on in production, careful in development
- Session engine choice: DB (default), cache (fast), signed_cookies (no server storage)
- Django auto-rotates session ID on login (session fixation prevention)
